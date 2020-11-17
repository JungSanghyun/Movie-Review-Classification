# Movie-Review-Classifier

KAIST 2020 Spring Semester - CS372: Natural Language Processing with Python - Term Project

20160288 Hansung Bae, 20160580 Sanghyun Jung, 20160487 Yongwook Lee, 20170278 Jongchan Park, 20180310 Kyusung Seo

## Dependency

* Python 3.7
* beautifulsoup4==4.6.0
* konlpy==0.5.2
* nltk==3.4.5
* requests==2.23.0

## Implementation

### 1. Data Processing

#### 1-1. Get Raw Data by Crawling
* Crawl the Naver movie site to get comments and ratings.
* Raw data includes 100,000 positive reviews and 100,000 negative reviews.
* Raw data is a list of [review code, movie title, comment, rating] in tsv format.
```
python src/data_processing/get_raw_data.py
```
Result Files
* ```data/raw_data/```
  * ```pos_raw.tsv```
  *  ```neg_raw.tsv```
  * ```status.log```

#### 1-2.  Get Dataset from Raw Data
* Combine raw data and shuffle them and divide them into train dataset and test dataset.
* Train dataset includes 150,000 reviews and test dataset includes 50,000 reviews.
* Dataset is a list of [review code, comment, label(1 for positive, 0 for negative)] in tsv format.
```
python src/data_processing/get_dataset.py
```
Result Files
* ```data/dataset/```
  * ```train_data.tsv```
  *  ```test_data.tsv```

#### 1-3. Text Preprocessing
* Remove all the non-Korean characters.
* Remove stopwords such as '은', '는', '이', '가', '을', '를'.
* Tokenizes and tags Part-of-Speech using tagger in ```konlpy``` library.
* Dataset is a list of [list of tagged words, label] in json format.

```
python src/data_processing/preprocess.py
```
Result Files
* ```data/preprocessed/```
  * ```prep_train.json```
  * ```prep_test.json```

### 2. Bag of Words

#### 2-1. Get BoW from Preprocessing
* Get preprocessed dataset in json format.
* Make BoW positive, BoW negative list in pickle format.
* pickle files are separated by BoW score and index information.

```
python src/bag_of_words/get_bow.py
```

Result files

* ```data/bag_of_words/```
  * ```1-gram/```
    * ```1-gram_bow_pos_idx_train.pkl```
    * ```1-gram_bow_pos_train.pkl```
    * ```1-gram_bow_neg_idx_train.pkl```
    * ```1-gram_bow_neg_train.pkl```
  * ```2-gram/```
    * ```2-gram_bow_pos_idx_train.pkl```
    * ```2-gram_bow_pos_train.pkl```
    * ```2-gram_bow_neg_idx_train.pkl```
    * ```2-gram_bow_neg_train.pkl```
  * ```3-gram/```
    * ```3-gram_bow_pos_idx_train.pkl```
    * ```3-gram_bow_pos_train.pkl```
    * ```3-gram_bow_neg_idx_train.pkl```
    * ```3-gram_bow_neg_train.pkl``` 

### 3. Naive Bayes Classifier

#### 3-1. Unique Words List
* Get BoW train set in pickle format.
* Make unique words list in pickle format.

```
python src/naive_bayes/unique_words.py
```

Result files

* ```data/naive_bayes/```
  * ```1-gram/```
    * ```1-gram_unique_words_train.pkl```
  * ```2-gram/```
    * ```2-gram_unique_words_train.pkl```
  * ```3-gram/```
    * ```3-gram_unique_words_train.pkl```

#### 3-2. Naive Bayes Classifier
* From BoW train set and unique words list, calculate probability.
* Laplace smoothing is applied.
* Calculate accuracy on test dataset.

```
python src/naive_bayes/classifier.py
```

## Result
### Test dataset Accuracy for N-gram model

```
1-GRAM Test Dataset Accuracy: 85.714% (Total: 50000, Correct: 42857)
2-GRAM Test Dataset Accuracy: 84.536% (Total: 50000, Correct: 42268)
3-GRAM Test Dataset Accuracy: 70.32% (Total: 50000, Correct: 35160)
```

### Main Program
```
python src/main.py
```

```
N-Gram(1~3): 1
Input Comment: 이렇게 재미없는 영화는 처음 봤어요.
| Word-wise Probability |
 | ('이렇게/Adverb',) | Positive: 38.4% | Negative: 61.6% |
 | ('재미없다/Adjective',) | Positive: 7.4% | Negative: 92.6% |
 | ('영화/Noun',) | Positive: 50.8% | Negative: 49.2% |
 | ('처음/Noun',) | Positive: 42.6% | Negative: 57.4% |
 | ('보다/Verb',) | Positive: 58.6% | Negative: 41.4% |
| NEGATIVE Comment in 94.8% Probability |
```
