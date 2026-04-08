# Appointment Assistant

Appointment Booking Assistant for a Small Clinic, leveraging OpenAI APIs, Tool Calling, and SQLite3.

## Features
- **Doctor Management**: Retrieve details of doctors visiting the clinic.
- **Timeslot Management**: Check available timeslots for doctors.
- **Appointment Booking**: Book appointments for patients with specific doctors.
- **Appointment History**: View previously booked appointments for doctors.

## Database Structure
The application uses an SQLite database (`clinic.db`) with the following tables:

1. **Doctors**:
   - `doctor_id` (Primary Key): Unique identifier for each doctor.
   - `name`: Name of the doctor.
   - `speciality`: Doctor's area of specialization.

2. **Timeslots**:
   - `timeslot_id` (Primary Key): Unique identifier for each timeslot.
   - `timeslot`: Time period for the slot.
   - `doctor_id` (Foreign Key): Links to the `doctor_id` in the `Doctors` table.

3. **Appointments**:
   - `appointment_id` (Primary Key): Unique identifier for each appointment.
   - `patient_name`: Name of the patient.
   - `patient_contact`: Contact details of the patient.
   - `patient_issue`: Description of the patient's issue.
   - `doctor_name`: Name of the consulting doctor.
   - `doctor_id` (Foreign Key): Links to the `doctor_id` in the `Doctors` table.
   - `appointment_time`: Scheduled time for the appointment.

## Tools and Technologies
- **OpenAI API**: Used for natural language processing and chatbot functionality.
- **Gradio**: Provides an interactive interface for the chatbot.
- **SQLite3**: Lightweight database for managing clinic data.
- **Python**: Core programming language for backend logic.

## Screenshots
Screenshots of the application can be found in the `Screenshots/` directory.
