import madmom
import numpy as np
import matplotlib.pyplot as plt


audiofile = '../audio-resources/rock4.mp3'


class BetterSuperFluxProcessing(object):

    def __init__(self, num_bands=24, diff_max_bins=3, positive_diffs=True):
        self.num_bands = num_bands
        self.diff_max_bins = diff_max_bins
        self.positive_diffs = positive_diffs

    def process(self, data):
        spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram(data, num_bands=self.num_bands)
        diff = madmom.audio.spectrogram.SpectrogramDifference(spec, diff_max_bins=self.diff_max_bins,
                                                              positive_diffs=self.positive_diffs)
        return np.mean(diff, axis=1)


class SuperFluxProcessor(madmom.processors.SequentialProcessor):

    def __init__(self, num_bands=24, diff_max_bins=3, positive_diffs=True):
        # define the processing chain
        spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogramProcessor(num_bands=num_bands)
        diff = madmom.audio.spectrogram.SpectrogramDifferenceProcessor(diff_max_bins=diff_max_bins,
                                                                       positive_diffs=positive_diffs)
        from functools import partial
        mean = partial(np.mean, axis=1)
        # sequentially process everything
        super(SuperFluxProcessor, self).__init__([spec, diff, mean])


superflux_processor = SuperFluxProcessor()


def main():
    # SuperFlux onset detection function
    sig = madmom.audio.signal.Signal(audiofile, num_channels=1)
    fs = madmom.audio.signal.FramedSignal(sig)
    stft = madmom.audio.stft.ShortTimeFourierTransform(fs)
    spec = madmom.audio.spectrogram.Spectrogram(stft)
    filt = madmom.audio.spectrogram.FilteredSpectrogram(spec, num_bands=24)
    log = madmom.audio.spectrogram.LogarithmicSpectrogram(filt)
    diff = madmom.audio.spectrogram.SpectrogramDifference(log, diff_max_bins=3, positive_diffs=True)
    superflux_1 = np.mean(diff, axis=1)

    spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram(audiofile, num_bands=24,
                                                                   num_channels=1)
    diff = madmom.audio.spectrogram.SpectrogramDifference(spec, diff_max_bins=3, positive_diffs=True)
    superflux_2 = np.mean(diff, axis=1)

    # madmom.audio.signal.Signal('audiofile') yields the same result as
    # madmom.audio.signal.SignalProcessor().process('audiofile')
    spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogramProcessor(num_bands=24).process(
        audiofile, num_channels=1)
    diff = madmom.audio.spectrogram.SpectrogramDifferenceProcessor(diff_max_bins=3, positive_diffs=True).process(spec)
    superflux_3 = np.mean(diff, axis=1)

    spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogramProcessor(num_bands=24)
    diff = madmom.audio.spectrogram.SpectrogramDifferenceProcessor(diff_max_bins=3, positive_diffs=True)
    # functions can also be used as processors!
    from functools import partial
    mean = partial(np.mean, axis=1)

    superflux_seq_processor = madmom.processors.SequentialProcessor([spec, diff, mean])

    superflux_4 = superflux_seq_processor.process(audiofile, num_channels=1)
    superflux_5 = superflux_processor.process(audiofile, num_channels=1)

    plt.figure()
    plt.plot(superflux_1)
    plt.plot(superflux_2)
    plt.plot(superflux_3)
    plt.plot(superflux_4)
    plt.plot(superflux_5)


if __name__ == '__main__':
    main()
