import rows
import re


class ParsearLog:
    def __init__(self, log_file, csv_file='samples/log.csv'):
        self.log_file = log_file
        self.csv_file = csv_file
        self.games_count = 0
        self.games_kill = 0
        self.players = []
        self.player_kills = {}

    def prepara_data_table(self):
        try:
            data = rows.import_from_csv(self.csv_file)
        except Exception as e:
            print('Arquivo csv inválido, ou não existe')
            raise e
        return data

    def pre_parser(self):
        file = open('{}'.format(self.log_file), 'r')
        fit = open('samples/log.csv', 'w')
        fit.write('event;info\n')
        for line in file.readlines():
            tata = line.split()
            if tata[1] == '------------------------------------------------------------':
                continue
            else:
                try:
                    fit.write('{};{}\n'.format(tata[1], ' '.join(tata[2:])))
                except IndexError:
                    fit.write('{};{}\n'.format(tata[1], '#'))
        file.close()
        fit.close()

    def estrutura_kills(self, data):
        self.games_kill += 1

        busca = re.search(': (.*) killed (.*) by', data.info)
        if busca:
            if busca.group(1) == busca.group(2):
                return
            if busca.group(1) == '<world>':
                if busca.group(2) in self.player_kills:
                    self.player_kills[busca.group(2)] -= 1
                else:
                    self.player_kills[busca.group(2)] = -1
            else:
                if busca.group(1) in self.player_kills:
                    self.player_kills[busca.group(1)] += 1
                else:
                    self.player_kills[busca.group(1)] = 1

    def parsear(self):
        data_table = self.prepara_data_table()

        games = {}

        for data in data_table:
            if data.event == 'InitGame:':
                self.cria_estrutura()
            if data.event == 'ClientUserinfoChanged:':
                self.estrutura_players(data)
            if data.event == 'Kill:':
                self.estrutura_kills(data)
            if data.event == 'ShutdownGame:':
                self.finaliza_estrutura(games)

        print(games)

    def finaliza_estrutura(self, games):
        self.add_players_zerados()
        games['game_{}'.format(self.games_count)] = {'players': self.players,
                                                     'total_kills': self.games_kill,
                                                     'kills': self.player_kills}
        return games

    def add_players_zerados(self):
        for player in self.players:
            if player not in self.player_kills:
                self.player_kills[player] = 0

    def estrutura_players(self, data):
        player = data.info.split('\\')
        if len(player) >= 2:
            if player[1] not in self.players:
                self.players.append(player[1])
            return self.players

    def cria_estrutura(self):
        self.games_count += 1
        self.games_kill = 0
        self.players = []
        self.player_kills = {}
