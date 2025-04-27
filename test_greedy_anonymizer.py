import pandas as pd
import numpy as np
from greedy_anonymizer import add_fake_zip_codes, generalize_education, greedy_anonymize, is_k_anonymous

#Setup reusable dataset
def load_dataset():
    df = pd.read_csv("adult.csv")
    df = add_fake_zip_codes(df)
    df = generalize_education(df)
    return df

def test_k_anonymity_small_k():
    df = load_dataset()
    quasi_identifiers = ["age", "zip-code", "education", "sex"]
    k = 2

    df = greedy_anonymize(df, quasi_identifiers, k)
    assert is_k_anonymous(df, quasi_identifiers, k), f"Failed k-anonymity for k={k}"

def test_k_anonymity_medium_k():
    df = load_dataset()
    quasi_identifiers = ["age", "zip-code", "education", "sex"]
    k = 5

    df = greedy_anonymize(df, quasi_identifiers, k)
    assert is_k_anonymous(df, quasi_identifiers, k), f"Failed k-anonymity for k={k}"

def test_k_anonymity_high_k():
    df = load_dataset()
    quasi_identifiers = ["age", "zip-code", "education", "sex"]
    k = 10

    df = greedy_anonymize(df, quasi_identifiers, k)
    assert is_k_anonymous(df, quasi_identifiers, k), f"Failed k-anonymity for k={k}"

if __name__ == "__main__":
    test_k_anonymity_small_k()
    print("✅ test_k_anonymity_small_k passed")

    test_k_anonymity_medium_k()
    print("✅ test_k_anonymity_medium_k passed")

    test_k_anonymity_high_k()
    print("✅ test_k_anonymity_high_k passed")
