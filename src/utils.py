import json
from swarm import Swarm

def run_demo_loop(
    swarm_client: Swarm,
    starting_agent,
    context_variables=None,    
    debug=False,    
) -> None:
    client = swarm_client
    print("Starting conversation with the Virtual Medical Center...")
    print("You can type 'exit' at any time to end the conversation.")
    print("Please share your symptoms and concerns with the Virtual Medical Assistant.")

    messages = []
    agent = starting_agent

    while True:
        user_input = input("\033[90mUser\033[0m: ")
        
        if user_input.lower() == "exit":
            print("Ending conversation.")
            break
        
        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=False,
            debug=debug,
        )
        pretty_print_messages(response.messages)
        messages.extend(response.messages)                      
        agent = response.agent


def pretty_print_messages(messages) -> None:
    for message in messages:
        if message["role"] != "assistant":
            continue
       
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")
       
        # print response, if any
        if message["content"]:
            print(message["content"])

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")

def print_patient_info(patient_data):
    """
    Pretty prints patient information in a formatted way.
    
    Args:
        patient_data (dict): Dictionary containing patient information
    """
    # Header
    print("=" * 50)
    print(f"Patient Record: {patient_data['first_name']} {patient_data['last_name']}")
    print("=" * 50)
    
    # Basic Information
    print("\nBasic Information:")
    print("-" * 20)
    fields = ['patient_id', 'status', 'birth_date', 'age']
    for field in fields:
        print(f"{field.replace('_', ' ').title()}: {patient_data[field]}")
    
    # Medical History
    print("\nMedical History:")
    print("-" * 20)
    
    # Allergies
    print("\nAllergies:")
    if patient_data['history']['allergies'] == ['none']:
        print("  • No known allergies")
    else:
        for allergy in patient_data['history']['allergies']:
            print(f"  • {allergy}")
    
    # Medications
    print("\nMedications:")
    if patient_data['history']['medications'] == ['none']:
        print("  • No current medications")
    else:
        medications = patient_data['history']['medications'][0].split(', ') if isinstance(patient_data['history']['medications'][0], str) else patient_data['history']['medications']
        for medication in medications:
            print(f"  • {medication}")
    
    print("\n" + "=" * 50)