import pandas as pd
import os

def get_data_directory():
    """Gets directory where data is located.
    """
    lib_dir = os.path.dirname(__file__)
    data_dir = os.path.join(lib_dir, "dataset")
    return data_dir

def read_data(train_path=None):
    if train_path is None:
        train_path = os.path.join(get_data_directory(), "train.csv")
    train = pd.read_csv(train_path, delimiter=";", decimal=".")
    return train
