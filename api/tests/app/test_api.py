from unittest import mock

from flask import url_for

from api import FlaskTest


class GameLogTest(FlaskTest):
    def setUp(self):
        self.mongo = mock.patch('api.app.api.mongo').start()

    def tearDown(self):
        mock.patch.stopall()

    def test_mostra_game_logs_vazio(self):
        self.mongo.db.gamelog.find.return_value = {}
        resp = self.client.get(url_for('api.games'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode('utf-8'), '[]\n')

    def test_mostra_game_logs(self):
        self.mongo.db.gamelog.find.return_value = [{"game_1": "teste"}]
        resp = self.client.get(url_for('api.games'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode('utf-8'), '[{"game_1":"teste"}]\n')

    def test_mostra_game_logs_erro(self):
        self.mongo.db.gamelog.find.side_effect = Exception
        resp = self.client.get(url_for('api.games'))

        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.data.decode('utf-8'), '{"erro":""}\n')

    def test_mostra_game_one_logs_vazio(self):
        self.mongo.db.gamelog.find_one_or_404.return_value = {}
        resp = self.client.get(url_for('api.games_one', id=1))

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data.decode('utf-8'), '{"erro":"404"}\n')

    def test_mostra_game_one_logs_encontra_um(self):
        self.mongo.db.gamelog.find_one_or_404.return_value = {"game_1": {"teste": "teste"},
                                                              "game_10": {"teste": "nao"}}
        resp = self.client.get(url_for('api.games_one', id=1))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode('utf-8'), '{"game_1":{"teste":"teste"}}\n')

    def test_mostra_game_one_logs_nao_encontra(self):
        self.mongo.db.gamelog.find_one_or_404.return_value = {"game_10": {"teste": "teste"},
                                                              "game_100": {"teste": "nao"}}
        resp = self.client.get(url_for('api.games_one', id=1))

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data.decode('utf-8'), '{"erro":"404"}\n')

    def test_mostra_game_one_logs_erro(self):
        self.mongo.db.gamelog.find_one_or_404.side_effect = Exception
        resp = self.client.get(url_for('api.games_one', id=1))

        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.data.decode('utf-8'), '{"erro":""}\n')
