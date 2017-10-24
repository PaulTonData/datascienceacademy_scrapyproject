from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

from spacy.en.language_data import STOP_WORDS

import itertools as it
import warnings

trigram_posts_file = "raw_trigram_posts.txt"
trigram_dict_file = 'raw_trigram_dict.dict'

trigram_posts = LineSentence(trigram_posts_file)
trigram_dictionary = Dictionary(trigram_posts)
trigram_dictionary.filter_extremes(no_below=5, no_above=0.4)
trigram_dictionary.compactify()

trigram_dictionary.save(trigram_dict_file)

trigram_dictionary = Dictionary.load(trigram_dict_file)

trigram_bow_file = 'raw_trigram_bow_corpus.mm'

def trigram_bow_generator(filepath):
    """
    generator function to read reviews from a file
    and yield a bag-of-words representation
    """
    
    for post in LineSentence(filepath):
        yield trigram_dictionary.doc2bow(post)

MmCorpus.serialize(trigram_bow_file, trigram_bow_generator(trigram_posts_file))

trigram_bow_corpus = MmCorpus(trigram_bow_file)

lda_model_file = "raw_lda_model"

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    
    lda = LdaMulticore(trigram_bow_corpus, num_topics=50, id2word=trigram_dictionary, workers=4)
    
lda.save(lda_model_file)

lda = LdaMulticore.load(lda_model_file)

def explore_topic(topic_number, topn=5):
    """
    accept a user-supplied topic number and
    print out a formatted list of the top terms
    """
        
    print('{:20} {}'.format('term', 'frequency') + '\n')

    for term, frequency in lda.show_topic(topic_number, topn):
        print('{:20} {:.3f}'.format(term, round(frequency, 3)))
