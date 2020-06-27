# -*- coding: utf-8 -*-
import os
import sys
import random

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from util.file import save_tsv, load_tsv
from util.directory import *

random.seed(1)

DATA_SIZE = 100000
TRAIN_SIZE, TEST_SIZE = 150000, 50000


def shuffle(pos, neg):
    """
    Shuffle given positive reviews and negative reviews.
    :param pos: List of positive reviews
    :param neg: List of negative reviews
    :return: Shuffled list of pos + neg
    """
    total_data = pos + neg
    random.shuffle(total_data)
    return total_data


if __name__ == '__main__':
    pos_reviews = [[r[0], r[2], 1] for r in load_tsv(POS_RAW, encoding='utf-8')[:DATA_SIZE]]
    neg_reviews = [[r[0], r[2], 0] for r in load_tsv(NEG_RAW, encoding='utf-8')[:DATA_SIZE]]
    shuffled_data = shuffle(pos_reviews, neg_reviews)
    train_data, test_data = shuffled_data[:TRAIN_SIZE], shuffled_data[TRAIN_SIZE:]
    save_tsv(TRAIN_DATA, dataset=train_data, encoding='utf-8')
    save_tsv(TEST_DATA, dataset=test_data, encoding='utf-8')
