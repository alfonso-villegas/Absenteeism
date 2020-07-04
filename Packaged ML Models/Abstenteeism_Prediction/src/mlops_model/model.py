from sklearn import linear_model
import pandas as pd
import os
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score
from mlops_model.util import get_data_directory, read_data

def feature_engineering(train):
    categorical_columns = ['ID', 'ID.Worker','Reason.for.absence', 'Month.of.absence', 'Day.of.the.week', 'Seasons', 'Disciplinary.failure', 'Social.drinker', 'Social.smoker', 'Absenteeism']
    train[categorical_columns] = train[categorical_columns].astype("category")
    train.drop(["Body.mass.index", "ID", "ID.Worker"], inplace=True, axis=1)
    train['Absenteeism'] = train['Absenteeism'].astype(int)
    return train

def train_model():
    train = read_data()
    train = feature_engineering(train)
    X = train.iloc[0:593].drop(['Absenteeism'],axis=1)
    y = train.iloc[0:593]['Absenteeism']
    model = linear_model.LogisticRegression(max_iter=10000)
    y_pred = cross_val_predict(model, X, y, cv=5)
    score = accuracy_score(y,y_pred)
    print("Accuracy = {0:.4f}".format(score))
    model.fit(X, y)
    return model, score
