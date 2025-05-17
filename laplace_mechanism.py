import pandas as pd
import numpy as np
import argparse

def load_data(path):
    df = pd.read_csv(path)

    np.random.seed(42)
    df["zip-code"] = np.random.choice(
        [97201, 97202, 97203, 97204, 97205, 97206, 97207, 97208],
        size=len(df)
    )

    return df

def laplace_dp_mechanism(value, sensitivity, epsilon):
    noisy_value =  value + np.random.laplace(loc=0, scale = sensitivity/epsilon)
    return noisy_value

def parse_args():
    parser = argparse.ArgumentParser(description="Laplace Mechanism Tool")
    parser.add_argument("--data", type=str, default="adult.csv", help="Path to dataset")
    parser.add_argument("--sensitivity", type=float, default=1.0, help="Minimum sensitivity to achieve differntial privacy")
    parser.add_argument("--epsilon", type=float, default=1.0, help="Chosen epsilon value")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.epsilon <= 0:
        raise ValueError("Epsilon must be a positive value")
    if args.sensitivity < 0:
        raise ValueError("Sensitivity must be non-negative")

    df = load_data(args.data)

    mean_age = df["age"].mean()
    noisy_age = laplace_dp_mechanism(mean_age, args.sensitivity, args.epsilon)

    print(f"Original mean age: {mean_age:.2f}")
    print(f"Noisy mean age (e={args.epsilon}, s={args.sensitivity}): {noisy_age:.2f}")

#func wrapper
def noisy_mean_age(df, epsilon=1.0, sensitivity=1.0):
    """
    Compute mean age with Laplace noise added.
    """
    mean_age = df["age"].mean()
    return laplace_dp_mechanism(mean_age, sensitivity, epsilon)
