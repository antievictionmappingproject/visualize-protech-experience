import pandas as pd
import CleanTech
from collections import defaultdict

data = pd.read_csv('Proptech Experience Survey (Responses).csv')
technologies = data.iloc[:, 2]
cleaned_technologies = []

# Process each row's technologies
for techs in technologies:
    split_tech = CleanTech.split_technologies(techs)
    cleaned_tech = [CleanTech.clean_technology_name(tech) for tech in split_tech if CleanTech.clean_technology_name(tech)]
    cleaned_technologies.append(cleaned_tech)

# Create a dictionary to count pairs
pair_counts = defaultdict(lambda: defaultdict(int))

# Count each pair
for tech_list in cleaned_technologies:
    for tech in tech_list:
        for other_tech in tech_list:
            if tech != other_tech:
                pair_counts[tech][other_tech] += 1

# Convert to a DataFrame for easier handling
df_pair_counts = pd.DataFrame(pair_counts).fillna(0).astype(int)
df_filtered_rows = df_pair_counts.drop(['maybe?', '³', 'if any', 'License plate scanner', 'Smart doorbell', 'PetScreening.com',
                                        'Audio recording', 'Phone scanner', 'Bluetooth Trackers', 'Spy cameras', 'Online payments',
                                        'Laundry app', 'Rent Payment software', 'Digital package lockers', 'spyware',
                                        'malware', 'register animals', 'OurPetPolicy.com', 'frauding bank accounts','Smart meter'])
df_filtered_columns = df_filtered_rows.drop(columns=['maybe?', '³', 'if any', 'License plate scanner', 'Smart doorbell', 'PetScreening.com',
                                        'Audio recording', 'Phone scanner', 'Bluetooth Trackers', 'Spy cameras', 'Online payments',
                                        'Laundry app', 'Rent Payment software', 'Digital package lockers', 'spyware',
                                        'malware', 'register animals', 'OurPetPolicy.com', 'frauding bank accounts','Smart meter'])

df_filtered_columns.to_csv('technology_pairs_filtered.csv', index_label='Technology')
