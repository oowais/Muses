import os
import sys
from time import sleep

import fastdtw
import librosa
from scipy.spatial.distance import euclidean

from core.db import Db
from core.extractor import get_all_features, get_distance
from core.util import scale, sha256sum

database_name = 'db.sqlite'
audio_folder_name = 'audio_resources'
root_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
db_file = os.path.join(root_dir_path, database_name)
audio_path = os.path.join(root_dir_path, audio_folder_name)


def is_hash_present_test():
    name1 = 'classical4.mp3'
    name2 = 'country6.mp3'
    file1 = os.path.join(audio_path, name1)
    file2 = os.path.join(audio_path, name2)

    db = Db(storage_file=db_file)
    sha1 = sha256sum(file1)
    sha2 = sha256sum(file2)
    if not db.is_hashes_present(sha1, sha2):
        print('flase')
    else:
        print('true')


def get_features_and_save_to_db_test():
    name1 = 'metal0.mp3'
    name2 = 'metal1.mp3'
    file1 = os.path.join(audio_path, name1)
    file2 = os.path.join(audio_path, name2)

    feature1 = get_all_features(file1)
    feature2 = get_all_features(file2)

    dist = get_distance(feature1, feature2)

    db = Db(storage_file=db_file)
    # print('deleting tables: ', db.delete_tables())
    print('creating tables: ', db.create_tables())
    print('Saving into db: ', db.save_feature_distances(dist_obj=dist))


def test_get_hash_from_db():
    db = Db(storage_file=db_file)
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    dist = db.get_distance(hash2, hash1)
    print(dist)


def check_hashes_present():
    db = Db(storage_file=db_file)
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    print(db.is_hashes_present(hash1, hash2))


def progress_bar_test():
    lim = 24
    for i in range(21):
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-20s] %d%%" % ('=' * i, 5 * i))
        sys.stdout.flush()
        sleep(0.25)


def draw_progress_bar(percent, barlen=20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barlen):
        if i < int(barlen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()


def progress(percent, barlen=20):
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(barlen * percent), barlen, percent * 100))
    sys.stdout.flush()


def sum_n(n):
    return (n * (n - 1)) / 2


def mfcc_test():
    dist_func = euclidean
    name1 = 'blues0.mp3'
    name2 = 'blues1.mp3'
    file1 = os.path.join(audio_path, name1)
    file2 = os.path.join(audio_path, name2)
    y1, sr1 = librosa.load(file1)
    mfcc1 = librosa.feature.mfcc(y1, sr1, n_mfcc=20)

    mel_spectrogram1 = librosa.feature.melspectrogram(y1, sr1)
    log_s1 = librosa.amplitude_to_db(mel_spectrogram1)
    mfccnew1 = librosa.feature.mfcc(S=log_s1)

    y2, sr2 = librosa.load(file2)
    mfcc2 = librosa.feature.mfcc(y2, sr2, n_mfcc=20)

    mel_spectrogram2 = librosa.feature.melspectrogram(y2, sr2)
    log_s2 = librosa.amplitude_to_db(mel_spectrogram2)
    mfccnew2 = librosa.feature.mfcc(S=log_s2)

    dist1, path = fastdtw.fastdtw(mfcc1.T, mfcc2.T, dist=dist_func)
    dist2, path = fastdtw.fastdtw(mfccnew1.T, mfccnew2.T, dist=dist_func)

    print(dist1, dist2)


def progress_loops_test():
    progress(0)
    size = 5
    total_prog = sum_n(size)
    print('total progress= ', total_prog)
    curr_prog = 0
    progress(curr_prog)
    for i in range(size):
        j = i + 1
        while j < size:
            curr_prog += 1
            progress(scale(0, total_prog, curr_prog))
            print('current: ', curr_prog)
            sleep(.25)
            j += 1
    progress(1)


if __name__ == '__main__':
    is_hash_present_test()
