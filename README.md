# Data-Engineering-Final
Final Project 690 DACSS

# NY Times Data Pipeline Project

## Overview
This project implements a data pipeline that fetches, processes, and analyzes data from the New York Times Most Popular API. The pipeline is automated using Flask and Prefect, and the results are saved for further analysis and visualization.

---

## Data Source
- **Source:** [New York Times Most Popular API](https://developer.nytimes.com/docs/most-popular-product/1/overview)
- **Details:** The API provides data on the most shared articles on Facebook, including metadata like section, publication date, and title.

---

## Transformation Steps
1. **Fetching Data:**
   - The pipeline connects to the New York Times API to fetch the most shared articles.
   - Data is retrieved in JSON format.
   
2. **Saving Data:**
   - The fetched data is saved locally in a CSV file (`most_shared_facebook_articles.csv`).

3. **Data Analysis:**
   - **Popular Sections:** Analyzes the most popular sections where articles are published.
   - **Publication Trends:** Examines trends in article publication across different days of the week.

4. **Model Training:**
   - **Sentiment Classification:** A Random Forest Classifier is trained on a mock sentiment column.
   - **Features Used:** 
     - Article section (encoded numerically).
     - Day of the week when the article was published.

---

## Data Destination
- **Local CSV File:** The data is saved in `most_shared_facebook_articles.csv`.
- **Analysis Output:** Results are displayed in the console/logs.
- **Trained Model:** The Random Forest model is created and evaluated in the pipeline.

---

## Automation
- **Prefect:** Orchestrates the pipeline into tasks and flows for robust execution.
- **Flask:** Provides an endpoint `/run_pipeline` that triggers the entire data pipeline.
- **Heroku Deployment:** The pipeline is deployed on Heroku for accessibility via a web interface.

---


## Features
- Fetches the most popular shared articles.
- Analyzes publication trends.
- Trains a Random Forest Classifier.

## Installation
1. Clone this repository: git clone https://github.com/Shravan-Sundar14/Data-Engineering-Final/
2.  Navigate to the project directory
3.  Run the Flask application locally
4.  Orchestrate the application on prefect
5.  deploy on heroku
6.  the output pictures have been uploaded aswell
7.  a successful run should ensure you get the .csv file downloaded after running the .py file

8. the output metrics of this execution can be found here https://github.com/Shravan-Sundar14/Data-Engineering-Final/blob/main/Output%20Metrics%20Data%20Engineering.pdf

9. the app metric can be viewed on https://dashboard.heroku.com/apps/dataengg-shravan-app
10. i have turned off all the dynos as it had charges - anyone can run them on their local system for 0.19$/hour
11. 


   

