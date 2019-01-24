from flask_testing import TestCase as FlaskTestCase

from api.factory import create_app


class FlaskTest(FlaskTestCase):
    def create_app(self):
        app = create_app('Gamelog')
        app.config['TESTING'] = True
        return app
