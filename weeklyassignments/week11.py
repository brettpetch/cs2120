# Student Name: Brett Petch
# Student Number: 251038051
from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def svc_things(X_train, X_test, y_train, y_test, model):
    """
    :param X_train: take in train data
    :param X_test: Test data on the x axis
    :param y_train: train data on y
    :param y_test: test data on y
    :param model: linear / poly
    :return: accuracy_score(y_test, y_p)
    """
    svc = SVC(kernel=model)
    svc.fit(X_train, y_train)
    y_p = svc.predict(X_test)
    print(accuracy_score(y_test, y_p))


iris = datasets.load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris['data'],
                                                    iris['target'],
                                                    test_size=0.33,
                                                    random_state=43,
                                                    stratify=iris['target'])


svc_things(X_train, X_test, y_train, y_test, 'linear')
svc_things(X_train, X_test, y_train, y_test, 'poly')
