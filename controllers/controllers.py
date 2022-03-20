# -*- coding: utf-8 -*-
# from odoo import http


# class ManagementBooking(http.Controller):
#     @http.route('/management_booking/management_booking', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/management_booking/management_booking/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('management_booking.listing', {
#             'root': '/management_booking/management_booking',
#             'objects': http.request.env['management_booking.management_booking'].search([]),
#         })

#     @http.route('/management_booking/management_booking/objects/<model("management_booking.management_booking"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('management_booking.object', {
#             'object': obj
#         })
