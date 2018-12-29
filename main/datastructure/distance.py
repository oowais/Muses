class Distance:

    def __init__(self, hash1=None, hash2=None, mfcc_dist=None, chroma_cens_dist=None, chroma_stft_dist=None,
                 mel_dist=None, tonnetz_dist=None, rhythm_dist=None):
        """Constructor for Song data class

        Parameters
        ----------
        hash1: hash of 1st audio
        hash2: hash of 2nd audio
        mfcc_dist: feautre
        chroma_cens_dist: feature
        chroma_stft_dist: feature
        mel_dist: feature
        tonnetz_dist: feature
        rhythm_dist: feature

        """
        self._hash1 = hash1
        self._hash2 = hash2
        self._mfcc_dist = mfcc_dist
        self._chroma_cens_dist = chroma_cens_dist
        self._chroma_stft_dist = chroma_stft_dist
        self._mel_dist = mel_dist
        self._tonnetz_dist = tonnetz_dist
        self._rhythm_dist = rhythm_dist

    @property
    def hash1(self):
        return self._hash1

    @property
    def hash2(self):
        return self._hash2

    @property
    def mfcc_dist(self):
        return self._mfcc_dist

    @property
    def chroma_cens_dist(self):
        return self._chroma_cens_dist

    @property
    def chroma_stft_dist(self):
        return self._chroma_stft_dist

    @property
    def mel_dist(self):
        return self._mel_dist

    @property
    def tonnetz_dist(self):
        return self._tonnetz_dist

    @property
    def rhythm_dist(self):
        return self._rhythm_dist
