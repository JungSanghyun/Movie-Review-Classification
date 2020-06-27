# -*- coding: utf-8 -*-
import os
import sys
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)
from util.file import save_tsv, load_tsv
from util.directory import *

MAX_MOVIE_CODE = 187321  # Maximum movie code
MAX_DATA = 100000  # Target number of each data

# URL can be changeable (based on 2020-04-29)
BASE_URL = 'https://movie.naver.com/movie/point/af/list.nhn'
MOVIE_URL = BASE_URL + '?st=mcode&sword=%d&target=after&page=%d'


def get_encoded_bs(url):
    """
    Get Encoded BeautifulSoup instance from URL.
    :param url: URL
    :return: Encoded BeautifulSoup instance
    """
    res = requests.get(url)
    http_encoding = res.encoding if 'charset' in res.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(res.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(res.content, 'lxml', from_encoding=encoding)
    return soup


def get_reviews_from_movie(movie_code, get_pos=True, get_neg=True):
    """
    Get Movie Reviews By Movie Code.
    :param movie_code: Movie code
    :param get_pos: Crawls positive reviews if True
    :param get_neg: Crawls negative reviews if True
    :return: positive reviews, negative reviews, title of movie
    """
    pos, neg, title = [], [], ''
    page_num = 50  # max access page num for each movie
    soup = get_encoded_bs(MOVIE_URL % (movie_code, page_num))

    review_tag = soup.find('table', 'list_netizen')
    page_num = soup.find('span', 'on')
    page_num = 0 if not review_tag or not page_num else int(page_num.get_text())  # max page for current movie (<= 50)

    while page_num > 0:
        soup = get_encoded_bs(MOVIE_URL % (movie_code, page_num))
        review_tag = soup.find('table', 'list_netizen')
        review_tag_list = review_tag.find('tbody').find_all('tr')

        for review in review_tag_list:
            number = review.find('td', 'ac num').get_text()
            title = review.find('td', 'title').find('a').get_text()
            comment = review.find('br').next_sibling
            comment = comment.strip() if comment is not None else comment
            score = int(review.find('div', 'list_netizen_score').find('em').get_text())
            if comment:
                if score > 8 and get_pos:
                    pos.append([number, title, comment, score])
                elif score < 5 and get_neg:
                    neg.append([number, title, comment, score])
        page_num -= 1
    return pos, neg, title


def write_log(movie_code, title, pos_num, neg_num):
    """
    Write Crawling Log.
    :param movie_code: Movie code
    :param title: title of movie
    :param pos_num: number of positive reviews
    :param neg_num: number of negative reviews
    """
    dataset = [[movie_code, title, pos_num, neg_num]]
    save_tsv(LOG_FILE, dataset, mode='a', encoding='utf-8')


def read_log():
    """
    Read Crawling Log.
    :return: Last movie code, title of movie, number of positives, number of negatives
    """
    try:
        logs = load_tsv(LOG_FILE, encoding='utf-8')
        last_log = logs[-1]
        return int(last_log[0]), last_log[1], int(last_log[2]), int(last_log[3])
    except FileNotFoundError as _:
        return MAX_MOVIE_CODE, '', 0, 0


if __name__ == '__main__':
    total_pos, total_neg = [], []
    movie_code, title, pos_num, neg_num = read_log()

    while pos_num < MAX_DATA or neg_num < MAX_DATA:
        pos, neg, title = get_reviews_from_movie(movie_code, pos_num < MAX_DATA, neg_num < MAX_DATA)
        pos_num += len(pos)
        neg_num += len(neg)
        save_tsv(POS_RAW, pos, mode='a', encoding='utf-8')
        save_tsv(NEG_RAW, neg, mode='a', encoding='utf-8')
        movie_code -= 1
        write_log(movie_code, title, pos_num, neg_num)
