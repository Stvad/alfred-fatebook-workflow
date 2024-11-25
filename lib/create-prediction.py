import os
import json
import requests


def main():
    # Read environment variables
    tags = os.getenv("tags", "")  # Tags from the environment variable
    question = os.getenv("question")  # Question from the environment variable
    user_date = os.getenv("user_date")  # Date from the environment variable
    percentage = float(os.getenv("percentage"))  # Percentage from the environment variable
    fatebook_api_key = os.getenv("fatebook_api_key")  # API key from the environment variable
    share_with_team = os.getenv("shareWithTeam")  # Team name from the environment variable (optional)

    # Ensure required environment variables are set
    if not all([question, user_date, fatebook_api_key]):
        raise ValueError(
            "Missing one or more required environment variables: 'question', 'user_date', or 'fatebook_api_key'."
        )

    # Convert percentage to decimal format
    forecast_percentage = round(percentage / 100, 2)

    # Parse tags if present (tab-separated)
    tags_list = tags.split("\t") if tags else []

    # Construct the query parameters
    query_params = {
        "apiKey": fatebook_api_key,
        "title": question,
        "resolveBy": user_date,
        "forecast": forecast_percentage,
    }

    # Add tags to the query parameters as repeated keys
    query_params_list = []
    for key, value in query_params.items():
        query_params_list.append((key, value))
    for tag in tags_list:
        query_params_list.append(("tags", tag.strip()))

    # Add shareWithLists parameter if shareWithTeam is set
    if share_with_team:
        query_params_list.append(("shareWithLists", share_with_team))

    # Make the PUT request
    base_url = "https://fatebook.io/api/v0/createQuestion"
    response = requests.put(base_url, params=query_params_list)

    # Output the result in Alfred workflow format
    print(json.dumps({
        "alfredworkflow": {
            "arg": response.text,
        }
    }))


if __name__ == "__main__":
    main()
