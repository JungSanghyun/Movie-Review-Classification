# -*- coding: utf-8 -*-
import os
import sys
from nltk import ngrams

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from util.file import load_tsv, load_pickle
from util.directory import *
from src.data_processing.preprocess import preprocess_sentence


class NaiveBayesClassifier(object):
    def __init__(self, n=1):
        """
        Initialize Naive Bayes Classifier Model.
        :param n: n-gram
        """
        self.n = n
        self.pos_word2idx = load_pickle(BOW_POS_IDX_TRAIN % (n, n))
        self.neg_word2idx = load_pickle(BOW_NEG_IDX_TRAIN % (n, n))
        self.pos_idx2cnt = load_pickle(BOW_POS_TRAIN % (n, n))
        self.neg_idx2cnt = load_pickle(BOW_NEG_TRAIN % (n, n))
        self.unique_words = load_pickle(UNIQUE_WORDS_TRAIN % (n, n))

    @staticmethod
    def _word_prop_with_laplace_smoothing(unique, word2idx, idx2cnt, word):
        """
        Laplace Smoothing for Naive Bayes Classifier.
        :param unique: unique words list
        :param word2idx: word2idx dictionary
        :param idx2cnt: idx2count list
        :param word: target word
        :return: P(word | class) of applying Laplace smoothing
        """
        if word in word2idx.keys():
            idx = word2idx[word]
            prob = (idx2cnt[idx] + 1) / (sum(idx2cnt) + len(unique))
        else:
            prob = 1 / (sum(idx2cnt) + len(unique))
        return prob

    def classify(self, sentence, verbose=False):
        """
        Implementation of Classification of Naive Bayes Classifier.
        :param sentence: input sentence
        :param verbose: Verbosity
        :return: positive probability, negative probability
        """
        pos_prob, neg_prob = 1.0, 1.0
        preprocessed_sentence = preprocess_sentence(sentence)[:50]
        n_gram_tokens = ngrams(preprocessed_sentence, self.n)

        if verbose:
            print('| Word-wise Probability |')

        for token in n_gram_tokens:
            word_pos_prob = self._word_prop_with_laplace_smoothing(self.unique_words, self.pos_word2idx,
                                                                   self.pos_idx2cnt, token)
            word_neg_prob = self._word_prop_with_laplace_smoothing(self.unique_words, self.neg_word2idx,
                                                                   self.neg_idx2cnt, token)

            if verbose:
                norm_word_pos_prob = word_pos_prob / (word_pos_prob + word_neg_prob)
                norm_word_neg_prob = word_neg_prob / (word_pos_prob + word_neg_prob)
                print(f' | {token} | Positive: {100 * norm_word_pos_prob:.1f}% | Negative: {100 * norm_word_neg_prob:.1f}% |')

            pos_prob *= word_pos_prob
            neg_prob *= word_neg_prob

        norm_pos_prob = pos_prob / (pos_prob + neg_prob)
        norm_neg_prob = neg_prob / (pos_prob + neg_prob)

        if verbose:
            if norm_pos_prob >= norm_neg_prob:
                print(f'| POSITIVE Comment in {100 * norm_pos_prob:.1f}% Probability |')
            else:
                print(f'| NEGATIVE Comment in {100 * norm_neg_prob:.1f}% Probability |')

        return norm_pos_prob, norm_neg_prob


if __name__ == '__main__':
    test_dataset = load_tsv(TEST_DATA, encoding='utf-8')
    for n in range(1, 4):
        total, correct = 0, 0
        model = NaiveBayesClassifier(n)

        for data in test_dataset:
            pos_prob, neg_prob = model.classify(data[1])
            if pos_prob >= neg_prob: result = 1
            else: result = 0

            if result == int(data[2]):
                correct += 1
            total += 1
        print(f'{n}-GRAM Test Dataset Accuracy: {100 * correct / total}% (Total: {total}, Correct: {correct})')
