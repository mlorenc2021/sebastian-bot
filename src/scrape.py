import requests
import html2text
import os


def scrape(url):

    # Set up the paths relative to the script location
    script_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')  # Path to the output directory

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Specify the path for the output file within the 'output' directory
    output_file_path = os.path.join(output_dir, "output.md")

    # Fetch the HTML
    url = url  # Change this URL to the one you're interested in
    response = requests.get(url)
    html_content = response.text

    # Convert HTML to Markdown
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    markdown_content = text_maker.handle(html_content)

    # Save to a Markdown file in the specified 'output' directory
    with open(output_file_path, "w") as file:
        file.write(markdown_content)

    print(f"Done! Your HTML has been converted and saved as a markdown file at {output_file_path}.")




#Example: scrape("https://archlinux.org/")