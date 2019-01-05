import librosa
import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np

from datastructure.feature import Feature
from datastructure.distance import Distance
from main.util import sha256sum, get_name
from main.thread import ThreadWithReturnValue


def _calculate_mfcc(y, sr):
    s = librosa.feature.melspectrogram(y=y, sr=sr)
    log_s = librosa.amplitude_to_db(s)
    return librosa.feature.mfcc(S=log_s)


def _calculate_cqt(y, sr):
    linear_cqt = np.abs(librosa.cqt(y=y, sr=sr)) ** 2
    return librosa.amplitude_to_db(linear_cqt)


def _calculate_pcp(y, sr):
    pcp_cqt = np.abs(librosa.hybrid_cqt(y=y, sr=sr)) ** 2
    return librosa.feature.chroma_cqt(C=pcp_cqt, sr=sr)


def get_all_features(file):
    name = get_name(file)
    y, sr = librosa.load(file)

    mfcc_thread = ThreadWithReturnValue(target=_calculate_mfcc, args=(y, sr,))
    mfcc_thread.start()
    cqt_thread = ThreadWithReturnValue(target=_calculate_cqt, args=(y, sr,))
    cqt_thread.start()
    chroma_stft_thread = ThreadWithReturnValue(target=librosa.feature.chroma_stft, args=(y, sr,))
    chroma_stft_thread.start()
    pcp_thread = ThreadWithReturnValue(target=_calculate_pcp, args=(y, sr,))
    pcp_thread.start()
    tonnetz_thread = ThreadWithReturnValue(target=librosa.feature.tonnetz, args=(y, sr,))
    tonnetz_thread.start()
    rhythm_thread = ThreadWithReturnValue(target=librosa.feature.tempogram, args=(y, sr,))
    rhythm_thread.start()

    hash_val = sha256sum(file)

    mfcc = mfcc_thread.join()
    cqt = cqt_thread.join()
    chroma_stft = chroma_stft_thread.join()
    pcp = pcp_thread.join()
    tonnetz = tonnetz_thread.join()
    rhythm = rhythm_thread.join()

    # print(name, ' processed')

    return Feature(hash=hash_val, name=name, mfcc=mfcc, cqt=cqt, chroma_stft=chroma_stft, pcp=pcp,
                   tonnetz=tonnetz, rhythm=rhythm)


def get_distance(feature1, feature2):
    dist_func = euclidean

    distance1, path1 = fastdtw.fastdtw(feature1.mfcc.T, feature2.mfcc.T, dist=dist_func)
    distance2, path2 = fastdtw.fastdtw(feature1.cqt.T, feature2.cqt.T, dist=dist_func)
    distance3, path3 = fastdtw.fastdtw(feature1.chroma_stft.T, feature2.chroma_stft.T, dist=dist_func)
    distance4, path4 = fastdtw.fastdtw(feature1.pcp.T, feature2.pcp.T, dist=dist_func)
    distance5, path5 = fastdtw.fastdtw(feature1.tonnetz.T, feature2.tonnetz.T, dist=dist_func)
    distance6, path6 = fastdtw.fastdtw(feature1.rhythm.T, feature2.rhythm.T, dist=dist_func)

    # print(feature1.name + ' <==> ' + feature2.name)

    return Distance(hash1=feature1.hash, hash2=feature2.hash, name1=feature1.name, name2=feature2.name,
                    mfcc_dist=distance1, cqt_dist=distance2, chroma_stft_dist=distance3,
                    pcp_dist=distance4, tonnetz_dist=distance5, rhythm_dist=distance6)
