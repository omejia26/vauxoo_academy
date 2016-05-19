# -*- coding: utf-8 -*-
"""Codificacion de caracteres bajo estandar utf-8"""
from openerp import fields, models, api, exceptions
from datetime import timedelta


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today, string="Fecha inicio")
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
    end_date = fields.Date(string="Fecha Final", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration in hours",
                         compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(string="Contador de Asistentes",
                                     compute='_get_attendees_count',
                                     store=True)
    color = fields.Integer()

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

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for element in self:
            if not (element.start_date and element.duration):
                element.end_date = element.start_date
                continue
            start = fields.Datetime.from_string(element.start_date)
            duration = timedelta(days=element.duration, seconds=-1)
            element.end_date = start + duration

    def _set_end_date(self):
        for element in self:
            if not (element.start_date and element.end_date):
                continue
            start_date = fields.Datetime.from_string(element.start_date)
            end_date = fields.Datetime.from_string(element.end_date)
            element.duration = (end_date - start_date).days + 1

    @api.one
    @api.depends('duration')
    def _get_hours(self):
        self.hours = self.duration * 24

    @api.one
    def _set_hours(self):
        self.duration = self.hours / 24

    @api.one
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        self.attendees_count = len(self.attendee_ids)
