import librosa
import fastdtw
from scipy.spatial.distance import euclidean

from datastructure.feature import Feature
from datastructure.distance import Distance
from util import sha256sum, get_name
from thread import ThreadWithReturnValue


def get_all_features(file):
    name = get_name(file)
    y, sr = librosa.load(file)

    # mfcc = librosa.feature.mfcc(y, sr, n_mfcc=20)
    # chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
    # chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    # mel = librosa.feature.melspectrogram(y=y, sr=sr)
    # tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    # rhythm = librosa.feature.tempogram(y=y, sr=sr)

    mfcc_thread = ThreadWithReturnValue(target=librosa.feature.mfcc, args=(y, sr,))
    mfcc_thread.start()
    chroma_cens_thread = ThreadWithReturnValue(target=librosa.feature.mfcc, args=(y, sr,))
    chroma_cens_thread.start()
    chroma_stft_thread = ThreadWithReturnValue(target=librosa.feature.mfcc, args=(y, sr,))
    chroma_stft_thread.start()
    mel_thread = ThreadWithReturnValue(target=librosa.feature.mfcc, args=(y, sr,))
    mel_thread.start()
    tonnetz_thread = ThreadWithReturnValue(target=librosa.feature.mfcc, args=(y, sr,))
    tonnetz_thread.start()
    rhythm_thread = ThreadWithReturnValue(target=librosa.feature.mfcc, args=(y, sr,))
    rhythm_thread.start()

    hash_val = sha256sum(file)

    mfcc = mfcc_thread.join()
    chroma_cens = chroma_cens_thread.join()
    chroma_stft = chroma_stft_thread.join()
    mel = mel_thread.join()
    tonnetz = tonnetz_thread.join()
    rhythm = rhythm_thread.join()

    # print(name, ' processed')

    return Feature(hash=hash_val, name=name, mfcc=mfcc, chroma_cens=chroma_cens, chroma_stft=chroma_stft, mel=mel,
                   tonnetz=tonnetz, rhythm=rhythm)


def get_distance(feature1, feature2):
    dist_func = euclidean

    distance1, path1 = fastdtw.fastdtw(feature1.mfcc.T, feature2.mfcc.T, dist=dist_func)
    distance2, path2 = fastdtw.fastdtw(feature1.chroma_cens.T, feature2.chroma_cens.T, dist=dist_func)
    distance3, path3 = fastdtw.fastdtw(feature1.chroma_stft.T, feature2.chroma_stft.T, dist=dist_func)
    distance4, path4 = fastdtw.fastdtw(feature1.mel.T, feature2.mel.T, dist=dist_func)
    distance5, path5 = fastdtw.fastdtw(feature1.tonnetz.T, feature2.tonnetz.T, dist=dist_func)
    distance6, path6 = fastdtw.fastdtw(feature1.rhythm.T, feature2.rhythm.T, dist=dist_func)

    # print(feature1.name + ' <==> ' + feature2.name)

    return Distance(hash1=feature1.hash, hash2=feature2.hash, name1=feature1.name, name2=feature2.name,
                    mfcc_dist=distance1, chroma_cens_dist=distance2, chroma_stft_dist=distance3,
                    mel_dist=distance4, tonnetz_dist=distance5, rhythm_dist=distance6)
