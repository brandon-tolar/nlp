
# coding: utf-8

import nltk
from nltk.corpus import udhr

TYPES = 676

def clean_str(orig):
    new = str()
    for e in orig:
        # remove punctuation and numbers
        if e not in [',','.','-',' '] and e not in ['0','1','2','3','4','5','6','7','8','9']:
            new += e
    return new

def clean_list(orig):
    new = list()
    for e in orig:
        # remove punctuation and numbers
        if e not in [',','.','-'] and e[0] not in ['0','1','2','3','4','5','6','7','8','9']:
            new.append(e)
    return new
            

english = clean_str(udhr.raw('English-Latin1').lower())
french = clean_str(udhr.raw("French_Francais-Latin1").lower())

english_train = english[0:1000]
french_train = french[0:1000]

english_test = clean_list(list(udhr.words('English-Latin1')[0:1000]))

## Build frequency distributions for each language and n value

en_uni_freqs = nltk.FreqDist(english_train)
fr_uni_freqs = nltk.FreqDist(french_train)

en_bigrams = list(nltk.bigrams(english_train))
fr_bigrams = list(nltk.bigrams(french_train))
en_bi_freqs = nltk.ConditionalFreqDist((c0,c1) for c0,c1 in en_bigrams)
fr_bi_freqs = nltk.ConditionalFreqDist((c0,c1) for c0,c1 in fr_bigrams)

en_trigrams = (((c0,c1),c2) for c0,c1,c2 in nltk.trigrams(english_train))
fr_trigrams = (((c0,c1),c2) for c0,c1,c2 in nltk.trigrams(french_train))
en_tri_freqs = nltk.ConditionalFreqDist(en_trigrams)
fr_tri_freqs = nltk.ConditionalFreqDist(fr_trigrams)

## Given a word and a probability distribution, return the probability that
## the word will occur

def uni_word_prob(word, lang):
    dist = None
    grams = None
    word = word.lower()
    
    if lang == "en":
        dist = en_uni_freqs
        grams = english_train
    elif lang == "fr":
        dist = fr_uni_freqs
        grams = french_train

    # calculate prob
    result = 1.0
    for c in word:
      freq = dist.freq(c)
      if freq > 0.0:
        result *= freq
      else:
        result *= TYPES/(TYPES+len(grams)) # Witten-Bell smoothing
    
    return result

def bi_word_prob(word, lang):
    dist = None
    grams = None
    word = word.lower()
    if lang == "en":
        dist = en_bi_freqs
        grams = en_bigrams
    elif lang == "fr":
        dist = fr_bi_freqs
        grams = fr_bigrams

    # calculate prob
    result = 1.0
    default = TYPES**2/(TYPES**2+len(grams))
    for c in range(len(word)-1):
        gram = tuple(word[c:c+2])
        freq = default
        
        freq = dist[gram[0]].freq(gram[1])
        if freq == 0.0:
            freq = default

        result *= freq
    return result

def tri_word_prob(word, lang):
    dist = None
    grams = None
    word = word.lower()
    
    if lang == "en":
        dist = en_tri_freqs
        grams = en_trigrams
    elif lang == "fr":
        dist = fr_tri_freqs
        grams = fr_trigrams

    # calculate prob
    result = 1.0
    default = TYPES**3/(TYPES**3+len(str(grams))) # Witten-Bell smoothing
    for c in range(len(word)-2):
        gram = tuple(word[c:c+3])
        freq = default
        if type(dist[gram[1]]) != int:
            freq = dist[gram[1:3]].freq(gram[0])
        
        result *= freq
    return result


##predicts whether a word is english or french based on unigram model

def predict_lang_uni(word):
    if uni_word_prob(word,"en") > uni_word_prob(word,"fr"):
        return "en"
    else:
        return "fr"

def predict_lang_bi(word):
    if bi_word_prob(word,"en") > bi_word_prob(word,"fr"):
        return "en"
    else:
        return "fr"
    
def predict_lang_tri(word):
    if tri_word_prob(word,"en") > tri_word_prob(word,"fr"):
        return "en"
    else:
        return "fr"


## Get accuracies of each model predicting english

uni_correct = 0
bi_correct = 0
tri_correct = 0

for word in english_test:
    if predict_lang_uni(word) == "en":
        uni_correct += 1
    if predict_lang_bi(word) == "en":
        bi_correct += 1
    if predict_lang_tri(word) == "en":
        tri_correct += 1

## Make word list length a float for float math
en_test_len = float(len(english_test))

print("Uni-model accuracy:",uni_correct,"/",int(en_test_len),"=",uni_correct/en_test_len)
print("Bi-model accuracy:",bi_correct,"/",int(en_test_len),"=",bi_correct/en_test_len)
print("Tri-model accuracy:",tri_correct,"/",int(en_test_len),"=",tri_correct/en_test_len)

