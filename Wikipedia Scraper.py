import time
import requests
from bs4 import BeautifulSoup


def get_wikipedia_content(website_url: str) -> str:
    """
    This function fetches the main text content from a given Wikipedia page URL.
    :param website_url: The URL of the Wikipedia page from which we want to get the main text content.
    :return: The main text content of the Wikipedia page.
    """
    try:
        # Fetch HTML content
        response = requests.get(website_url)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the main content
        main_content_div = soup.find('div', class_='mw-content-ltr mw-parser-output')

        if main_content_div:
            # Initialize an empty list to hold formatted text
            formatted_text = []

            # Iterate through the children of the main content div
            for element in main_content_div.children:
                # Add double newline for headings and paragraphs
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']:
                    formatted_text.append('\n\n' + element.get_text(separator=" ", strip=True))
                # Add single newline for other block elements
                elif element.name in ['ul', 'ol', 'blockquote', 'pre']:
                    formatted_text.append('\n' + element.get_text(separator=" ", strip=True))
                else:
                    # Append inline elements directly
                    formatted_text.append(element.get_text(separator=" ", strip=True))

            # Join the formatted text list into a single string
            text_content = ''.join(formatted_text).strip()
            return text_content
        else:
            return "Main content div not found."
    except requests.exceptions.RequestException as e:
        # Handle exceptions that may occur during the HTTP request
        return f"An error occurred: {e}"


if __name__ == "__main__":
    start = time.time()

    # Example usage
    url = "https://en.wikipedia.org/wiki/Solar_System"
    text_content_test = get_wikipedia_content(url)

    end = time.time()

    print(text_content_test)
    print(f"Duration: {end - start} seconds")
