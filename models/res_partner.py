# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Customer(models.Model):
    _inherit = 'res.partner'

    hadBooking = fields.Boolean("Booking", default=False)
    reservations_ids = fields.One2many('booking_management.booking', 'client_id', string="Client Booking")




