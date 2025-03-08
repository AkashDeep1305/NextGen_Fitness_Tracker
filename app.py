import streamlit as st
import pandas as pd
import os
import joblib
import uuid
from datetime import datetime
from train_model import train_models, initialize_csv
from bmi import calculate_bmi

# Initialize CSV files
initialize_csv()


# Load models if available or train if missing
model_file = "models.pkl"
if os.path.exists(model_file) and os.path.getsize(model_file) > 0:
    models = joblib.load(model_file)
else:
    models = train_models()
    if models:
        joblib.dump(models, model_file)

# Function to calculate calories burned
def calculate_calories(age, weight, heart_rate, duration, gender, method, exercise):
    if method == "Heart Rate-Based":
        if gender.lower() == "male":
            calories_per_min = (age * 0.2017 + weight * 0.09036 + heart_rate * 0.6309 - 55.0969) / 4.184
        else:
            calories_per_min = (age * 0.074 + weight * 0.05741 + heart_rate * 0.4472 - 20.4022) / 4.184
        return round(calories_per_min * duration, 2)
    
    else:  # MET-Based Calculation
        MET_VALUES = {"Cycling": 6.0, "Running": 10.0, "Walking": 3.8, "Jump Rope": 10.0}
        met = MET_VALUES.get(exercise, 6.0)
        return round(met * weight * (duration / 60), 2)

# Main Window Title
st.title("🏋️ Personal Fitness Tracker")

# About Section
st.markdown("""
### About This App
This WEBapp helps you track your fitness progress by estimating calories burned during exercise. 
Enter your details in the sidebar and click **Predict** to see your results!
""")

# Sidebar for User Inputs
st.sidebar.header("🔹 Enter Your Details")

userid = str(uuid.uuid4())[:8]  # Generate a unique user ID
st.sidebar.write(f"**Your Unique User ID:** {userid}")

gender = st.sidebar.radio("Gender", ["Male", "Female"])
age = st.sidebar.number_input("Age", min_value=10, max_value=150, value=25)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
duration = st.sidebar.number_input("Exercise Duration (minutes)", min_value=5, max_value=120, value=30)
heart_rate = st.sidebar.number_input("Heart Rate (bpm)", min_value=50, max_value=200, value=120)
body_temp = st.sidebar.number_input("Body Temperature (°C)", min_value=35.0, max_value=40.0, value=37.0)
exercise = st.sidebar.selectbox("Exercise Type", ["Cycling", "Running", "Walking", "Jump Rope"])

# Info about Calculation Methods
method_info = {
    "Heart Rate-Based": "This method estimates calories burned based on age, weight, heart rate, and duration.",
    "MET-Based": "This method uses MET (Metabolic Equivalent of Task) values for different exercises to estimate calories burned."
}

# Method Selection with Info Icon
col1, col2 = st.sidebar.columns([4, 1])

if "show_method_info" not in st.session_state:
    st.session_state.show_method_info = False

with col1:
    method = st.selectbox("Choose Calculation Method", ["Heart Rate-Based", "MET-Based"])

with col2:
    if st.button("ℹ️", key="info_button"):
        st.session_state.show_method_info = not st.session_state.show_method_info

    if st.session_state.show_method_info:
        with st.sidebar.expander("Method Information"):
            st.write(method_info[method])

# Predict Button
if "save_disabled" not in st.session_state:
    st.session_state.save_disabled = True 

if "calories_burned" not in st.session_state:
    st.session_state.calories_burned = None

if "bmi" not in st.session_state:
    st.session_state.bmi = None

if st.sidebar.button("Predict"):
    st.session_state.calories_burned = calculate_calories(age, weight, heart_rate, duration, gender, method, exercise)

    st.session_state.save_disabled = False

    st.session_state.bmi = calculate_bmi(weight, height)

    # Save to exercise.csv (excluding calculation method)
    exercise_data = pd.DataFrame([{
        "userid": userid,
        "gender": gender,
        "age": age,
        "height": height,
        "weight": weight,
        "duration": duration,
        "heart_rate": heart_rate,
        "body_temp": body_temp,
        "exercise": exercise
    }])
    exercise_data.to_csv("exercise.csv", mode='a', header=not os.path.exists("exercise.csv"), index=False)

    # Save to calories.csv
    calories_data = pd.DataFrame([{"userid": userid, "calories": st.session_state.calories_burned}])
    calories_data.to_csv("calories.csv", mode='a', header=not os.path.exists("calories.csv"), index=False)

    # Display user input on main window
    st.subheader("📝 User Inputs")
    user_data = {
        "User ID": userid,
        "Gender": gender,
        "Age": str(age),  
        "Height (cm)": str(height),
        "Weight (kg)": str(weight),
        "Duration (minutes)": str(duration),
        "Heart Rate (bpm)": str(heart_rate),
        "Body Temperature (°C)": str(body_temp),
        "Exercise Type": exercise,
        "Calculation Method": method,
    }
    df_user_data = pd.DataFrame(user_data.items(), columns=["Parameter", "Value"])
    df_user_data["Value"] = df_user_data["Value"].astype(str)  # Ensure all values are strings
    st.table(df_user_data)

    # Display Predicted Calories Burned
    st.markdown(f"<h4 style='margin-left: 1rem;'>🔥 Estimated Calories Burned: <span style='color: green;'>{st.session_state.calories_burned:.2f}</span> kcal</h2>", unsafe_allow_html=True)

    # Display BMI with color highlighting
    if st.session_state.bmi < 18.5 or st.session_state.bmi > 24.9:
        bmi_color = "red"  # Unhealthy BMI
    else:
        bmi_color = "#87A96B"  # Healthy BMI

    st.markdown(f"<h4 style='margin-left: 1rem;'>⚖️ BMI: <span style='color: {bmi_color};'>{st.session_state.bmi:.2f}</span></h4>", unsafe_allow_html=True)


# Save Entry Button
if st.button("Save Entry", disabled=st.session_state.save_disabled):

    if st.session_state.calories_burned is not None and st.session_state.bmi is not None:

        # Save to exercise.csv (excluding calculation method)
        history_data = pd.DataFrame([{
            "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Userid": userid,
            "Gender": gender,
            "Age": age,
            "Height (cm)": height,
            "Weight (Kg)": weight,
            "BMI": st.session_state.bmi,
            "Duration (min)": duration,
            "Heart Rate (bpm)": heart_rate,
            "Body Temperature (°C)": body_temp,
            "Exercise": exercise,
            "Calories (kcal)": st.session_state.calories_burned,
            "Method": method
        }])
        history_data.to_csv("history.csv", mode='a', header=not os.path.exists("history.csv"), index=False)


    # Train models only if there is sufficient data
    models = train_models()
    if models:
        joblib.dump(models, model_file)

st.session_state.save_disabled = True


# Display Previous Entries
st.subheader("📊 Previous Entries")
history_file = "history.csv"

if os.path.exists(history_file) and os.path.getsize(history_file) > 0:
    history_data = pd.read_csv(history_file)
    # print("History Data Loaded:\n", history_data.head())

    if not history_data.empty:
        # Convert numeric values to string before displaying
        for col in ["DateTime", "Userid", "Gender", "Age", "Height (cm)", "Weight (Kg)", "BMI", "Duration (min)", "Heart Rate (bpm)", "Body Temperature (°C)", "Exercise", "Calories (kcal)", "Method"]:
            history_data[col] = history_data[col].astype(str)
            
        st.dataframe(history_data)
    else:
        st.warning("⚠️ No previous entries found.")
else:
    st.warning("⚠️ History file not found. Entries will be recorded once you save your first entry.")
