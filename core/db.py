import sqlite3


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
            print(str(e))

    def create_tables(self):
        """
        Create tables if not exists

        :return:
        True if table created or already present, False if database error
        """
        # create_song_table = "CREATE TABLE IF NOT EXISTS {} (hash text PRIMARY KEY, " \
        #                     "name text NOT NULL, mfcc BLOB, chroma_cens BLOB, chroma_stft BLOB, mel BLOB," \
        #                     "tonnetz BLOB, rhythm BLOB)".format(self.song_table)

        create_distance_table = "CREATE TABLE IF NOT EXISTS {} (" \
                                "hash1 text NOT NULL, hash2 text NOT NULL, name1 text NOT NULL, name2 text NOT NULL," \
                                "mfcc_dist real, cqt_dist real, chroma_stft_dist real, pcp_dist real," \
                                "tonnetz_dist real, rhythm_dist real, PRIMARY KEY (hash1, hash2))" \
            .format(self.distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            # self.cursor.execute(create_song_table)
            self.cursor.execute(create_distance_table)

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            print("Error in creating table: " + str(e.args[0]))
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

        insert_into_distance_table = "INSERT INTO {} (hash1, hash2, name1, name2, mfcc_dist, cqt_dist," \
                                     "chroma_stft_dist, pcp_dist, tonnetz_dist, rhythm_dist) " \
                                     "VALUES (?,?,?,?,?,?,?,?,?,?)" \
            .format(self.distance_table)

        try:
            self.cursor.execute(insert_into_distance_table, (dist_obj.hash1, dist_obj.hash2,
                                                             dist_obj.name1, dist_obj.name2,
                                                             dist_obj.mfcc_dist, dist_obj.cqt_dist,
                                                             dist_obj.chroma_stft_dist, dist_obj.pcp_dist,
                                                             dist_obj.tonnetz_dist, dist_obj.rhythm_dist))

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

            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            self.conn.close()
            return False
        return True

    def delete_tables(self):
        """
        deletes the database
        :return:
        """
        delete_feature_table = 'DROP TABLE {}'.format(self.distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(delete_feature_table)
            self.conn.commit()
            self.conn.close()
        except sqlite3.Error as e:
            print("Error in deleting table: " + str(e.args[0]))
            self.conn.close()
            return False
        return True

    @DeprecationWarning
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
            print('Error in fetching song data', str(e.args[0]))
            self.conn.close()
            return None
        return song

    def is_hashes_present(self, hash1, hash2):
        """
        check if hashes already present in distance table

        :param hash1:
        :param hash2:
        :return: True, False or None
        """
        get_distance = 'SELECT * FROM {} WHERE ((hash1=? AND hash2=?) OR (hash1=? AND hash2=?))' \
            .format(self.distance_table)
        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_distance, (hash1, hash2, hash2, hash1))
            distances = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            print('Error in fetching from distance table', str(e.args[0]))
            self.conn.close()
            return None
        if len(distances) > 0:
            return True
        else:
            return False

    def get_complete_distance_table(self):
        """
        Returns the numbers of rows in distance table
        """
        get = 'SELECT * FROM {}'.format(self.distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get)
            value = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            print('Error in fetching number of rows in distance table', str(e.args[0]))
            self.conn.close()
            return None
        return value

    def get_distance(self, hash1, hash2):
        """
        Return the feature distances between two audio files from db if present

        :param hash1:
        :param hash2:
        :return: feature class or None
        """
        get_distance = 'SELECT * FROM {} WHERE hash1=? AND hash2=?'.format(self.distance_table)
        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_distance, (hash1, hash2))
            distance = self.cursor.fetchall()
            if len(distance) == 0:
                self.cursor.execute(get_distance, (hash2, hash1))
                distance = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            print('Error in fetching from distance table', str(e.args[0]))
            self.conn.close()
            return None
        return distance

    def get_all_distances(self):
        """
        Returns all the factors values of features from the distance tables
        """

        get_factor = 'SELECT name1, name2, mfcc_dist, cqt_dist, chroma_stft_dist, pcp_dist, tonnetz_dist,' \
                     'rhythm_dist FROM {}'.format(self.distance_table)

        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_factor)
            distances = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            print('Error in fetching distances from extreme distance table', str(e.args[0]))
            self.conn.close()
            return None
        return distances

    def get_all_names(self):
        """
        Returns name of all the files present in database
        """
        get_names = 'SELECT name1, name2 FROM {}'.format(self.distance_table)
        try:
            self.open_connection(db_file=self.db_file)
            self.cursor.execute(get_names)
            names = self.cursor.fetchall()
            self.conn.close()
        except sqlite3.Error as e:
            print('Error in fetching names from extreme distance table', str(e.args[0]))
            self.conn.close()
            return None
        return names
