import logging
from pathlib import Path

FILE_DIRECTORY = "prompts"
FILE = "categorisation_prompt.md"

def process_file(file, placeholders: dict=None):
    script_dir = Path(__file__).parent 
    file_path = script_dir.parent / FILE_DIRECTORY / FILE

    try:
        with open(file_path, "r") as file:
            text = file.read()
        placeholders = {
            "assistant_name" : "Xian",
            "date" : "2024-05-01",
            "user_name" : "Yan"

        }
        formatted_text = text.format(**placeholders)
        return formatted_text
    
    except FileNotFoundError:
        logging.error(f"File not found - {file}")
        raise
    except KeyError as e:
        logging.error(f"Missing placeholder in template: {e}")
        raise
    except Exception as e:
        logging.error(f"Cannot open file: {file} - {e}")
        raise