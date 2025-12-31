# Electrical Machines Q&A Platform

A full-stack web application built with Django and MySQL that allows users to ask questions about electrical machines and receive AI-powered answers using the Groq API (Llama 3.3 70B model).

## 🚀 Features

- **User Authentication**: Complete registration and login system
- **Question Management**: Ask and browse questions about electrical machines
- **AI-Powered Answers**: Real-time answers using Llama 3.3 70B AI model via Groq API
- **Category System**: Organized by topics (DC Machines, AC Machines, Transformers, etc.)
- **Admin Dashboard**: Full administrative control panel
- **Responsive Design**: Beautiful gradient UI that works on all devices
- **MySQL Database**: Robust data storage with proper relationships

## 📊 Database Statistics

- **Users**: 13 (including admin and sample users)
- **Questions**: 22+ (including AI-generated and user-submitted)
- **Answers**: 22+ (AI-generated responses)
- **Categories**: 6 (General, DC Machines, AC Machines, Transformers, Induction Motors, Synchronous Machines)

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL 8.0
- **AI Model**: Llama 3.3 70B (via Groq API)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Authentication**: Django built-in auth system
- **API Integration**: Groq REST API
- **Python Version**: 3.11.9

## 📋 Prerequisites

- Python 3.11+
- MySQL 8.0+
- Groq API Key (free from https://console.groq.com/)
- Windows/Linux/Mac OS

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd electrical_qa
```

### 2. Install MySQL

**For Windows:**
1. Download from: https://dev.mysql.com/downloads/installer/
2. Run installer and choose "Developer Default"
3. Set root password
4. Start MySQL service

**For Ubuntu:**
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 3. Create MySQL Database

```bash
mysql -u root -p
```

Then in MySQL:
```sql
CREATE DATABASE electrical_qa_db;
CREATE USER 'qauser'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON electrical_qa_db.* TO 'qauser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Install Python Dependencies

```bash
pip install Django==4.2.7 PyMySQL cryptography python-decouple requests
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_NAME=electrical_qa_db
DB_USER=qauser
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=3306

# Groq API Key (Get from https://console.groq.com/)
GROQ_API_KEY=your_groq_api_key_here

# Django Secret Key
SECRET_KEY=your_django_secret_key_here

# Debug Mode
DEBUG=True
```

**To generate Django SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Create Database Tables

```bash
python backend.py migrate
```

### 7. Create Superuser (Admin)

```bash
python backend.py createsuperuser
```

Enter:
- Username: admin
- Email: admin@example.com
- Password: (your choice)

### 8. Create Sample Data (Optional)

The database already contains 13 users and 22+ questions. To add more:

```bash
python backend.py shell
```

Then run the provided seed script in the shell.

### 9. Run the Application

```bash
python backend.py runserver
```

Visit: **http://localhost:8000**

## 📁 Project Structure

```
electrical_qa/
├── backend.py              # Main Django application (all-in-one)
├── .env                    # Environment variables (DO NOT COMMIT)
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── templates/             # HTML templates
    ├── base.html          # Base template with navbar
    ├── home.html          # Homepage
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── ask.html           # Ask question page
    ├── questions.html     # Questions list
    └── answer.html        # Question detail with answer
```

## 💾 Database Schema

### Users Table (auth_user)
- id (Primary Key)
- username
- email
- first_name
- last_name
- password (hashed)

### Questions Table
- id (Primary Key)
- user_id (Foreign Key → auth_user)
- question_text
- category
- created_at
- updated_at

### Answers Table
- id (Primary Key)
- question_id (Foreign Key → questions)
- answer_text
- source
- confidence_score
- created_at

## 🌐 Application URLs

- **Homepage**: http://localhost:8000/
- **Login**: http://localhost:8000/login/
- **Register**: http://localhost:8000/register/
- **Ask Question**: http://localhost:8000/ask/
- **Questions List**: http://localhost:8000/questions/
- **Admin Panel**: http://localhost:8000/admin/

## 🤖 AI Integration

The application uses **Groq API** with the **Llama 3.3 70B** model for generating answers:

- **Model**: llama-3.3-70b-versatile
- **Provider**: Groq (https://groq.com)
- **Response Time**: 2-5 seconds
- **Quality**: High-quality, contextual answers
- **Rate Limit**: Free tier provides generous limits

### How It Works:
1. User submits a question
2. Application sends question to Groq API
3. Llama 3.3 processes the question
4. AI generates a detailed answer
5. Answer is stored in database and displayed

## 👥 Sample Users

The application includes 13 pre-created users for testing:

| Username | Email | Password |
|----------|-------|----------|
| admin | admin@example.com | (your superuser password) |
| john_doe | john@email.com | password123 |
| jane_smith | jane@email.com | password123 |
| mike_wilson | mike@email.com | password123 |
| sarah_jones | sarah@email.com | password123 |
| david_brown | david@email.com | password123 |
| emma_davis | emma@email.com | password123 |
| chris_miller | chris@email.com | password123 |
| lisa_garcia | lisa@email.com | password123 |
| tom_rodriguez | tom@email.com | password123 |
| amy_martinez | amy@email.com | password123 |

## 📚 Sample Questions

Pre-loaded questions include:
- What is the difference between AC and DC motors?
- How does a transformer work?
- What are the main components of an induction motor?
- Explain the working principle of a synchronous generator
- What causes armature reaction in DC machines?
- How to calculate efficiency of electrical machines?
- What is slip in an induction motor?
- Explain power factor in AC machines
- What are transformer losses?
- How does DC motor speed control work?

## 🔒 Security Features

- ✅ Password hashing (Django's built-in PBKDF2)
- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Session management
- ✅ Environment variable for sensitive data

## 📝 Code Standards

- **PEP 8 Compliant**: All code follows Python style guidelines
- **Well Documented**: Comprehensive docstrings and comments
- **Type Hints**: Used where appropriate
- **Error Handling**: Proper exception handling throughout
- **Logging**: INFO level logging for debugging

## 🐛 Troubleshooting

### MySQL Connection Error
```bash
# Check if MySQL is running
# Windows:
net start MySQL80

# Ubuntu:
sudo systemctl status mysql
```

### API Key Error
- Verify GROQ_API_KEY in .env file
- Get new key from https://console.groq.com/

### Port Already in Use
```bash
# Use a different port
python backend.py runserver 8001
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 🚀 Deployment on Ubuntu

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies
```bash
sudo apt install python3-pip python3-venv mysql-server nginx -y
```

### 3. Clone Project
```bash
git clone <your-repo-url>
cd electrical_qa
```

### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure MySQL
```bash
sudo mysql_secure_installation
mysql -u root -p < setup.sql
```

### 6. Setup .env File
```bash
nano .env
# Add your production settings
```

### 7. Run Migrations
```bash
python backend.py migrate
python backend.py createsuperuser
```

### 8. Collect Static Files
```bash
python backend.py collectstatic
```

### 9. Configure Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 backend:application
```

### 10. Configure Nginx (Optional)
```bash
sudo nano /etc/nginx/sites-available/electrical_qa
# Add your Nginx configuration
sudo ln -s /etc/nginx/sites-available/electrical_qa /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 11. Setup Systemd Service
```bash
sudo nano /etc/systemd/system/electrical_qa.service
# Add service configuration
sudo systemctl start electrical_qa
sudo systemctl enable electrical_qa
```

## 📊 Performance

- **Page Load**: < 1 second
- **AI Response**: 2-5 seconds
- **Database Queries**: Optimized with Django ORM
- **Concurrent Users**: Supports multiple users
- **Scalability**: Can be scaled horizontally

## 🤝 Contributing

This project was created as part of an internship assignment. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is created for educational purposes as part of an internship assignment.

## 👨‍💻 Author

**ksr**
- Email: srihari95027@gmail.com
- GitHub: [ksr2005]

## 🙏 Acknowledgments

- Django Documentation
- Groq AI Platform
- MySQL Community
- Bootstrap Framework

## 📞 Support


**Built with ❤️ using Django, MySQL, and Groq AI**
