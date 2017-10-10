import collections, nltk, math
class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 1) #+1 smoothing
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    for sentence in corpus.corpus:
      for datumPair in nltk.bigrams(sentence.data): 
        token = datumPair[0].word + datumPair[1].word
        self.bigramCounts[token] += 1
        self.total += 1
    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0 
    for bigram in nltk.bigrams(sentence):
      token = bigram[0] + bigram[1]
      count = self.bigramCounts[token]
      #smoothed
      score += math.log(count) - math.log(self.total)
    return score
