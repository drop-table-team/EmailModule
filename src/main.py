import asyncio
import imaplib
import email
import os
from email.header import decode_header

import aioimaplib

from src.ai.ai import extract_email_info
from src.classes.email_class import Email

from src.api import router

USERNAME = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("EMAIL_IMAP")

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

        return Email(mail_subject, mail_from, mail_text, mail_html)

async def main():
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(USERNAME, PASSWORD)

    status, messages = imap.select()

    message_count = int(messages[0])
    print(message_count)

    for i in range(message_count, 0, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        print(len(msg))
        for response_part in msg:
            print(response_part)
            entry = find_data(response_part)
            info = extract_email_info(entry)
            # print(info)
            # await router.store_backend(info, entry.mail_html)


    typ, data = imap.search(None, 'ALL')
    for num in data[0].split():
        imap.store(num, '+FLAGS', '\\Deleted')
    # imap.expunge()
    # imap.close()
    imap.logout()

if __name__ == "__main__":
    asyncio.run(main())
