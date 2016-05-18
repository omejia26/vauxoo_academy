# -*- coding: utf-8 -*-
from openerp import fields, models, api, exceptions


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
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
    active = fields.Boolean(default=True)   # Todos los registros sean activos
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

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Valor incorrecto para los 'asientos'",
                    'message': "El numero de asientos disponibles " +
                    "no pueden ser negativos",
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendes",
                    'message': "Increase seats or remove excess attendees",
                }
            }

    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError("Un instructor no puede" +
                                             " ser su propio asistente")
