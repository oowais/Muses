class Feature:

    def __init__(self, name=None, hash=None, mfcc=None, cqt=None, chroma_stft=None, pcp=None, tonnetz=None,
                 rhythm=None):
        """Constructor for Song data class

        Parameters
        ----------
        name: name of audio
        hash: hash of audio
        mfcc: feautre
        cqt: feature
        chroma_stft: feature
        pcp: feature
        tonnetz: feature
        rhythm: feature

        """
        self._name = name
        self._hash = hash
        self._mfcc = mfcc
        self._cqt = cqt
        self._chroma_stft = chroma_stft
        self._pcp = pcp
        self._tonnetz = tonnetz
        self._rhythm = rhythm

    @property
    def name(self):
        return self._name

    @property
    def hash(self):
        return self._hash

    @property
    def mfcc(self):
        return self._mfcc

    @property
    def cqt(self):
        return self._cqt

    @property
    def chroma_stft(self):
        return self._chroma_stft

    @property
    def pcp(self):
        return self._pcp

    @property
    def tonnetz(self):
        return self._tonnetz

    @property
    def rhythm(self):
        return self._rhythm
