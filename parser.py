import rows
import re

def pre_parser():
    file = open('games.log', 'r')
    fit = open('log.csv', 'w')
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

if __name__ == '__main__':
    # pre_parser()
    teste = rows.import_from_csv('log.csv')
    games_count = 0
    games = {}

    for t in teste:
        if t.event == 'InitGame:':
            games_count += 1
            games_kill = 0
            players = []
            player_kills = {}
        if t.event == 'ClientUserinfoChanged:':
            player = t.info.split('\\')
            if player[1] not in players:
                players.append(player[1])
        if t.event == 'Kill:':
            games_kill += 1
            for player in players:
                if player not in player_kills:
                    player_kills[player] = 0

            busca = re.search(': (.*) killed (.*) by', t.info)
            if busca.group(1) == busca.group(2):
                continue
            if busca.group(1) == '<world>':
                if busca.group(2) in player_kills:
                    player_kills[busca.group(2)] -= 1
                else:
                    player_kills[busca.group(2)] = -1
            else:
                if busca.group(1) in player_kills:
                    player_kills[busca.group(1)] += 1
                else:
                    player_kills[busca.group(1)] = 1

        if t.event == 'ShutdownGame:':
            games['game_{}'.format(games_count)] = {'players': players, 'total_kills': games_kill, 'kills': player_kills}

        print(t)
    print(games)
