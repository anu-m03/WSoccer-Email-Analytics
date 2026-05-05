# import libraries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import logging
import pandas as pd
from imap_tools import MailBox, MailboxLoginError
import os
from dotenv import load_dotenv

# create a logging file
logging.basicConfig(filename="email_errors.log",
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s'
                    )

# all receiver emails
receiver_email = ["sgrief@purdue.edu", "nguy1051@purdue.edu", "liu3951@purdue.edu"]

# get email and password
load_dotenv()
APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')
EMAIL = os.getenv('EMAIL')

# url for gmail
gmail_url = 'imap.gmail.com'

# get today's date and format the date
today = date.today()
date_tag = today.strftime("%-d_%b_%Y")

# create a message with a from, to, and subject
message = MIMEMultipart()
message["From"] = EMAIL
message["To"] = ", ".join(receiver_email)
message["Subject"] = "Email Analysis"

# add a body to the email
body = "Email Analysis attached"
message.attach(MIMEText(body, "plain"))

# list of all attached files
files = [f"results/Achievement_Details_{date_tag}.csv",
         f"results/Keyword_Candidates_{date_tag}.csv",
         f"results/Player_Data_{date_tag}.csv",
         f"results/Promoted_Players_{date_tag}.csv",
         "results/strength_histogram.png",
         "results/strength_scores.png",
         "email_errors.log"]

# attach all files to the email
for file in files:
    try:
        attachment = open(file, "rb")

        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {file}")

        message.attach(p)
    except Exception as e:
        logging.error(f"Error occurred while attaching file {e}")

# convert message to byte format
message_bytes = message.as_bytes()

# read the player data csv and get the file_name and promoted columns
player_data = pd.read_csv(f"results/Player_Data_{date_tag}.csv", usecols=["file_name", "promoted"])

# add report to emails
# loop through data frame and move each email to the designated folder
try:
    with MailBox(gmail_url).login(EMAIL, APP_PASSWORD, "Inbox") as mb:
        try:
            mb.append(message_bytes, "reports")
        except Exception as e:
            logging.error(f"An error occurred while adding report {e}")
        for row in player_data.itertuples():
            try:
                uid = row.file_name.replace(".txt", "")
                if (row.promoted == 1):
                    mb.move(uid, "promoted")
                else:
                    mb.move(uid, "not promoted")
            except Exception as e:
                logging.error(f"An error occurred while moving email {e}")
except MailboxLoginError as e:
    logging.error(f"An error occurred while logging in {e}")
except Exception as e:
    logging.error(f"Unexpected error: {e}")

server = None

# send email with the reports
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)

    server.sendmail(EMAIL, receiver_email, message.as_string())
except Exception as e:
    logging.error(f"Error occurred while sending email: {e}")
finally:
    server.quit()
