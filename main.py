# -*- coding: utf-8 -*-
"""main.py"""

from prefect import task, flow
import requests
import pandas as pd
import time
from flask import Flask, jsonify
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# Task 1: Fetch articles from the NYT API
@task
def fetch_nytimes_articles(api_key: str, retries: int = 5, timeout: int = 10):
    url = f"https://api.nytimes.com/svc/mostpopular/v2/shared/1/facebook.json?api-key={api_key}"
    retry_count = 0
    data = None

    while retry_count < retries:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                print("Data fetched successfully!")
                data = response.json()
                break
            elif response.status_code == 503:
                print(f"Service unavailable (503). Retrying... ({retry_count + 1}/{retries})")
                retry_count += 1
                time.sleep(2)
            else:
                print(f"Error: {response.status_code}, {response.text}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying... ({retry_count + 1}/{retries})")
            retry_count += 1
            time.sleep(2)

    if data and "results" in data:
        return data["results"]
    else:
        print("Failed to fetch articles.")
        return []


# Task 2: Save articles to a CSV
@task
def save_articles_to_csv(articles: list, filename: str = "most_shared_facebook_articles.csv"):
    if not articles:
        print("No articles to save.")
        return

    df = pd.DataFrame(articles)
    df.to_csv(filename, index=False)
    print(f"Saved articles to {filename}")
    return filename


# Task 3: Analyze the articles
@task
def analyze_articles(file: str):
    df = pd.read_csv(file)

    # Analyze popular sections
    print("Columns available in the dataset:")
    print(df.columns)  # Debugging to see column names

    popular_sections = df["section"].value_counts()
    print("Most popular sections:")
    print(popular_sections)

    # Analyze publication trends
    df["published_date"] = pd.to_datetime(df["published_date"])
    df["day_of_week"] = df["published_date"].dt.day_name()
    popular_days = df["day_of_week"].value_counts()
    print("\nMost popular publication days:")
    print(popular_days)

    return popular_sections, popular_days


# Task 4: Train a model
@task
def train_random_forest(file: str):
    df = pd.read_csv(file)

    # Check for the sentiment column or compute it
    if "sentiment" not in df.columns:
        print("The 'sentiment' column is missing. Computing sentiment as an example.")
        df["sentiment"] = 1  # Replace with actual sentiment analysis logic if needed

    # Encode categorical features
    df["section_encoded"] = pd.factorize(df["section"])[0]
    df["day_of_week"] = pd.to_datetime(df["published_date"]).dt.dayofweek

    # Define features and target
    X = df[["section_encoded", "day_of_week"]]
    y = (df["sentiment"] > 0).astype(int)  # Target: Positive sentiment

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train model
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    # Evaluate model
    accuracy = clf.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy}")

    return clf


# Prefect Flow
@flow
def nytimes_pipeline():
    # API key
    api_key = "bxGyZ7BvL4f4OdaYEHvGbeU110z25HUj"

    # Step 1: Fetch articles
    articles = fetch_nytimes_articles(api_key)

    # Step 2: Save articles to CSV
    file = save_articles_to_csv(articles)

    # Step 3: Analyze articles
    analyze_articles(file)

    # Step 4: Train a model
    train_random_forest(file)


# Flask app to trigger the Prefect flow
app = Flask(__name__)

@app.route("/run_pipeline", methods=["GET"])
def run_pipeline():
    nytimes_pipeline()
    return jsonify({"message": "Pipeline executed successfully!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
