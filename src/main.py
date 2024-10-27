import imaplib
import email
from email.header import decode_header
from mypy.state import state
from nltk.misc.chomsky import subjects
import os

from sympy import content


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

        print("Subject:", mail_subject)
        print("From:", mail_from)

        mail_text = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    mail_text = body
        else:
            content_type = email_message.get_content_type()
            body = email_message.get_payload(decode=True).decode()
            if content_type == "text/plain":
                mail_text = body
        return mail_subject, mail_from, mail_text

def quitImap(imap):
    imap.close()
    imap.logout()

username = "knowledge@mailo.com"
password = "knowledge-2024"
imap_server = "mail.mailo.com"

def main():
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)

    status, messages = imap.select("INBOX")

    N = 1

    messages = int(messages[0])

    current_mails = []

    for i in range (messages, messages-N, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response_part in msg:
            current_mails.append(find_data(response_part))


    quitImap(imap)

main()
