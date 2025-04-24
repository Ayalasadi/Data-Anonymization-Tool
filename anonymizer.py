import pandas as pd
import numpy as np

def load_data(path):
    return pd.read_csv(path)

def generalize_age(df):
    df['age'] = pd.cut(df['age'], bins=[0, 20, 30, 40, 50, 60, 100], 
                       labels = ["0-20", "21-30", "31-40", "41-50", "51-60", "61+"])
    return df

if __name__ == "__main__":
    df = load_data("adult.csv")
    df = generalize_age(df)
    print(df.head())