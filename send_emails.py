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

# get email and password
load_dotenv()

# all receiver emails (REPORT_RECIPIENTS="a@x.com,b@y.com" overrides them for test sends)
receiver_email = ["sgrief@purdue.edu", "nguy1051@purdue.edu", "liu3951@purdue.edu"]
if os.getenv("REPORT_RECIPIENTS"):
    receiver_email = [r.strip() for r in os.getenv("REPORT_RECIPIENTS").split(",") if r.strip()]
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

# count errors logged so far this run (fetching emails, analysis)
n_errors = 0
if os.path.exists("email_errors.log"):
    with open("email_errors.log", encoding="utf-8", errors="ignore") as log:
        n_errors = sum(1 for line in log if " - ERROR - " in line)

# add a body to the email: the summary written by testing_main.py
summary_file = f"results/Report_Summary_{date_tag}.html"
if os.path.exists(summary_file):
    with open(summary_file, encoding="utf-8") as f:
        body = f.read()
else:
    logging.error(f"Summary file not found: {summary_file}")
    body = "<p>Email Analysis attached</p>"
errors_html = ""
if n_errors:
    errors_html = (f"<p style='color:#b00020'><b>&#9888; {n_errors} error(s) during this run</b> "
                   "&mdash; see email_errors.log (attached).</p>")
body = body.replace("<!--ERRORS-->", errors_html) if "<!--ERRORS-->" in body else errors_html + body
message.attach(MIMEText(body, "html"))

# list of all attached files: the coach-facing workbook, plus keyword candidates
# for the team's keyword/scoring tuning
files = [f"results/Recruiting_Report_{date_tag}.xlsx",
         f"results/Keyword_Candidates_{date_tag}.csv"]
if n_errors:
    files.append("email_errors.log")

# attach all files to the email
for file in files:
    if not os.path.exists(file):
        logging.error(f"File not found, skipping: {file}")
        continue  # skip to next file instead of crashing
    try:
        with open(file, "rb") as attachment:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file)}")
            message.attach(p)
    except Exception as e:
        logging.error(f"Error occurred while attaching file {file}: {e}")

# convert message to byte format
message_bytes = message.as_bytes()

# read the player data csv and get the file_name and promoted columns
player_data = None
player_data_file = f"results/Player_Data_{date_tag}.csv"
if os.path.exists(player_data_file):
    player_data = pd.read_csv(player_data_file, usecols=["file_name", "promoted"])
else:
    logging.error(f"Player data file not found: {player_data_file}")

# add report to emails
# loop through data frame and move each email to the designated folder
try:
    with MailBox(gmail_url).login(EMAIL, APP_PASSWORD, "Inbox") as mb:
        try:
            mb.append(message_bytes, "reports")
        except Exception as e:
            logging.error(f"An error occurred while adding report {e}")
        if player_data is not None:
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
    if server:
        server.quit()
