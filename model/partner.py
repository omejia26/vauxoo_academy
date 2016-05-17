# -*- encoding: utf-8 -*-
from openerp import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor",default=False)
    session_ids = fields.Many2many('openacademy.session',
                                   string="Sesion como instructor",
                                   readonly=True)
