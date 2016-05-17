# -*- coding: utf-8 -*-
from openerp import fields, models


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duracion en dias")
    seats = fields.Integer(string="Numero de asientos")
    # El ilike busca en los tags tambien
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|',
                                            ("instructor", "=", True,),
                                            ("category_id.name", "ilike",
                                             "Profesor")])
    course_id = fields.Many2one('openacademy.course',
                                ondelete='cascade',
                                string="Curso",
                                required=True)
    attendee_ids = fields.Many2many('res.partner', string="Asistentes")
