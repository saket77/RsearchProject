# Re-define functions from driver_with_rules_and_nlp.py since module import failed

import pandas as pd
import joblib

# Load trained model and vectorizer
vectorizer = joblib.load("/mnt/data/tfidf_vectorizer.pkl")
model = joblib.load("/mnt/data/team_classifier.pkl")

# Business rules for routing
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
        return ""

# Combined logic to triage bugs
def triage_bugs(input_csv_path: str, output_csv_path: str = "results.csv"):
    df = pd.read_csv(input_csv_path)

    if "Description" not in df.columns:
        raise ValueError("Missing required column: 'Description'")

    df["AssignedTeam"] = df["Description"].apply(classify_with_rules)

    mask_needs_nlp = df["AssignedTeam"] == ""
    if mask_needs_nlp.any():
        X_nlp = vectorizer.transform(df.loc[mask_needs_nlp, "Description"])
        df.loc[mask_needs_nlp, "AssignedTeam"] = model.predict(X_nlp)

    df.to_csv(output_csv_path, index=False)

# Run the same test suite again now that functions are reloaded
def run_driver_tests():
    results = []

    # TC01: Valid CSV Input (10 entries)
    try:
        data = {
            "IssueID": [f"BUG-{i}" for i in range(10)],
            "Description": [
                "API error on checkout", "CSS broken on login",
                "Login button fails", "Database not reachable",
                "Dropdown overlaps footer", "Session timeout too soon",
                "Unidentified bug", "Password reset email missing",
                "Cache not cleared", "Header not loading"
            ]
        }
        df_valid = pd.DataFrame(data)
        valid_path = "/mnt/data/test_tc01_valid.csv"
        df_valid.to_csv(valid_path, index=False)
        triage_bugs(valid_path, "/mnt/data/test_tc01_output.csv")
        df_out = pd.read_csv("/mnt/data/test_tc01_output.csv")
        results.append(("TC01", len(df_out) == 10 and "AssignedTeam" in df_out.columns, "10 entries labeled with teams"))
    except Exception as e:
        results.append(("TC01", False, str(e)))

    # TC02: Missing 'Description' Column
    try:
        df_missing = pd.DataFrame({"Summary": ["Login issue"], "Priority": ["High"]})
        missing_path = "/mnt/data/test_tc02_missing.csv"
        df_missing.to_csv(missing_path, index=False)
        triage_bugs(missing_path, "/mnt/data/test_tc02_output.csv")
        results.append(("TC02", False, "Did not raise error for missing Description column"))
    except ValueError as e:
        results.append(("TC02", "Description" in str(e), str(e)))

    # TC03: HTML content in Description
    try:
        df_html = pd.DataFrame({"Description": ["<div>API failure</div>"]})
        html_path = "/mnt/data/test_tc03_html.csv"
        df_html.to_csv(html_path, index=False)
        triage_bugs(html_path, "/mnt/data/test_tc03_output.csv")
        df_out = pd.read_csv("/mnt/data/test_tc03_output.csv")
        prediction = df_out.loc[0, "AssignedTeam"]
        results.append(("TC03", isinstance(prediction, str) and prediction != "", f"Predicted team: {prediction}"))
    except Exception as e:
        results.append(("TC03", False, str(e)))

    # TC04: Prediction Accuracy
    try:
        test_desc = "Login button error"
        predicted_team = classify_with_rules(test_desc)
        if not predicted_team:
            df = pd.DataFrame({"Description": [test_desc]})
            df.to_csv("/mnt/data/test_tc04_input.csv", index=False)
            triage_bugs("/mnt/data/test_tc04_input.csv", "/mnt/data/test_tc04_output.csv")
            df_out = pd.read_csv("/mnt/data/test_tc04_output.csv")
            predicted_team = df_out.loc[0, "AssignedTeam"]
        results.append(("TC04", predicted_team == "Frontend Team", f"Prediction: {predicted_team}"))
    except Exception as e:
        results.append(("TC04", False, str(e)))

    # TC05: Output CSV Check
    try:
        df_input = pd.DataFrame({"Description": ["Cache not cleared after logout"]})
        in_path = "/mnt/data/test_tc05_input.csv"
        out_path = "/mnt/data/test_tc05_output.csv"
        df_input.to_csv(in_path, index=False)
        triage_bugs(in_path, out_path)
        df_out = pd.read_csv(out_path)
        results.append(("TC05", "AssignedTeam" in df_out.columns, f"Output columns: {list(df_out.columns)}"))
    except Exception as e:
        results.append(("TC05", False, str(e)))

    return results

# Execute and save
test_results = run_driver_tests()
df_results = pd.DataFrame(test_results, columns=["Test Case ID", "Pass/Fail", "Comment"])
result_file_path = "/mnt/data/driver_test_results.csv"
df_results.to_csv(result_file_path, index=False)
