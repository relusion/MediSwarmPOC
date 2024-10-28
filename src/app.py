from openai import AzureOpenAI
from swarm import Swarm
from dotenv import load_dotenv
import os
from agents import triage_agent
from utils import run_demo_loop

load_dotenv()

# Initialize Azure OpenAI client
az_oai_client = AzureOpenAI(
    api_version=os.getenv("OPENAI_DEPLOYMENT_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
    azure_deployment=os.getenv("OPENAI_DEPLOYMENT"),    
)

client = Swarm(az_oai_client)
run_demo_loop(client, triage_agent)
