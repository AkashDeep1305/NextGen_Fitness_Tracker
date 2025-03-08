# 🏋️ NextGen Fitness Tracker(Personal Fitness Tracker)

## 📌 About This Project
The **Personal Fitness Tracker** is a **Streamlit web application** that helps users monitor their fitness progress. It estimates **calories burned** during exercise based on user input and also calculates **BMI (Body Mass Index)**.

---

## 📸 Screenshots

![Home Page](assets/home_page.png)

![User Result](assets/user_input.png)

---

## 🚀 Features
- 🔢 **Estimates calories burned** based on Heart rate or MET method.
- 📊 **Tracks previous exercise records** and displays historical data.
- 🔍 **Calculates BMI** and highlights health status.
- 📁 **Stores user exercise data** in CSV files for tracking progress.
- 🏃 **Supports different exercise types** like cycling, running, walking, and jump rope.

---

## 🛠 Installation Guide

### 🔹 Prerequisites
Ensure you have **Python 3.8+** installed. Install the required dependencies before running the app.

### 🔹 Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 Step 2: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501` 🚀

---

## 📌 How to Use
1. Enter your **personal details** (age, weight, height, etc.) in the sidebar.
2. Select an **exercise type** and the **calculation method**.
3. Click the **Predict** button to calculate calories burned and BMI.
4. View results and **save your entry** to track your progress.
5. View your **previous entries** in the history section.

---

## 📁 Project Structure
```
├── assets/                 # Images and UI assets
├── app.py                  # Main Streamlit application
├── bmi.py                  # BMI calculation function
├── train_model.py          # Machine learning model training script
├── requirements.txt        # List of dependencies
├── models.pkl              # Pre-trained models (if available)
├── exercise.csv            # Stored exercise data
├── calories.csv            # Stored calorie data
├── history.csv             # User activity history
└── README.md               # This file
```

---

## 🤖 Technologies Used
- **Python** 🐍
- **Streamlit** 🎨 (For UI)
- **Pandas** 📊 (For data handling)
- **Joblib** 💾 (For model storage)
- **Scikit-learn** 🤖 (For training models)

---

## 📜 License
This project is licensed under the **MIT License**.

---
