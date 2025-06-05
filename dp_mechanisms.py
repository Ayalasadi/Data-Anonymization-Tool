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

def gaussian_dp_mechanism(value, sensitivity, epsilon, delta):
    # sigma is the standard deviation of the noise that will be added
    sigma = np.sqrt(2 * np.log(1.25 / delta)) * (sensitivity / epsilon)
    noisy_value = value + np.random.normal(loc=0, scale=sigma)
    return noisy_value

def parse_args():
    parser = argparse.ArgumentParser(description="Laplace Mechanism Tool")
    parser.add_argument("--data", type=str, default="adult.csv", help="Path to dataset")
    parser.add_argument("--sensitivity", type=float, default=1.0, help="Minimum sensitivity to achieve differntial privacy")
    parser.add_argument("--epsilon", type=float, default=1.0, help="Chosen epsilon value")
    parser.add_argument("--delta", type=float, default=1e-5, help="Delta for (ε, δ)-differential privacy") 
    parser.add_argument("--mechanism", type=str, choices=["laplace", "gaussian"], default="laplace", help="Choose noise mechanism")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.epsilon <= 0:
        raise ValueError("Epsilon must be a positive value")
    if args.sensitivity < 0:
        raise ValueError("Sensitivity must be non-negative")
    if args.mechanism == "gaussian" and (args.delta <= 0 or args.delta >= 1):
        raise ValueError("Delta must be between 0 and 1 for Gaussian mechanism")


    df = load_data(args.data)

    mean_age = df["age"].mean()
    
    if args.mechanism == "laplace":
        noisy_age = laplace_dp_mechanism(mean_age, args.sensitivity, args.epsilon)
        print(f"Laplace mechanism used (e={args.epsilon})")
    elif args.mechanism == "gaussian":
        noisy_age = gaussian_dp_mechanism(mean_age, args.sensitivity, args.epsilon, args.delta)
        print(f"Gaussian mechanism used (e={args.epsilon}, d={args.delta})")

    print(f"Original mean age: {mean_age:.2f}")
    print(f"Noisy mean age (e={args.epsilon}, s={args.sensitivity}): {noisy_age:.2f}")
