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
def submit_general_id():
    id = st.session_state['general_id']
  
    if id.startswith('PFL'):
        st.session_state['general_id'] = ''
        st.session_state['profile_id'] = id
        st.session_state['profile_summary'] = get_summary(st.session_state['profile_id'], Path('summarized_log.txt'), 
                                                        Path('events.txt'), 'dlc_names_dict.json', Path('.'), PROMPT_PATH,
                                                        st.session_state['sql_conn'])
    else:
        if id.startswith('ACC'):
            column_name = 'ACCOUNT_ID'
        else:
            column_name = 'ACCOUNT_EMAIL'
            
        query = "SELECT PROFILE_ID, PROFILE_AGE, PROFILE_GENDER, PROFILE_CREATION_TIME, LAST_EVENT_TS FROM CORE_SP_PROFILES WHERE %s = '%s'" % (column_name, id)
        st.session_state['possible_profiles'] = execute_query(query, st.session_state['sql_conn'])
        
  
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

    st.text_input("Account ID / E-mail / Profile ID", key="general_id", on_change=submit_general_id)
    
    if 'possible_profiles' in st.session_state:
        st.table(st.session_state['possible_profiles'])
        
    if st.session_state.get('general_id', '') != '' and not 'profile_id' in st.session_state:
        st.text_input("Profile ID", key="profile_id", on_change=submit_profile_id)

    if 'profile_summary' in st.session_state:
        st.write(st.session_state['profile_summary'])


if __name__ == "__main__":
    main()