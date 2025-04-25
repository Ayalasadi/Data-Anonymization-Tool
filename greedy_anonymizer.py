import pandas as pd
import numpy as np


def add_fake_zip_codes(df):
    np.random.seed(42)
    df["zip-code"] = np.random.choice(
        [97201, 97202, 97203, 97204, 97205, 97206, 97207, 97208],
        size=len(df)
    )
    return df

def generalize_age(df):
    df['age'] = pd.cut(df['age'], bins=[0, 20, 30, 40, 50, 60, 100], 
                       labels=["0-20", "21-30", "31-40", "41-50", "51-60", "61+"])
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

def is_k_anonymous(df, quasi_identifiers, k):
    """
    Returns True if all groups formed by quasi_identifiers
    contain at least k records.
    """
    group_sizes = df.groupby(quasi_identifiers).size()
    return all(group_sizes >= k)

def generalize_age_level(df, level):
    if level == 0:
        return generalize_age(df)
    elif level == 1:
        df['age'] = df['age'].replace({
            "0-20": "0-40", "21-30": "0-40", "31-40": "0-40",
            "41-50": "41+", "51-60": "41+", "61+": "41+"
        })
    elif level == 2:
        df['age'] = "ALL"
    return df

def generalize_zip_level(df, level):
    if level == 0:
        #keep only first 3 digits
        df['zip-code'] = df['zip-code'].astype(str).str.slice(0,3) + '**'
    elif level == 1:
        #keep only first 2 digits
        df['zip-code'] = df['zip-code'].astype(str).str.slice(0,2) + '***'
    elif level == 2:
        #full suppression (all zip codes are replaced by a generic token)
        df['zip-code'] = "UNKNOWN"
    return df

def greedy_anonymize(df, quasi_identifiers, k):
    """
    Iteratively generalizes the quasi-identifiers to achieve k-anonymity.
    """
    # Track generalization levels
    gen_levels = {
        "age": 0,
        "zip-code": 0
        # (optional: you can later add education/sex too if you want)
    }

    max_levels = {
        "age": 2,  # 0, 1, 2
        "zip-code": 2
    }

    while not is_k_anonymous(df, quasi_identifiers, k):
        # Find an attribute that can still be generalized
        attribute_to_generalize = None

        for attr in gen_levels:
            if gen_levels[attr] < max_levels[attr]:
                attribute_to_generalize = attr
                break

        if attribute_to_generalize is None:
            print("Cannot achieve k-anonymity with available generalizations!")
            break

        print(f"⚙️ Generalizing {attribute_to_generalize} to level {gen_levels[attribute_to_generalize] + 1}")

        # Apply next generalization
        if attribute_to_generalize == "age":
            df = generalize_age_level(df, gen_levels["age"] + 1)
        elif attribute_to_generalize == "zip-code":
            df = generalize_zip_level(df, gen_levels["zip-code"] + 1)

        # Update level
        gen_levels[attribute_to_generalize] += 1

    return df

if __name__ == "__main__":
    import sys

    df = pd.read_csv("adult.csv")
    df = add_fake_zip_codes(df)
    df = generalize_education(df)

    quasi_identifiers = ["age", "zip-code", "education", "sex"]

    if len(sys.argv) > 1:
        k = int(sys.argv[1])
    else:
        k = 3

    df = greedy_anonymize(df, quasi_identifiers, k)

    print(df[["age", "zip-code", "education", "sex", "income"]].head())

    print(f"🔒 Achieved k-anonymity with k={k}: {is_k_anonymous(df, quasi_identifiers, k)}")

