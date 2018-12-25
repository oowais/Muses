from db import Db
import os


# download database browser and check if tables are shown properly
# calculate hash of audio and compare
def main():
    # db = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), 'database/db.sqlite')))
    print(db.create_tables())


if __name__ == '__main__':
    main()
