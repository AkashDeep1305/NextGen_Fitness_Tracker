def calculate_bmi(weight, height):
    """Calculates BMI using the formula: BMI = weight (kg) / (height (m) ^ 2)"""
    height_m = height / 100  # Convert height from cm to meters
    bmi = round(weight / (height_m ** 2), 2)
    return bmi
