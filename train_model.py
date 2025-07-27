# train_model.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Step 1: Load the labeled training data
df = pd.read_csv("/mnt/data/training_data.csv")

# Step 2: Prepare features and labels
X = df["Description"]              # Bug descriptions
y = df["Team"]                     # Team labels

# Step 3: Convert text to TF-IDF vectors (basic NLP)
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Step 4: Train a logistic regression classifier
clf = LogisticRegression(max_iter=200)
clf.fit(X_vectorized, y)

# Step 5: Save the model and vectorizer for reuse
joblib.dump(clf, "/mnt/data/team_classifier.pkl")
joblib.dump(vectorizer, "/mnt/data/tfidf_vectorizer.pkl")

print("✅ Model and vectorizer trained and saved successfully.")
