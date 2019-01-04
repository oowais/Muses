import os
import time

from db import Db
from util import sha256sum, scale, get_name, progress, sum_n
from thread import ThreadWithReturnValue
from extractor import get_all_features, get_distance

# database_name = 'db.sqlite'
database_name = 'test.sqlite'
audio_folder_name = 'audio_resources'
root_dir_path = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(root_dir_path, database_name)
audio_path = os.path.join(root_dir_path, audio_folder_name)


def calc_feature():
    """
    Loop through the audio_resources folder and calculate features of each track and the distance between them
    """
    start_time = time.time()
    db = Db(storage_file=db_file)
    if not db.create_tables():
        print('Problems in creating tables')
        return

    # loop over the directory
    file_list = os.listdir(audio_path)
    file_list_size = len(file_list)
    processed_file_list = []
    i = 0
    processing = False
    total_prog = sum_n(file_list_size + 1)
    curr_prog = 0
    print('Processing...')
    while i < file_list_size:
        ifile = file_list[i]
        # get two audios
        if ifile not in processed_file_list:
            ipath = os.path.join(audio_path, ifile)
            update_ifile = True

            processed_file_list.append(ifile)
            ifile_sha = sha256sum(os.path.join(audio_path, ifile))
            j = i + 1
            while j < file_list_size:
                jfile = file_list[j]
                jpath = os.path.join(audio_path, jfile)
                jfile_sha = sha256sum(os.path.join(audio_path, jfile))

                # check if their hash is already present in the distance table
                if db.is_hashes_present(ifile_sha, jfile_sha):
                    j += 1
                    continue
                else:
                    # if not, calculate features and distances and save to db
                    if update_ifile:
                        ithread = ThreadWithReturnValue(target=get_all_features, args=(ipath,))
                        ithread.start()
                        # ifeature = ex.get_all_features(os.path.join(audio_path, ifile))
                    jthread = ThreadWithReturnValue(target=get_all_features, args=(jpath,))
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
                    dist_thread = ThreadWithReturnValue(target=save_dist_to_db, args=(db, ifeature, jfeature,))
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


def save_dist_to_db(db, ifeature, jfeature):
    dist = get_distance(ifeature, jfeature)
    db.save_feature_distances(dist)


def get_names_from_db():
    db = Db(storage_file=db_file)
    names_db = db.get_all_names()
    names = []
    for n in names_db:
        if n[0] not in names:
            names.append(n[0])
        if n[1] not in names:
            names.append(n[1])
    return names


def show_similarity():
    db = Db(storage_file=db_file)
    names = get_names_from_db()
    factors = db.get_all_distances()

    sum_list = []
    for fact in factors:
        sum_list.append(fact[2] + fact[3] + fact[4] + fact[5] + fact[6] + fact[7])

    min_val = min(sum_list)
    max_val = max(sum_list)

    while True:
        print()
        var = 0
        # Printing name of files from the folder

        while var < len(names):
            print('%-30s %-30s' % (str(var + 1) + ' ' + names[var], str(var + 2) + ' ' + names[var + 1]))
            var += 2

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

        print('Similarity measure with ', selected_track)
        result = []
        for index, factor in enumerate(factors):
            scaled_sum = scale(rmin=min_val, rmax=max_val, val=sum_list[index])
            if factor[0] == selected_track:
                result.append((factor[1], 100 * (1 - scaled_sum)))
            elif factor[1] == selected_track:
                result.append((factor[0], 100 * (1 - scaled_sum)))

        # Sorting according to similarity
        result.sort(key=lambda tup: tup[1], reverse=True)
        for a in result:
            print('%-30s - %.1f%%' % (a[0], a[1]))
        print('---------------------------------------------------------------')
        print('Press Enter to continue...')
        input()
        print()


if __name__ == '__main__':
    calc_feature()
    show_similarity()
