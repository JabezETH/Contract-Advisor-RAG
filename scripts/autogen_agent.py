import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from dotenv import load_dotenv
load_dotenv()

llm_config = {"config_list": [{"model": "gpt-4", }]}
code_execution_config = {"use_docker": False}


# Initialize the assistant agent with the given configurations
config_list = [
{"model": "gpt-4", "api_type": "openai"},
]
assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a knowledgeable contract assistant. Your task is to provide precise and accurate answers to user questions based on the content of the contract document. Always refer to the specific section and clause of the contract where the information is found to support your response",
    llm_config=llm_config,
    code_execution_config=code_execution_config,
    human_input_mode="NEVER",  # Never ask for human input
)

# Initialize the proxy agent responsible for retrieving documents and handling the Q&A
ragproxyagent = RetrieveUserProxyAgent(
name="ragproxyagent",
retrieve_config={
    "task": "qa",
    "docs_path": "/home/jabez/Documents/week_11/Contract-Advisor-RAG/data/document.md",
    "chunk_token_size":250,
    "model": config_list[0]["model"],
    # "client": chromadb.PersistentClient(path="/tmp/chromadb"),  # deprecated, use "vector_db" instead
    "vector_db": "chroma",  # to use the deprecated `client` parameter, set to None and uncomment the line above
    "overwrite": True,  # set to True if you want to overwrite an existing collection

},
code_execution_config=code_execution_config,
human_input_mode="NEVER",  # Never ask for human input.
)
def autogen_bot(file_path, question):
    # Reset the assistant's state (if needed)
    assistant.reset()

    # Initiate the chat with the assistant using the proxy agent
    ragproxyagent.initiate_chat(
        assistant, 
        message=ragproxyagent.message_generator, 
        problem=question
    )
    return ragproxyagent.last_message()
