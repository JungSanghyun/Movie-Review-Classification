# -*- coding: utf-8 -*-
import os
import sys
import re
from konlpy.tag import Okt

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from util.file import load_tsv, save_json
from util.directory import *

STOP_WORD = ['은', '는', '이', '가', '도', '을', '를', '의', '과', '하다', '너무', '그냥', '더']
STOP_POS = ['Josa', 'Suffix', 'Modifier', 'VerbPrefix', 'Exclamation']

tagger = Okt()


def preprocess_sentence(sentence):
    """
    Preprocess given sentence.
    :param sentence: Input setence
    :return: Preprocessed sentence
    """
    refined = []
    removed = re.sub('[^가-힣]', ' ', sentence)  # Remove all the non-Korean characters
    tagged = tagger.pos(removed, stem=True)  # Tokenize and tag Part-of-Speech
    for word in tagged:
        if word[0] not in STOP_WORD and word[1] not in STOP_POS:
            refined.append(f'{word[0]}/{word[1]}')
    return refined


def preprocess_dataset(dataset):
    """
    Preprocess given dataset.
    :param dataset: List of review data
    :return: Preprocessed dataset
    """
    preprocessed = []
    for data in dataset:
        refined = preprocess_sentence(data[1])
        if refined:
            preprocessed.append([refined, data[2]])
    return preprocessed


if __name__ == '__main__':
    train_dataset = load_tsv(TRAIN_DATA, encoding='utf-8')
    test_dataset = load_tsv(TEST_DATA, encoding='utf-8')

    prep_train = preprocess_dataset(train_dataset)
    prep_test = preprocess_dataset(test_dataset)

    save_json(PREP_TRAIN, dataset=prep_train)
    save_json(PREP_TEST, dataset=prep_test)
