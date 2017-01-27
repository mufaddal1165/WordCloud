from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import sys
import os
import numpy as np
from time import time
import refinery
from refinery import get_clean_tweets
# import pyLDAvis
# import pyLDAvis.sklearn
import importlib
import json
from watson import get_entities_keywords

def read_doc(doc_name):
    return open(doc_name, mode='r').read();

def makeCorpus(path = "docs"):
    corpus = []
    for filenames in os.listdir(path):
        corpus.append(read_doc(os.path.join(path,filenames)))
    return corpus

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % (topic_idx+1))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
def get_no_of_topics():
    if len(sys.argv) > 1:
        try:
            no_of_topics = int(sys.argv[1])
            return no_of_topics
        except Exception as e:
            print(e)

    else:
        return 20

def get_top_words():
    if len(sys.argv) > 2:
        try:
            no_of_words = int(sys.argv[2])
            return no_of_words
        except Exception as e:
            print(e)
    else:
        return 20

def get_max_features():
    if len(sys.argv) > 3:
        try:
            no_of_features = int(sys.argv[3])
            return no_of_features
        except Exception as e:
            print(e)
    else:
        return 1000

def tfidf_vector_features(corpus):
    tfidf_vectorizer = TfidfVectorizer(  stop_words="english", max_df=0.95, min_df=5,max_features=get_max_features())
    tfidf = tfidf_vectorizer.fit_transform(corpus, y=None)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    return (tfidf,tfidf_feature_names,tfidf_vectorizer)

def tf_vector_features(corpus):
    tf_vectorizer = CountVectorizer(stop_words='english',max_df=0.95,min_df=5,max_features=get_max_features())
    tf = tf_vectorizer.fit_transform(corpus)
    tf_feature_names = tf_vectorizer.get_feature_names()
    return (tf,tf_feature_names)


def main():
    t0 = time()
    corpus = get_clean_tweets(r'C:\Users\Mufaddal\Desktop\FYP\Word Cloud\data\trump_up.jsonl')
    with open('../watson_results/results.json', mode='w') as fp:
        json.dump(get_entities_keywords(corpus), fp,indent=2)
    fp.close()
    print("Time taken to read corpus %0.3f" %(time()- t0))
    t0 = time()
    tf,tf_feature_names = tf_vector_features(corpus)
    tfidf,tfidf_feature_names,tfidf_vectorizer = tfidf_vector_features(corpus)

    print("Time taken to vectorize %0.3f" %(time()- t0))
    t0 = time()
    lda = LatentDirichletAllocation(n_topics=get_no_of_topics(), doc_topic_prior=None, topic_word_prior=None, learning_method='online', learning_decay=.7, learning_offset=10., max_iter=10, batch_size=128, evaluate_every=-1, total_samples=1e6, perp_tol=1e-1, mean_change_tol=1e-3, max_doc_update_iter=100, n_jobs=1, verbose=0, random_state=1)

    lda.fit(tf, y=None)
    print("Time taken for LDA %0.3f" %(time()- t0))
    # pyLDAvis.sklearn.prepare(lda, tfidf, tfidf_vectorizer)
    # print_top_words(lda, feature_names=tf_feature_names, n_top_words=get_top_words())
    with open('../watson_results/results.json', mode='r') as fp:
        obj = json.load(fp)
    fp.close()
    entities = obj['entities']
    for entity in entities:
        if entity['count'] > 5:
            print(entity['text'])
            
if __name__ == '__main__':
    #format python main.py no_topics no_of_topwords no_of_features
    main()
