# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from util.file import load_pickle, save_pickle
from util.directory import *


def make_unique_set(pos_idx, neg_idx):
    """
    Make unique word list from word2idx dictionary
    :param pos_idx: positive word2idx dictionary
    :param neg_idx: negative word2idx dictionary
    :return: unique words list
    """
    return list(set(list(pos_idx.keys()) + list(neg_idx.keys())))


if __name__ == '__main__':
    for n in range(1, 4):
        pos_idx2cnt_train = load_pickle(BOW_POS_TRAIN % (n, n))
        pos_word2idx_train = load_pickle(BOW_POS_IDX_TRAIN % (n, n))
        neg_idx2cnt_train = load_pickle(BOW_NEG_TRAIN % (n, n))
        neg_word2idx_train = load_pickle(BOW_NEG_IDX_TRAIN % (n, n))

        unique_words_train = make_unique_set(pos_word2idx_train, neg_word2idx_train)
        save_pickle(UNIQUE_WORDS_TRAIN % (n, n), unique_words_train)
