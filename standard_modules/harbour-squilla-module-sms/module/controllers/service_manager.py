import re
import subprocess

from flask.ext.restful import Resource

from squilla import api

from ..sms import app


class Start(Resource):
    def post(self):
        if not app.started:
            app.start()

        return {'status': True}


class Stop(Resource):
    def post(self):
        if app.started:
            app.stop()

        return {'status': False}


class Status(Resource):
    def get(self):
        return {'status': app.started}




api.add_resource(Start, '/sms/start')
api.add_resource(Stop, '/sms/stop')
api.add_resource(Status, '/sms/status')
