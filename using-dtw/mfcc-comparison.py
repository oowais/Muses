import librosa
import matplotlib.pyplot as plt
from dtw import dtw
from scipy.spatial.distance import euclidean
import time
import fastdtw


mfcc1: any
mfcc2: any


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
    file1 = 'pop1.mp3'
    file2 = 'pop0.mp3'

    # Loading audio files
    y1, sr1 = librosa.load('../audio-resources/' + file1)
    y2, sr2 = librosa.load('../audio-resources/' + file2)
    print('Audio files loaded')

    # Calculating their mfcc feature
    mfcc1 = librosa.feature.mfcc(y1, sr1, n_mfcc=20)
    mfcc2 = librosa.feature.mfcc(y2, sr2, n_mfcc=20)
    print('Calculated MFCC features')

    # Getting frames from audio
    fs1 = librosa.util.frame(y1, frame_length=2048, hop_length=64)
    fs2 = librosa.util.frame(y2, frame_length=2048, hop_length=64)

    dist_func = euclidean

    print('Calculating distance..')
    time1 = time.time()
    dist, cost, accumulated_cost, path = dtw.dtw(mfcc1.T, mfcc2.T, dist_func)
    time2 = time.time()
    print("Normalized distance between " + file1 + " and " + file2 + " : ", dist)
    print('Time calculated to calculate: ', time2-time1)

    time1 = time.time()
    distance, path = fastdtw.dtw(mfcc1.T, mfcc2.T, dist_func)
    time2 = time.time()
    print("Normalized distance between " + file1 + " and " + file2 + " : ", distance)
    print('Time calculated to calculate: ', time2-time1)

    plt.figure(num='Comparison graph')
    plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
    plt.plot(path[0], path[1], 'w')  # creating plot for DTW

    plt.show()  # To display the plots graphically
