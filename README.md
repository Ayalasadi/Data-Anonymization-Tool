# Data Anonymization Tool

A Python-based data anonymization tool implementing greedy k-anonymity with optional l-diversity, using generalization and suppression techniques.

## Motivation
With the rise of machine learning and data sharing, protecting individual privacy is more critical than ever. Even datasets stripped of names can leak sensitive information through quasi-identifiers like age, ZIP code, and education. This project provides a hands-on implementation of privacy techniques to balance data utility and confidentiality.

## Features
- Greedy generalization of quasi-identifiers to satisfy k-anonymity
- Multi-level hierarchy generalization (age and ZIP code)
- Iterative approach with minimal information loss
- Dynamic k control via command-line interface (CLI)
- Full unit test coverage validating k-anonymity
- Modular and extensible design for future enhancements

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/Ayalasadi/Data-Anonymization-Tool.git
    cd Data-Anonymization-Tool
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Download the dataset:
    ```bash
    python download_data.py
    ```

4. Run the anonymizer:
    ```bash
    python greedy_anonymizer.py 5
    ```
    (The above command anonymizes the data with `k=5`.)

5. Run unit tests:
    ```bash
    python test_greedy_anonymizer.py
    ```

## Example Output
```bash
Generalizing age to level 1
Generalizing zip-code to level 1
Achieved k-anonymity with k=5 
```
