# -*- coding: utf-8 -*-
from openerp import fields, models


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duracion en dias")
    seats = fields.Integer(string="Numero de asientos")
