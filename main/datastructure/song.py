class Song:

    def __init__(self, name=None, hash=None, mfcc=None, chroma_cens=None, chroma_stft=None, mel=None, tonnetz=None,
                 rhythm=None):
        """Constructor for Song data class

        Parameters
        ----------
        name: name of audio
        hash: hash of audio
        mfcc: feautre
        chroma_cens: feature
        chroma_stf: feature
        mel: feature
        tonnetz: feature
        rhythm: feature

        """
        self._name = name
        self._hash = hash
        self._mfcc = mfcc
        self._chroma_cens = chroma_cens
        self._chroma_stft = chroma_stft
        self._mel = mel
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
    def chroma_cens(self):
        return self._chroma_cens

    @property
    def chroma_stft(self):
        return self._chroma_stft

    @property
    def mel(self):
        return self._mel

    @property
    def tonnetz(self):
        return self._tonnetz

    @property
    def rhythm(self):
        return self._rhythm
