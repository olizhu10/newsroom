class ASData(object):
    """A class representing data for an article-summary analysis

    INSTANCE ATTRIBUTES:
        _match [bool]: whether or not the summary is a match for the article
        _data [str]: name of jsonl file with articles
        _coverage [float]: the coverage for the article-summary pair
        _density [float]: the density for the article-summary pair
        _compression [float]: the compression for the article-summary pair
        """

    def __init__(self, article, summary, match, coverage = None, density = None, compression = None):
        self._match = match
        self._article = article
        self._summary = summary
        if match == True:
            self._coverage = coverage
            self._density = density
            self._compression = compression

    def getMatch(self):
        return self._match

    def getCoverage(self):
        return self._coverage

    def getDensity(self):
        return self._density

    def getCompression(self):
        return self._compression

    def setMatch(self, match):
        self._match = match

    def setCoverage(self, coverage):
        self._coverage = coverage

    def setDensity(self, density):
        self._density = density

    def setCompression(self, compression):
        self._compression = compression

    def __repr__(self):
        if self._match == True:
            return "Coverage: "+str(self._coverage)+", Density: "+str(self._density)+", Compression: "+str(self._compression)+'\n'
        else:
            return "Not a match\n"
