# ML imports
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

from datetime import date

import pickle


class TextModel(object):

    def __init__(self):
        """Simple NLP
        Attributes:
            clf: sklearn classifier model pipeline
        """
        self.clf = Pipeline([
                ('vect', CountVectorizer(stop_words='english')),
                ('tfidf', TfidfTransformer()),
                ('clf', MultinomialNB()),
            ])
        self.version = ""
        self.model_date = ""

    def train(self, X, y):
        """Trains the classifier to associate the label with the sparse matrix
        """
        # X_train, X_test, y_train, y_test = train_test_split(X, y)
        self.clf.fit(X, y)

    def predict(self, X):
        """Returns the predicted class in an array
        """
        y_pred = self.clf.predict(X)
        return y_pred
    
    def score(self, X, y):
        """Returns the prediction scores for the dataset
        """
        predicted = text_clf.predict(X)
        return np.mean(predicted == y)

    def update_version(self, version):
        self.version = version

    def update_date(self):
        """Update the model date
        """
        self.model_date = str(date.today())

    def pickle_model(self, path='./model.pkl'):
        """Saves the trained classifier for future use.
        """
        d = {'model':self.clf, 
            'model_version':self.version, 
            'model_date':self.model_date}
        with open(path, 'wb') as f:
            pickle.dump(d, f)
            print("--- Pickled classifier at {}".format(path))