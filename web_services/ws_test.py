# -*- encoding: utf-8 -*-

import functools
import xmlrpclib

HOST = '127.0.0.1'
PORT = 8069
DB = 'training_vauxoo'
USER = 'admin'
PASS = raw_input("Contraseña : ")
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

# 1. Login
uid = xmlrpclib.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
print "Logged in as %s (uid:%d)" % (USER, uid)

call = functools.partial(
    xmlrpclib.ServerProxy(ROOT + 'object').execute,
    DB, uid, PASS)

# 2. Read the sessions
sessions = call('openacademy.session', 'search_read', [], ['name', 'seats'])
for session in sessions:
    print "Session %s (%s seats)" % (session['name'], session['seats'])
# 3. Crear una nueva sesion para el curso Programacion
course_id = call('openacademy.course', 'search',
                 [('name', 'ilike', 'Programación')])[0]
session_id = call('openacademy.session', 'create', {
    'name': 'El programador',
    'course_id': course_id,
})
