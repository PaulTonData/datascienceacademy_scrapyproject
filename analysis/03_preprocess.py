import json
import re
import spacy
import pandas as pd
import itertools as it
from sklearn.model_selection import train_test_split
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
import time

f = open('clean_posts.txt', 'r')
s = f.read()
f.close()

posts = json.loads(s)
df = pd.DataFrame(posts)

train, test = train_test_split(df, test_size=0.2)
train.to_csv('train.txt', index=False)
test.to_csv('test.txt', index=False)

train = pd.read_csv('train.txt')
train = train.fillna('')
test = pd.read_csv('test.txt')
test = test.fillna('')

nlp = spacy.load('en')

texts = list(train['text'])

# convert text from list to generator to pipe
text_gen = (x for x in texts)

unigram_file = 'unigram_sentences.txt'

def punct_space(token):
    return token.is_punct or token.is_space

def lemmatized_sentence_corpus(post_gen):
    for parsed_post in nlp.pipe(post_gen, batch_size=10000, n_threads=4):
        for sent in parsed_post.sents:
            yield ' '.join([token.lemma_ for token in sent if not punct_space(token)])


t0 = time.time()
with open(unigram_file, 'w', encoding='utf_8') as f:
    for sentence in lemmatized_sentence_corpus(text_gen):
        f.write(sentence + '\n')

t1 = time.time()
print('Time to run: ' + str(t1 - t0))
# 745 sec

from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

unigram_sentences = LineSentence(unigram_file)

bigram_model_file = "bigram_model"
bigram_file = "bigram_sentences.txt"

bigram_model = Phrases(unigram_sentences)

bigram_model.save(bigram_model_file)

bigram_model = Phrases.load(bigram_model_file)

t0 = time.time()
with open(bigram_file, 'w', encoding='utf_8') as f:
    for unigram_sentence in unigram_sentences:
        bigram_sentence = ' '.join(bigram_model[unigram_sentence])
        f.write(bigram_sentence + '\n')

t1 = time.time()
print("Time to write bigram sentences: " + str(t1 - t0))
# 163 sec

bigram_sentences = LineSentence(bigram_file)

trigram_model_file = "trigram_model"
trigram_file = "trigram_sentences.txt"

trigram_model = Phrases(bigram_sentences)
trigram_model.save(trigram_model_file)

trigram_model = Phrases.load(trigram_model_file)

t0 = time.time()
with open(trigram_file, 'w', encoding='utf_8') as f:
    for bigram_sentence in bigram_sentences:
        trigram_sentence = ' '.join(trigram_model[bigram_sentence])
        f.write(trigram_sentence + '\n')

t1 = time.time()
print("Time to write trigram sentences: " + str(t1 - t0))
# 158.4 sec

trigram_sentences = LineSentence(trigram_file)

trigram_posts_file = "trigram_posts.txt"

text_gen = (x for x in texts)

t0 = time.time()
with open(trigram_posts_file, 'w', encoding='utf_8') as f:
    for parsed_post in nlp.pipe(text_gen, batch_size=5000, n_threads=4):
        unigram_post = [token.lemma_ for token in parsed_post if not punct_space(token)]
        bigram_post = bigram_model[unigram_post]
        trigram_post = trigram_model[bigram_post]
        trigram_post = [term for term in trigram_post if term not in spacy.en.English.Defaults.stop_words]
        trigram_post = ' '.join(trigram_post)
        f.write(trigram_post + '\n')

t1 = time.time()
print("Time to write trigram posts: " + str(t1 - t0))
# 989 sec

# threads as unit of observation -- group posts into threads
f = open(trigram_posts_file, 'r')
trigram_posts = f.readlines()
f.close()

# remove newline character from read
trigram_posts = [line[:-1] for line in trigram_posts]

train['text'] = trigram_posts

trigram_threads =  train.groupby('thread_id')['text'].apply(lambda x: ' '.join(x)).reset_index()
trigram_threads_file = "trigram_threads.txt"

f = open(trigram_threads_file, 'w')
for thread in trigram_threads['text']:
    f.write(thread + '\n')

f.close()


# users as unit of observation -- group posts by users

trigram_users = train.groupby('user_id')['text'].apply(lambda x: ' '.join(x)).reset_index()
trigram_users_file = "trigram_users.txt"

f = open(trigram_users_file, 'w')
for user in trigram_users['text']:
    f.write(user + '\n')

f.close()

