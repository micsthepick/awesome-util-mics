import json
import base64
from pathlib import Path
from urllib.parse import urlparse, unquote

def extract_files_from_har(har_path, output_dir):
    """
    Extracts files from a HAR file and saves them using filenames derived from their request URLs.

    :param har_path: Path to the HAR file.
    :param output_dir: Directory where extracted files will be saved.
    """
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(har_path, 'r') as har_file:
        har_data = json.load(har_file)

    for entry in har_data['log']['entries']:
        # Attempt to extract the filename from the request URL
        url_path = urlparse(entry['request']['url']).path
        filename = unquote(url_path.split('/')[-1])

        # If unable to extract a meaningful filename, generate one based on the request timestamp
        if not filename or '.' not in filename:
            mime_type = entry['response']['content'].get('mimeType', '')
            file_extension = determine_extension(mime_type)
            filename = f"{entry['startedDateTime'].replace(':', '-').replace('.', '-')}{file_extension}"

        file_path = Path(output_dir) / filename

        # Check if the response content is available and is encoded
        if 'text' in entry['response']['content'] and 'encoding' in entry['response']['content']:
            content = entry['response']['content']['text']

            # Decode the base64 content and save it to a file
            with open(file_path, 'wb') as file_out:
                file_out.write(base64.b64decode(content))

            print(f"Saved {file_path}")

def determine_extension(mime_type):
    """
    Determines the file extension based on the MIME type.

    :param mime_type: The MIME type of the file.
    :return: A file extension, including the dot (e.g., '.jpg', '.html').
    """
    # Add more MIME types and extensions as needed
    extensions = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'text/html': '.html',
        'application/javascript': '.js',
    }
    return extensions.get(mime_type, '')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py path_to_har_file output_directory")
    else:
        har_path, output_dir = sys.argv[1], sys.argv[2]
        extract_files_from_har(har_path, output_dir)
