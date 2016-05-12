# -*- encoding: utf-8 -*-
from openerp import models, fields


class Course(models.Model):
    """
      Esta clase crea el modelo del curso
    """
    _name = 'openacademy.course'  # Nombre de la tabla

    name = fields.Char(string='Titulo', required=True)
    description = fields.Text(string='Descripcion')

