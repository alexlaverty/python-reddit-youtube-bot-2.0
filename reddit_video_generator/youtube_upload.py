from typing import Optional, List
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import os.path
import csv
from datetime import datetime

def upload_video_to_youtube(
    client_secrets_file: str,
    video_title: str,
    video_description: str,
    video_tags: List[str],
    video_file_path: str,
    privacy_status: str = 'private'
) -> str:
    """
    Upload a video to YouTube using the YouTube Data API.

    Args:
        client_secrets_file (str): Path to the client secrets file.
        video_title (str): Title of the video.
        video_description (str): Description of the video.
        video_tags (list): List of tags for the video.
        video_file_path (str): Path to the video file to be uploaded.
        privacy_status (str, optional): Privacy status of the video ('public', 'unlisted', or 'private').
            Defaults to 'private'.

    Returns:
        str: ID of the uploaded video.

    Raises:
        ValueError: If the provided privacy_status is not one of ['public', 'unlisted', 'private'].
    """
    # Validate privacy_status
    valid_privacy_statuses = ['public', 'unlisted', 'private']
    if privacy_status not in valid_privacy_statuses:
        raise ValueError(f"Invalid privacy_status. Must be one of {valid_privacy_statuses}")

    # Set up API credentials
    credentials = None
    token_file = 'token.json'

    if os.path.exists(token_file):
        credentials = Credentials.from_authorized_user_file(token_file)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, ['https://www.googleapis.com/auth/youtube.upload'])
            credentials = flow.run_local_server(port=8080)

        # Save the credentials for future runs
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    # Build the YouTube API service
    youtube = build('youtube', 'v3', credentials=credentials)

    # Upload video
    request_body = {
        'snippet': {
            'title': video_title,
            'description': video_description,
            'tags': video_tags
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media_file = MediaFileUpload(video_file_path)

    upload_response = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()

    return upload_response['id']

def initialize_tracking_file(file_path: str) -> None:
    """
    Create a CSV file with headers if it doesn't exist.

    Args:
        file_path (str): Path to the CSV file.
    """
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "File Name", "Status", "Upload Date"])

def add_entry(file_path: str, title: str, file_name: str, status: str, upload_date: Optional[str] = None) -> None:
    """
    Add a new entry to the CSV file.

    Args:
        file_path (str): Path to the CSV file.
        title (str): Title of the video.
        file_name (str): File name of the video.
        status (str): Status of the video ('Pending' or 'Uploaded').
        upload_date (str, optional): Upload date in the format '%Y-%m-%d %H:%M:%S'.
            Defaults to None.
    """
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if upload_date is None:
            upload_date = ""
        writer.writerow([title, file_name, status, upload_date])

def mark_as_uploaded(file_path: str, title: str) -> None:
    """
    Update the status to "Uploaded" and set the upload date in the CSV file.

    Args:
        file_path (str): Path to the CSV file.
        title (str): Title of the video.
    """
    entries = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        entries = [row for row in reader]

    for entry in entries:
        if entry[0] == title and entry[2] != "Uploaded":
            entry[2] = "Uploaded"
            entry[3] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(entries)

# Example usage:
if __name__ == "__main__":
    tracking_file_path = "upload_tracking.csv"

    # Initialize the tracking file if it doesn't exist
    initialize_tracking_file(tracking_file_path)

    # Add a new entry (pending)
    add_entry(tracking_file_path, "Video 1", "video1.mp4", "Pending")

    # Add another entry (uploaded)
    add_entry(tracking_file_path, "Video 2", "video2.mp4", "Uploaded", "2023-01-01")

    # Mark an entry as uploaded
    mark_as_uploaded(tracking_file_path, "Video 1")
