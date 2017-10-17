import re
from ipy_table import *
## we tokenise with types too.By the regex given below but I think its not required.
#tokeniserRegex =  re.compile('(?P<phoneNumber>(\+[0-9]{2}-?)?([0-9]{8,10}))|(?P<others>[\d]+|[+]|[\w+-]+|,+|\.+)')

tokeniserRegex = re.compile('[0-9]{2}\s*-\s*[0-9]{2}\s*-\s*[0-9]{4}|[0-9]{2}\s*/\s*[0-9]{2}\s*/\s*[0-9]{4}|([0-9]+(\.[0-9]+)?)\s*([a-zA-Z]+/[a-zA-Z]+)|[0-9]*(\.[0-9]+)|http(s?)\s*:\s*//\s*(\S*)|(\S*)\s*@\s*(\S*)\s*\.\s*(\S*)|(\+\s*[0-9]{2}\s*-\s*)?([0-9]{8,10})|[a-z]+\s*\'[sltdm]|[\d]+|[+]|[\w+-]+|\S')
class LanguageReader:
    unigram, bigram, trigram, corpusSize = {}, {}, {}, 0

    def insert(self,dict,key):
        if key not in dict:
            dict[key] = 0
        dict[key]+=1

    def __init__(self,filename):
        with open(filename,'r') as FileObj:
            for line in FileObj:
                prev_unigram,prev_bigram = "<start>",["null","<start>"]
                self.corpusSize += 1
                self.insert(self.unigram,"<start>")
                for token in [x.group() for x in tokeniserRegex.finditer(line)]:
                    self.corpusSize+=1
                    new_bigram = [prev_unigram, token]
                    new_trigram = [prev_bigram,token]
                    self.insert(self.unigram,token)
                    self.insert(self.bigram, new_bigram)
                    self.insert(self.trigram, new_trigram)
                    prev_unigram = token
                    prev_bigram = new_bigram
                self.corpusSize += 1
                new_bigram = [prev_unigram, "<end>"]
                new_trigram = [prev_bigram, "<end>"]
                self.insert(self.unigram, "<end>")
                self.insert(self.bigram, new_bigram)
                self.insert(self.trigram, new_trigram)
                self.unigram = sorted(self.unigram.items(), key=lambda x: x[1], reverse=True)
                self.bigram =  sorted(self.bigram.items() , key=lambda x: x[1], reverse=True)
                self.trigram = sorted(self.trigram.items(), key=lambda x: x[1], reverse=True)