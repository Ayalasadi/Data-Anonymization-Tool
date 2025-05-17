# Experimental Results

## 1. Machine Learning Evaluation

We trained a Logistic Regression model on the original dataset (`adult.csv`) and the anonymized dataset (`anonymized_kl.csv`). The goal was to assess how much predictive performance is retained after applying k-anonymity (k=3) and l-diversity (l=2).

| Metric           | Original | Anonymized |
|------------------|----------|------------|
| Accuracy         | 83.4%    | 83.3%      |
| Precision (>50K) | 71%      | 70%        |
| Recall (>50K)    | 54%      | 54%        |
| F1-score (>50K)  | 61%      | 61%        |

This indicates **minimal utility loss** — the anonymized data retains high predictive value.

---

## 2. Certainty Penalty

We measured the model's average confidence in its predictions:

- **Original dataset**: 83.57%
- **Anonymized dataset**: 83.71%

**Certainty Penalty** = -0.0014  
(Surprisingly, the anonymized model was slightly more confident.)

---

## 3. Query Distortion

We compared average hours worked per week by gender:

| Gender | Original Avg | Anonymized Avg | Distortion |
|--------|--------------|----------------|------------|
| Female | 36.41        | 36.41          | 0.00       |
| Male   | 42.43        | 42.43          | 0.00       |

This shows **no distortion** in this aggregate statistic — anonymization preserved important summary data.

---

## 4. Utility vs Privacy Tradeoff

We compared how different privacy models affect the **mean age** statistic — a commonly used attribute in population analysis.

| Method               | Mean Age | Absolute Difference from Original |
|----------------------|----------|-----------------------------------|
| Original             | 38.58    | 0.00                              |
| k-Anonymity (k=3)    | 38.97    | 0.39                              |
| Differential Privacy | 37.31    | 1.27                              |

As expected:
- **k-Anonymity** introduced slight distortion through generalization.
- **Differential Privacy** added random noise via Laplace mechanism, leading to higher distortion but stronger formal privacy guarantees.

We used an epsilon value of **1.0**, which is considered a moderate privacy budget.

![DP vs k-Anonymity Chart](images/mean_age_comparison.png)

This visualization clearly demonstrates the **trade-off between privacy strength and data utility**. While k-anonymity preserves structure better, differential privacy provides rigorous protection at the cost of precision.

---

### ✅ Conclusion (update)

Our enhanced pipeline now supports both **identity-based anonymization (k-anonymity + l-diversity)** and **formal statistical privacy (differential privacy)**. This makes the tool more adaptable and robust for real-world use cases requiring varying privacy guarantees.
