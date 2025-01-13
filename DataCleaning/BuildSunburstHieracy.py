import pandas as pd
import json
import CleanTech

def parse_company_list(company_list_str):
    if company_list_str == '[]':
        return []
    company_list_str = company_list_str.strip('[]')
    companies = company_list_str.split(', ')
    return [company.strip("'") for company in companies]

def parse_list_from_string(input_str, delimiter=','):
    if pd.isna(input_str) or input_str.strip() == '':
        return []
    return [item.strip() for item in input_str.split(delimiter)]

def convert_to_int(input_val):
    try:
        return int(input_val)
    except (ValueError, TypeError):
        return None

def parse_preference_values(preference_str):
    # Parse preference values from a string (e.g., "-1, 1") and return a list of integers.
    if pd.isna(preference_str) or preference_str.strip() == '':
        return []
    return [convert_to_int(value) for value in preference_str.split(',') if value.strip()]

survey_df = pd.read_csv('Proptech Experience Survey (Responses).csv')
company_names_df = pd.read_csv('Extracted_Company_Names.csv')

amenity_column = "Does your building have any of the following amenities:"
unit_column = "How many units are in your building?"
rent_column = "What is your monthly rent?"
tech_column = "Would you consider this technology any of the following:"
preference_column = "Tech User Preference"

possible_tech = ["Smart lock", "Keyless Entry", "Smart Meter", "Phone app", "Lock boxes", "Facial recognition",
                 "Smart home technology", "Short term rentals", "Cameras"]

exclude_tech = ["maybe?", "PetScreening.com", "if any"]

technology_preferences = {}

root = {"name": "Technologies", "children": []}

for idx, row in company_names_df.iterrows():
    companies = parse_company_list(row['Extracted Companies'])
    survey_row = survey_df.iloc[idx]

    technologies = CleanTech.split_technologies(survey_row[tech_column])
    technologies = [CleanTech.clean_technology_name(tech, exclude_tech) for tech in technologies]

    for technology in technologies:
        # Track preferences for this technology
        if technology not in technology_preferences:
            technology_preferences[technology] = []

        # Collect preference scores (if available)
        preference_values = parse_preference_values(survey_row[preference_column])
        for preference_value in preference_values:
            if preference_value is not None:
                technology_preferences[technology].append(preference_value)

        tech_node = next((item for item in root['children'] if item['name'] == technology), None)
        if tech_node is None:
            tech_node = {"name": technology, "children": []}
            root['children'].append(tech_node)

        for company in companies:
            company_node = next((item for item in tech_node['children'] if item['name'] == company), None)
            if company_node is None:
                company_node = {"name": company, "children": []}
                tech_node['children'].append(company_node)

            # Create or retrieve nodes for Rent, Units, and Amenities
            rent_node = next((n for n in company_node['children'] if n['name'] == "Rent"), None)
            if rent_node is None:
                rent_node = {"name": "Rent", "children": []}
                company_node['children'].append(rent_node)

            units_node = next((n for n in company_node['children'] if n['name'] == "Units"), None)
            if units_node is None:
                units_node = {"name": "Units", "children": []}
                company_node['children'].append(units_node)

            amenities_node = next((n for n in company_node['children'] if n['name'] == "Amenities"), None)
            if amenities_node is None:
                amenities_node = {"name": "Amenities", "children": []}
                company_node['children'].append(amenities_node)

            # Append Rent if not None
            rent_value = convert_to_int(survey_row[rent_column])
            if rent_value is not None:
                rent_child = next((n for n in rent_node['children'] if n['name'] == rent_value), None)
                if rent_child:
                    rent_child['value'] += 1
                else:
                    rent_node['children'].append({"name": rent_value, "value": 1})

            # Append Units if not None
            units_value = convert_to_int(survey_row[unit_column])
            if units_value is not None:
                units_child = next((n for n in units_node['children'] if n['name'] == units_value), None)
                if units_child:
                    units_child['value'] += 1
                else:
                    units_node['children'].append({"name": units_value, "value": 1})

            # Append amenities
            amenities_list = parse_list_from_string(survey_row[amenity_column])
            for amenity in amenities_list:
                if CleanTech.is_within_word_limit(amenity):
                    amenity_node = next((n for n in amenities_node['children'] if n['name'] == amenity), None)
                    if amenity_node:
                        amenity_node['value'] += 1
                    else:
                        amenities_node['children'].append({"name": amenity, "value": 1})

# Compute average preferences and add them to the hierarchy
for tech_node in root['children']:
    tech_name = tech_node['name']
    if tech_name in technology_preferences and technology_preferences[tech_name]:
        avg_preference = sum(technology_preferences[tech_name]) / len(technology_preferences[tech_name])
        tech_node['averagePreference'] = avg_preference
    else:
        tech_node['averagePreference'] = None  # No data available

def rename_null_tech_nodes(root, new_name="Uncategorized Technologies"):
    # Rename null or empty technology nodes directly under the root node
    if "children" in root:
        for tech_node in root["children"]:
            if not tech_node.get("name") or tech_node["name"] in [None, ""]:
                tech_node["name"] = new_name

rename_null_tech_nodes(root)

json_hierarchy = json.dumps(root, indent=4)

# To save to a file
with open('sunburstHierachy.json', 'w') as json_file:
    json_file.write(json_hierarchy)