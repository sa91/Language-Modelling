from Tokeniser import LanguageReader
from Constants import constants
from plotly.offline import  iplot

def part1_function(corpus):
    reader = LanguageReader(constants[corpus])
    iplot([{"x": list(zip(*reader.unigram))[0], "y": list(zip(*reader.unigram))[1]}])
