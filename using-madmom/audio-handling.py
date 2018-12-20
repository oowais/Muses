import numpy as np
import madmom


def main():
    # load audio file method level
    signal, sample_rate = madmom.audio.signal.load_audio_file('../audio-resources/blues0.mp3')
    # lead audio file class level
    signal2 = madmom.audio.signal.Signal('../audio-resources/blues1.mp3')
    # load audio file using new methodology
    signal3 = madmom.io.audio.Signal('../audio-resources/blues2.mp3')

    # print("Signal: ")
    # print(signal)
    # print("Sample rate: ", sample_rate)
    #
    # print("Signal2: ")
    # print(signal2)
    # print("Sample rate2: ", signal2.sample_rate)

    # framing an audio signal
    fs = madmom.audio.signal.FramedSignal(signal=signal, frame_size=2048, hop_size=441)

    # Short Time Fourier Transform (Complex STFT)


if __name__ == '__main__':
    main()
