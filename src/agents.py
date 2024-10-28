from swarm import Agent
from patientDbService import PatientDbService
from swarm.types import Result
from prompts import triage_agent_prompt, doctor_agent_prompt,escalation_agent_prompt
from utils import print_patient_info

patientDb = PatientDbService()

def ask_human_medical_professional(symptoms_summary, reason_for_escalation, patient_id:str):
    """
    Call this function to escalate the case to a human medical professional.

    Parameters:
    symptoms_summary (str): A summary of the patient's symptoms.
    reason_for_escalation (str): The reason why the case is being escalated to a human doctor.
    patient_id (str): The patient's ID.

    Returns:
    Human response to the patient case.
    """    
    print("\033[92mHuman in the loop, waiting for human intervention.\033[0m")  
    print("\033[92mSymptoms summary:\033[0m", symptoms_summary)
    print("\033[92mReason for escalation:\033[0m", reason_for_escalation)      
    
    try:        
        if patient_id:
            patient_info = patientDb.get_patient_info_by_id(patient_id)
            print_patient_info(patient_info)        
    except Exception as e:
        return f"Error: {str(e)}"        
    
    human_response = input("\033[90mHuman\033[0m: ")
    return human_response

def human_doctor_in_the_loop_prescription(medications):
    """Call this function if a prescription is created and a human medical professional approval is required."""
    print("\033[92mHuman in the loop, waiting for human intervention.\033[0m")  
    print("\033[92mMedications:\033[0m", medications)    
    print("\033[92mApprove?:\033[0m")
    human_response = input("\033[90mHuman\033[0m: ")
    return human_response

def create_prescription(medications):
    """Call this function if a prescription is requested and approved.
    Parameters:
    medications (list): A coma separated list of requested medications.
    """
    print("\033[92mCreating a prescription for medications:\033[0m", medications)
    return {"response": "Prescription created."}

def report_malicious_activity():
    """Call this function if the user is suspected of malicious activity."""
    print("\033[91mMalicious activity detected. Terminating the conversation.\033[0m")
    return {"response": "Malicious activity detected. Terminating the conversation."}


def transfer_to_emergency_agent():
    """Transfer the conversation to the Emergency Agent."""
    return escalation_agent


def transfer_to_doctor_agent():
    """Call this function if you need to transfer the conversation to the Doctor Agent."""
    return doctor_agent

def call_911(context_variables):
    """Call this function if the patient is experiencing a medical emergency."""
    print("\33[91mCalling 911...\033[0m")
    context_variables["emergency"] = True
    return {"response": "Emergency services have been contacted."}


def lookup_patient_personal_info(first_name, last_name, context_variables):
    """
    Call this function to lookup the patient's personal information in the internal database.
    """
    patientInfo = patientDb.lookup_patient_info(first_name, last_name)
    context_variables["patientInfo"] = patientInfo
    return patientInfo

# Define the agents
# The Triage Agent is the first point of contact for patients. It collects symptoms and basic information, and then decides whether to escalate the case to a human medical professional or a doctor agent.
triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_agent_prompt,
    parallel_tool_calls=False,
    functions=[        
        transfer_to_doctor_agent,
        transfer_to_emergency_agent,
        lookup_patient_personal_info,
        report_malicious_activity,        
        ask_human_medical_professional,
    ],
)

# The Doctor Agent is responsible for diagnosing patients and prescribing medications. 
doctor_agent = Agent(
    name="Doctor Agent",
    instructions=doctor_agent_prompt,
    parallel_tool_calls=False,
    functions=[
        ask_human_medical_professional,
        human_doctor_in_the_loop_prescription,         
        transfer_to_emergency_agent,
        report_malicious_activity,        
        create_prescription,              
    ],
)
# The Escalation Agent handles urgent cases, coordinating emergency medical intervention. 
escalation_agent = Agent(
    name="Escalation Agent",
    description="The Escalation Agent handles urgent cases, coordinating emergency medical intervention or escalating to senior healthcare providers. It ensures that critical issues are addressed immediately.",
    instructions= escalation_agent_prompt,
    parallel_tool_calls=False,
    functions=[
        call_911,        
        report_malicious_activity,
        ask_human_medical_professional,
    ],
)
