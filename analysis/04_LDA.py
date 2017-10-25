from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

from spacy.en.language_data import STOP_WORDS

import itertools as it
import warnings
import time

trigram_posts_file = 'trigram_posts.txt'
trigram_dict_file = 'trigram_dict.dict'

trigram_posts = LineSentence(trigram_posts_file)
trigram_dictionary = Dictionary(trigram_posts)
trigram_dictionary.filter_extremes(no_below=10, no_above=0.4)
trigram_dictionary.compactify()

trigram_dictionary.save(trigram_dict_file)

trigram_dictionary = Dictionary.load(trigram_dict_file)

print(trigram_dictionary)
# 34,487 unique tokens



trigram_threads_bow_file = 'trigram_threads_bow_corpus.mm'
trigram_users_bow_file = 'trigram_users_bow_corpus.mm'

def trigram_bow_generator(filepath):
    """
    generator function to read reviews from a file
    and yield a bag-of-words representation
    """
    
    for post in LineSentence(filepath):
        yield trigram_dictionary.doc2bow(post)

trigram_threads_file = "trigram_threads.txt"
trigram_users_file = "trigram_users.txt"

t0 = time.time()
MmCorpus.serialize(trigram_threads_bow_file, trigram_bow_generator(trigram_threads_file))
t1 = time.time()
print("Time to generate BoW for threads: " + str(t1 - t0))
# 18.3 sec

t0 = time.time()
MmCorpus.serialize(trigram_users_bow_file, trigram_bow_generator(trigram_users_file))
t1 = time.time()
print("Time to generate BoW for users: " + str(t1 - t0))
# 18 sec

trigram_threads_bow_corpus = MmCorpus(trigram_threads_bow_file)
trigram_users_bow_corpus = MmCorpus(trigram_users_bow_file)

lda_threads_model_file = "lda_threads_model"
lda_users_model_file = "lda_users_model"

t0 = time.time()
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    lda_threads = LdaMulticore(trigram_threads_bow_corpus, num_topics=50, id2word=trigram_dictionary, workers=4)
    

t1 = time.time()
print("Time to generate lda_threads: " + str(t1 - t0))
# 226.8 sec

lda_threads.save(lda_threads_model_file)
lda_threads = LdaMulticore.load(lda_threads_model_file)

t0 = time.time()
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    lda_users = LdaMulticore(trigram_users_bow_corpus, num_topics=50, id2word=trigram_dictionary, workers=4)
    

t1 = time.time()
print("Time to generate lda_users: " + str(t1 - t0))
# 178.4 sec

lda_users.save(lda_users_model_file)
lda_users = LdaMulticore.load(lda_users_model_file)


def explore_topic(lda, topic_number, topn=5):
    """
    accept a user-supplied topic number and
    print out a formatted list of the top terms
    """        
    print('{:20} {}'.format('term', 'frequency') + '\n')
    for term, frequency in lda.show_topic(topic_number, topn):
        print('{:20} {:.3f}'.format(term, round(frequency, 3)))


