from HMM import HiddenMarkovModel
from nltk.corpus import brown
import numpy as np

TopElem = 100
Folds = 10
Tags =10
Obs = list(set(brown.words()))
Sentences = brown.sents()
alphabetReverseMap = {Obs[t]:t for t in xrange(len(Obs))}
number_obs = len(Obs)
number_sents = len(Sentences)
foldsize = number_sents/Folds
for fold in xrange(Folds):
    train = Sentences[0:foldsize*fold] + Sentences[foldsize*(fold+1):-1]
    train = [alphabetReverseMap[word] for sentence in train for word in sentence]
    #print train[:20]
    hmm = HiddenMarkovModel(Tags,len(train),number_obs)
    I = np.random.rand(Tags)
    A = np.random.rand(Tags,Tags)
    B = np.random.rand(Tags,number_obs)
    I/=I.sum()
    for i in xrange(Tags):
        A[i][:] /= A[i][:].sum()
        B[i][:] /= B[i][:].sum()
    #print A[1:3]
    #print B[1:3]
    #print I
    I,A,B = hmm.forward_backward(I,A,B,train)

    print "#Fold: ", fold
    for i in xrange(Tags):
        top = B[i].argsort()[-TopElem:][::-1]
        print
        print "#Tag", i+1, ":",
        for x in top:
            print Obs[x],
