import json
import re
import spacy
import pandas as pd
import itertools as it


f = open('clean_raw_posts.txt', 'r')
s = f.read()
f.close()

posts = json.loads(s)
df = pd.DataFrame(posts)

nlp = spacy.load('en')

texts = df['text']

# convert text from list to generator to pipe
text_gen = (x for x in texts)

unigram_file = 'raw_unigram_sentences.txt'

def punct_space(token):
    return token.is_punct or token.is_space

def lemmatized_sentence_corpus(post_gen):
    for parsed_post in nlp.pipe(post_gen, batch_size=10000, n_threads=4):
        for sent in parsed_post.sents:
            yield ' '.join([token.lemma_ for token in sent if not punct_space(token)])

with open(unigram_file, 'w', encoding='utf_8') as f:
    for sentence in lemmatized_sentence_corpus(text_gen):
        f.write(sentence + '\n')

from gensim.models import Phrases
from gensim.models.word2vec import LineSentence

unigram_sentences = LineSentence(unigram_file)

bigram_model_file = "raw_bigram_model"
bigram_file = "raw_bigram_sentences.txt"

bigram_model = Phrases(unigram_sentences)

bigram_model.save(bigram_model_file)

bigram_model = Phrases.load(bigram_model_file)

with open(bigram_file, 'w', encoding='utf_8') as f:
    for unigram_sentence in unigram_sentences:
        bigram_sentence = ' '.join(bigram_model[unigram_sentence])
        f.write(bigram_sentence + '\n')

bigram_sentences = LineSentence(bigram_file)

trigram_model_file = "raw_trigram_model"
trigram_file = "raw_trigram_sentences.txt"

trigram_model = Phrases(bigram_sentences)
trigram_model.save(trigram_model_file)

trigram_model = Phrases.load(trigram_model_file)

with open(trigram_file, 'w', encoding='utf_8') as f:
    for bigram_sentence in bigram_sentences:
        trigram_sentence = ' '.join(trigram_model[bigram_sentence])
        f.write(trigram_sentence + '\n')

trigram_sentences = LineSentence(trigram_file)

trigram_posts_file = "raw_trigram_posts.txt"

text_gen = (x for x in clean_texts)
with open(trigram_posts_file, 'w', encoding='utf_8') as f:
    for parsed_post in nlp.pipe(text_gen, batch_size=2000, n_threads=2):
        unigram_post = [token.lemma_ for token in parsed_post if not punct_space(token)]
        bigram_post = bigram_model[unigram_post]
        trigram_post = trigram_model[bigram_post]
        trigram_post = [term for term in trigram_post if term not in spacy.en.English.Defaults.stop_words]
        trigram_post = ' '.join(trigram_post)
        f.write(trigram_post + '\n')

