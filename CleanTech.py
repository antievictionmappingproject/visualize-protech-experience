import pandas as pd
import re

def split_technologies(input_str):
    # Split the technology string, keeping phrases inside parentheses intact
    if pd.isna(input_str) or input_str.strip() == '':
        return []
    # Pattern to split by commas that are not inside parentheses
    pattern = r',\s*(?![^()]*\))'
    technologies = [tech.strip() for tech in re.split(pattern, input_str)]
    return technologies

def clean_technology_name(tech_name, exclude_tech):
    # Remove any parenthetical content from the technology name
    cleaned_name = re.sub(r'\s*\([^)]*\)', '', tech_name).strip()
    if is_within_word_limit(cleaned_name) and cleaned_name not in exclude_tech:
        return cleaned_name

def is_within_word_limit(response, limit=3):
    words = response.split()
    return len(words) <= limit