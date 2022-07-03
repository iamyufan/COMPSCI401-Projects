from model import TextModel
import pandas as pd
from sklearn.model_selection import train_test_split


def build_model():
    model = TextModel()

    data_train = pd.read_csv('./training.csv', delimiter=";")

    data_train = data_train[['text', 'country_code']]
    data_train['target_id'] = data_train['country_code'].apply(lambda x: int(x == 'US'))
    data_train.drop(['country_code'], axis=1, inplace=True)
    X_train = list(data_train['text'].values)
    y_train = list(data_train['target_id'].values)

    model.train(X_train, y_train)
    print('--- Model training complete')

    model.update_version("v0.3")
    print('--- The model_version has been updated to ' + model.version)

    model.update_date()
    print('--- The model_date has been updated to ' + model.model_date)

    model.pickle_model()

if __name__ == "__main__":
    build_model()