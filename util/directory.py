# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 프로젝트 디렉토리
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)

# List of Directory

# For Raw Data
RAW_DIR = os.path.join(PROJECT_ROOT, 'data/raw_data/')
LOG_FILE = os.path.join(RAW_DIR, 'status_log.txt')
POS_RAW, NEG_RAW = os.path.join(RAW_DIR, 'pos_raw.tsv'), os.path.join(RAW_DIR, 'neg_raw.tsv')

# For Dataset
DATASET_DIR = os.path.join(PROJECT_ROOT, 'data/dataset/')
TRAIN_DATA, TEST_DATA = os.path.join(DATASET_DIR, 'train_data.tsv'), os.path.join(DATASET_DIR, 'test_data.tsv')

# For Preprocess
PREP_DIR = os.path.join(PROJECT_ROOT, 'data/preprocessed/')
PREP_TRAIN, PREP_TEST = os.path.join(PREP_DIR, 'prep_train.json'), os.path.join(PREP_DIR, 'prep_test.json')

# For Bag-Of-Words
BOW_DIR = os.path.join(PROJECT_ROOT, 'data/bag_of_words/%d-gram/')
BOW_POS_TRAIN = os.path.join(BOW_DIR, '%d-gram_bow_pos_train.pkl')
BOW_NEG_TRAIN = os.path.join(BOW_DIR, '%d-gram_bow_neg_train.pkl')
BOW_POS_IDX_TRAIN = os.path.join(BOW_DIR, '%d-gram_bow_pos_idx_train.pkl')
BOW_NEG_IDX_TRAIN = os.path.join(BOW_DIR, '%d-gram_bow_neg_idx_train.pkl')

# For Naive-Bayes
NAIVE_DIR = os.path.join(PROJECT_ROOT, 'data/naive_bayes/%d-gram/')
UNIQUE_WORDS_TRAIN = os.path.join(NAIVE_DIR, '%d-gram_unique_words_train.pkl')
