import matplotlib.pyplot as plt
import madmom


def main():
    # load audio file method level old way
    # signal, sample_rate = madmom.audio.signal.load_audio_file('../audio-resources/blues0.mp3')

    # lead audio file class level
    signal2 = madmom.audio.signal.Signal('../../audio_resources/blues1.mp3', num_channels=1)

    # load audio file using new methodology
    # signal3 = madmom.io.audio.Signal('../audio-resources/blues2.mp3')

    print("Signal2: ")
    print(signal2)
    print("Sample rate2: ", signal2.sample_rate)

    # framing an audio signal
    fs = madmom.audio.signal.FramedSignal(signal2, frame_size=2048, hop_size=441)
    # print(fs.frame_rate, fs.hop_size, fs)

    # Short Time Fourier Transform (Complex STFT)
    # Self-Note: for STFT, while loading audio in Signal class, provide num_channels=1
    stft = madmom.audio.stft.STFT(fs)
    # print(stft[0:2])

    # Magnitude Spectrogram
    spec = madmom.audio.spectrogram.Spectrogram(stft)
    # plot for jupyter
    plt.imshow(spec[:, :200].T, aspect='auto', origin='lower')
    # print(spec.shape, spec.bin_frequencies)
    # print(spec.stft.frames.overlap_factor)


if __name__ == '__main__':
    main()
