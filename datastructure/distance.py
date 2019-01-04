class Distance:

    def __init__(self, hash1=None, hash2=None, name1=None, name2=None, mfcc_dist=None, cqt_dist=None,
                 chroma_stft_dist=None, pcp_dist=None, tonnetz_dist=None, rhythm_dist=None):
        """Constructor for Song data class

        Parameters
        ----------
        hash1: hash of 1st audio
        hash2: hash of 2nd audio
        mfcc_dist: feautre
        cqt_dist: feature
        chroma_stft_dist: feature
        pcp_dist: feature
        tonnetz_dist: feature
        rhythm_dist: feature

        """
        self._hash1 = hash1
        self._hash2 = hash2
        self._name1 = name1
        self._name2 = name2
        self._mfcc_dist = mfcc_dist
        self._cqt_dist = cqt_dist
        self._chroma_stft_dist = chroma_stft_dist
        self._pcp_dist = pcp_dist
        self._tonnetz_dist = tonnetz_dist
        self._rhythm_dist = rhythm_dist

    @property
    def hash1(self):
        return self._hash1

    @property
    def hash2(self):
        return self._hash2

    @property
    def name1(self):
        return self._name1

    @property
    def name2(self):
        return self._name2

    @property
    def mfcc_dist(self):
        return self._mfcc_dist

    @property
    def cqt_dist(self):
        return self._cqt_dist

    @property
    def chroma_stft_dist(self):
        return self._chroma_stft_dist

    @property
    def pcp_dist(self):
        return self._pcp_dist

    @property
    def tonnetz_dist(self):
        return self._tonnetz_dist

    @property
    def rhythm_dist(self):
        return self._rhythm_dist
