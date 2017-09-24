class LaplaceSmoothing:
    def __init__(self,reader,vectorV):
        unigram,bigram,trigram = {},{},{}
        total_unigram,total_bigram,total_trigram = sum(reader.unigrams.value()),sum(reader.bigrams.value()),sum(reader.trigrams.value())
        self.unigram = {v:{item[0]:((item[1]+1) * total_unigram)/(float(total_unigram) + v) for item in reader.sorted_unigrams} for v in vectorV}
        self.bigram = {v: {item[0]: ((item[1] + 1) * total_bigram) / (float(total_bigram) + v) for item in reader.sorted_unigrams}for v in vectorV}
