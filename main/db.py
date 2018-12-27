import sqlite3
import logging
import numpy


class Db:
    def __init__(self, storage_file):
        """Constructor for Database

        Parameters
        ----------
        storage_file: location of db file in String

         Attributes
        ----------
        db_file : Location of database file
        feature_table: Name of features table
        song_table: Name of song table

        """
        self.logger = logging.getLogger(__name__)
        self.db_file = storage_file
        self.open_connection(db_file=storage_file)
        self.distance_table = 'distance'
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
        # create_song_table = "CREATE TABLE IF NOT EXISTS {} (hash text PRIMARY KEY, " \
        #                     "name text NOT NULL, mfcc BLOB, chroma_cens BLOB, chroma_stf BLOB, mel BLOB," \
        #                     "tonnetz BLOB, rhythm BLOB)".format(self.song_table)

        create_feature_table = "CREATE TABLE IF NOT EXISTS {} (hash1 text NOT NULL, hash2 text " \
                               "NOT NULL, mfcc_dist real, chroma_cens_dist real, chroma_stf_dist real, mel_dist real," \
                               "tonnetz_dist real, rhythm_dist real, PRIMARY KEY (hash1, hash2))" \
            .format(self.distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            # self.cursor.execute(create_song_table)
            self.cursor.execute(create_feature_table)

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error(e)
            return False
        return True

    def save_feature_distances(self, feature):
        """Saves the song name and its hash to table

        Parameters
        ----------
        song1: Song class
        song2: Song class
        feature: Feature class

        Returns
        -------
        True if data saved successfully, False otherwise
        """
        self.open_connection(self.db_file)

        # insert_into_song_table = "INSERT INTO {} (hash, name, mfcc, chroma_cens, chroma_stf, mel, tonnetz, rhythm) " \
        #                          "VALUES (?,?,?,?,?,?,?,?)".format(self.song_table)

        insert_into_feature_table = "INSERT INTO {} (hash1, hash2, mfcc_dist, chroma_cens_dist, chroma_stf_dist," \
                                    "mel_dist, tonnetz_dist, rhythm_dist) VALUES (?,?,?,?,?,?,?,?)" \
            .format(self.distance_table)

        try:
            # self.cursor.execute(insert_into_song_table, (song1.hash, song1.name,
            #                                              numpy.ndarray.tobytes(song1.mfcc),
            #                                              numpy.ndarray.tobytes(song1.chroma_cens),
            #                                              numpy.ndarray.tobytes(song1.chroma_stft),
            #                                              numpy.ndarray.tobytes(song1.mel),
            #                                              numpy.ndarray.tobytes(song1.tonnetz),
            #                                              numpy.ndarray.tobytes(song1.rhythm)))
            #
            # self.cursor.execute(insert_into_song_table, (song2.hash, song2.name,
            #                                              numpy.ndarray.tobytes(song2.mfcc),
            #                                              numpy.ndarray.tobytes(song2.chroma_cens),
            #                                              numpy.ndarray.tobytes(song2.chroma_stft),
            #                                              numpy.ndarray.tobytes(song2.mel),
            #                                              numpy.ndarray.tobytes(song2.tonnetz),
            #                                              numpy.ndarray.tobytes(song2.rhythm)))

            self.cursor.execute(insert_into_feature_table, (feature.hash1, feature.hash2, feature.mfcc_dist,
                                                            feature.chroma_cens_dist, feature.chroma_stf_dist,
                                                            feature.mel_dist, feature.tonnetz_dist,
                                                            feature.rhythm_dist))

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error("Error in adding data to table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    def delete_tables(self):
        delete_song_table = 'DROP TABLE ' + self.song_table
        delete_feature_table = 'DROP TABLE ' + self.distance_table

        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(delete_song_table)
            self.cursor.execute(delete_feature_table)
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error("Error in deleting table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    def get_song(self, hash_val):
        """
        Get song data according to selected hash
        :param hash: hash of audio
        :return song class: data of song
        """
        get_song = 'SELECT * FROM {} WHERE hash = ?'.format(self.song_table)
        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_song, (hash_val,))
            song = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error('Error in fetching song data', str(e.args[0]))
            self.conn.close()
            return None
        return song

    def get_distance(self, hash1, hash2):
        """
        Return the feature distnaces between two files

        :param hash1:
        :param hash2:
        :return: feature class
        """
        get_distance = 'SELECT * FROM {} WHERE hash1=? AND hash2=?'.format(self.distance_table)
        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_distance, (hash1, hash2))
            distances = self.cursor.fetchall()
            if len(distances) == 0:
                self.cursor.execute(get_distance, (hash2, hash1))
                distances = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error('Error in fetching song data', str(e.args[0]))
            self.conn.close()
            return None
        return distances

    # toDO: correct save data method get data from database and compare the previous numpy array with new ones
    # todo: np.fromstring()
