# -*- coding: utf-8 -*-
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from src.naive_bayes.classifier import NaiveBayesClassifier


if __name__ == '__main__':
    n = int(input('N-Gram(1~3): '))
    sentence = input('Input Comment: ')
    model = NaiveBayesClassifier(n)
    pos_prob, neg_prob = model.classify(sentence, verbose=True)
