import numpy as np
from main.db import Db
from main.hash import sha256sum
from main.datastructure.song import Song
from main.datastructure.feature import Feature
from scipy.spatial.distance import euclidean
import os
import librosa
import fastdtw


# to do change the datatype of features from REAL to BLOB
def main():
    name1 = 'metal0.mp3'
    name2 = 'metal1.mp3'
    file1 = '../audio_resources/' + name1
    file2 = '../audio_resources/' + name2

    y1, sr1 = librosa.load(file1)
    y2, sr2 = librosa.load(file2)

    # Calculating mfcc feature
    mfcc1 = librosa.feature.mfcc(y1, sr1, n_mfcc=20)
    mfcc2 = librosa.feature.mfcc(y2, sr2, n_mfcc=20)
    print('mfcc1 , mfcc2')

    # Calculating chroma_cens feature
    chroma_cens1 = librosa.feature.chroma_cens(y=y1, sr=sr1)
    chroma_cens2 = librosa.feature.chroma_cens(y=y2, sr=sr2)
    print('chroma_cens1, chroma_cens2')

    chroma_stft1 = librosa.feature.chroma_stft(y=y1, sr=sr1)
    chroma_stft2 = librosa.feature.chroma_stft(y=y2, sr=sr2)
    print('chroma_stft1, chroma_stft2')

    mel1 = librosa.feature.melspectrogram(y=y1, sr=sr1)
    mel2 = librosa.feature.melspectrogram(y=y2, sr=sr2)
    print('mel1, mel2')

    tonnetz1 = librosa.feature.tonnetz(y=y1, sr=sr1)
    tonnetz2 = librosa.feature.tonnetz(y=y2, sr=sr2)
    print('tonnetz1, tonnetz2')

    # Rhythm
    tempogram1 = librosa.feature.tempogram(y=y1, sr=sr1)
    tempogram2 = librosa.feature.tempogram(y=y2, sr=sr2)
    print('tempogram1, tempogram2')

    hash1 = sha256sum(file1)
    hash2 = sha256sum(file2)
    print(hash1, hash2)

    song1 = Song(hash=hash1, name=name1, mfcc=mfcc1, chroma_cens=chroma_cens1, chroma_stft=chroma_stft1, mel=mel1,
                 tonnetz=tonnetz1, rhythm=tempogram1)

    song2 = Song(hash=hash2, name=name2, mfcc=mfcc2, chroma_cens=chroma_cens2, chroma_stft=chroma_stft2, mel=mel2,
                 tonnetz=tonnetz2, rhythm=tempogram2)

    dist_func = euclidean

    distance, new_path = fastdtw.fastdtw(mfcc1.T, mfcc2.T, dist=dist_func)
    distance2, new_path2 = fastdtw.fastdtw(chroma_cens1.T, chroma_cens2.T, dist=dist_func)
    distance3, new_path3 = fastdtw.fastdtw(chroma_stft1.T, chroma_stft2.T, dist=dist_func)
    distance4, new_path4 = fastdtw.fastdtw(mel1.T, mel2.T, dist=dist_func)
    distance5, new_path5 = fastdtw.fastdtw(tonnetz1.T, tonnetz2.T, dist=dist_func)
    distance6, new_path6 = fastdtw.fastdtw(tempogram1.T, tempogram2.T, dist=dist_func)

    features = Feature(hash1=hash1, hash2=hash2, mfcc_dist=distance, chroma_cens_dist=distance2,
                       chroma_stf_dist=distance3, mel_dist=distance4, tonnetz_dist=distance5, rhythm_dist=distance6)

    database_name = 'db.sqlite'
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    # print('deleting tables: ', db.delete_tables())
    print('creating tables: ', db.create_tables())
    print('Saving into db: ', db.save_feature_distances(feature=features))


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
    # main()
    # test()
    test2()
