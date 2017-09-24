import re
from ipy_table import *
## we tokenise with types too.By the regex given below but I think its not required.
#tokeniserRegex =  re.compile('(?P<phoneNumber>(\+[0-9]{2}-?)?([0-9]{8,10}))|(?P<others>[\d]+|[+]|[\w+-]+|,+|\.+)')

tokeniserRegex = re.compile('[0-9]{2}\s*-\s*[0-9]{2}\s*-\s*[0-9]{4}|[0-9]{2}\s*/\s*[0-9]{2}\s*/\s*[0-9]{4}|([0-9]+(\.[0-9]+)?)\s*([a-zA-Z]+/[a-zA-Z]+)|[0-9]*(\.[0-9]+)|http(s?)\s*:\s*//\s*(\S*)|(\S*)\s*@\s*(\S*)\s*\.\s*(\S*)|(\+\s*[0-9]{2}\s*-\s*)?([0-9]{8,10})|[a-z]+\s*\'[sltdm]|[\d]+|[+]|[\w+-]+|\S')
class LanguageReader:
    unigram, bigram, trigram, corpusSize = {}, {}, {}, 0

    def insert(self,dic,key):
        if key not in dic:
            dic[key] = 0
        dic[key]+=1

    def bucketify(self,tuple_list):
        dic,freq={},[]
        for x in tuple_list:
            if x[1] not in dic:
                dic[x[1]] = []
                freq.append(x[1])
            dic[x[1]].append(x[0])
        return dic,freq

    def __init__(self,filename):
        self.unigram, self.bigram, self.trigram, self.corpusSize = {}, {}, {}, 0
        with open(filename,'r') as FileObj:
            for line in FileObj:
                prev_unigram,prev_bigram = ["<start>"],["null","<start>"]
                self.corpusSize += 1
                self.insert(self.unigram,"<start>")
                for token in [x.group() for x in tokeniserRegex.finditer(line)]:
                    token = "".join(token.split())
                    #print token,
                    self.corpusSize+=1
                    prev_unigram.append(token)
                    prev_bigram.append(token)
                    self.insert(self.unigram,token)
                    #print new_trigram,new_bigram
                    self.insert(self.bigram, tuple(prev_unigram))
                    self.insert(self.trigram, tuple(prev_bigram))
                    prev_bigram = prev_unigram
                    prev_unigram = [token]
                #print
                self.corpusSize += 1
                prev_unigram.append("<end>")
                prev_bigram.append("<end>")
                self.insert(self.unigram, "<end>")
                self.insert(self.bigram, tuple(prev_unigram))
                self.insert(self.trigram, tuple(prev_bigram))
        self.sorted_unigram = sorted(self.unigram.items(), key=lambda x: x[1], reverse=True)
        self.sorted_bigram =  sorted(self.bigram.items() , key=lambda x: x[1], reverse=True)
        self.sorted_trigram = sorted(self.trigram.items(), key=lambda x: x[1], reverse=True)
        self.unigram_frequency_bucket,self.unigram_frequencies  = self.bucketify(self.sorted_unigram)
        self.bigram_frequency_bucket, self.bigram_frequencies  = self.bucketify(self.sorted_bigram)
        self.trigram_frequency_bucket,self.trigram_frequencies = self.bucketify(self.sorted_trigram)
        #print self.sorted_unigram
        #print self.sorted_bigram
        #print self.sorted_trigram