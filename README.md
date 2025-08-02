# 🐞 SmartBug: NLP + Rule-Based Bug Triaging Tool

This project is part of an applied research assignment that uses a hybrid approach of **business rules** and **machine learning (NLP)** to automatically classify and triage JIRA bug reports into relevant engineering teams.

---

## 🎯 Objective

Help Product Owners (POs) save time and reduce manual work by automatically routing bug descriptions to the appropriate team using intelligent automation.

---

## 📁 Project Structure and Purpose

| Purpose                  | File                           |
|--------------------------|--------------------------------|
| 📄 Training Data         | `training_data.csv`            |
| 🧠 Model File            | `team_classifier.pkl`          |
| 📊 Vectorizer File       | `tfidf_vectorizer.pkl`         |
| 🛠 Train Script          | `train_model.py`               |
| 🚀 Driver Script (ML)    | `driver.py`                    |
| 🧪 Driver Test Script    | `drivertest.py`                |
| ✅ Test Output           | `driver_test_results.csv`      |
| 📥 Mock JIRA Input       | `mock_jira_bugs.csv`           |
| 📤 Final Output Example  | `classified_jira_bugs.csv`                  |

---

## 🧠 How It Works

1. **Business Rules First**:  
   Bug descriptions are matched against a list of known keywords (e.g., "API", "button", "CSS") to assign the appropriate team.

2. **NLP Fallback (Logistic Regression)**:  
   If the bug cannot be classified by rules, a machine learning model trained on labeled bug descriptions uses TF-IDF vectorization to predict the team.

3. **Output**:  
   A new column `AssignedTeam` is added to the CSV and saved as `results.csv`.

---

## 🔧 How to Train the Model

```bash
python train_model.py
```

This uses `training_data.csv` and generates:
- `team_classifier.pkl`
- `tfidf_vectorizer.pkl`

---

## 🚀 How to Run the Driver

```bash
python driver_with_rules_and_nlp.py
```

Or call from another script:

```python
from driver_with_rules_and_nlp import triage_bugs
triage_bugs("mock_jira_bugs.csv", "results.csv")
```

---

## ✅ How to Run Tests

```bash
python drivertest.py
```

It checks the following:

| Test Case | Description                                      |
|-----------|--------------------------------------------------|
| TC01      | Valid CSV with 10 entries – all classified       |
| TC02      | Missing `Description` column – error thrown      |
| TC03      | HTML in bug text – still classified              |
| TC04      | Known bug like "Login button error" – correct team |
| TC05      | Output contains expected `AssignedTeam` column   |

Results are saved to: `driver_test_results.csv`

---

## 🛠 Requirements

```bash
pip install pandas scikit-learn joblib
```

---

## 👨‍💻 Author

Developed by Saket Mundhada
Applied Research Project   


## Appendix: 

🧠 team_classifier.pkl – Model File
This file contains the trained machine learning model.

It's a Logistic Regression classifier trained on bug descriptions (from training_data.csv) and their corresponding team labels (e.g., "Backend Team", "Frontend Team").

It predicts which team should handle a bug report based on the text in the Description field.

Saved using joblib, so it can be reloaded in your driver script for fast, repeatable predictions.

📊 tfidf_vectorizer.pkl – Vectorizer File
This file stores the TF-IDF vectorizer, which transforms raw bug descriptions into a numerical format that the model can understand.

TF-IDF (Term Frequency–Inverse Document Frequency) assigns importance to words in each description based on how frequently they occur across all bugs.

This vectorizer was fit on the training data and must be reused during prediction to maintain consistency between training and inference.

Also saved using joblib for easy reloading.
