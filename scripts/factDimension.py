import pandas as pd

# Load the dataset
df = pd.read_csv('C:\\Users\\Vishva\\Documents\\DOMO\\Project_Database\\Hospital Management Database_Updated.csv')

# Create DimPatient
dim_patient = df[['Patient_Id', 'Name', 'Gender', 'Age Group', 'Blood Group', 'Weight (in kg)', 'Height (in m)', 'Body Mass Index (BMI)', 'BMI Weight Status', 'Mental Health Status', 'Hydration Status', 'Immunization Status', 'Allergy Status']].drop_duplicates().reset_index(drop=True)

# Create DimDoctor
dim_doctor = df[['Doctor_Id', 'Doctor_Name', 'State', 'Specialization']].drop_duplicates().reset_index(drop=True)

# Create DimHospital
dim_hospital = df[['Hospital_Name', 'State', 'Total Beds']].drop_duplicates().reset_index(drop=True)
dim_hospital['Hospital_Id'] = dim_hospital.index + 1  # Adding a Hospital_Id column

# Create DimTime
appointment_dates = df[['Appointment_Date']].drop_duplicates().reset_index(drop=True)
admission_dates = df[['Admission_Date']].drop_duplicates().reset_index(drop=True)
all_dates = pd.concat([appointment_dates, admission_dates]).drop_duplicates().reset_index(drop=True)
all_dates['Time_Id'] = all_dates.index + 1  # Adding a Time_Id column

# Assuming all_dates['Appointment_Date'] is a string column
all_dates['Appointment_Date'] = pd.to_datetime(all_dates['Appointment_Date'], format='%d-%m-%Y')

all_dates['Day'] = all_dates['Appointment_Date'].dt.day
all_dates['Month'] = all_dates['Appointment_Date'].dt.month
all_dates['Year'] = all_dates['Appointment_Date'].dt.year
all_dates['Quarter'] = all_dates['Appointment_Date'].dt.to_period('Q')

# Create FactAppointment
fact_appointment = df[['Patient_Id', 'Doctor_Id', 'Hospital_Name', 'Appointment_Date', 'Admission_Date', 'Appointment_Status', 'Length of Stay', 'Outpatients', 'Inpatients', 'Treatment Plan Feedback', 'Confidence Feedback', 'Customer Feedback', 'Waiting Time (minutes)', 'Consulting Time (minutes)', 'Cost of Operation', 'Cost Incurred', 'Profit', 'Operating Margin', 'Complication Rate (in %)', 'Compliance Rate (in %)', 'Emergency Visits', 'Readmitted?', 'Operating Room Utilisation (in %)', 'Pain Management Score', 'Patient Died?', 'Claimed Status']]

# Map Hospital_Name to Hospital_Id
fact_appointment = fact_appointment.merge(dim_hospital[['Hospital_Id', 'Hospital_Name']], on='Hospital_Name').drop(columns=['Hospital_Name'])

# Assuming fact_appointment['Appointment_Date'] is a string column
fact_appointment['Appointment_Date'] = pd.to_datetime(fact_appointment['Appointment_Date'], format='%d-%m-%Y')

# Assuming Admission_Date is a string column
fact_appointment['Admission_Date'] = pd.to_datetime(fact_appointment['Admission_Date'], format='%d-%m-%Y')

# Merge DataFrames (assuming both have 'Appointment_Date' columns)
fact_appointment = fact_appointment.merge(all_dates[['Time_Id', 'Appointment_Date']], left_on='Appointment_Date', right_on='Appointment_Date').rename(columns={'Time_Id': 'Appointment_Time_Id'}).drop(columns=['Appointment_Date'])
merged_df = fact_appointment.merge(all_dates[['Time_Id', 'Appointment_Date']], left_on='Admission_Date', right_on='Appointment_Date').rename(columns={'Time_Id': 'Appointment_Time_Id'}).drop(columns=['Admission_Date', 'Appointment_Date'])

# Save the tables to CSV files
dim_patient.to_csv('DimPatient.csv', index=False)
dim_doctor.to_csv('DimDoctor.csv', index=False)
dim_hospital.to_csv('DimHospital.csv', index=False)
all_dates.to_csv('DimTime.csv', index=False)
fact_appointment.to_csv('FactAppointment.csv', index=False)
