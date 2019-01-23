from unittest import TestCase, mock
from unittest.mock import MagicMock

from parser.app.log_parser import ParsearLog
from tests.utils import MockedData


class TestParsearLog(TestCase):
    @mock.patch('app.log_parser.rows.import_from_csv')
    def test_prepare_data_table(self, mocked_import_from_csv):
        mocked_import_from_csv.return_value = True
        parser = ParsearLog(log_file=MagicMock())
        teste = parser.prepara_data_table()
        self.assertTrue(mocked_import_from_csv.called)
        self.assertTrue(teste)

    @mock.patch('app.log_parser.rows.import_from_csv')
    def test_prepare_data_table_raise(self, mocked_import_from_csv):
        mocked_import_from_csv.side_effect = Exception
        parser = ParsearLog(log_file=MagicMock())
        self.assertRaises(Exception, parser.prepara_data_table)

    def test_prepare_data_table_csv_invalido(self):
        parser = ParsearLog(log_file=MagicMock(), csv_file=MagicMock())
        self.assertRaises(Exception, parser.prepara_data_table)

    def test_estrutura_kills_contabiliza_games_kill(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.estrutura_kills(data=MockedData(event='teste', info='teste'))
        self.assertEqual(parser.games_kill, 1)

    def test_estrutura_kills_player_se_mata_nao_contabiliza(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['Fulano', 'Sicrano', 'Feuplano']
        parser.estrutura_kills(data=MockedData(event='teste', info=': Fulano killed Fulano by'))
        self.assertEqual(parser.player_kills, {})

    def test_estrutura_kills_world_mata_player(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['Fulano', 'Sicrano', 'Feuplano']
        parser.estrutura_kills(data=MockedData(event='teste', info=': <world> killed Fulano by'))
        self.assertEqual(parser.player_kills, {'Fulano': -1})

    def test_estrutura_kills_world_mata_player_ja_existente(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['Fulano', 'Sicrano', 'Feuplano']
        parser.player_kills = {'Fulano': 9}
        parser.estrutura_kills(data=MockedData(event='teste', info=': <world> killed Fulano by'))
        self.assertEqual(parser.player_kills, {'Fulano': 8})

    def test_estrutura_kills_player_mata_player_ja_existente(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['Fulano', 'Sicrano', 'Feuplano']
        parser.player_kills = {'Fulano': 9}
        parser.estrutura_kills(data=MockedData(event='teste', info=': Fulano killed Sicrano by'))
        self.assertEqual(parser.player_kills, {'Fulano': 10})

    def test_estrutura_kills_player_mata_player_novo(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['Fulano', 'Sicrano', 'Feuplano']
        parser.estrutura_kills(data=MockedData(event='teste', info=': Fulano killed Sicrano by'))
        self.assertEqual(parser.player_kills, {'Fulano': 1})

    def test_estrutura_players_string_invalida(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.estrutura_players(data=MockedData(event='teste', info='teste'))
        self.assertEqual(parser.players, [])

    def test_estrutura_players(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.estrutura_players(data=MockedData(event='teste', info='lala\\teste'))
        self.assertEqual(parser.players, ['teste'])

    def test_estrutura_players_nome_do_meio(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.estrutura_players(data=MockedData(event='teste', info='lala\\teste\\outro'))
        self.assertEqual(parser.players, ['teste'])

    def test_cria_estrutura(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.cria_estrutura()
        self.assertEqual(parser.games_count, 1)
        self.assertEqual(parser.games_kill, 0)
        self.assertEqual(parser.players, [])
        self.assertEqual(parser.player_kills, {})

    def test_cria_estrutura_games_count_maior(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.games_count = 8
        parser.cria_estrutura()
        self.assertEqual(parser.games_count, 9)
        self.assertEqual(parser.games_kill, 0)
        self.assertEqual(parser.players, [])
        self.assertEqual(parser.player_kills, {})

    def test_finaliza_estrutura_add_players_zerados(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['teste']
        estrutura = parser.finaliza_estrutura(games={})
        self.assertEqual(estrutura, {'game_0': {'kills': {'teste': 0}, 'players': ['teste'], 'total_kills': 0}})
        self.assertEqual(parser.player_kills,  {'teste': 0})

    def test_finaliza_estrutura(self):
        parser = ParsearLog(log_file=MagicMock())
        parser.players = ['teste']
        parser.games_kill = 8
        estrutura = parser.finaliza_estrutura(games={})
        self.assertEqual(estrutura, {'game_0': {'kills': {'teste': 0}, 'players': ['teste'], 'total_kills': 8}})
