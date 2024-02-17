import codecs
import os

from Dbias.bias_classification import *
from Dbias.text_debiasing import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from app import app


def analyze_context(context):
    # Convert the context to lowercase to allow for case-insensitive matching
    context = context.lower()

    # Check for keywords in the context and return the corresponding action
    if "applications" in context or "resume" in context:
        print("We need to remove attributes!")
        return "remove_attributes"
    elif "news" in context:
        return "check_bias"


def analyze_bias(text):
    biased_texts = [
        "Men make better programmers than women",
        "People who wear Y clothing are untrustworthy.",
    ]
    # results = run_pipeline_on_texts(biased_texts)
    # results.to_csv("<save_path>.csv", index=False)


def anonymize_original_file(file_path):
    # Define the keys to anonymize and their placeholders in the original file
    keys_to_anonymize = {
        "Name:": "ANON",
        "Age:": "ANON",
        "Gender:": "ANON",
        "Ethnicity:": "ANON",
    }

    # Read the original file content
    with codecs.open(file_path, "r", "utf-8") as file:
        lines = file.readlines()

    # Replace the values of the attributes with "ANON"
    for i, line in enumerate(lines):
        for key, anon in keys_to_anonymize.items():
            if key in line:
                # Replace the entire line after the key with "ANON"
                lines[i] = key + " " + anon + "\n"

    # Write the anonymized content back to the file
    with codecs.open(file_path, "w", "utf-8") as file:
        file.writelines(lines)


def generate_summary_of_anonymization():
    # Static summary explanation of the anonymization process
    summary = (
        "For datasets with job applications that will be used for training AI, "
        "it is crucial to anonymize personally identifying information such as names, "
        "age, nationality, and gender. This is important both for privacy reasons and "
        "to prevent the AI from developing biases towards certain demographics. "
        "By removing these attributes, it will ensure the AI model evaluates candidates "
        "based on their skills and experiences rather than personal characteristics."
    )
    return summary


def preprocess_file(file_path):
    with codecs.open(file_path, "r", "utf-8") as file:
        file_content = file.read()

    # Tokenize the text
    tokens = word_tokenize(file_content)

    # Remove punctuation and convert to lowercase
    tokens = [word.lower() for word in tokens if word.isalpha()]

    # Remove stop words
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    with codecs.open(file_path, "w", "utf-8") as file:
        file.write(" ".join(tokens))


def remove_attributes(file_path):
    # Read the file content
    with codecs.open(file_path, "r", "utf-8") as file:
        tokens = file.read().split()

    # Define the keys to anonymize with the number of tokens to replace after the key
    keys_to_anonymize = {"name": 2, "age": 1, "gender": 1, "ethnicity": 1}
    anonymized_attributes = []

    # Iterate over the keys and replace the specified number of tokens following each key with "ANON"
    for key, num_tokens_to_replace in keys_to_anonymize.items():
        while key in tokens:
            key_index = tokens.index(key)
            # Special handling for the 'age' key to check if the following token is an integer
            if key == "age":
                try:
                    # Attempt to parse the next token as an integer
                    int(tokens[key_index + 1])
                    # If successful, replace it with "ANON"
                    tokens[key_index + 1] = "ANON"
                except ValueError:
                    # If parsing fails, it's not an integer, so we don't replace it
                    tokens.insert(key_index + 1, "ANON")
            else:
                # Replace the specified number of tokens following the key with "ANON"
                tokens[key_index + 1 : key_index + num_tokens_to_replace + 1] = [
                    "ANON"
                ] * num_tokens_to_replace
            anonymized_attributes.append(key)
            # Remove the key itself to prevent further matches
            del tokens[key_index]

    # Write the anonymized tokens back to the file
    with codecs.open(file_path, "w", "utf-8") as file:
        file.write(" ".join(tokens))


def save_file_and_context(file, context):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    context_filename = os.path.splitext(file.filename)[0] + "_cntxt.txt"
    context_file_path = os.path.join(app.config["UPLOAD_FOLDER"], context_filename)

    with codecs.open(context_file_path, "w", "utf-8") as context_file:
        context_file.write(context)

    return file_path, context_file_path


def debias_text(file_path):
    # Read the file content
    with open(file_path, "r") as file:
        content = file.read()

    # Truncate the content to the maximum sequence length if necessary
    max_length = 1024  # This is the typical max length for models like BERT
    if len(content) > max_length:
        content = content[:max_length]

    # Debias the content
    debiased_content = run(content, show_plot=False)

    # Check if debiased_content is not None before writing it to the file
    if debiased_content is not None:
        # Handle the case when debiased_content is a list of dictionaries
        if isinstance(debiased_content, list) and all(
            isinstance(item, dict) for item in debiased_content
        ):
            # Find the sentence with the lowest bias rating
            min_bias_sentence = min(debiased_content, key=lambda x: x["bias"])

            # Write the sentence with the lowest bias rating to a new file
            debiased_file_path = file_path.replace(".txt", "_debiased.txt")
            with open(debiased_file_path, "w") as file:
                file.write(min_bias_sentence["Sentence"])

            return debiased_file_path
        else:
            print("Debiasing failed. Content was not written to the file.")


def check_bias(file_path):
    # Read the file content
    with open(file_path, "r") as file:
        content = file.read()

    # Classify the bias in the content using the correct function
    classification_output = classifier(content)

    # Extract the label and score from the first prediction
    label = classification_output[0]["label"]
    score = classification_output[0]["score"]

    # Print the label and score
    return label, score
