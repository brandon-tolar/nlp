
# coding: utf-8

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import *
from collections import Counter

##1a
##  encapsulates string split function
def words_in(s):
    return s.split()

##1b
##  returns concatenated string of the 2nd chars of each word in a list
def second_letter(words):
    letters = ""
    for w in words:
        letters += w[1]
    return letters

##1c
##  returns list of all words in a list before a given word
def phrases(s,word):
    words = words_in(s)
    return words[0:words.index(word)]

##1d
##  returns string representation of list with words seperated by spaces
def combine(words):
    return " ".join(words)

##1e
##  prints the words in alphabetical order without changing original list order
def print_alpha(words):
    sorted_words = words
    sorted_words.sort()
    for w in sorted_words:
        print(w)
        
##2
##  returns dict with words as keys and word counts as values
def word_counts(s):
    words = words_in(s)
    freqs = dict()
    for w in words:
        if w in freqs:
            freqs[w] += 1
        else:
            freqs[w] = 1
    return freqs

##5
##  remove all duplicate lines from a file
def remove_dups_file(filename):
    newcontent = []
    try: infile = open(filename)
    except:
        print("FILE ERROR")
        return
    for line in infile:
        if line.strip() not in newcontent:
            newcontent.append(line.strip())
    infile.close()
    try: outfile = open(filename, "w")
    except Exception as e:
        print(e)
        return
    for line in newcontent:
        outfile.write(line+"\n")
    outfile.close()

##  returns string without start/end whitespace, uppercase chars, non-speech words
def clean_string(old):
    clean_str = ""
    #remove whitespace at start/end
    #make lowercase
    #remove speaker labels and commentary
    old = old.strip().lower().replace(currentSpeaker+": ","").replace("(inaudable)","")
    for c in old:
        #remove punctuation
        if c not in ":.?!,/;'-$":
            clean_str += c
        
    return clean_str

##  return list of words without stop words
def remove_stopwords(words):
    result = list()
    for w in words:
        if w not in stopwords.words("english"):
            result.append(w)
    return result

##  return list of words stemmed using given stemmer
def stem_words(words, use):
    result = []
    stemmer = None
    if use == "porter":
        stemmer = nltk.PorterStemmer()
    elif use == "snowball":
        stemmer = nltk.SnowballStemmer('english')
    else:
        stemmer = nltk.LancasterStemmer()
    
    for w in words:
        result.append(stemmer.stem(w))
    return result

##BEGIN

##1
funny = "colorless green ideas sleep furiously"
print("1a: " + str(words_in(funny)))
print("1b: " + second_letter(words_in(funny)))
print("1c: " + str(phrases(funny)))
print("1d: " + combine(phrases(funny)))
print("1e:")
print_alpha(words_in(funny))

##2
print("\n2:")
freqs = word_counts(funny)
for i in freqs:
    print(i + " : " + str(freqs[i]))

##4
emails = "austen-emma.txt:hart@vmd.cso.uiuc.edu (internet)hart@uiucvmd (bitnet)austen-emma.txt:Internet (72600.2026@compuserve.com); TEL: (212-254-5093) austen-persuasion.txt:Editing by Martin Ward (Martin.Ward@uk.ac.durham)blake-songs.txt:Prepared by David Price, email ccx074@coventry.ac.uk"
print("\n4:")
print(re.findall("[A-Za-z0-9.]+@[A-Za-z]+\.[A-Za-z]+",emails))


##5
##for testing
#remove_dups_file("test.txt")


##7a
debateFile = open("debate.txt")
speakers = {"LEHRER" : "", "OBAMA" : "", "ROMNEY" : "","NONE" : ""}
currentSpeaker = "NONE"
for line in debateFile:
    if re.match("LEHRER", line):
        currentSpeaker = "LEHRER"
    elif re.match("OBAMA", line):
        currentSpeaker = "OBAMA"
    elif re.match("ROMNEY", line):
        currentSpeaker = "ROMNEY"
    if not re.match("\(", line):
        speakers[currentSpeaker] += clean_string(line) #7b
speakers.__delitem__("NONE") #ignore notes

speakers["OBAMA"] = remove_stopwords(speakers["OBAMA"].split())
speakers["ROMNEY"] = remove_stopwords(speakers["ROMNEY"].split())
speakers["LEHRER"] = remove_stopwords(speakers["LEHRER"].split())

porter = dict()
porter["OBAMA"] = stem_words(speakers["OBAMA"],"porter")
porter["ROMNEY"] = stem_words(speakers["ROMNEY"],"porter")
porter["LEHRER"] = stem_words(speakers["LEHRER"],"porter")
snowball = dict()
snowball["OBAMA"] = stem_words(speakers["OBAMA"],"snowball")
snowball["ROMNEY"] = stem_words(speakers["ROMNEY"],"snowball")
snowball["LEHRER"] = stem_words(speakers["LEHRER"],"snowball")
lancaster = dict()
lancaster["OBAMA"] = stem_words(speakers["OBAMA"],"lancaster")
lancaster["ROMNEY"] = stem_words(speakers["ROMNEY"],"lancaster")
lancaster["LEHRER"] = stem_words(speakers["LEHRER"],"lancaster")


##7c
print("\n7c:")
topPorter = {"OBAMA":Counter(porter["OBAMA"]), "ROMNEY":Counter(porter["ROMNEY"]), "LEHRER":Counter(porter["LEHRER"])}
print("    Porter:")
print("OBAMA: ",end=" ")
for p in topPorter["OBAMA"].most_common(10):
    print(p[0],end=" ")
print("")
print("ROMNEY: ",end=" ")
for p in topPorter["ROMNEY"].most_common(10):
    print(p[0],end=" ")
print("")
print("LEHRER: ",end=" ")
for p in topPorter["LEHRER"].most_common(10):
    print(p[0],end=" ")
print("")
    
topSnowball = {"OBAMA":Counter(snowball["OBAMA"]),"ROMNEY":Counter(snowball["ROMNEY"]),"LEHRER":Counter(snowball["LEHRER"])}
print("    Snowball:")
print("OBAMA: ",end=" ")
for p in topSnowball["OBAMA"].most_common(10):
    print(p[0],end=" ")
print("")
print("ROMNEY: ",end=" ")
for p in topSnowball["ROMNEY"].most_common(10):
    print(p[0],end=" ")
print("")
print("LEHRER: ",end=" ")
for p in topSnowball["LEHRER"].most_common(10):
    print(p[0],end=" ")
print("")

topLancaster = {"OBAMA":Counter(lancaster["OBAMA"]),"ROMNEY":Counter(lancaster["ROMNEY"]),"LEHRER":Counter(lancaster["LEHRER"])}
print("    Lancaster:")
print("OBAMA: ",end=" ")
for p in topLancaster["OBAMA"].most_common(10):
    print(p[0],end=" ")
print("")
print("ROMNEY: ",end=" ")
for p in topLancaster["ROMNEY"].most_common(10):
    print(p[0],end=" ")
print("")
print("LEHRER: ",end=" ")
for p in topLancaster["LEHRER"].most_common(10):
    print(p[0],end=" ")
print("")

##7d
def get_pos_words(filename):
    stemmer = nltk.PorterStemmer()
    posWords = set()
    try:
        infile = open(filename)
        for line in infile:
            posWords.add(stemmer.stem(line.strip()))
        infile.close()
    except Exception as e:
        print(e)
        return

    return posWords

##7d
print("\n7d:")
posWords = get_pos_words("positive.txt")

posSpeaker = dict()
posSpeaker["OBAMA"] = Counter()
posSpeaker["ROMNEY"] = Counter()
posSpeaker["LEHRER"] = Counter()
for w in porter["OBAMA"]:
    if w in posWords:
        posSpeaker["OBAMA"][w] += 1
for w in porter["ROMNEY"]:
    if w in posWords:
        posSpeaker["ROMNEY"][w] += 1
for w in porter["LEHRER"]:
    if w in posWords:
        posSpeaker["LEHRER"][w] += 1

print("OBAMA: ",end="")
for e in posSpeaker["OBAMA"].most_common(10):
    print(e[0],end=" ")
print("\nROMNEY: ",end="")
for e in posSpeaker["ROMNEY"].most_common(10):
    print(e[0],end=" ")
print("\nLEHRER: ",end=" ")
for e in posSpeaker["LEHRER"].most_common(10):
    print(e[0],end=" ")

