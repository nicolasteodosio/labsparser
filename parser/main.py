from argparse import ArgumentParser

from app.log_parser import ParsearLog


def main():
    parser = ArgumentParser(description='Parser de log ')

    parser.add_argument('--log', type=str,  help='Caminho do rquivo com o log',
                        required=True)
    parser.add_argument('--print', help='Mostra na tela o log depois do parser')

    arg = parser.parse_args()

    parser_log = ParsearLog(log_file=arg.log)

    parser_log.pre_parser()

    resultado = parser_log.parsear()

    if arg.print:
        print(resultado)


if __name__ == '__main__':
    main()
