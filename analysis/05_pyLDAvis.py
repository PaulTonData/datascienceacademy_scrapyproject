import pyLDAvis
import pyLDAvis.gensim
import warnings
import pickle
import time

from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

trigram_dict_file = 'trigram_dict.dict'
trigram_dictionary = Dictionary.load(trigram_dict_file)

trigram_threads_bow_file = 'trigram_threads_bow_corpus.mm'
trigram_users_bow_file = 'trigram_users_bow_corpus.mm'

trigram_threads_bow_corpus = MmCorpus(trigram_threads_bow_file)
trigram_users_bow_corpus = MmCorpus(trigram_users_bow_file)

lda_threads_model_file = "lda_threads_model"
lda_users_model_file = "lda_users_model"

lda_threads = LdaMulticore.load(lda_threads_model_file)
lda_users = LdaMulticore.load(lda_users_model_file)

LDAvis_threads_file = 'ldavis_threads_prep'
LDAvis_users_file = 'ldavis_users_prep'

t0 = time.time()
LDAvis_threads_prep = pyLDAvis.gensim.prepare(lda_threads, trigram_threads_bow_corpus, trigram_dictionary)

t1 = time.time()
print("Time to prep ldavis_threads: " + str(t1 - t0))
# 182 sec

with open(LDAvis_threads_file, 'wb') as f:
    pickle.dump(LDAvis_threads_prep, f)

t0 = time.time()
LDAvis_users_prep = pyLDAvis.gensim.prepare(lda_users, trigram_users_bow_corpus, trigram_dictionary)

t1 = time.time()
print("Time to prep ldavis_users: " + str(t1 - t0))
# 125.8 sec

with open(LDAvis_users_file, 'wb') as f:
    pickle.dump(LDAvis_users_prep, f)

