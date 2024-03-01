# data_manager.py
import json

def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def load_all_questions():
    try:
        multiple_choice_data = load_questions("multiple_choice_questions.json")
        return multiple_choice_data
    except (FileNotFoundError) as e:
        print(f"Error loading questions: {e}")
        return {}
