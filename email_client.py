# Link to add app password -- https://myaccount.google.com/apppasswords?rapt=AEjHL4PHwK2i8gRH3cftzAYssw0vkt1Xas4Qds6l5KEKNLi8kQSYOPh4ZGcOs27nBz-rDdXkD0ATWGNwp3anwU_hJb_dO7e6oKNxaAQr7bqKa1ise7x6Ers
import imaplib2
from email import message_from_bytes
from queue import Queue
from database import DataBase


class Mail:
    mails = Queue(maxsize=0)
    ssl_server = 'imap.gmail.com'
    db = DataBase()
    def __init__(self, email, password):
        try:
            self.imap = imaplib2.IMAP4_SSL(self.ssl_server)
            res = self.imap.login(email, password)
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
            category = ['Support','Help', 'Query','Request']
            subject = msg['subject'].lower()
            mail_category = None
            for cat in category:
                if cat.lower() in subject:
                    mail_category = cat
                    break
            if mail_category is None:
                mail_category = 'General'
               
            self.db.insertOne(msg['from'],msg['to'],msg['cc'],msg['subject'],msg['date'],body,mail_category,'','')
