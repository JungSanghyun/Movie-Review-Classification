# -*- coding: utf-8 -*-
import csv
import json
import pickle


def save_tsv(filename, dataset, mode='w', encoding='utf-8'):
    """
    Save dataset in tsv file.
    :param filename: Name of tsv file
    :param dataset: Dataset to save
    :param mode: File open mode ('w' for write, 'a' for append)
    :param encoding: Encoding (ex. 'utf-8')
    """
    with open(filename, mode, encoding=encoding) as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        for data in dataset:
            writer.writerow(data)
        f.close()


def load_tsv(filename, encoding='utf-8'):
    """
    Load tsv file and returns dataset as list.
    :param filename: Name of tsv file
    :param encoding: Encoding (ex. 'utf-8')
    :return: List of data
    """
    with open(filename, 'r', encoding=encoding) as f:
        dataset = []
        reader = csv.reader(f, delimiter='\t')
        for data in reader:
            dataset.append(data)
        f.close()
        return dataset


def save_json(filename, dataset, encoding='utf-8', indent=2, ensure_ascii=False):
    """
    Save dataset in json file.
    :param filename: Name of json file
    :param dataset: Dataset to save
    :param encoding: Encoding (ex. 'utf-8')
    :param indent: indentation of json file (recommend 2)
    :param ensure_ascii: ensure ASCII
    """
    with open(filename, 'w', encoding=encoding) as f:
        json.dump(dataset, f, indent=indent, ensure_ascii=ensure_ascii)
        f.close()


def load_json(filename, encoding='utf-8'):
    """
    Load json file and returns dataset as list.
    :param filename: Name of json file
    :param encoding: Encoding (ex. 'utf-8')
    :return: List of data
    """
    with open(filename, 'r', encoding=encoding) as f:
        dataset = json.load(f)
        f.close()
        return dataset


def save_pickle(filename, dataset):
    """
    Save dataset in pickle file.
    :param dataset: Dataset to save
    :param filename: Name of pickle file
    """
    with open(filename, 'wb') as f:
        pickle.dump(dataset, f)
        f.close()


def load_pickle(filename):
    """
    Load pickle file and returns dataset.
    :param filename: Name of pickle file
    :return: Dataset
    """
    with open(filename, 'rb') as f:
        dataset = pickle.load(f)
        f.close()
        return dataset
