from flask import Flask, render_template, request, jsonify
from database import DataBase 
import re
from email_client import Mail
from threading import Thread
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

app = Flask(__name__)
db = DataBase()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/emails')
def api_emails():
    emails = db.fetchAll()
    for mail in emails:
        mail['_id'] = str(mail['_id'])
    return jsonify(emails)

def parse_sender(sender_str):
    match = re.match(r'(.+?)\s*<(.+?)>', sender_str)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return sender_str, ""

@app.route('/api/emails/<email_id>')
def view_email(email_id):
    email = db.get_email_by_id(email_id)
    if not email:
        return "Email not found", 404
    email['_id'] = str(email['_id'])
    sender_name, sender_email = parse_sender(email.get('sender', ''))
    return render_template('email_view.html', email=email, sender_name=sender_name, sender_email=sender_email)

@app.route('/api/emails/<email_id>/mark_read', methods=['POST'])
def mark_email_read(email_id):
    db.collection.update_one({'_id': ObjectId(email_id)}, {'$set': {'status': 'read'}})
    return jsonify({'success': True})

if __name__ == '__main__':
    load_dotenv()
    email = os.getenv('email')
    password = os.getenv('password')

    m = Mail(email, password)
    Thread1 = Thread(target=m.listener, daemon=True)
    Thread2 = Thread(target=m.operations, daemon=True)

    Thread1.start()
    Thread2.start()

    app.run(debug=True)



