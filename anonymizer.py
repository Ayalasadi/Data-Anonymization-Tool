import pandas as pd
import numpy as np
import argparse 


def load_data(path):
    df = pd.read_csv(path)

    #Simulate ZIP codes
    np.random.seed(42)
    df["zip-code"] = np.random.choice(
        [97201, 97202, 97203, 97204, 97205, 97206, 97207, 97208],
        size=len(df)
    )

    return df

def generalize_age(df):
    df['age'] = pd.cut(df['age'], bins=[0, 20, 30, 40, 50, 60, 100], 
                       labels = ["0-20", "21-30", "31-40", "41-50", "51-60", "61+"])
    return df

def generalize_zip(df):
    df['zip-code'] = df['zip-code'].astype(str).str.slice(0, 3) + '**'
    return df


def generalize_education(df):
     mapping = {
        'Preschool': 'HS or Less',
        '1st-4th': 'HS or Less',
        '5th-6th': 'HS or Less',
        '7th-8th': 'HS or Less',
        '9th': 'HS or Less',
        '10th': 'HS or Less',
        '11th': 'HS or Less',
        '12th': 'HS or Less',
        'HS-grad': 'HS or Less',
        'Some-college': 'Some College',
        'Assoc-acdm': 'Some College',
        'Assoc-voc': 'Some College',
        'Bachelors': 'Bachelors',
        'Masters': 'Advanced Degree',
        'Doctorate': 'Advanced Degree',
        'Prof-school': 'Advanced Degree'
    } 
     df['education'] = df['education'].map(mapping)
     return df

def parse_args():
    parser = argparse.ArgumentParser(description="Data Anonymizaation Tool")
    parser.add_argument("--data", type=str, default="adult.csv", help="Path to dataset")
    parser.add_argument("--k", type=int, default=3, help="Minimum k for k-anonymity")
    parser.add_argument("--l", type=int, default=1, help="Minimum l for l-diversity")
    return parser.parse_args()

def suppress_low_frequency_groups(df, quasi_identifiers, k):
    grouped = df.groupby(quasi_identifiers, observed=False)
    valid_indices = []

    for _, group in grouped:
        if len(group) >= k:
            valid_indices.extend(group.index)

    return df.loc[valid_indices]
   

if __name__ == "__main__":
    args = parse_args()
    df = load_data("adult.csv")
    df = generalize_age(df)
    df = generalize_zip(df)
    df = generalize_education(df)

    print("🔒 Generalized Sample:")
    print(df[["age", "zip-code", "education", "sex", "income"]].head())
    print("📊 Original Size:", len(df))

    qi = ["age", "zip-code", "education", "sex"]
    df = suppress_low_frequency_groups(df, qi, args.k) 

    print("🔒 After Suppression Size:", len(df))
    print(df[["age", "zip-code", "education", "sex", "income"]].head())
    