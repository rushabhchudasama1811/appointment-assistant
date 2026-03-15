#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import sqlite3
import json
import uuid



# In[ ]:


# constants
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4.1-mini"
openai = OpenAI()
DB = "prices.db"


# In[ ]:


message = "Hello, GPT! This is my first ever message to you! Hi!"

messages = [{"role": "user", "content": message}]

messages


# In[ ]:


openai = OpenAI()

response = openai.chat.completions.create(model="gpt-5-nano", messages=messages)
response.choices[0].message.content


# In[ ]:


system_message = (f"you are a helpfull assistant to a doctors clinic named as Sanjeevni, your job is to provide an appointment to the patients, doctor consult patient in a span of 30 min so appointment will also aligned with that time span and doctor only comes to visit this clinic on Monday, Wednesday and Friday between 2:30PM to 6:30PM and doctor takes 1 hour of break in between the appointment usually 4:30PM to 5:30PM, Give short, courteous answers, no more than 1 sentence. Always be accurate. If you don't know the answer, say so. \
    always green patients with atmost politeness and for that always ask the patient name first")


# In[ ]:


messages = [{"role": "system", "content": system_message}]
messages


# In[ ]:


def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


# In[ ]:


gr.ChatInterface(fn=chat, type="messages").launch()


# In[ ]:


timeslots = """CREATE TABLE IF NOT EXISTS timeslots (
    timeslot_id int AUTO_INCREMENT PRIMARY KEY,
    timeslot varchar(255) NOT NULL,
    doctor_id int,
    CONSTRAINT fk_doctor
    FOREIGN KEY (doctor_id)
    REFERENCES doctors(doctor_id)
)"""

appointments = """
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id int AUTO_INCREMENT PRIMARY KEY,
    patient_name varchar(255) NOT NULL,
    patient_contact varchar(255) NOT NULL,
    patient_issue varchar(255) NOT NULL,
    doctor_name varchar(255) NOT NULL,
    doctor_id int,
    appointment_time varchar(255) NOT NULL,
    CONSTRAINT fk_doctor
    FOREIGN KEY (doctor_id)
    REFERENCES doctors(doctor_id)
)
"""

doctors = """
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id int AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL,
    speciality varchar(255) NOT NULL
)
"""


# In[ ]:


DB = "clinic.db"

with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    cursor.execute(doctors)
    cursor.execute(timeslots)
    cursor.execute(appointments)
    conn.commit()


# In[ ]:


def getDoctors():
    print(f"DATABASE TOOL CALLED: Getting Doctors Details", flush=True)
    empty_dict = {}
    arrayasd = []
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM doctors')
        result = cursor.fetchall()
        for row in result:
            dict_new = {'id': str(row[0]), 'name': row[1], 'speciality': row[2]}
            empty_dict[str(row[0])] = dict_new
            arrayasd = arrayasd + [dict_new]
        return json.dumps(arrayasd)

def checkDoctorTimeslots(id):
    empty_dict = {}
    arrayasd = []
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM timeslots WHERE doctor_id = ?', (id,))
        result = cursor.fetchone()
        return f"Doctor Timeslots: {result[1]}"

def checkDoctorAppointments(id):
    empty_dict = {}
    arrayasd = []
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE doctor_id = ?', (id,))
        result = cursor.fetchall()
        for row in result:
            dict_new = {'id': str(row[0]), 'doctorId': row[5], 'doctorName': row[4], 'appointmentTime': row[6]}
            empty_dict[str(row[0])] = dict_new
            arrayasd = arrayasd + [dict_new]
        return json.dumps(arrayasd)

def setDoctorAppointments(patient_name, patient_contact, patient_issue, doctor_name, doctor_id, appointment_time):
    appointment_id = str(uuid.uuid4())
    sql = """INSERT INTO appointments(appointment_id, patient_name, patient_contact, patient_issue, doctor_name, doctor_id, appointment_time)
             VALUES(?,?,?,?,?,?,?)"""
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (appointment_id, patient_name, patient_contact, patient_issue, doctor_name, doctor_id, appointment_time,))
        conn.commit()
        return f"Your Appointment has been confirmed successfully, Please be on time"


# In[ ]:


getDoctors()


# In[ ]:


checkDoctorTimeslots('3')


# In[ ]:


checkDoctorAppointments(1)


# In[ ]:


setDoctorAppointments(
    'tes2',
    '8811881188',
    'fracture',
    'Rushabh',
    '1',
    '3:30PM to 4:00PM'
)


# In[ ]:


doctors_function = {
    "name": "getDoctors",
    "description": "Get All Doctors Details Visiting in Clinic",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
}

check_doctor_timeslots_function = {
    "name": "checkDoctorTimeslots",
    "description": "Checks Doctors available TimeSlots",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The DoctorId who will consult patient",
            },
        },
        "required": ['id'],
        "additionalProperties": False
    }
}

checkDoctorAppointments_function = {
    "name": "checkDoctorAppointments",
    "description": "checks the doctors previously booked appointments",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The DoctorId who will consult patient",
            },
        },
        "required": ['id'],
        "additionalProperties": False
    }
}

setDoctorAppointments_function = {
    "name": "setDoctorAppointments",
    "description": "sets Doctors appointments at clinic",
    "parameters": {
        "type": "object",
        "properties": {
            "patient_name": {
                "type": "string",
                "description": "Name of the patient",
            },
            "patient_contact": {
                "type": "string",
                "description": "Contact details (Phone Number) of the patient",
            },
            "patient_issue": {
                "type": "string",
                "description": "patient illness ",
            },
            "doctor_name": {
                "type": "string",
                "description": "Doctor who will going to consult the patient",
            },
            "doctor_id": {
                "type": "string",
                "description": "The DoctorId who will consult patient",
            },
            "appointment_time": {
                "type": "string",
                "description": "Appointment time of the consultation in 30 min period. for Example 2:30PM to 3:00PM",
            },
        },
        "required": ['patient_name', 'patient_contact', 'patient_issue', 'doctor_name', 'doctor_id', 'appointment_time'],
        "additionalProperties": False
    }
}
tools = [
    {"type": "function", "function": doctors_function},
    {"type": "function", "function": check_doctor_timeslots_function},
    {"type": "function", "function": checkDoctorAppointments_function},
    {"type": "function", "function": setDoctorAppointments_function},
]


# In[ ]:


tools


# In[ ]:


system_message = (f"you are a helpfull and clever assistant to a doctors clinic named as Sanjeevni, \
your job is to provide an appointment to the patients, doctor consult patient in a span of 30 min so appointment will also aligned with that time span, \
you can use the tools to get the doctors currently visiting clinic and their timeslots, also check the previous appointments of that doctor so that you don't book the different appointment at the same time\
    doctor timeslot and its appointment at clinic will be grabbed with the ID of the doctor which you get with getdoctors tool call so for timeslot and appointments input parameter will be the id, use that to get the details \
, Give short, courteous answers, no more than 1 sentence. Always be accurate. If you don't know the answer, say so. \
    always first greet patients with atmost politeness and 2nd ask the patient name and 3rd ask what problem the patient is facing and then recommend doctor")


# In[ ]:


def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "getDoctors":
            allDoctorDetails = getDoctors()
            responses.append({
                "role": "tool",
                "content": allDoctorDetails,
                "tool_call_id": tool_call.id
            })
        if tool_call.function.name == "checkDoctorTimeslots":
            allDoctorDetails = getDoctors()
            arguments = json.loads(tool_call.function.arguments)
            id = arguments.get('id')
            details = checkDoctorTimeslots(id)
            responses.append({
                "role": "tool",
                "content": details,
                "tool_call_id": tool_call.id
            })
        if tool_call.function.name == "checkDoctorAppointments":
            arguments = json.loads(tool_call.function.arguments)
            id = arguments.get('id')
            details = checkDoctorAppointments(id)
            responses.append({
                "role": "tool",
                "content": details,
                "tool_call_id": tool_call.id
            })
        if tool_call.function.name == "setDoctorAppointments":
            arguments = json.loads(tool_call.function.arguments)
            patient_name = arguments.get('patient_name')
            patient_contact = arguments.get('patient_contact')
            patient_issue = arguments.get('patient_issue')
            doctor_name = arguments.get('doctor_name')
            doctor_id = arguments.get('doctor_id')
            appointment_time = arguments.get('appointment_time')
            details = setDoctorAppointments(patient_name, patient_contact, patient_issue, doctor_name, doctor_id, appointment_time)
            responses.append({
                "role": "tool",
                "content": details,
                "tool_call_id": tool_call.id
            })
    return responses

def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    while response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        responses = handle_tool_calls(message)
        messages.append(message)
        messages.extend(responses)
        response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    return response.choices[0].message.content


# In[ ]:


gr.ChatInterface(fn=chat, type="messages").launch(show_error=True, inbrowser=True)
