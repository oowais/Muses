import os
import time
import sys
from itertools import chain

from core.db import Db
from core.util import sha256sum, scale, progress, sum_n
from core.thread import StartThread
from core.extractor import get_all_features, get_distance


class Main:

    def __init__(self, db_name):
        """
        Constructor for Main class

        Attributes
        ----------
        audio_path: location of audio files
        db: database class object
        """
        # Go through README.md to see which database to use
        _database_name = db_name
        _audio_folder_name = 'audio_resources'
        _root_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        _db_file = os.path.join(_root_dir_path, _database_name)
        self.audio_path = os.path.join(_root_dir_path, _audio_folder_name)
        self.db = Db(storage_file=_db_file)

    def calc_feature_new(self):
        """
        Loop through the audio_resources folder and calculate features of each track and the distance between them
        and then save the distance to the database
        """
        start_time = time.time()
        if not self.db.create_tables():
            print('Problem in creating tables')
            return

        file_list, file_list_size = self._get_files_from_folder()

        # if there is no file in audio_resources, no point in going forward
        if file_list_size == 0:
            return

        print('Checking if already present in db...')
        val = self.db.get_all_names()
        if len(val) == 0:
            print('Database is empty')
            to_be_processed = file_list
        else:
            # check if file is already processed in database
            to_be_processed = self._not_present_in_db(file_list=file_list)

        # if all files are already processed, then exit this and show similarities
        if len(to_be_processed) == 0:
            return

        print()
        # calculate the features of all the files
        features = self._calculate_features(files=to_be_processed)
        print()

        # calculate the distances between all the features
        dist = self._calulate_distances(features=features)
        print()

        # save the distances in the distance table
        self._save_dist_to_db_new(distances=dist)
        print()
        finish_time = time.time() - start_time
        if finish_time > 120:
            print('Done! Took %.2f minutes to complete' % (finish_time / 60))
        else:
            print('Done! Took %.2f seconds to complete' % finish_time)

    def calc_feature(self):
        """
        Loop through the audio_resources folder and calculate features of each track and the distance between them
        and then save the distance to the database
        """
        start_time = time.time()
        if not self.db.create_tables():
            print('Problems in creating tables')
            return

        # loop over the directory
        file_list, file_list_size = self._get_files_from_folder()
        processed_file_list = []

        processing = False
        total_prog = sum_n(file_list_size + 1)
        curr_prog = 0
        print('Processing...')
        # start progress bar in console
        progress(curr_prog)
        i = 0
        while i < file_list_size:
            ifile = file_list[i]
            # get audios
            if ifile not in processed_file_list:
                ipath = os.path.join(self.audio_path, ifile)
                update_ifile = True

                processed_file_list.append(ifile)
                ifile_sha = sha256sum(ipath)
                j = i + 1
                while j < file_list_size:
                    jfile = file_list[j]
                    jpath = os.path.join(self.audio_path, jfile)
                    jfile_sha = sha256sum(jpath)

                    # check if their hash is already present in the distance table
                    if self.db.is_hashes_present(ifile_sha, jfile_sha):
                        j += 1
                        continue
                    else:
                        # if not, calculate features and distances and save to db
                        if update_ifile:
                            ithread = StartThread(target=get_all_features, args=(ipath,))
                            ithread.start()
                            # ifeature = ex.get_all_features(os.path.join(audio_path, ifile))
                        jthread = StartThread(target=get_all_features, args=(jpath,))
                        jthread.start()

                        if update_ifile:
                            ifeature = ithread.join()
                            update_ifile = False
                            curr_prog += 1
                            progress(scale(0, total_prog, curr_prog))
                        jfeature = jthread.join()
                        # jfeature = ex.get_all_features(os.path.join(audio_path, jfile))

                        # dist = ex.get_distance(ifeature, jfeature)
                        # db.save_feature_distances(dist)
                        if processing:  # distances can be calculated until the next features are calculated
                            dist_thread.join()
                        dist_thread = StartThread(target=self._save_dist_to_db, args=(ifeature, jfeature,))
                        dist_thread.start()
                        curr_prog += 1
                        progress(scale(0, total_prog, curr_prog))
                        processing = True
                    j += 1
            i += 1
        if processing:
            dist_thread.join()
            message = 'Done! Took %.0f seconds to calculate features and distances between ' % (
                    time.time() - start_time) + str(file_list_size) + ' files'
        else:
            message = 'Data collected from database'
        progress(1)
        print()
        print(message)

    def show_similarity(self):
        """
        Gets the data from database and shows the similarity between the tracks
        """
        names = self._get_names_from_db()
        factors = self.db.get_all_distances()
        
        if factors == None:
            print('Audio_resources folder and the database is empty!')
            return

        if len(factors) == 0:
            print('Nothing to show')
            return

        sum_list = []
        for fact in factors:
            sum_list.append(fact[2] + fact[3] + fact[4] + fact[5] + fact[6] + fact[7])

        min_val = min(sum_list)
        max_val = max(sum_list)

        while True:
            print()
            # Printing name of files from the database
            for i, name in enumerate(names):
                print(' %-30s ' % (str(i + 1) + '. ' + name), end='')
                if (i + 1) % 3 == 0:
                    print()
            print()
            # Getting a file number
            try:
                val = int(input('Select a track number(0 to exit)...'))
            except ValueError as e:
                print('Enter a valid number, Press enter to continue')
                input()
                continue
            if val == 0:
                break
            elif val > len(names):
                print('Enter a valid number, Press enter to continue')
                input()
                continue
            print()
            selected_track = names[val - 1]

            print('Top 10 tracks closer to ', selected_track, ' are:')
            # print('Similarity measure with ', selected_track)
            result = []
            for index, factor in enumerate(factors):
                scaled_sum = scale(rmin=min_val, rmax=max_val, val=sum_list[index])
                if factor[0] == selected_track:
                    result.append((factor[1], 100 * (1 - scaled_sum)))
                elif factor[1] == selected_track:
                    result.append((factor[0], 100 * (1 - scaled_sum)))

            # Sorting the list according to maximum distance
            result.sort(key=lambda tup: tup[1], reverse=True)
            for ind, val in enumerate(result):
                # Printing top 10 results
                if ind is 10:
                    break
                print('%2d. %-30s - %.1f %%' % (ind+1, val[0], val[1]))
            print('-------------------------------------------------')
            x = input('Press Enter to continue or 0 to exit...')
            if x == '0':
                break
            print()

    # method used in older calc_feature
    def _save_dist_to_db(self, ifeature, jfeature):
        dist = get_distance(ifeature, jfeature)
        self.db.save_feature_distances(dist)

    def _get_names_from_db(self):
        names_db = self.db.get_all_names()
        tup_to_list = list(chain.from_iterable(names_db))
        names = list(set(tup_to_list))
        return names

    def _get_files_from_folder(self):
        file_list = []
        for file in os.listdir(self.audio_path):
            if file.endswith('.mp3') or file.endswith('.wav'):
                file_list.append(file)
        return file_list, len(file_list)

    def _not_present_in_db(self, file_list):
        """
        Checks if files present in audio_resources is already not processed in database
        :param file_list: list of files in audio_resources folder
        :return to_be_processed: list of files which are in audio_resources and not yet processed
        """
        to_be_processed = []
        size = len(file_list)
        total_prog = sum_n(size + 1)
        curr_prog = 0
        progress(0)
        for i, ifile in enumerate(file_list):
            ifile_sha = sha256sum(os.path.join(self.audio_path, ifile))
            j = i + 1
            while j < size:
                jfile = file_list[j]
                jfile_sha = sha256sum(os.path.join(self.audio_path, jfile))
                if ifile not in to_be_processed and not self.db.is_hashes_present(ifile_sha, jfile_sha):
                    to_be_processed.append(ifile)
                curr_prog += 1
                progress(scale(0, total_prog, curr_prog))
                j += 1
        progress(1)
        return to_be_processed

    def _calculate_features(self, files):
        print('Calculating features...')
        features = []
        total_prog = len(files)
        curr_prog = 0
        for file in files:
            progress(percent=scale(0, total_prog, curr_prog), name=file)
            features.append(get_all_features(os.path.join(self.audio_path, file)))
            curr_prog += 1
        progress(1)
        return features

    def _calulate_distances(self, features):
        print('Calculating distances...')
        dist = []
        size = len(features)
        total_prog = sum_n(size)
        curr_prog = 0
        for i, ifeature in enumerate(features):
            j = i + 1
            while j < size:
                jfeature = features[j]
                progress(percent=scale(0, total_prog, curr_prog), name=ifeature.name + ' <==> ' + jfeature.name)
                dist.append(get_distance(ifeature, jfeature))
                curr_prog += 1
                j += 1
        progress(1)
        return dist

    def _save_dist_to_db_new(self, distances):
        print('Saving to DB...')
        total_prog = len(distances)
        curr_prog = 0
        progress(curr_prog)
        for dist in distances:
            if self.db.is_hashes_present(dist.hash1, dist.hash2):
                continue
            self.db.save_feature_distances(dist)
            curr_prog += 1
            progress(scale(0, total_prog, curr_prog))
        progress(1)
