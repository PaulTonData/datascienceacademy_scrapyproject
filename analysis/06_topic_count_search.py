from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore

import pyLDAvis
import pyLDAvis.gensim

import itertools as it
import warnings
import time
import pickle

trigram_dict_file = 'trigram_dict.dict'
trigram_dictionary = Dictionary.load(trigram_dict_file)

trigram_threads_bow_file = 'trigram_threads_bow_corpus.mm'
trigram_users_bow_file = 'trigram_users_bow_corpus.mm'

trigram_threads_bow_corpus = MmCorpus(trigram_threads_bow_file)
trigram_users_bow_corpus = MmCorpus(trigram_users_bow_file)

lda_threads_model_file = "lda_threads_model"
lda_users_model_file = "lda_users_model"

for i in range(5, 50, 5):
    print("Starting to process with " + str(i) + " topics")
    t0 = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        lda_threads = LdaMulticore(trigram_threads_bow_corpus, num_topics=i, id2word=trigram_dictionary, workers=4)
    t1 = time.time()
    lda_threads.save("models/" + lda_threads_model_file + str(i))
    print("Time to generate lda_threads " + str(i) + " : " + str(t1 - t0))

'''
Starting to process with 5 topics
Time to generate lda_threads 5 : 53.75977849960327
Starting to process with 10 topics
Time to generate lda_threads 10 : 75.05263686180115
Starting to process with 15 topics
Time to generate lda_threads 15 : 99.37945866584778
Starting to process with 20 topics
Time to generate lda_threads 20 : 118.13127422332764
Starting to process with 25 topics
Time to generate lda_threads 25 : 138.435448884964
Starting to process with 30 topics
Time to generate lda_threads 30 : 166.0134561061859
Starting to process with 35 topics
Time to generate lda_threads 35 : 181.7455701828003
Starting to process with 40 topics
Time to generate lda_threads 40 : 202.01066303253174
Starting to process with 45 topics
Time to generate lda_threads 45 : 217.8033344745636
'''

for i in range(5, 50, 5):
    print("Starting to process with " + str(i) + " topics")
    t0 = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        lda_users = LdaMulticore(trigram_users_bow_corpus, num_topics=i, id2word=trigram_dictionary, workers=4)
    t1 = time.time()
    lda_users.save("models/" + lda_users_model_file + str(i))
    print("Time to generate lda_users " + str(i) + " : " + str(t1 - t0))

'''
Starting to process with 5 topics
Time to generate lda_users 5 : 65.08135390281677
Starting to process with 10 topics
Time to generate lda_users 10 : 89.98998785018921
Starting to process with 15 topics
Time to generate lda_users 15 : 103.45646500587463
Starting to process with 20 topics
Time to generate lda_users 20 : 115.90595817565918
Starting to process with 25 topics
Time to generate lda_users 25 : 132.31075239181519
Starting to process with 30 topics
Time to generate lda_users 30 : 140.43196153640747
Starting to process with 35 topics
Time to generate lda_users 35 : 147.64551663398743
Starting to process with 40 topics
Time to generate lda_users 40 : 159.57209134101868
Starting to process with 45 topics
Time to generate lda_users 45 : 163.54147338867188
'''

LDAvis_threads_file = 'ldavis_threads_prep'
LDAvis_users_file = 'ldavis_users_prep'

for i in range(5, 50, 5):
    print("Starting to process with " + str(i) + " topics")
    t0 = time.time()
    lda_threads = LdaMulticore.load("models/" + lda_threads_model_file + str(i))
    LDAvis_threads_prep = pyLDAvis.gensim.prepare(lda_threads, trigram_threads_bow_corpus, trigram_dictionary)
    t1 = time.time()
    with open("vis/" + LDAvis_threads_file + str(i), 'wb') as f:
        pickle.dump(LDAvis_threads_prep, f)
    print("Time to prep ldavis_threads " + str(i) + ": " + str(t1 - t0))


for i in range(5, 50, 5):
    print("Starting to process with " + str(i) + " topics")
    t0 = time.time()
    lda_users = LdaMulticore.load("models/" + lda_users_model_file + str(i))
    LDAvis_users_prep = pyLDAvis.gensim.prepare(lda_users, trigram_users_bow_corpus, trigram_dictionary)
    t1 = time.time()
    with open("vis/" + LDAvis_users_file + str(i), 'wb') as f:
        pickle.dump(LDAvis_users_prep, f)
    print("Time to prep ldavis_users " + str(i) + ": " + str(t1 - t0))



