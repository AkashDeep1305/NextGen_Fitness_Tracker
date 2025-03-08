import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression

# Ensure CSV files exist
def initialize_csv():
    if not os.path.exists("exercise.csv") or os.stat("exercise.csv").st_size == 0:
        exercise_df = pd.DataFrame(columns=["userid", "gender", "age", "height", "weight", "duration", "heart_rate", "body_temp", "exercise"])
        exercise_df.to_csv("exercise.csv", index=False)

    if not os.path.exists("calories.csv") or os.stat("calories.csv").st_size == 0:
        calories_df = pd.DataFrame(columns=["userid", "calories"])
        calories_df.to_csv("calories.csv", index=False)

    if not os.path.exists("history.csv") or os.stat("history.csv").st_size == 0:
        history_df = pd.DataFrame(columns=["DateTime", "Userid", "Gender", "Age", "Height (cm)", "Weight (Kg)", "BMI", "Duration (min)", "Heart Rate (bpm)", "Body Temperature (°C)", "Exercise", "Calories (kcal)", "Method"])
        history_df.to_csv("history.csv", index=False)

# Train models
def train_models():
    initialize_csv()

    exercise_data = pd.read_csv("exercise.csv")
    calories_data = pd.read_csv("calories.csv")

    if exercise_data.empty or calories_data.empty:
        return None

    df = pd.merge(exercise_data, calories_data, on="userid")

    # Encode categorical values
    label_encoder = LabelEncoder()
    df["gender"] = label_encoder.fit_transform(df["gender"])
    df["exercise"] = label_encoder.fit_transform(df["exercise"])

    X = df.drop(["userid", "calories"], axis=1)
    y = df["calories"]

    if len(X) < 2:  # Require at least 2 samples for meaningful training
        return None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "RandomForest": RandomForestRegressor(),
        "SVM": SVR(),
        "LinearRegression": LinearRegression()
    }

    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model

    joblib.dump(trained_models, "models.pkl")
    return trained_models
