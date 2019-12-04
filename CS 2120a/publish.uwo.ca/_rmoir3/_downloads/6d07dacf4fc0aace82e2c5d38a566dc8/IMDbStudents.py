
import numpy as np
import sklearn.datasets as ds
from scipy.sparse import hstack, vstack, csr_matrix
import re

N_REVIEWS = 50000
NEG_OFFSET = 12500
N_FEATURES = 89527

def validate_n(n):
    
    if n > N_REVIEWS:
        raise ValueError('n must be smaller than 50 000')
    elif n < 2:
        raise ValueError('n must be greater than 1')
    else:
        return int(n/2)

def load_data(path):
    
    data = ds.load_svmlight_file(path,
                                 dtype=np.int64,
                                 n_features=N_FEATURES)
    
    return data

def load_labeled_data(num_data_items,Bow_path):
    
    n = validate_n(num_data_items)
    labeled_data = load_data(Bow_path)
    
    rm = labeled_data[0]                    # Review Matrix
    sv = labeled_data[1].astype(np.int64)   # Sentiment Vector
    offset = NEG_OFFSET
    
    reviews = vstack((rm[0:n],rm[offset:offset+n]))
    sentiments = np.concatenate((sv[0:n],sv[offset:offset+n]))
    
    return (reviews,sentiments)

def load_unlabeled_data(num_data_items,
                        Bow_path='./aclImdb/train/unsupBow.feat'):
      
    n = validate_n(num_data_items)
    unlabeled_data = load_data(Bow_path)

    rm = unlabeled_data[0]  # Review Matrix
    offset = NEG_OFFSET
    
    reviews = vstack((rm[0:n],rm[offset:offset+n]))
    
    return reviews

def make_vocab_dict():
    
    vocab_dict = {}
    
    with open('./aclImdb/imdb.vocab', encoding='utf8') as f:
        for index, word in enumerate(f):
            vocab_dict[word.strip()] = index
    
    return vocab_dict

def create_review_matrix(review_list):
    
    rm = csr_matrix((len(review_list),N_FEATURES),dtype=np.int64)
    
    d = make_vocab_dict()
    
    for row, rev in enumerate(review_list):
        for word in rev.split():
            word = re.sub(r'[.,:;]+', '', word)
            new_word = word.strip('!')
            if word != new_word:
                rm[0,d['!']] += len(word) - len(new_word)
                word = new_word
            try:
                rm[row,d[word.lower()]] += 1
            except KeyError:
                pass

    return rm
        

labeled_train_path='./aclImdb/train/labeledBow.feat'
labeled_test_path='./aclImdb/test/labeledBow.feat'
unlabeled_path='./aclImdb/train/unsupBow.feat'


## Example of creating a list of reviews and computing their review matrix
rev1 = 'This is a review of a crappy movie, and it sucked!'
rev2 = 'This is a review of an awesome movie; it was fantastic!!'

revs = [rev1, rev2]
rm = create_review_matrix(revs)
