class Email:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, mail_subject, mail_from, mail_text, mail_html):
        self.mail_subject = mail_subject
        self.mail_from = mail_from
        self.mail_text = mail_text
        self.mail_html = mail_html


    def __str__(self):
        return f"Subject: {self.mail_subject}\nFrom: {self.mail_from}\n\n{self.mail_text}"
