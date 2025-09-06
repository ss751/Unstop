# Unstop - AI-Powered Email Management System

An intelligent email management system that automatically categorizes, analyzes, and generates responses for incoming emails using AI and machine learning technologies.

# Video link for working project
[text](https://drive.google.com/file/d/1Kjt3mugSNC_0GE4wk5MjZWK_1FqhTbtp/view?usp=drive_link)


## 🚀 Features

- **Real-time Email Monitoring**: Continuously monitors Gmail inbox for new emails using IMAP
- **AI-Powered Email Categorization**: Automatically categorizes emails into predefined categories (Account, Contact, Feedback, Order, Payment, Refund)
- **Intelligent Auto-Reply**: Generates contextual responses using Google's Gemini AI with RAG (Retrieval-Augmented Generation)
- **Sentiment Analysis**: Analyzes email sentiment using BERT-based multilingual models
- **Urgency Scoring**: Calculates email priority based on content, category, and sentiment
- **Web Interface**: Gmail-like interface for viewing and managing emails
- **Reply Management**: Track and manage email responses with status updates

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: MongoDB
- **AI/ML**: 
  - Transformers (BERT for sentiment analysis)
  - SentenceTransformers (for semantic search)
  - FAISS (for vector similarity search)
  - Google Gemini API (for response generation)
- **Email**: IMAP/SMTP for Gmail integration
- **Frontend**: HTML, CSS, JavaScript

## 📁 Project Structure

```
src/
├── app.py              # Flask web application
├── email_client.py     # Email monitoring and operations
├── database.py         # MongoDB database operations
├── sentiment.py        # Sentiment analysis and urgency calculation
├── auto_reply.py       # AI-powered response generation
├── templates/          # HTML templates
│   ├── index.html      # Main email interface
│   └── email_view.html # Email detail view
├── static/             # CSS and JavaScript files
└── data/               # Training data and FAISS index
    ├── cust_support.csv
    └── faiss.index
```

## ⚙️ Setup and Installation

### Prerequisites
- Python 3.7+ (3.13.5 recommended)
- MongoDB
- Gmail account with App Password enabled (**Make sure your gmail account has two factor authentication on**)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ss751/Unstop.git
   cd Unstop
   ```

2. **Install dependencies**
   ```bash
   pip install flask pymongo transformers sentence-transformers faiss-cpu google-generativeai python-dotenv imaplib2
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   email=your_gmail@gmail.com
   password=your_app_password
   api_key=your_gemini_api_key
   ```

4. **Configure Gmail App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Generate an App Password for the application

5. **Start MongoDB**
   ```bash
   mongod
   ```

6. **Run the application**
   ```bash
   cd src
   python app.py
   ```

## 🎯 How It Works

1. **Email Monitoring**: The system continuously monitors your Gmail inbox using IMAP
2. **Processing Pipeline**: 
   - Extracts email content and metadata
   - Categorizes emails using similarity search with customer support dataset
   - Analyzes sentiment and calculates urgency scores
   - Generates AI-powered responses using Gemini API
3. **Storage**: All processed emails are stored in MongoDB with metadata
4. **Web Interface**: View, manage, and reply to emails through the web interface

## 🔧 Configuration

### Email Categories
- **ACCOUNT**: Account-related inquiries
- **CONTACT**: General contact requests
- **FEEDBACK**: Customer feedback and reviews  
- **ORDER**: Order-related queries
- **PAYMENT**: Payment and billing issues
- **REFUND**: Refund requests and processing

### Urgency Calculation
The system calculates urgency scores based on:
- Category priority weights
- Keyword analysis in subject lines
- Sentiment analysis of email body
- Combined scoring for prioritization

## 🌐 API Endpoints

- `GET /` - Main email interface
- `GET /api/emails` - Fetch all emails
- `GET /api/emails/<id>` - View specific email
- `POST /api/emails/<id>/mark_read` - Mark email as read
- `POST /api/emails/<id>/reply` - Send reply to email
- `GET /api/pending_mails` - Get emails pending replies

## 📊 Features in Detail

### Intelligent Response Generation
- Uses RAG with customer support dataset
- Contextual responses based on email category
- Professional tone with personalized greetings
- Maintains conversation history

### Real-time Processing
- Multi-threaded architecture for concurrent email processing
- Automatic email categorization and response generation
- Real-time status updates and notifications

## 🤝 Contributing

This project was developed as part of the Unstop AI Engineer Fresher Challenge. Contributions and improvements are welcome!

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Links

- [Gmail App Passwords Setup](https://myaccount.google.com/apppasswords)
- [MongoDB Installation Guide](https://docs.mongodb.com/manual/installation/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)

Not enough time to complete documentation and dashboard feature mentioned in challenge.