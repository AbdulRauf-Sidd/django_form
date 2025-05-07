import os
import boto3
from pathlib import Path
import time
from urllib.parse import quote
# from dotenv import load_dotenv

# base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# env_path = os.path.join(base_path, '.env')
# load_dotenv(env_path)

# Load the .env file
# Set up your Cloudflare R2 credentials and endpoint
access_key = 'f1ac1dc043a240f996be558cfba72868'
secret_key = 'de1dd032fe83dc7bc8b8f8b207ca54807fa851b07483428396c141ebaf46d8bb'
endpoint_url = 'https://3c5636b6cfe0011ec1887ff62b057097.r2.cloudflarestorage.com'

# Create a session using your credentials

# r2_folder = 'why/bye/world/'  # Set your desired folder path within R2


# Function to upload a single file and return the R2 URL
def upload_to_r2(file_path, file_name, r2_folder, test_run):
    session = boto3.session.Session()
    if test_run == 'true':
        s3 = session.client('s3', 
                       aws_access_key_id='f1ac1dc043a240f996be558cfba72868', 
                       aws_secret_access_key="de1dd032fe83dc7bc8b8f8b207ca54807fa851b07483428396c141ebaf46d8bb", 
                       endpoint_url="https://3c5636b6cfe0011ec1887ff62b057097.r2.cloudflarestorage.com") 
        bucket_name = 'fin-scraping-bucket'
        public_url = 'https://pub-43b7342d87a7428998f14a200ddd2a26.r2.dev/'
    else:
        s3 = session.client('s3', 
                       aws_access_key_id='75ab8895b1384c0274072b23d0eb9d3d', 
                       aws_secret_access_key="eb384a4f3bc3c5504ec6c5ee355d4b1358ab191a6968f0521f83e330992882ef", 
                       endpoint_url="https://3f80db7adc544850c6ad4904a0fb8f54.r2.cloudflarestorage.com") 
        bucket_name = 'equity-data'
        public_url = 'https://pub-2c783279b61043e19fbdadd1bee5153a.r2.dev/'
 
    # Check if the file exists
    # if not os.path.isfile(file_path):
    #     continue
        # raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Extract the filename from the file path
    filename = os.path.basename(file_path)

    # Construct the R2 key by combining the folder and the filename
    r2_file_key = os.path.join(r2_folder, file_name)

    # Upload the file to R2
    attempts = 0
    while attempts < 3:
        try:
            # Upload the file to R2
            with open(file_path, 'rb') as data:
                s3.put_object(Bucket=bucket_name, Key=r2_file_key, Body=data)

            # Construct the URL of the uploaded file
            safe_r2_file_key = quote(r2_file_key)
            file_url = f'{public_url}{safe_r2_file_key}'
            print(f"Uploaded: {r2_file_key}, URL: {file_url}")
            return file_url

        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts}: Failed to upload file. Error: {str(e)}")
            if attempts < 3:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Maximum retry attempts reached, failed to upload.")
                return None

# upload_file_to_r2('downloads/_cs_ferrari_05.05.2021_eng_0.pdf', "test/")

def compile_content_name(content_type, equity_ticker, fiscal_year, fiscal_quarter):
    # Remove underscores from content_type
    if content_type:
        content_type_cleaned = content_type.replace('_', ' ').title()
    # Combine the parameters to form the content_name
    content_name = f"{equity_ticker} Q{fiscal_quarter} {fiscal_year} {content_type_cleaned}"
    return content_name

# Example usage
# content_name = compile_content_name("earnings_transcript", "NVDA", 2025, 4)
# print(content_name)  # Output: NVDA Q4 2025 Earnings Transcript
def construct_path(ticker: str, date: str, file_name: str) -> str:
    """
    Join four string parameters with '/' between them.
    
    Args:
        param1: First string
        param2: Second string
        param3: Third string
        param4: Fourth string
        
    Returns:
        String with all parameters joined by '/'
        
    Example:
        >>> join_with_slashes("a", "b", "c", "d")
        'a/b/c/d'
    """
    return f"{ticker}/{date}/{file_name}"

def construct_event(
    equity_ticker,
    content_name,
    content_type,
    published_date,
    r2_url,
    periodicity,
    file_type = "pdf",
    geography = 'US',
    fiscal_date=None,
    fiscal_year='0000',
    fiscal_quarter='0'
):
    """
    Constructs an earnings document JSON object with smart defaults.
    
    Args:
        equity_ticker (str): Stock ticker (e.g., "AAPL")
        geography (str): Geographic region (e.g., "US")
        content_name (str): Document name (used to detect content type)
        file_type (str): File extension (e.g., "pdf")
        published_date (str): Date published in YYYY-MM-DD format
        r2_url (str): URL to the document in R2 storage
        fiscal_date (str, optional): Fiscal date in YYYY-MM-DD format
        fiscal_year (int, optional): Fiscal year
        fiscal_quarter (int, optional): Fiscal quarter (1-4)
    
    Returns:
        dict: Structured earnings document JSON object
    """
    # Determine content type from content_name
    
    
    return {
        "equity_ticker": equity_ticker.upper(),
        "geography": geography.upper(),
        "content_name": content_name,
        "file_type": file_type.lower(),
        "content_type": content_type,
        "published_date": published_date,
        "fiscal_date": fiscal_date,
        "fiscal_year": fiscal_year,
        "fiscal_quarter": fiscal_quarter,
        "r2_url": r2_url,
        "periodicity": periodicity  # Default for earnings documents
    }

import json
import os

def append_event_to_json(event):
    # Extract the equity_ticker from the event
    equity_ticker = event.get("equity_ticker")

    # Define the filename
    filename = f"{equity_ticker}.json"

    # Check if the file exists
    if os.path.exists(filename):
        # If the file exists, open it and load the existing data
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        # If the file does not exist, initialize an empty list
        data = []

    # Append the new event to the data list
    data.append(event)

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
# event = {
#     "equity_ticker": "AAPL",
#     "geography": "US",
#     "content_name": "Quarterly Report",
#     "file_type": "pdf",
#     "content_type": "Earnings Report",
#     "published_date": "2025-05-07",
#     "fiscal_date": "2025-03-31",
#     "fiscal_year": 2025,
#     "fiscal_quarter": 1,
#     "r2_url": "https://example.com/r2/AAPL_Q1_2025.pdf",
#     "periodicity": "Quarterly"
# }

# append_event_to_json(event)
