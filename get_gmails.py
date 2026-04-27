# import libraries
from imap_tools import MailBox, MailboxLoginError
import os
import logging
from dotenv import load_dotenv
from datetime import date

# gets the environment variables for the app passwor and email
load_dotenv()
APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')
EMAIL = os.getenv('EMAIL')

gmail_email = 'samanthagrief2@gmail.com'
gmail_password = 'igpeoahxnlzhglty'
gmail_url = 'imap.gmail.com'

logging.basicConfig(filename="email_errors.log",
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    )

# sets a count for 1
count = 1

# gets the current date
current_date = date.today()

# creates a folder with the name as the current date
# first checks if the folder already exists
folder_path = f"test_emails/{current_date}"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# access the gmail inbox of the email using MailBox
# fetches all the emails and loops through all the emails
# creates a text file for each email
# each text file writes the from, subject, date, and text of the email
try:
    with MailBox(gmail_url).login(gmail_email, gmail_password, "Inbox") as mb:
        try:
            for msg in mb.fetch():
                try:
                    with open(f'{folder_path}/email_{count}.txt', 'w') as file:
                        file.write(f"{msg.from_}\n{msg.subject}\n{msg.date}\n{msg.text}")
                    count += 1
                except Exception as e:
                    logging.error(f"An error occurred while converting while writing to  file {e}")
        except Exception as e:
            logging.error(f"An error occurred while fetching emails {e}")
except MailboxLoginError as e:
    logging.error(f"An error occurred while logging in {e}")
except Exception as e:
    logging.error(f"Unexpected error: {e}")




