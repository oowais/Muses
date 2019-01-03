import os
import time
from threading import Thread

from db import Db
from extractor import Extractor
from util import sha256sum, scale, get_name

database_name = 'db.sqlite'
audio_folder_name = 'audio_resources'
root_dir_path = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(root_dir_path, database_name)
audio_path = os.path.join(root_dir_path, audio_folder_name)


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def get_features_and_distance():
    """
    Loop through the audio_resources folder and caluclate features of each track and the distance between them
    """
    start_time = time.time()
    ex = Extractor()
    db = Db(storage_file=db_file)
    print('Creating tables if not present...')
    if not db.create_tables():
        return

    # todo: loop over the directory
    file_list = os.listdir(audio_path)
    file_list_size = len(file_list)
    processed_file_list = []
    i = 0
    while i < file_list_size:
        ifile = file_list[i]
        # get two audios
        if ifile not in processed_file_list:
            ipath = os.path.join(audio_path, ifile)
            update_ifile = 1
            processed_file_list.append(ifile)
            print('------------------------')
            # using names instead of hashes so that while checking results its easier to read
            ifile_sha = sha256sum(os.path.join(audio_path, ifile))
            j = i + 1
            while j < file_list_size:
                jfile = file_list[j]
                jpath = os.path.join(audio_path, jfile)
                jfile_sha = sha256sum(os.path.join(audio_path, jfile))

                # check if their hash is already present in the distance table
                if db.is_hashes_present(ifile_sha, jfile_sha):
                    print(ifile, ' and ', jfile, ' already present in database')
                    j += 1
                    continue
                else:
                    # if not, calculate features and distances and save to db
                    if update_ifile:
                        ithread = ThreadWithReturnValue(target=ex.get_all_features, args=(ipath,))
                        ithread.start()
                        # ifeature = ex.get_all_features(os.path.join(audio_path, ifile))
                        update_ifile = 0
                    jthread = ThreadWithReturnValue(target=ex.get_all_features, args=(jpath,))
                    jthread.start()
                    ifeature = ithread.join()
                    jfeature = jthread.join()
                    # jfeature = ex.get_all_features(os.path.join(audio_path, jfile))

                    # dist = ex.get_distance(ifeature, jfeature)
                    # db.save_feature_distances(dist)
                    if i > 0:
                        dist_thread.join()
                    dist_thread = ThreadWithReturnValue(target=save_feature, args=(db, ex, ifeature, jfeature,))
                    dist_thread.start()
                j += 1
        i += 1
    # todo: check if its an object or not
    dist_thread.join()
    print("Done! Took %.0f seconds to calculate features and distances between " % (
            time.time() - start_time) + str(file_list_size) + " files")


def save_feature(db, ex, ifeature, jfeature):
    dist = ex.get_distance(ifeature, jfeature)
    db.save_feature_distances(dist)


def print_factors():
    db = Db(storage_file=db_file)
    file_list = os.listdir(audio_path)
    name_list = []

    for file in file_list:
        name_list.append(get_name(file))
    factors = db.get_all_distances()
    while True:
        print()
        var = 0
        while var < len(name_list):
            print(var + 1, ' ', name_list[var])
            var += 1
        val = int(input('Select a track number(0 to exit)...'))
        if val == 0:
            break
        elif val > len(name_list):
            print('Enter a valid number, Press enter to continue')
            input()
            continue
        print()
        selected_track = name_list[val - 1]

        sum_list = []
        for fact in factors:
            # sum_list.append(fact[2] + fact[3] + fact[4] + fact[5] + fact[6] + fact[7])
            # not using chroma_cens and mel feature
            sum_list.append(fact[2] + fact[4] + fact[6] + fact[7])

        min_val = min(sum_list)
        max_val = max(sum_list)

        print('Tracks closest to ', selected_track, '(in ascending order):')
        result = []
        i = 0
        while i < len(factors):
            scaled_sum = scale(rmin=min_val, rmax=max_val, val=sum_list[i])
            if factors[i][0] == selected_track:
                result.append((factors[i][1], scaled_sum))
            elif factors[i][1] == selected_track:
                result.append((factors[i][0], scaled_sum))
            i += 1

        result.sort(key=lambda tup: tup[1])
        for a in result:
            print(a[0])
        print('---------------------------------------------------------------')
        print()


if __name__ == '__main__':
    get_features_and_distance()
    print_factors()
