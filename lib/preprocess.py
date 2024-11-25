import sys
from dateparser import search
import json
import re

def extract_date(input_text):
    """
    Extracts the first future date from the input text using dateparser.
    Returns the ISO formatted date as a string, or None if no date is found.
    """
    date_suggestions = search.search_dates(input_text, settings={'PREFER_DATES_FROM': 'future'})
    if date_suggestions and date_suggestions[0]:
        return date_suggestions[0][1].strftime('%Y-%m-%d')
    return None

def extract_tags(input_text):
    """
    Extracts hashtags (#tag) and multi-word tags ([[multi word tag]]) from the input text.
    Returns a list of tags with hashtags stripped of the '#' symbol.
    """
    # Define patterns
    hashtag_pattern = r"#\w+"
    multi_word_tag_pattern = r"\[\[.*?\]\]"

    # Extract single-word hashtags and strip '#'
    hashtags = [tag[1:] for tag in re.findall(hashtag_pattern, input_text)]  # Remove '#' from tags

    # Extract multi-word tags and remove brackets
    multi_word_tags = [tag.strip("[[]]") for tag in re.findall(multi_word_tag_pattern, input_text)]

    # Combine both types of tags
    return hashtags + multi_word_tags

def build_output(iso_date, tags):
    """
    Constructs the Alfred workflow JSON output with the given date and tags.
    Returns the output as a dictionary.
    """
    return {
        "alfredworkflow": {
            "arg": iso_date or "",
            "variables": {
                "tags": tags
            }
        }
    }

def main():
    input_text = sys.argv[1]

    # Extract the date and tags
    iso_date = extract_date(input_text)
    tags = extract_tags(input_text)

    # Build the output
    alfred_output = build_output(iso_date, tags)

    # Print the result as JSON
    print(json.dumps(alfred_output))

if __name__ == "__main__":
    main()
