import pandas as pd

def extract_company_names_using_keywords(response, keywords, match_percentage):
    # Convert the entire response to string
    response = str(response)
    # Initialize an empty list to store company names without repeats
    company_names = []
    if response != 'nan':
        # Iterate over each keyword
        for keyword in keywords:
            # Check if the keyword is in the response and not already added to the list
            if keyword in response and keyword not in company_names:
                company_names.append(keyword)
            elif find_fuzzy_match(response, keyword, match_percentage) and keyword not in company_names:
                company_names.append(keyword)

    return company_names

def find_fuzzy_match(match_string, text, match_percentage):
    # use an iterator so that we can skip to the end of a match.
    text_iter = enumerate(text)
    for index, char in text_iter:
        try:
            match_start = match_string.index(char)
        except ValueError:
            continue
        match_count = 0
        zip_char = zip(match_string[match_start:], text[index:])
        for match_index, (match_char, text_char) in enumerate(zip_char):
            if match_char == text_char:
                match_count += 1
        if match_count >= len(match_string) * match_percentage:
            return True
    return False

data = pd.read_csv('Proptech Experience Survey (Responses).csv')
responsesB = data.iloc[:, 1]
responsesW = data.iloc[:, 22]

all_company_names_B = []
all_company_names_W = []

# Manually create a list of company keywords
possible_company_names = ['Google', 'Dish TV', "Carson", 'GateGuard','ConEdison', 'Amazon Ring', 'DoorBird'
                          'FST21', 'AppFolio', 'Trinity', 'Latch', 'Airbnb', 'Cozy', 'BuildingLink',
                          'SmartRent','Rent Cafe', 'Rent Redi App', 'ManageGo', 'RealPage', 'LuxerOne', 'ActiveBuilding',
                          'ButterflyMX', 'Experiential Capital Group', 'Apartments.com', 'Virtual Doorman',
                          'Schlage', 'SightPlan', 'ResidentService.com', 'KnockRentals', 'Flock', 'Resident Portal',
                          'Entrata', 'HP', "Apple", 'Chirp', 'Paragon Mobile', 'Yardi Systems', 'HID', 'Alarm.com',
                          'CWSI', 'Blink XT2', 'Avail', 'PayYourRent.com', 'Swan Security', 'Domuso',
                          'Nest', 'Rhino', 'petscreening', 'MVI My Video Intercom', 'Yale', 'HoneyWell', 'Akuvox Smartplus',
                          'Coinmeter', 'Swiftlane', 'Blink', 'Samsung', 'Conservice', 'Wyze',
                          'Tenant WebAccess', 'Forgeglobal', 'RiseBuildings', 'Bilt', 'GateWise', 'UDR', 'Brivo Pass',
                          'TownSteel', 'PayRange', 'ViewTech', 'Buildium', 'Alloy', 'Flex', "HIK", "Zelle", "ResidentCenter",
                          'REED', 'Eufy']

# Loop through each response and extract company names
for response in responsesB:
    company_names = extract_company_names_using_keywords(response, possible_company_names, 0.7)
    all_company_names_B.append(company_names)

for response in responsesW:
    company_names = extract_company_names_using_keywords(response, possible_company_names, 0.9)
    all_company_names_W.append(company_names)

all_company_names = []

for i in range(len(all_company_names_B)):
    company_names_B = all_company_names_B[i]

    company_names_B_set = set(all_company_names_B[i])
    company_names_W_set = set(all_company_names_W[i])

    in_W_but_not_in_B = company_names_W_set - company_names_B_set

    result = company_names_B + list(in_W_but_not_in_B)

    all_company_names.append(result)


# Convert the list of lists to a DataFrame
# Create a DataFrame from the list of lists where each list becomes a row
company_names_df = pd.DataFrame({'Extracted Companies': all_company_names})

# Save to CSV, ensuring each list of names is handled as a single entry
company_names_df.to_csv('Extracted_Company_Names.csv', index=False)