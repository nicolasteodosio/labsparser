from argparse import ArgumentParser

from app.log_parser import ParsearLog


def main():
    parser = ArgumentParser(description='Parser de log ')

    parser.add_argument('--log', type=str,  help='Caminho do rquivo com o log',
                        required=True)
    arg = parser.parse_args()

    parser_log = ParsearLog(log_file=arg.log)

    parser_log.pre_parser()

    parser_log.parsear()


if __name__ == '__main__':
    main()
