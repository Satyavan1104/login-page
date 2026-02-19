# Registration and Login Application

A secure registration and login application that connects to an Aiven MySQL database. The application features password hashing and session management.

## Features

- User registration with email, password, name, and optional phone number
- Secure password hashing using bcrypt
- User login with session management
- Responsive design with Bootstrap 5
- Flash messages for user feedback
- Automatic redirection after registration/login

## Prerequisites

- Python 3.7+
- Aiven MySQL database
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd login-app
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the database credentials with your Aiven MySQL details
   - Set a strong `SECRET_KEY`

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Database Setup

The application will automatically create the necessary `User` table with the following structure:

```sql
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);
```

## Security Notes

- Passwords are hashed using bcrypt before being stored in the database
- Session management is handled by Flask with a secure secret key
- Environment variables are used to store sensitive information
- SQL injection is prevented using parameterized queries

## License

This project is open source and available under the MIT License.
