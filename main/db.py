import sqlite3
import logging
import numpy


# TODO: add a new table for storing highest and lowest value of all the features
# TODO: add a method to factorize the values
# TODO: create update_tables() method which might be used later on
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
        self.extreme_distance_table = 'extreme_distance'

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

        create_distance_table = "CREATE TABLE IF NOT EXISTS {} (" \
                                "hash1 text NOT NULL, hash2 text NOT NULL, " \
                                "mfcc_dist real, mfcc_dist_factor real, " \
                                "chroma_cens_dist real, chroma_cens_dist_factor real, " \
                                "chroma_stf_dist real, chroma_stf_dist_factor real," \
                                "mel_dist real, mel_dist_factor real, " \
                                "tonnetz_dist real, tonnetz_dist_factor real," \
                                "rhythm_dist real, rhythm_dist_factor real," \
                                "PRIMARY KEY (hash1, hash2))" \
            .format(self.distance_table)

        create_max_distance_table = "CREATE TABLE IF NOT EXISTS {} (feature PRIMARY KEY, min_distance REAL NOT NUll," \
                                    "max_distance REAL NOT NULL)".format(self.extreme_distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            # self.cursor.execute(create_song_table)
            self.cursor.execute(create_distance_table)
            self.cursor.execute(create_max_distance_table)

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error("Error in creating table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    def save_feature_distances(self, dist_obj):
        """Saves the song name and its hash to table

        Parameters
        ----------
        dist_obj: distance class object

        Returns
        -------
        True if data saved successfully, False otherwise
        """
        self.open_connection(self.db_file)

        # insert_into_song_table = "INSERT INTO {} (hash, name, mfcc, chroma_cens, chroma_stf, mel, tonnetz, rhythm) " \
        #                          "VALUES (?,?,?,?,?,?,?,?)".format(self.song_table)

        insert_into_distance_table = "INSERT INTO {} (hash1, hash2, mfcc_dist, chroma_cens_dist, chroma_stf_dist," \
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

            self.cursor.execute(insert_into_distance_table, (dist_obj.hash1, dist_obj.hash2, dist_obj.mfcc_dist,
                                                             dist_obj.chroma_cens_dist, dist_obj.chroma_stf_dist,
                                                             dist_obj.mel_dist, dist_obj.tonnetz_dist,
                                                             dist_obj.rhythm_dist))

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error("Error in adding data to table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    def set_initial_extreme_distance(self, min_feature, max_feature):
        """
        Update the table with min and max features values initially

        :param min_feature:
        :param max_feature:
        :return:
        """
        insert_into_extreme_distance = 'INSERT INTO {} (feature, min_distance, max_distance) VALUES (?,?,?)' \
            .format(self.extreme_distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(insert_into_extreme_distance, ('mfcc', min_feature.mfcc, max_feature.mfcc))
            self.cursor.execute(insert_into_extreme_distance,
                                ('chroma_cens', min_feature.chroma_cens, max_feature.chroma_cens))
            self.cursor.execute(insert_into_extreme_distance,
                                ('chroma_stft', min_feature.chroma_stft, max_feature.chroma_stft))
            self.cursor.execute(insert_into_extreme_distance, ('mel', min_feature.mel, max_feature.mel))
            self.cursor.execute(insert_into_extreme_distance, ('tonnetz', min_feature.tonnetz, max_feature.tonnetz))
            self.cursor.execute(insert_into_extreme_distance, ('rhythm', min_feature.rhythm, max_feature.rhythm))
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error("Error in inserting initially into extreme table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    def update_extreme_distance(self, feature_name, min_dist, max_dist):
        """
        Update the table with min and max features values initially

        :param feature_name:
        :param min_dist:
        :param max_dist:
        :return:
        """
        update_extreme_distance = 'UPDATE {} SET min_distance=?, max_distance=? WHERE feature=?' \
            .format(self.extreme_distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(update_extreme_distance, (min_dist, max_dist, feature_name))
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error("Error in updating features values in extreme table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    # TODO: allows the user to add factors values to distance table
    def add_factors(self, feature):
        """add the factors to """
        pass

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
            self.logger.error('Error in fetching from distance table', str(e.args[0]))
            self.conn.close()
            return None
        return distances

    def get_extreme_distances(self):
        """
        Returns the min and max distances of all the feautures

        :return:
        """
        get_extreme_distances = "SELECT * FROM {}".format(self.extreme_distance_table)
        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_extreme_distances)
            data = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            self.logger.error('Error in fetching from extreme distance table', str(e.args[0]))
            self.conn.close()
            return None
        return data
