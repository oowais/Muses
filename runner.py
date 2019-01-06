import argparse
from core.main import Main


def _get_args():
    parser = argparse.ArgumentParser(
        description='Calculates distances between a dataset of audio files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("in_path",
                        action="store",
                        help="Name of database")
    args = parser.parse_args()
    return args.in_path


if __name__ == '__main__':
    print('######################################')

    db_name = _get_args()
    if not db_name.endswith('.sqlite'):
        print('Provide a proper database file name. (for eg: db.sqlite)')
    else:
        main_obj = Main(db_name)
        main_obj.calc_feature_new()
        main_obj.show_similarity()
