from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage

# from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv
import os
import yaml
import logging, json, re

load_dotenv()

serper_api_key = os.getenv("serper_api_key")
gemini_key = os.getenv("gemini_key")


search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    google_api_key=gemini_key,
)


def load_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data

data = load_yaml("prompts.yaml")
PROMPT = data["PROMPT"]
system_prompt = data["system_prompt"]

def clean_json_response(response):
    # Remove markdown-like code fences (``` or ''') and optional json label
    response = re.sub(r"^[`']{3}json\s*|[`']{3}$", "", response.strip(), flags=re.IGNORECASE)

    # Attempt to fix missing quotes on string values (basic case)
    response = re.sub(r'("post"\s*:\s*)([a-zA-Z0-9_]+)', r'\1"\2"', response)

    return response

def news_extraction(topic):
  """Extract news links and snippets about a given topic using Google Serper API."""
  link = []
  text = []
  result = search.results(f"what is the latest news about {topic}")
  for item in result.get("organic", []):
    link.append(item.get("link"))
    text.append(item.get("snippet"))
  return link,text


def get_response(prompt,news):
    """Generate a response using the LLM based on the provided prompt and news."""
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=news),
    ]
    ai_msg = llm.invoke(messages)

    return ai_msg.content


def news2post(topic,prompt):
    """Generate a social media post based on the latest news about a given topic."""
    url ,news = news_extraction(topic)
    post = get_response(prompt,news)

    return post,url


def agent_creation(user_query):
    """Create and invoke an agent to generate a social media post based on user query."""
    agent = create_react_agent(
        model=llm,
        tools=[news2post],
        prompt=system_prompt,
    )
    logging.info("Agent created successfully.")
    response = agent.invoke({"messages": user_query})
    result = response["messages"][-1].content
    print("Agent response:", result)
    new_result = clean_json_response(result)
    print("cleaned response", new_result)
    new_result = json.loads(new_result)
    print("after json", new_result)
    return new_result
