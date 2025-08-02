# driver_with_rules_and_nlp.py

import pandas as pd
import joblib

# Load the trained NLP model and vectorizer
vectorizer = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("team_classifier.pkl")

# Business rule–based team classification
def classify_with_rules(description: str) -> str:
    desc = description.lower()
    if "api" in desc or "database" in desc or "backend" in desc:
        return "Backend Team"
    elif "css" in desc or "alignment" in desc or "color" in desc or "style" in desc or "spacing" in desc:
        return "UX Team"
    elif "button" in desc or "mobile" in desc or "dropdown" in desc or "form" in desc or "header" in desc:
        return "Frontend Team"
    elif "cache" in desc or "session" in desc or "backup" in desc:
        return "Platform Team"
    else:
        return ""  # Not matched by business rules

# Combined rule + ML prediction
def triage_bugs(input_csv_path: str, output_csv_path: str = "results.csv"):
    # Step 1: Read input CSV
    df = pd.read_csv(input_csv_path)

    # Step 2: Ensure 'Description' column is present
    if "Description" not in df.columns:
        raise ValueError("Missing required column: 'Description'")

    # Step 3: Apply business rules first
    df["AssignedTeam"] = df["Description"].apply(classify_with_rules)

    # # Step 4: Identify rows that still need prediction via NLP
    # mask_needs_nlp = df["AssignedTeam"] == ""
    # if mask_needs_nlp.any():
    #     # Extract descriptions needing ML prediction
    #     X_nlp = vectorizer.transform(df.loc[mask_needs_nlp, "Description"])
    #     df.loc[mask_needs_nlp, "AssignedTeam"] = model.predict(X_nlp)

    # Step 5: Save final output
    df.to_csv(output_csv_path, index=False)
    print(f"✅ Triaging complete using rules + NLP. Output saved to: {output_csv_path}")

# Example usage:
triage_bugs("mock_jira_bugs.csv", "results.csv")
