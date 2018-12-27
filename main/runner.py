import numpy as np
from main.db import Db
from main.datastructure.feature import Feature
from main.datastructure.distance import Distance
from main.extractor import Extractor
from scipy.spatial.distance import euclidean
import os
import fastdtw


def main():
    name1 = 'metal0.mp3'
    name2 = 'metal1.mp3'
    file1 = '../audio_resources/' + name1
    file2 = '../audio_resources/' + name2

    ex = Extractor()

    feature1 = ex.get_all_features(file1)
    feature2 = ex.get_all_features(file2)

    dist = ex.get_distance(feature1, feature2)

    database_name = 'db.sqlite'
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    # print('deleting tables: ', db.delete_tables())
    print('creating tables: ', db.create_tables())
    # todo: insert zero values in extreme distance table
    # print('Saving into db: ', db.save_feature_distances(dist_obj=dist))


def test():
    database_name = 'db.sqlite'
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    song1 = db.get_song(hash1)
    song2 = db.get_song(hash2)

    print(song1[0][0])
    print(song1[0][1])

    print(song2[0][0])
    print(song2[0][1])

    mfcc1 = np.frombuffer(song1[0][2])
    mfcc1 = mfcc1.reshape(20, int(len(mfcc1) / 20))
    mfcc2 = np.frombuffer(song2[0][2])
    mfcc2 = mfcc2.reshape(20, int(len(mfcc2) / 20))

    chroma_cens1 = np.frombuffer(song1[0][3])
    chroma_cens1 = chroma_cens1.reshape(12, int(len(chroma_cens1) / 12))
    chroma_cens2 = np.frombuffer(song2[0][3])
    chroma_cens2 = chroma_cens2.reshape(12, int(len(chroma_cens2) / 12))

    chroma_stft1 = np.frombuffer(song1[0][4])
    chroma_stft1 = chroma_stft1.reshape(12, int(len(chroma_stft1) / 12))
    chroma_stft2 = np.frombuffer(song2[0][4])
    chroma_stft2 = chroma_stft2.reshape(12, int(len(chroma_stft2) / 12))

    mel1 = np.frombuffer(song1[0][5])
    mel1 = mel1.reshape(128, int(len(mel1) / 128))
    mel2 = np.frombuffer(song2[0][5])
    mel2 = mel2.reshape(128, int(len(mel2) / 128))

    tonnetz1 = np.frombuffer(song1[0][6])
    tonnetz1 = tonnetz1.reshape(6, int(len(tonnetz1) / 6))
    tonnetz2 = np.frombuffer(song2[0][6])
    tonnetz2 = tonnetz2.reshape(6, int(len(tonnetz2) / 6))

    tempogram1 = np.frombuffer(song1[0][7])
    tempogram1 = tempogram1.reshape(384, int(len(tempogram1) / 384))
    tempogram2 = np.frombuffer(song2[0][7])
    tempogram2 = tempogram2.reshape(384, int(len(tempogram2) / 384))

    dist_func = euclidean

    distance, new_path = fastdtw.fastdtw(mfcc1.T, mfcc2.T, dist=dist_func)
    distance2, new_path2 = fastdtw.fastdtw(chroma_cens1.T, chroma_cens2.T, dist=dist_func)
    distance3, new_path3 = fastdtw.fastdtw(chroma_stft1.T, chroma_stft2.T, dist=dist_func)
    distance4, new_path4 = fastdtw.fastdtw(mel1.T, mel2.T, dist=dist_func)
    distance5, new_path5 = fastdtw.fastdtw(tonnetz1.T, tonnetz2.T, dist=dist_func)
    distance6, new_path6 = fastdtw.fastdtw(tempogram1.T, tempogram2.T, dist=dist_func)

    print(distance)
    print(distance2)
    print(distance3)
    print(distance4)
    print(distance5)
    print(distance6)


def test2():
    database_name = 'db.sqlite'
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    dist = db.get_distance(hash2, hash1)
    print(dist)


if __name__ == '__main__':
    main()
    # test()
    # test2()
