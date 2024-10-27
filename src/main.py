import imaplib
import email
import os
from email.header import decode_header

from src.api import router

USERNAME = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")

def decode_msg(string, message):
    subject, encoding = decode_header(message[string])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)

    return subject

def find_data(response_part):
    if isinstance(response_part, tuple):
        email_message = email.message_from_bytes(response_part[1])

        mail_subject = decode_msg("Subject", email_message)
        mail_from = decode_msg("From", email_message)

        mail_text = ""
        mail_html = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                body = ""
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    mail_text = body
                if content_type == "text/html" and "attachment" not in content_disposition:
                    mail_html = body
        else:
            content_type = email_message.get_content_type()
            body = email_message.get_payload(decode=True).decode()
            if content_type == "text/plain":
                mail_text = body
            if content_type == "text/html":
                mail_html = body

        if not mail_html and mail_text:
            mail_html = f"<html><body><pre>{mail_text}</pre></body></html>"

        return mail_subject, mail_from, mail_text, mail_html

def main():
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(USERNAME, PASSWORD)

    status, messages = imap.select("INBOX")

    messages = int(messages[0])
    print(f"Messages: {messages}")
    current_mails = []

    for i in range(messages, 0, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response_part in msg:
            current_mails.append(find_data(response_part))

    for i in range(len(current_mails)):
        router.store_backend(current_mails[i])

    imap.close()
    imap.logout()

main()
