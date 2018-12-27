import logging
import librosa
import fastdtw
from scipy.spatial.distance import euclidean
from main.datastructure.feature import Feature
from main.datastructure.distance import Distance
from main.hash import sha256sum


class Extractor:
    def __init__(self):
        """Constructor"""
        self.logger = logging.getLogger(__name__)

    def get_all_features(self, file):
        file_list = file.split('/')
        name = file_list[len(file_list) - 1]

        self.logger.info('Calculating features of ' + file)
        print('Calculating features of ' + file)
        y, sr = librosa.load(file)

        # Calculating mfcc feature
        mfcc = librosa.feature.mfcc(y, sr, n_mfcc=20)

        # Calculating chroma_cens feature
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)

        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

        mel = librosa.feature.melspectrogram(y=y, sr=sr)

        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

        # Rhythm
        rhythm = librosa.feature.tempogram(y=y, sr=sr)

        hash = sha256sum(file)

        return Feature(hash=hash, name=name, mfcc=mfcc, chroma_cens=chroma_cens, chroma_stft=chroma_stft, mel=mel,
                       tonnetz=tonnetz, rhythm=rhythm)

    def get_distance(self, feature1, feature2):
        self.logger.info('Calculating distance between ' + feature1.name + ' and ' + feature2.name)
        print('Calculating distance between ' + feature1.name + ' and ' + feature2.name)
        dist_func = euclidean

        distance1, new_path = fastdtw.fastdtw(feature1.mfcc.T, feature2.mfcc.T, dist=dist_func)
        distance2, new_path2 = fastdtw.fastdtw(feature1.chroma_cens.T, feature2.chroma_cens.T, dist=dist_func)
        distance3, new_path3 = fastdtw.fastdtw(feature1.chroma_stft.T, feature2.chroma_stft.T, dist=dist_func)
        distance4, new_path4 = fastdtw.fastdtw(feature1.mel.T, feature2.mel.T, dist=dist_func)
        distance5, new_path5 = fastdtw.fastdtw(feature1.tonnetz.T, feature2.tonnetz.T, dist=dist_func)
        distance6, new_path6 = fastdtw.fastdtw(feature1.rhythm.T, feature2.rhythm.T, dist=dist_func)

        return Distance(hash1=feature1.hash, hash2=feature2.hash, mfcc_dist=distance1, chroma_cens_dist=distance2,
                        chroma_stf_dist=distance3, mel_dist=distance4, tonnetz_dist=distance5,
                        rhythm_dist=distance6)
