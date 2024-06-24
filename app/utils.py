# Basic Imports
import json
import pandas as pd
import sqlite3
from pathlib import Path

# Constants
DATABASES_PATH = Path(__file__).parent.parent.joinpath("data").joinpath("databases")

# Variables
memory_db_connection = sqlite3.connect(
    DATABASES_PATH.joinpath("memory.db"), check_same_thread=False
)

# Functions
def load_metadata_from_state_memory(thread_id):
    """
    Load metadata from the state memory database for a specific thread.

    Parameters
    ----------
    thread_id : str
        The ID of the thread for which to load the metadata.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the metadata for the specified thread.
    """
    df_metadata = pd.read_sql_query(
        f"SELECT metadata FROM checkpoints WHERE thread_id = '{thread_id}';",
        memory_db_connection,
    )
    return df_metadata

def extract_message_for_streamlit(metadata):
    """
    Extract the last message for Streamlit display from the metadata.

    Parameters
    ----------
    metadata : bytes
        The metadata containing the messages in a byte json string format.

    Returns
    -------
    dict or None
        A dictionary containing the role and content of the last message, or None if no message is found.
        
        The dictionary has the following structure:
        - For user messages: {"role": "user", "content": content}
        - For AI messages: {"role": "assistant", "content": content}
    """
    # Convert b-string to JSON string and parse it
    json_str = metadata.decode("utf-8")
    metadata_dict = json.loads(json_str)
    
    # Initialize result
    result = None
    
    # Check if "writes" is present
    writes = metadata_dict.get("writes")
    
    if writes:
        messages = None
        if "messages" in writes:
            # If "messages" key is directly present
            messages = writes["messages"]
        else:
            # If "messages" key is in nested dictionary
            for value in writes.values():
                if isinstance(value, dict) and "messages" in value:
                    messages = value["messages"]
                    break
        
        # Extract the last message and its type
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, dict):
                content = last_message.get("kwargs", {}).get("content", "")
                message_type = last_message.get("kwargs", {}).get("type", "")
            elif isinstance(last_message, list) and len(last_message) >= 2:
                content = last_message[1]
                message_type = last_message[0]
            
            if content:
                if message_type == "user":
                    result = {"role": "user", "content": content}
                elif message_type == "ai":
                    result = {"role": "assistant", "content": content}
    return result
