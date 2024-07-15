from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
import random

# Initialize the Faker generator
fake = Faker()

# Define the number of records
num_records = 20000
unique_patient_ids = 17000
repeat_patient_ids = 3000

# Generate unique patient IDs
patient_ids = [fake.unique.random_int(min=1, max=50000) for _ in range(unique_patient_ids)]

# Select 3000 IDs to be repeated
repeated_ids = random.choices(patient_ids, k=repeat_patient_ids)

# Combine the unique and repeated IDs
all_patient_ids = patient_ids + repeated_ids

# Shuffle the list to distribute the repeated IDs randomly
random.shuffle(all_patient_ids)

# Dictionary to store patient details
patient_details = {}

# Define realistic age, gender and blood group distributions
age_distribution = [("0-10", 0.05), ("10-20", 0.10), ("20-30", 0.15), ("30-40", 0.20), ("40-50", 0.25), ("50 Above", 0.25)]
gender_distribution = [("Male", 0.52), ("Female", 0.48)]
blood_group_distribution = [("O+", 0.37), ("A+", 0.34), ("B+", 0.10), ("AB+", 0.04), ("O-", 0.07), ("A-", 0.06), ("B-", 0.02), ("AB-", 0.01)]

treatment_plan_feedback_distribution = [("Don't Know",0.003),("Fully Agree",0.85),("Fully Disagree",0.002),("Somewhat Agree",0.14),("Somewhat Disagree",0.005)]
confidence_feedback_distribution = [("Don't Know",0.05),("Fully Agree",0.80),("Fully Disagree",0.02),("Somewhat Agree",0.10),("Somewhat Disagree",0.03)]

# Define realistic height and weight ranges
height_ranges = {
    "0-10": {"Male": (0.9, 1.4), "Female": (0.9, 1.4)},
    "10-20": {"Male": (1.4, 1.8), "Female": (1.4, 1.7)},
    "20-30": {"Male": (1.6, 1.9), "Female": (1.5, 1.7)},
    "30-40": {"Male": (1.6, 1.9), "Female": (1.5, 1.7)},
    "40-50": {"Male": (1.6, 1.9), "Female": (1.5, 1.7)},
    "50 Above": {"Male": (1.5, 1.8), "Female": (1.4, 1.7)}
}

# Define realistic weight ranges
weight_ranges = {
    "0-10": {"Male": (14, 40), "Female": (13, 39)},
    "10-20": {"Male": (40, 70), "Female": (38, 65)},
    "20-30": {"Male": (60, 90), "Female": (50, 80)},
    "30-40": {"Male": (70, 100), "Female": (55, 85)},
    "40-50": {"Male": (75, 110), "Female": (60, 90)},
    "50 Above": {"Male": (70, 120), "Female": (55, 100)}
}

# Define BMI weight status categories
bmi_weight_status = {
    "Underweight": {"min": 0, "max": 18.5},
    "Normal": {"min": 18.5, "max": 24.9},
    "Overweight": {"min": 25, "max": 29.9},
    "Obese": {"min": 30, "max": float('inf')}
}

# Define mental health status distribution
mental_health_status_distribution = [
    ("No Issues", 0.35),  
    ("Fair", 0.10), 
    ("Anxiety", 0.25), 
    ("Depression", 0.30)
]

# Define hydration status distribution
hydration_status_distribution = [("Hydrated", 0.65), ("Dehydrated", 0.35)]

immunization_status = ["upto date", "incomplete"]
immunization_weights = [0.764, 0.236]

allergy_status = ["None", "Pollen", "Dust", "Food", "Pet Dander", "Insect Stings", "Latex", "Mold", "Eggs", "Milk", "Peanut", "Nuts", "Dairy"]
allergy_weights = [0.70, 0.10, 0.08, 0.06, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

# Define waiting time distribution
waiting_time_distribution = [(10, 30, 0.50), (31, 60, 0.30), (61, 90, 0.15), (91, 120, 0.05)]

# Define consulting time distribution
consulting_time_distribution = [(10, 20, 0.50), (21, 30, 0.30), (31, 45, 0.15), (46, 60, 0.05)]

# Function to select a random integer from a given range based on defined probabilities
def select_random_value(distribution):
    ranges = [range(low, high + 1) for low, high, _ in distribution]
    weights = [weight for _, _, weight in distribution]
    selected_range = random.choices(ranges, weights=weights, k=1)[0]
    return random.choice(selected_range)

# Generate patient details for unique patient IDs
for pid in patient_ids:
    age_group = random.choices([age for age, _ in age_distribution], weights=[weight for _, weight in age_distribution], k=1)[0]
    gender = random.choices([gender for gender, _ in gender_distribution], weights=[weight for _, weight in gender_distribution], k=1)[0]
    blood_group = random.choices([bg for bg, _ in blood_group_distribution], weights=[weight for _, weight in blood_group_distribution], k=1)[0]
    weight = random.randint(*weight_ranges[age_group][gender])
    height = round(random.uniform(*height_ranges[age_group][gender]),2)
    immunization = random.choices(immunization_status, weights=immunization_weights, k=1)[0]
    allergy = random.choices(allergy_status, weights=allergy_weights, k=1)[0]

    # Calculate BMI
    bmi = round(weight / (height ** 2),2)

    # Determine BMI weight status
    for status, ranges in bmi_weight_status.items():
        if ranges["min"] <= bmi < ranges["max"]:
            bmi_status = status
            break
    
    mental_health_status = random.choices(
        [status for status, _ in mental_health_status_distribution], 
        weights=[weight for _, weight in mental_health_status_distribution], 
        k=1
    )[0]

     # Assign hydration status
    hydration_status = random.choices(
        [status for status, _ in hydration_status_distribution], 
        weights=[weight for _, weight in hydration_status_distribution], 
        k=1
    )[0]

    patient_details[pid] = {
        "Name": fake.name(),
        "Gender": gender,
        "Age Group": age_group,
        "Blood Group": blood_group,
        "Weight": weight,
        "Height": height,
        "BMI": bmi,
        "BMI Weight Status": bmi_status,
        "Mental Health Status": mental_health_status,
        "Hydration Status": hydration_status,
        "Immunization Status": immunization,
        "Allergy Status" : allergy
    }

# Generate the data
data = []

start_date = datetime(2023, 6, 1)
end_date = datetime(2024, 6, 30)

states = ["Maharashtra", "Tamil Nadu", "Uttar Pradesh", "Karnataka", "West Bengal"]
maha_hospitals = ["Hospital_1", "Hospital_2", "Hospital_3"]
up_hospotals = ["Hospital_4", "Hospital_5", "Hospital_6"]
tn_hospitals = ["Hospital_7", "Hospital_8"]
karnataka_hospitals = ["Hospital_9", "Hospital_10"]
wb_hospitals = ["Hospital_11"]

hospitals_by_state = {
    "Maharashtra": maha_hospitals,
    "Uttar Pradesh": up_hospotals,
    "Tamil Nadu": tn_hospitals,
    "Karnataka": karnataka_hospitals,
    "West Bengal": wb_hospitals
}

total_beds_by_hospital = {
    "Hospital_1": 560, "Hospital_2": 670, "Hospital_3": 693,
    "Hospital_4": 720, "Hospital_5": 699, "Hospital_6": 800,
    "Hospital_7": 730, "Hospital_8": 780   ,
    "Hospital_9": 800, "Hospital_10": 730,
    "Hospital_11": 976
}

specializations = ["Cardiologist", "Dermatologist", "Neurologist", "Ophthalmology",
                   "Orthopaedics", "Pediatrician", "Psychiatrist", "Urologist",
                   "Dentist", "Radiologist", "Pulmonologist", "Endocrinologist",
                   "Gastroenterologist", "Hematologist", "Infectious Disease Specialist",
                   "Neonatologist", "Nephrologist", "Oncologist", "Otolaryngologist (ENT)",
                   "Pathologist", "Rheumatologist"]

appointment_status = ["Confirmed", "Pending", "Postponed", "Cancelled", "Completed"]
appointment_status_weights = [0.20, 0.4, 0.15, 0.1, 0.15]  # Example weights

# Assign a state to each doctor
doctors = []
for _ in range(60):
    doctor_id = fake.unique.random_int(min=1000, max=9999)
    doctor_name = fake.unique.name()
    state = random.choice(states)
    doctors.append((doctor_id, doctor_name, state))

# Dictionary to track the number of specializations assigned to each doctor
doctor_specialization_count = {doctor_id: [] for doctor_id, doctor_name, state in doctors}

# Ensure 11,000 patients have a length of stay of 1
length_of_stay_values = [1] * 11000

# Generate weighted values for the remaining length of stays (2-15)
weights = [0.3, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02, 0.02, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005]
length_of_stay_values += random.choices(range(2, 16), weights=weights, k=9000)

# Shuffle the list to distribute the lengths of stay randomly
random.shuffle(length_of_stay_values)

# EXECUTIVE 
operation_cost_distribution = [(500, 2000, 0.5), (2000, 4000, 0.3), (4000, 5000, 0.15), (5000, 200000, 0.05)]
incurred_cost_distribution = [(200, 1000, 0.5), (1001, 3000, 0.3), (3000, 4500, 0.15), (4501, 10000, 0.05)]
complication_rate_distribution = [(1, 5, 0.8), (6, 10, 0.18), (11, 15, 0.013), (16, 20, 0.007)]
compliance_rate_distribution = [(80, 85, 0.2), (86, 90, 0.4), (91, 95, 0.2), (96, 100, 0.2)]
emergency_visits_distribution = [("No",0.7),("Yes",0.3)]
readmitted_distribution = [("No",0.8),("Yes",0.2)]
utilisation_distribution = [(80, 85, 0.005), (86, 90, 0.395), (91, 95, 0.15), (96, 99, 0.45)]
pain_score_distribution = [(1, 3, 0.6), (3, 5, 0.2), (5, 7, 0.17), (8, 10, 0.03)]
death_distribution = [("No",0.933),("Yes",0.067)]
claim_distribution = [("Yes",0.75),("No",0.25)]
appointment_type_distribution = [("Emergency", 0.15), ("Walk-in", 0.35),("Appointment",0.5)]

for i in range(num_records):
    appointment = fake.date_between_dates(date_start=start_date, date_end=end_date)
    admission = appointment + timedelta(days=random.randint(0, 3))

    doctor_id, doctor_name, state_name = random.choice(doctors)

    if len(doctor_specialization_count[doctor_id]) < 2:
        specialization_choice = random.choice(specializations)
        if specialization_choice not in doctor_specialization_count[doctor_id]:
            doctor_specialization_count[doctor_id].append(specialization_choice)
    else:
        specialization_choice = random.choice(doctor_specialization_count[doctor_id])

    hospital_name = random.choice(hospitals_by_state[state_name])
    total_beds = total_beds_by_hospital[hospital_name]

    length_of_stay = length_of_stay_values[i]   
    # Adjust outpatient and inpatient based on length of stay
    if length_of_stay == 1:
        outpatients = 1
        inpatients = 0
    else:
        outpatients = 0
        inpatients = 1

    appointment_status_choice = random.choices(appointment_status, weights=appointment_status_weights, k=1)[0]

    treatment_plan_feedback = random.choices(
        [status for status, _ in treatment_plan_feedback_distribution], 
        weights=[weight for _, weight in treatment_plan_feedback_distribution], 
        k=1
    )[0]

    confidence_feedback = random.choices(
        [status for status, _ in confidence_feedback_distribution], 
        weights=[weight for _, weight in confidence_feedback_distribution], 
        k=1
    )[0]

     # Calculate Customer Feedback based on Confidence Feedback and Treatment Plan Feedback
    def determine_customer_feedback(confidence, treatment):
        if (confidence in ["Fully Agree", "Somewhat Agree"] and treatment in ["Fully Agree", "Somewhat Agree"]):
            return "Positive"
        elif (confidence == "Don't Know" or treatment == "Don't Know"):
            return "Neutral"
        elif (confidence in ["Fully Disagree", "Somewhat Disagree"] or treatment in ["Fully Disagree", "Somewhat Disagree"]):
            return "Negative"
        else:
            return "Neutral"

    customer_feedback = determine_customer_feedback(confidence_feedback, treatment_plan_feedback)

    patient_id = all_patient_ids[i]
    patient_detail = patient_details[patient_id]

    # Assign waiting time and consulting time
    waiting_time = select_random_value(waiting_time_distribution)
    consulting_time = select_random_value(consulting_time_distribution)

    #EXECUTIVE
    cost_of_operation = select_random_value(operation_cost_distribution)
    cost_incurred_for_operation = select_random_value(incurred_cost_distribution)
    profit_from_operation = cost_of_operation - cost_incurred_for_operation
    complication_rate = select_random_value(complication_rate_distribution)
    compliance_rate = select_random_value(compliance_rate_distribution)
    emergency_visits = random.choices(
        [status for status, _ in emergency_visits_distribution], 
        weights=[weight for _, weight in emergency_visits_distribution], 
        k=1
    )[0]
    operating_margin = (profit_from_operation / cost_of_operation) * 100  # Operating margin as a percentage
    readmitted = random.choices(
        [status for status, _ in readmitted_distribution], 
        weights=[weight for _, weight in readmitted_distribution], 
        k=1
    )[0]
    utilisation_rate = select_random_value(utilisation_distribution)
    pain_score = select_random_value(pain_score_distribution)
    death = random.choices(
        [status for status, _ in death_distribution], 
        weights=[weight for _, weight in death_distribution], 
        k=1
    )[0]
    claim_status = random.choices(
        [status for status, _ in claim_distribution], 
        weights=[weight for _, weight in claim_distribution], 
        k=1
    )[0]
    appointment_type = random.choices(
        [status for status, _ in appointment_type_distribution], 
        weights=[weight for _, weight in appointment_type_distribution], 
        k=1
    )[0]

    record = {
        "Patient_Id": patient_id,
        "Name": patient_detail["Name"],
        "Gender": patient_detail["Gender"],
        "Age Group": patient_detail["Age Group"],
        "Blood Group": patient_detail["Blood Group"],
        "Weight (in kg)": patient_detail["Weight"],
        "Height (in m)": patient_detail["Height"],
        "Body Mass Index (BMI)": patient_detail["BMI"],
        "BMI Weight Status" : patient_detail["BMI Weight Status"],
        "Mental Health Status" : patient_detail["Mental Health Status"],
        "Hydration Status" : patient_detail["Hydration Status"],
        "Immunization Status" : patient_detail["Immunization Status"],
        "Allergy Status" : patient_detail["Allergy Status"],
        "Appointment_Date": appointment,
        "Appointment Type" : appointment_type,
        "Cost": fake.random_int(min=500, max=5000),
        "Admission_Date": admission,
        "Appointment_Status": appointment_status_choice,
        "Doctor_Id": doctor_id,
        "Doctor_Name": doctor_name,
        "Specialization": specialization_choice,
        "State": state_name,
        "Hospital_Name": hospital_name,
        "Total Beds": total_beds,
        "Length of Stay": length_of_stay,
        "Outpatients": outpatients,
        "Inpatients": inpatients,
        "Treatment Plan Feedback" : treatment_plan_feedback,
        "Confidence Feedback" : confidence_feedback,
        "Customer Feedback": customer_feedback,
        "Waiting Time (minutes)": waiting_time,
        "Consulting Time (minutes)": consulting_time,
        "Cost of Operation": cost_of_operation,
        "Cost Incurred": cost_incurred_for_operation,
        "Profit": profit_from_operation,
        "Operating Margin": operating_margin,
        "Complication Rate (in %)": complication_rate,
        "Compliance Rate (in %)": compliance_rate,
        "Emergency Visits": emergency_visits,
        "Readmitted?" : readmitted,
        "Operating Room Utilisation (in %)": utilisation_rate,
        "Pain Management Score": pain_score,
        "Patient Died?" : death,
        "Claimed Status": claim_status
    }
    data.append(record)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('Hospital Management Database_Updated.csv', index=False)

print("Dataset generated and saved to 'Hospital Management Database_Updated.csv'")