import madmom
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter


# Comparison of SuperFlux function to normal spectral flux for beat detection
def main():
    spec = madmom.audio.spectrogram.Spectrogram('../../audio_resources/rock4.mp3', num_channels=1)

    # calculate the difference
    diff = np.diff(spec, axis=0)
    # keep only the positive differences
    pos_diff = np.maximum(0, diff)
    # sum everything to get the spectral flux
    sf = np.sum(pos_diff, axis=1)

    # for jupyter
    plt.figure()
    plt.imshow(spec[:, :200].T, origin='lower', aspect='auto')
    plt.figure()
    plt.imshow(pos_diff[:, :200].T, origin='lower', aspect='auto')
    plt.figure()
    plt.plot(sf)

    # Spectral flux
    sf = madmom.features.onsets.spectral_flux(spec)

    filt_spec = madmom.audio.spectrogram.FilteredSpectrogram(spec, filterbank=madmom.audio.filters.LogFilterbank,
                                                             num_bands=24)
    plt.imshow(filt_spec.T, origin='lower', aspect='auto')

    log_spec = madmom.audio.spectrogram.LogarithmicSpectrogram(filt_spec, add=1)
    plt.imshow(log_spec.T, origin='lower', aspect='auto')

    # maximum filter size spreads over 3 frequency bins
    size = (1, 3)
    max_spec = maximum_filter(log_spec, size=size)
    plt.imshow(max_spec.T, origin='lower', aspect='auto')

    # init the diff array
    diff = np.zeros_like(log_spec)
    # calculate the difference between the log. spec and the max. filtered version thereof
    diff[1:] = (log_spec[1:] - max_spec[: -1])
    # then continue as with the spectral flux, i.e. keep only the positive differences
    pos_diff = np.maximum(0, diff)

    plt.figure()
    plt.imshow(pos_diff.T, origin='lower', aspect='auto')

    # sum everything to get the onset detection function
    superflux = np.sum(pos_diff, axis=1)

    plt.figure()
    plt.plot(superflux)

    log_filt_spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram('../audio-resources/rock4.mp3',
                                                                            num_bands=24, num_channels=1)
    # this is the same as before:
    superflux_diff = madmom.audio.spectrogram.SpectrogramDifference(log_filt_spec, positive_diffs=True, diff_max_bins=3)
    superflux_2 = np.sum(superflux_diff, axis=1)

    superflux_3 = madmom.features.onsets.superflux(log_filt_spec)

    # we scale them to have the same range
    plt.figure()
    plt.plot(sf / sf.max(), 'b')  # blue
    plt.plot(superflux / superflux.max(), 'g')  # green
    plt.plot(superflux_2 / superflux_2.max(), 'r--')  # dashed red
    plt.plot(superflux_3 / superflux_3.max(), 'k:')  # dotted black


if __name__ == '__main__':
    main()
