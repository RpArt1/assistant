import logging
from pathlib import Path

DEFAULT_FILE_DIRECTORY = "prompts"

def process_file(file_name: str,  placeholders: dict = None,  file_dir: str = DEFAULT_FILE_DIRECTORY) -> str:
    script_dir = Path(__file__).parent 
    file_path = script_dir.parent / file_dir / file_name

    try:
        with open(file_path, "r") as file:
            text = file.read()
        if(placeholders):
            text = text.format(**placeholders)
        return text
    
    except FileNotFoundError:
        logging.error(f"File not found - {file}")
        raise
    except KeyError as e:
        logging.error(f"Missing placeholder in template: {e}")
        raise
    except Exception as e:
        logging.error(f"Cannot open file: {file} - {e}")
        raise