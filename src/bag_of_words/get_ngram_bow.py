# -*- coding: utf-8 -*-
import os
import sys
from nltk import ngrams

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from util.file import load_json, save_pickle
from util.directory import *


def get_ngram_bow(dataset, n):
    """
    Get N-gram BOW from given dataset.
    :param dataset: Preprocessed review data
    :param n: n-gram
    :return: (positive BoW list, positive BoW index info, negative BoW list, negative BoW index info)
    """
    word2index_neg = {}
    word2index_pos = {}
    bow_neg = []
    bow_pos = []

    for data in dataset:
        n_grams_tokens = ngrams(data[0], n)
        label = int(data[1])
        # Negative bow
        if label == 0:
            for n_gram_token in n_grams_tokens:
                if n_gram_token not in word2index_neg.keys():
                    word2index_neg[n_gram_token] = len(word2index_neg)
                    bow_neg.insert(len(word2index_neg) - 1, 1)
                else:
                    idx = word2index_neg.get(n_gram_token)
                    bow_neg[idx] = bow_neg[idx] + 1

        # Positive bow
        elif label == 1:
            for n_gram_token in n_grams_tokens:
                if n_gram_token not in word2index_pos.keys():
                    word2index_pos[n_gram_token] = len(word2index_pos)
                    bow_pos.insert(len(word2index_pos) - 1, 1)
                else:
                    idx = word2index_pos.get(n_gram_token)
                    bow_pos[idx] = bow_pos[idx] + 1
    return bow_pos, word2index_pos, bow_neg, word2index_neg


if __name__ == '__main__':
    prep_train = load_json(PREP_TRAIN, encoding='utf-8')
    for n in range(1, 4):
        bow_pos_train, bow_pos_idx_train, bow_neg_train, bow_neg_idx_train = get_ngram_bow(prep_train, n)
        save_pickle(BOW_POS_TRAIN % (n, n), dataset=bow_pos_train)
        save_pickle(BOW_POS_IDX_TRAIN % (n, n), dataset=bow_pos_idx_train)
        save_pickle(BOW_NEG_TRAIN % (n, n), dataset=bow_neg_train)
        save_pickle(BOW_NEG_IDX_TRAIN % (n, n), dataset=bow_neg_idx_train)
