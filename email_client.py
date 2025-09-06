# Link to add app password -- https://myaccount.google.com/apppasswords?rapt=AEjHL4PHwK2i8gRH3cftzAYssw0vkt1Xas4Qds6l5KEKNLi8kQSYOPh4ZGcOs27nBz-rDdXkD0ATWGNwp3anwU_hJb_dO7e6oKNxaAQr7bqKa1ise7x6Ers
import imaplib2
from email import message_from_bytes
from queue import Queue
from database import DataBase
from sentiment import cal_urgency
from auto_reply import response
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class Mail:
    mails = Queue(maxsize=0)
    ssl_server = 'imap.gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    db = DataBase()
    
    def __init__(self, email, password):
        try:
            self.imap = imaplib2.IMAP4_SSL(self.ssl_server)
            res = self.imap.login(email, password)
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(email, password)

            print(res)
        except Exception as e:
            print(e)
    
    def listener(self):
        try:
            self.imap.select('INBOX')
            while(True):
                print("Waiting for new mails")
                self.imap.idle(timeout=3600)
                typ, data = self.imap.search(None,'UNSEEN')
                print(typ)
                if typ == 'OK':
                    uid = ','.join(data[0].decode().split())
                    _, mail = self.imap.fetch(uid, 'RFC822')
                    for response_part in mail:
                        if isinstance(response_part, tuple):
                            self.mails.put(response_part[1])
                        
                
        except Exception as e:
            print(e)

    def operations(self):
        while(True):
            raw_msg = self.mails.get(block=True)
            msg = message_from_bytes(raw_msg)
            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain' and not part.get('Content-Disposition'):
                        payload = part.get_payload(decode=True)
                        if payload is not None:
                            charset = part.get_content_charset() or 'utf-8'
                            body = payload.decode(charset)
                            break
            else:
                payload = msg.get_payload(decode=True)
                if payload is not None:
                    charset = msg.get_content_charset() or 'utf-8'
                    body = payload.decode(charset)

            # Categorization Logic
            category = ['ACCOUNT', 'CONTACT', 'FEEDBACK', 'ORDER', 'PAYMENT', 'REFUND']
            subject = msg['subject'].lower()
            query = f"subject: {subject} " + f"body: {body}"
            category, auto_rep = response(msg['from'],query)
            urgency = cal_urgency(subject, body, category)
            self.db.insertOne(msg['from'],msg['to'],msg['cc'],msg['subject'],msg['date'],body,category,auto_rep,urgency)
    
        

    def reply(self, email_id, reply_text):
        mail = self.db.get_email_by_id(email_id)
        if not mail:
            print("Email not found")
            return False

        # Check if already replied
        if mail['replied'] == 'yes':
            print("Already replied to this email")
            return False

        sender_email = mail.get('reciever')
        recipient_email = mail.get('sender')
        subject = "Re: " + mail.get('subject', '')
        message_id = mail.get('message_id', None)  # If you store this

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        if message_id:
            msg['In-Reply-To'] = message_id
            msg['References'] = message_id
        msg.attach(MIMEText(reply_text, 'plain'))

        try:
            self.server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Reply sent successfully")
            return True
        except Exception as e:
            print("Failed to send reply:", e)
            return False


