import librosa
import matplotlib.pyplot as plt
from dtw import dtw

if __name__ == '__main__':
    # Loading audio files
    file1 = 'blues0.mp3'
    file2 = 'rock1.mp3'

    y1, sr1 = librosa.load('../audio-resources/' + file1)
    y2, sr2 = librosa.load('../audio-resources/' + file2)

    mfcc1 = librosa.feature.mfcc(y1, sr1)
    mfcc2 = librosa.feature.mfcc(y2, sr2)

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

    # from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
    # from nltk.metrics.distance import edit_distance
    #
    # dist_fun = manhattan_distances
    #
    # dist, cost, path = dtw.dtw(mfcc1.T, mfcc2.T, dist_fun)
    # print("The normalized distance between the two : ", dist)  # 0 for similar audios
    #
    # plt.figure()
    # plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
    # plt.plot(path[0], path[1], 'w')  # creating plot for DTW
    #
    # plt.show()  # To display the plots graphically
