import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")
stop_words = nlp.Defaults.stop_words

def extract_nouns(text):
    try:
        doc = nlp(text)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks if not any(word.lower() in stop_words for word in chunk.text.split())]
        return noun_phrases
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def extract_potential_company_names(text):
    try:
        doc = nlp(text)
        company_names = [
            chunk.text for chunk in doc.noun_chunks
            if any(word[0].isupper() for word in chunk.text.split())  # Contains capitalized words
            and not all(word.lower() in stop_words for word in chunk.text.split())  # Not all words are stopwords
        ]
        return company_names
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def main():
    file_path = 'Proptech Experience Survey (Responses).csv'
    data = pd.read_csv(file_path)

    # column 1 contains the text from which to extract noun phrases
    texts_to_extract = data.iloc[:, 22]

    results_1 = []
    for text in texts_to_extract:
        result = extract_nouns(text)
        results_1.append(result)

    # Convert the list of lists to a DataFrame
    results_df = pd.DataFrame({'Extracted Noun Phrases': results_1})

    # Save the results to a new CSV file
    output_file_path = 'Extracted_Noun.csv'

    results_df.to_csv(output_file_path, index=False)
    print("Extraction complete. Data saved to:", output_file_path)

if __name__ == "__main__":
    main()
