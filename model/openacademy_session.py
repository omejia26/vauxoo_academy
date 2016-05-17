# -*- coding: utf-8 -*-
from openerp import fields, models, api


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
    taken_seats = fields.Float(string="Asientos tomados",
                               compute="_taken_seats")

    """
    Decoradores:
        @api.one: Entre a cada uno de los registros
        @api.depends: Campos a utilizar
        Se declaran de manera consecutiva a la definicion de la clase
    """
    @api.one
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        if not self.seats:
            self.seats = 0
        else:
            self.taken_seats = 100.0 * len(self.attendee_ids) / self.seats
