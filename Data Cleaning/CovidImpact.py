import pandas as pd
from collections import defaultdict
import CleanTech

data = pd.read_csv('Proptech Experience Survey (Responses).csv')
dataCovid = pd.read_csv('Proptech Experience Survey (Responses) with Manually entered Covid Boolean.csv')

technologies = data.iloc[:, 2]
covid = dataCovid.iloc[:, 5]

# Process technologies
cleaned_technologies = []
for techs in technologies:
    split_tech = CleanTech.split_technologies(techs)
    cleaned_tech = [CleanTech.clean_technology_name(tech) for tech in split_tech if CleanTech.clean_technology_name(tech)]
    cleaned_technologies.append(cleaned_tech)

# Prepare covid column to clean "yes" and "no" responses
covid_cleaned = covid.fillna("").apply(
    lambda x: 1 if "yes" in str(x).lower() else (0 if "no" in str(x).lower() else None)
)

# Initialize dictionary for technology counts
tech_count = defaultdict(lambda: {"0s": 0, "1s": 0})

# Count 0s and 1s for each technology
for row_techs, covid_value in zip(cleaned_technologies, covid_cleaned):
    if covid_value is not None:  # Only consider rows with valid 0/1 values
        for tech in row_techs:
            if covid_value == 0:
                tech_count[tech]["0s"] += 1
            elif covid_value == 1:
                tech_count[tech]["1s"] += 1

# Convert results to a DataFrame
tech_count_df = pd.DataFrame.from_dict(tech_count, orient="index").reset_index()
tech_count_df.columns = ["Technology", "0s", "1s"]

# List of technologies to exclude
exclude_technologies = [
    'License plate scanner', 'Smart meter', 'Audio recording', 'maybe?',
    'Bluetooth Trackers', 'Spy cameras', 'frauding bank accounts',
    'spyware', 'malware', 'Online payments', 'Laundry app',
    'Digital package lockers', 'if any'
]

# Filter out rows where the Technology column matches the exclusion list
filtered_tech_count_df = tech_count_df[~tech_count_df["Technology"].isin(exclude_technologies)]

# Save
filtered_tech_count_df.to_csv('filtered_technology_impact_covid_response.csv', index=False)
