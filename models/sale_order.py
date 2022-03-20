# -*- coding: utf-8 -*-
from odoo import fields, models


class CostumerQuotation(models.Model):
    _inherit = 'sale.order'

    booking_ids = fields.One2many('booking_management.booking', 'quotation_id', string="Booking")
    count_reserv = fields.Integer(string="Reservations", compute='_count_reservations')

    def _count_reservations(self):
        for r in self:
            r.count_reserv = len(r.booking_ids)

    def action_view_reservations(self):
        action = self.env['ir.actions.act_window']._for_xml_id('management_booking.all_booking_list_action')
        if self.count_reserv > 1:
            action['domain'] = [('id', 'in', self.booking_ids.ids)]
        elif self.booking_ids:
            tree_view = [(self.env.ref('management_booking.booking_tree_view').id, 'tree')]
            action['view_mode'] = tree_view
            action['res_id'] = self.booking_ids.id
        return action
