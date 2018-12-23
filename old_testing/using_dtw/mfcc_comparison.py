import librosa
import matplotlib.pyplot as plt
from dtw import dtw
from scipy.spatial.distance import euclidean
import time
import fastdtw


def plot_graphs():
    # Showing multiple plots in same figure using subplot
    plt.subplot(1, 2, 1)
    plt.title('MFCC of ' + file1)
    plt.imshow(mfcc1, aspect='auto', origin='lower')
    plt.subplot(1, 2, 2)
    plt.title('MFCC of ' + file2)
    plt.imshow(mfcc2, aspect='auto', origin='lower')

    # Showing plots in separate figures
    plt.figure(num='MFCC of ' + file1)
    plt.title('MFCC of ' + file1)
    plt.imshow(mfcc1, aspect='auto', origin='lower')
    plt.figure(num='MFCC of ' + file2)
    plt.title('MFCC of ' + file2)
    plt.imshow(mfcc2, aspect='auto', origin='lower')


if __name__ == '__main__':
    file1 = 'metal2.mp3'
    file2 = 'metal0.mp3'

    # Loading audio files
    y1, sr1 = librosa.load('../../audio_resources/' + file1)
    y2, sr2 = librosa.load('../../audio_resources/' + file2)
    print('Audio files loaded', file1, " ", file2)

    # Calculating mfcc feature
    mfcc1 = librosa.feature.mfcc(y1, sr1, n_mfcc=20)
    mfcc2 = librosa.feature.mfcc(y2, sr2, n_mfcc=20)

    # Calculating chroma_cens feature
    chroma_cens1 = librosa.feature.chroma_cens(y=y1, sr=sr1)
    chroma_cens2 = librosa.feature.chroma_cens(y=y2, sr=sr2)

    chroma_stft1 = librosa.feature.chroma_stft(y=y1, sr=sr1)
    chroma_stft2 = librosa.feature.chroma_stft(y=y2, sr=sr2)

    mel1 = librosa.feature.melspectrogram(y=y1, sr=sr1)
    mel2 = librosa.feature.melspectrogram(y=y2, sr=sr2)

    tonnetz1 = librosa.feature.tonnetz(y=y1, sr=sr1)
    tonnetz2 = librosa.feature.tonnetz(y=y2, sr=sr2)

    # Rhythm
    tempogram1 = librosa.feature.tempogram(y=y1, sr=sr1)
    tempogram2 = librosa.feature.tempogram(y=y2, sr=sr2)

    # Getting frames from audio
    fs1 = librosa.util.frame(y1, frame_length=2048, hop_length=64)
    fs2 = librosa.util.frame(y2, frame_length=2048, hop_length=64)

    dist_func = euclidean

    # print('Calculating distance..')
    # time1 = time.time()
    # dist, cost, accumulated_cost, path = dtw(mfcc1.T, mfcc2.T, dist_func)
    # dist, cost, accumulated_cost, path = dtw(chroma_cens1.T, chroma_cens2.T, dist_func)
    # time2 = time.time()
    # print("Normalized distance between " + file1 + " and " + file2 + ": ", dist)
    # print('Time calculated to calculate: ', time2-time1)

    time1 = time.time()
    distance, new_path = fastdtw.fastdtw(mfcc1.T, mfcc2.T, dist=dist_func)
    distance2, new_path2 = fastdtw.fastdtw(chroma_cens1.T, chroma_cens2.T, dist=dist_func)
    distance3, new_path3 = fastdtw.fastdtw(chroma_stft1.T, chroma_stft2.T, dist=dist_func)
    distance4, new_path4 = fastdtw.fastdtw(mel1.T, mel2.T, dist=dist_func)
    distance5, new_path5 = fastdtw.fastdtw(tonnetz1.T, tonnetz2.T, dist=dist_func)
    distance6, new_path6 = fastdtw.fastdtw(tempogram1.T, tempogram2.T, dist=dist_func)

    time2 = time.time()
    print('mfcc distance: ', distance)
    print('chroma_cens distance: ', distance2)
    print('chroma_stft distance: ', distance3)
    print('mel distance: ', distance4)
    print('tonnetz distance: ', distance5)
    print('rhythm tempogram distance: ', distance6)
    print('Time calculated to calculate: %.2f' % (time2 - time1))

    # plt.figure(num='Comparison graph')
    # plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
    # plt.plot(path[0], path[1], 'w')  # creating plot for DTW
    #
    # plt.show()  # To display the plots graphically
