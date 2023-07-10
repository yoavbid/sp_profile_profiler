import os
import streamlit as st
import openai.error
import openai
from pathlib import Path

from profile_profiler import get_summary
from jt_sql_alt import execute_query, get_conn

# params
PROMPT_PATH = "prompt.txt"

def submit_profile_id():
    st.session_state['profile_summary'] = get_summary(st.session_state['profile_id'], Path('summarized_log.txt'), 
                                                      Path('events.txt'), 'dlc_names_dict.json', Path('.'), PROMPT_PATH,
                                                      st.session_state['sql_conn'])
  
def main():
  # set API key in two ways to support both local and remote execution
  os.environ['SNOWFLAKE_USER'] = st.secrets["SNOWFLAKE_USER"]
  os.environ['SNOWFLAKE_PASSWORD'] = st.secrets["SNOWFLAKE_PASSWORD"]
  os.environ['OPENAI_API_KEY'] = st.secrets["api_secret"]
  openai.api_key = st.secrets["api_secret"]
  
  if 'sql_conn' not in st.session_state:
    st.session_state['sql_conn'] = get_conn()

  st.set_page_config(layout="wide")
  st.title("SP Profile Profiler")

  st.text_input("Profile ID", key="profile_id", on_change=submit_profile_id)

  summary = st.session_state.get('profile_summary', None)
  if summary is not None:
    st.write(summary)


if __name__ == "__main__":
  main()