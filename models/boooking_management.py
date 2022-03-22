from datetime import timedelta
from odoo import models, fields, api


class booking(models.Model):
    _name = 'booking_management.booking'

    reference = fields.Char('Order Reference', required=True, readonly=True, index=True, copy=False, default='New')
    client_id = fields.Many2one('res.partner', string="Client")
    article_id = fields.Many2one('product.template', ondelete='set null', string="Products")
    booking_date = fields.Date(string="Booking date", default=fields.Date.today)
    duration = fields.Integer(string="Duration", help="Duration in hours, days or month")
    duration_unit = fields.Selection([('hour', 'Hours'), ('day', 'Days'), ('month', 'Month')],
                                     default='day', string="Unit")
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    state = fields.Selection([('new', 'New'), ('approve', 'Approved'), ('valid', 'Validated'),
                              ('cancel', 'Canceled'), ('close', 'Closed')], default='new',
                             string="status")
    color = fields.Integer()
    quotation_id = fields.Many2one('sale.order', string="Quotation")
    ####quotation related file
    quotation_date = fields.Datetime(string="date order", related='quotation_id.date_order')
    quotation_origin = fields.Char(string="origin order",  related='quotation_id.origin')
    ###
    nb_reservations = fields.Integer(string="Number reservations",
                                     compute='_number_reservation',store=True, compute_sudo=True)
    nb_reservations_cancel = fields.Integer(string="Number reservations canceled",
                                              compute='_number_reservation_canceled',store=True, compute_sudo=True)
    nb_hours_reservations = fields.Integer(string="Number of hours reservations",
                                           compute='_number_reservation_hours',store=True, compute_sudo=True)

    @api.model
    def create(self, vals):
        if vals.get('reference', 'New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('booking.order') or 'New'
            self.client_id.hadBooking = True
        return super(booking, self).create(vals)

    @api.depends('booking_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.booking_date and r.duration):
                r.end_date = r.booking_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            compute = 0
            if r.duration_unit == 'hour':
                compute = r.duration
            elif r.duration_unit == 'day':
                compute = r.duration * 24
            else:
                compute = r.duration * 30 * 24
            start = fields.Datetime.from_string(r.booking_date)
            duration = timedelta(hours=compute, seconds=-1)
            r.end_date = start + duration

    def _set_end_date(self):
        for r in self:
            if not (r.booking_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            booking_date = fields.Datetime.from_string(r.booking_date)
            end_date = fields.Datetime.from_string(r.end_date)
            r.duration = (end_date - booking_date).days + 1

    def btn_generate_multiple_sale_order(self):
        reservations = self.env["booking_management.booking"].browse(self._context.get('active_ids', []))
        group_by_client = {}

        for r in reservations:
            if r.client_id in group_by_client:
                group_by_client[r.client_id].append(r)
            else:
                group_by_client[r.client_id] = [r]
        for client in group_by_client:
            reservs = group_by_client[client]
            sale_order = self.env['sale.order'].create({
                'partner_id': client.id,
                'date_order': fields.Datetime.now(),
                'origin': '/'.join([r.reference for r in reservs]),
                'order_line': [(0, 0, {
                    'product_id': r.article_id.id,
                    'product_uom_qty': r.duration,
                    'price_unit': 150 if r.duration < 10 else 140,
                }) for r in reservs]
            })
            for r in reservs:
                r.quotation_id = sale_order

    def action_new(self):
        self.state = 'new'

    def action_approved(self):
        self.state = 'approve'

    def action_validated(self):
        self.state = 'valid'

    def action_canceled(self):
        self.state = 'cancel'

    def action_closed(self):
        self.state = 'close'

    def create_order(self):
        self.ensure_one()
        if self.duration < 10:
            price = 150
        else:
            price = 140
        order = self.env['sale.order'].search([], limit=1)
        sales_order_line = self.quotation_id.create({
            'date_order': fields.Datetime.now(),
            'origin': self.reference,
            'order_line': [
                (0, 0, {'price_unit': price,
                        'product_uom_qty': self.duration,
                        'product_id': self.article_id.id
                        })
            ],
            'partner_id': self.client_id.id,
            'pricelist_id': order.pricelist_id.id
        })
        self.quotation_id = sales_order_line

    def _number_reservation(self):
        for r in self:
            r.nb_reservations = len(r.ids)
        print('2hh')

    @api.depends('state')
    def _number_reservation_canceled(self):
        for r in self:
            if r.state == 'cancel':
                r.nb_reservations_cancel += 1

    @api.depends('duration')
    def _number_reservation_hours(self):
        for r in self:
            if r.duration_unit == 'hour':
                r.nb_hours_reservations += r.duration
            elif r.duration_unit == 'day':
                r.nb_hours_reservations += r.duration * 24
            else:
                r.nb_hours_reservations += r.duration * 30 * 24
        print('hhh')


