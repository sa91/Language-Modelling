import Tokeniser
import datetime
from Constants import constants
from math import log
from plotly.offline import  init_notebook_mode, plot
from Smoothing import *
from NaiveBaiyesTokenisation import *
init_notebook_mode()

Reader = {}
def plotter(data,address):
   # data[0]['x'] = [xx.decode('utf-8', 'ignore') for xx in data[0]['x']]
    plot({'data': data,                                              # [{'y': y},{'x': x}],
               'layout': {'title': address,
                          'font': dict(family='Comic Sans MS', size=16)}},
             auto_open=False, image = 'png', image_filename='plot_image' ,
             output_type='file', image_width=800, image_height=600, filename="./plots/"+address+'.html', validate=False)

def plot_basic(corpus):
    reader = Reader[corpus]
    print corpus
    plotter([{'x': [ x.decode('utf-8', 'ignore') for x in list(zip(*reader.sorted_unigram))[0]], "y": list(zip(*reader.sorted_unigram))[1]}], corpus +"-unigram-word")
    plotter([{"x": ['_'.join(x).decode('utf-8', 'ignore') for x in list(zip(*reader.sorted_bigram))[0]],  "y": list(zip(*reader.sorted_bigram))[1]}] , corpus + "-bigram-word" )
    plotter([{"x": ['_'.join(x).decode('utf-8', 'ignore') for x in list(zip(*reader.sorted_trigram))[0]],  "y": list(zip(*reader.sorted_trigram))[1]}], corpus + "-trigram-word" )
    plotter([{"x": [i+1 for i in xrange(len(reader.unigram_frequencies))], "y": reader.unigram_frequencies}], corpus + "-unigram-zipf")
    plotter([{"x": [i+1 for i in xrange(len(reader.bigram_frequencies))],  "y": reader.bigram_frequencies}], corpus +"-bigram-zipf")
    plotter([{"x": [i+1 for i in xrange(len(reader.trigram_frequencies))], "y": reader.trigram_frequencies}], corpus + "-trigram-zipf")
    plotter([{"x": [log(i+1) for i in xrange(len(reader.unigram_frequencies))], "y": [log(yy) for yy in reader.unigram_frequencies]}], corpus +"-unigram-log")
    plotter([{"x": [log(i+1) for i in xrange(len(reader.bigram_frequencies))],  "y": [log(yy) for yy in reader.bigram_frequencies]}], corpus +"-bigram-log")
    plotter([{"x": [log(i+1) for i in xrange(len(reader.trigram_frequencies))], "y": [log(yy) for yy in reader.trigram_frequencies]}], corpus +"-trigram-log")

def plot_laplaceSmoothing(corpus):
    reader = Reader[corpus]
    v = [200,2000,len(reader.unigram),len(reader.unigram)*10]
    LaplaceSmoothing(reader,v)


def main():
    Reader['anime'] = Tokeniser.LanguageReader(constants['anime'])
    Reader['movies'] = Tokeniser.LanguageReader(constants['movies'])
    Reader['news'] = Tokeniser.LanguageReader(constants['news'])
    for corpus in Reader.keys():
        print corpus
        plot_basic(corpus)
    for corpus in Reader.keys():
        plot_laplaceSmoothing(corpus)




if __name__ == '__main__':
    main()
