import shutil
from pathlib import Path

REQUIRED_CODE_FILES = [
    "profile_profiler.py"
]

def update_from_original_repo():
    streamlit_path = Path(__file__).parent
    tutor_path = streamlit_path.parent / "simply_tutor"
    sg_recog_path = tutor_path.parent / "sg_recog"
    
    shutil.copy(tutor_path / "queries" / "get_profile_info.sql", streamlit_path)
    shutil.copy(tutor_path / "queries" / "get_profile_session_events.sql", streamlit_path)
    shutil.copy(tutor_path / "queries" / "dlc_names_dict.json", streamlit_path)
    shutil.copy(tutor_path / "prompts" / "user_history.txt", streamlit_path / "prompt.txt")
    
    for filename in REQUIRED_CODE_FILES:
        shutil.copy(tutor_path / "src" / filename, streamlit_path / filename)
    
    
if __name__ == "__main__":
    update_from_original_repo()