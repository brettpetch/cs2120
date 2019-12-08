# Student Name: Brett Petch
# Student Number: 251038051
# CS2120 Assignment 4

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from pylab import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def data_check(url='https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_multilingual_US_v1_00.tsv.gz',
               file='./data/amazon_reviews_multilingual_US_v1_00.tsv'):
    """
    If you know the data is present, you do not need to use this function.
    The following function does the following:
        1. Check for file to exist
            - Go to 3.
        2. If file not exists:
            a. Check if there is a data folder.
            b. If there is no data folder, create one.
            c. Download data from the website to the data folder.
            d. Unzip data using gzip
        3. Load Data.
    :param url: File download address
    :param file: File location (rel os)
    :return: loaded data from external function.
    """
    import gzip as gz
    import os, shutil, urllib.request
    try:
        if os.path.isfile(file):  # check to see if file exists
            print("Found data!")
        else:
            print("Data not found.")  # File wan't real
            directory = "./data/"  # store directory in variable
            if not os.path.exists(directory):  # check if data directory exists
                print("Creating directory...")
                os.makedirs(directory)  # make the directory if it doesn't exist
            print("Downloading data... This may take a while (1.5gb here we go!)")
            urllib.request.urlretrieve(url, './data/amazon_reviews_multilingual_US_v1_00.tsv.gz')  # Download data
            print("Unzipping data")
            with gz.open(directory + 'amazon_reviews_multilingual_US_v1_00.tsv.gz', 'rb') as f_in:  # Ungzip the data
                with open(file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)  # copy to new file
            print("Cleaning up...")
            os.remove('./data/amazon_reviews_multilingual_US_v1_00.tsv.gz')  # delete the compressed file
            print("Done.")
    finally:
        return load_data(file)  # load data


def load_data(filename="./data/amazon_reviews_multilingual_US_v1_00.tsv",
              cols=['star_rating', 'review_headline', 'review_body', 'vine', 'helpful_votes', 'product_category']):
    """
    Takes in a filename, as well as a list of column names that are to be imported.
    :dependant pd: Pandas
    More info about data available at: https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt
    Removing HTML from Python regex: https://stackoverflow.com/questions/45999415/removing-html-tags-in-pandas#_=_
    :param filename: File that you wish to open
    :param cols: Columns of file that you wish to use
                    star rating, review headline, review body
    :return: 3.1gb dataset
    """
    clean = re.compile('<.*?>')
    cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|<.*>')

    print('Creating Pandas DataFrame... Grab a cup of coffee.')
    df = pd.read_csv(filename, delimiter='\t', usecols=cols)
    df.dropna(inplace=True)
    print('Creating star rating vectors (positive)')
    df[df['star_rating'] != 3.0]
    df['positivity'] = np.where(df['star_rating'] > 3, 1, 0)
    print('Counting number of words in review body...')
    df['n_words'] = df['review_body'].str.count(' ') + 1
    df.head()
    print('DataFrame Created, sorry for the wait: maybe invest in SSD?')

    # Test to see if actually cleaned:
    # df.to_csv('./data/out.csv')

    return df


def vis1(amzn):
    """
    This function processes a dataset, then visualizes it in a horizontal bar graph.
    :param amzn: Amazon Data. bar graph of 5 star reviews by product category
    :return:
    """
    df = amzn
    print("Checking to see if there are more than 5 helpful votes, this should only take a sec.")
    df = df.loc[df['helpful_votes'] > 5]
    print("Making dataframe smaller... just a second or two longer")
    df = df[['product_category', 'star_rating']]
    df = df.groupby('product_category').mean().reset_index()
    df = df.loc[df['star_rating'] < 3]

    print("Plotting... this could take a sec")

    plt.rcdefaults()
    fig, ax = plt.subplots()
    ax.barh(df['product_category'].str.replace('_', ' ', regex=True).values, df['star_rating'].values)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Star Rating')
    ax.set_title('Lowest Mean Star Ratings by Product Category')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 8.5)
    plt.savefig('vis1.png')


def vis2(amzn):
    """
    product catagory by number of reviews.
    :param data: Amazon Data. Stars by product section of amazon.
    :return:
    """
    print('Creating DataFrame...')
    df = amzn.product_category.value_counts()
    df = pd.DataFrame(df).reset_index().nlargest(6, ['product_category'])
    print('Plotting... This could take a sec')
    plt.rcdefaults()
    fig, az = plt.subplots()
    az.barh(df['index'], df['product_category'])
    az.invert_yaxis()  # labels read top-to-bottom
    az.set_xlabel('Amount of reviews')
    az.set_title('Highest Amount of Review by Product Category')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(20, 8.5)
    plt.savefig('vis2.png')


def test_splitting(amzn):
    """
    Splits data into pieces, then runs the ML functions.
    :param amzn: input of dataset,
    :return: X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(amzn['review_body'].values,
                                                        amzn['positivity'].values,
                                                        test_size=0.1,
                                                        random_state=0)
    print('X_train first entry: \n\n', X_train[0])
    print('Y_train first entry: \n\n', y_train[0])
    print('\n\nX_train shape: ', X_train.shape)
    return X_train, X_test, y_train, y_test


def learn1(X_train, X_test, y_train, y_test):
    """
    This function uses Logistic Regression to identify a multitude of info from data.
    :param X_train_vectorized:
    :param X_test:
    :param y_train:
    :param y_test:
    :param vect:
    :return:
    """
    dick = []
    for review in X_train:
        review_text = BeautifulSoup(review, features='lxml').get_text()
        letters_only = re.sub("[^a-zA-Z]", " ", review_text)
        words = letters_only.lower().split()
        stops = set(stopwords.words("english"))
        meaningful_words = [w for w in words if not w in stops]
        dick.append(" ".join(meaningful_words))
    vect = CountVectorizer(analyzer='word',
                           tokenizer=None,
                           preprocessor=None,
                           stop_words=None,
                           max_features=5000).fit(X_train)
    X_train_vectorized = vect.fit_transform(dick)
    X_train_vectorized = X_train_vectorized.toarray()
    model = LogisticRegression()
    model.fit(X_train_vectorized, y_train)
    pred = model.predict(vect.transform(X_test))
    print('AUC: ', roc_auc_score(y_test, pred))
    feature_names = np.array(vect.get_feature_names())
    sorted_coef_index = model.coef_[0].argsort()
    print('Smallest Coefs: \n{}\n'.format(feature_names[sorted_coef_index[:10]]))
    print('Largest Coefs: \n{}\n'.format(feature_names[sorted_coef_index[:-11:-1]]))
    print(model.predict(vect.transform(['This was terrible!'])))


def learn2(X_train, X_test, y_train, y_test):
    """
    This one uses info from the model before, and tweaks it a bit.
    :param amzn:
    :return:
    """
    vect = TfidfVectorizer(min_df=5, ngram_range=(1, 2)).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    model = LogisticRegression()
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(vect.transform(X_test))
    print('AUC: ', roc_auc_score(y_test, predictions))
    print(model.predict(vect.transform(['The candy is not good, I would never buy them again',
                                        'The candy is not bad, I will buy them again'])))


# This is the Test
data = data_check()

vis1(data)
vis2(data)

# a -> X_train, b -> X_text, c -> Y_train, d-> Y_test
a, b, c, d = test_splitting(data)

learn1(a, b, c, d)
learn2(a, b, c, d)
