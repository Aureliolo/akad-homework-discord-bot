import os
import schedule
import time
import requests
import pdfplumber

# Configurable variables
folder_path = "/path/to/pdf/folder"
discord_webhook_url = "your_discord_webhook_url"

def extract_homework(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        # Add logic to extract specific homework text
        return text

def post_to_discord(message):
    data = {"content": message}
    response = requests.post(discord_webhook_url, data=data)
    if response.status_code != 204:
        print("Failed to post message to Discord")

def weekly_task():
    files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not files:
        post_to_discord("No PDF files found in the folder.")
        return

    all_homework = ""
    for file in files:
        file_path = os.path.join(folder_path, file)
        homework = extract_homework(file_path)
        if homework.strip():
            all_homework += f"**{file}**\n{homework}\n"
        else:
            all_homework += f"**{file}**: No more homework to extract.\n"

    post_to_discord(all_homework)

schedule.every().tuesday.at("18:00").do(weekly_task)

while True:
    schedule.run_pending()
    time.sleep(1)
