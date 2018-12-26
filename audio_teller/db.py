import sqlite3
import logging


class Db:
    def __init__(self, storage_file):
        """Constructor for Database

        Parameters
        ----------
        storage_file: location of db file in String

         Attributes
        ----------
        db_file : Location of database file
        features_table: Name of features table
        song_table: Name of song table

        """
        self.logger = logging.getLogger(__name__)
        self.db_file = storage_file
        self.open_connection(db_file=storage_file)
        self.features_table = 'features'
        self.song_table = 'song'

    def open_connection(self, db_file):
        """Create a database connection to SQLite database file provided

        :param db_file
        :return connection
        """
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            self.logger.error(str(e))

    def create_tables(self):
        """
        Create tables if not exists

        :return:
        True if table created or already present, False if database error
        """
        create_features_table = "CREATE TABLE IF NOT EXISTS {} (hash1 text NOT NULL, hash2 text " \
                                "NOT NULL, mfcc real, chroma_cens real, chroma_stf REAL, mel real," \
                                "tonnetz real, rhythm real, PRIMARY KEY (hash1, hash2))".format(self.features_table)

        create_song_table = "CREATE TABLE IF NOT EXISTS {} (hash text PRIMARY KEY, " \
                            "name text NOT NULL)".format(self.song_table)

        try:
            self.cursor.execute(create_features_table)
            self.cursor.execute(create_song_table)

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error(e)
            return False
        return True

    def save_song(self):
        
