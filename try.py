import imaplib2
from email import message_from_bytes, policy

from dotenv import load_dotenv
import os 


ssl_server = 'imap.gmail.com'
imap = imaplib2.IMAP4_SSL(ssl_server)

load_dotenv()
email = os.getenv('email')
password = os.getenv('password')
    
try:
    res = imap.login(email, password)
    print(res)
except Exception as e:
     print(e)

imap.select("INBOX")
_, mail = imap.fetch('1,2,3', 'RFC822')
for response_part in mail:
    if isinstance(response_part, tuple):
        msg = message_from_bytes(response_part[1])  # This is the message data in bytes
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

        print(body)
        print('================================================')



# from database import DataBase

# m = DataBase()
# m.insertOne('shreyas@gmail.com','xyz','2q3452345','2345i234jk5lh23klj45 23kj45h2o34i58720394 5j','ajsdfkoeir')
# for i in m.fetchAll():
#     print(i)


from queue import PriorityQueue

pq = PriorityQueue()

pq.put(0,'1')
pq.put(5,'2')
pq.put(2,'3')


print(pq.get())
print(pq.get())
print(pq.get())


