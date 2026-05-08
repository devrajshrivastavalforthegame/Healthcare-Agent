import numpy as np
import pandas as pd
import random
from faker import Faker

fake = Faker()

symptoms_list = [
    "Fever", "Headache", "Chest Pain", "Cough",
    "Fatigue", "Dizziness", "Skin Rash",
    "Body Pain", "Nausea", "Breathing Difficulty"
]

conditions = [
    "Viral Infection", "Migraine", "Hypertension",
    "Diabetes", "Asthma", "Heart Disease",
    "Allergy", "Skin Infection"
]

specialists = [
    "General Physician", "Cardiologist",
    "Dermatologist", "Neurologist",
    "Orthopedic", "Pulmonologist"
]

emergency_levels = [
    "Low", "Medium", "High", "Critical"
]

recommended_actions = [
    "Home Care",
    "Doctor Consultation",
    "Emergency Visit",
    "Medication Required"
]

data = []

for i in range(2000):

    age = random.randint(1, 90)

    record = {
        "Patient_ID": f"P{i+1}",
        "Age": age,
        "Gender": random.choice(["Male", "Female"]),
        "Symptoms": random.choice(symptoms_list),
        "Possible_Condition": random.choice(conditions),
        "Suggested_Specialist": random.choice(specialists),
        "Emergency_Level": random.choice(emergency_levels),
        "Recommended_Action": random.choice(recommended_actions),
        "Medications": fake.word(),
        "Allergies": fake.word(),
        "Region": fake.city(),
        "Language": random.choice(["English", "Hindi"])
    }

    data.append(record)

df = pd.DataFrame(data)

df.to_csv("healthcare_dataset.csv", index=False)

print(df.head())

print("Dataset Generated Successfully!")