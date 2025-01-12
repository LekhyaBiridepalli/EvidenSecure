# EvidenSecure: Secure Digital Evidence Management Platform

**EvidenSecure** is a robust web-based platform designed for law enforcement to securely manage digital evidence. This project ensures the confidentiality, integrity, and security of evidence while providing advanced features like immutable evidence, secure file storage, and user authentication.

---

## Contributors

- [Ifrah Naaz](https://github.com/ifrahnz26)  
- [Lekhya Beridapalli](https://github.com/LekhyaBiridepalli)
- [Ishika Mohol](https://github.com/justishika)

---

## Features

### General Features:
- **Evidence Management**: Secure upload and storage of evidence files using MongoDB GridFS.
- **Immutable Evidence**: Evidence cannot be altered after submission; additional details can only be appended.
- **User Authentication**: Role-based login for admins and investigators.

### Implemented CNS Aspects:
1. **Encryption of Sensitive Data**:  
   - Uses AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode to encrypt evidence and case details.  

2. **Immutable Evidence**:  
   - Ensures evidence integrity by preventing modifications to original files while allowing appends.  

3. **Password Hashing**:  
   - Hashes passwords using Django's `make_password` method and verifies them with `check_password`.  

4. **Secure Storage**:  
   - Utilizes MongoDB GridFS for storing large forensic files securely with encryption.  

5. **CSRF Protection**:  
   - Prevents unauthorized commands using Django's default CSRF protection.

---

## Screenshots

![Dashboard]()
![Evidence Upload]()
![Case Management]()

---

## Prerequisites

- Python 3.8+
- MongoDB 4.4+
- Django 4.0+
- pip (Python package manager)

---

## Project Setup

### Step 1: Clone the Repository
1. Clone the repository:  
   ```bash
   git clone https://github.com/ifrahnz26/evidensecure.git
2. Navigate to the Project Directory
   ```bash
   cd evidensecure

### Step 2: Install Required Dependencies
1. Install all necessary dependencies using the requirements.txt file:
   ```bash
   pip install -r requirements.txt
2. If you don’t have the requirements.txt file, generate it:
    ```bash
   pip freeze > requirements.txt

### Step 3: Set Up the Database
1. Start MongoDB:
   ```bash
   mongod 
2. Connect to MongoDB using the following settings:
   Database Name: EvidenSecure_db
   Sample Python connection:
   ```bash
   from pymongo import MongoClient
   client = MongoClient('mongodb://localhost:27017/')
   db = client['EvidenSecure_db']
3. Import sample data if available:
   ```bash
   mongoimport --db EvidenSecure_db --collection users --file sample-users.json

### Step 4: Configure the Project
1. Update database settings in settings.py:
   ```bash
   DATABASES = {
        'default': {
                   'ENGINE': 'djongo',
                   'NAME': 'EvidenSecure_db',
         }
   }

### Step 5: Run the Application
1. Apply migrations:
   ```bash
   python manage.py migrate
2. Start the development server:
   ```bash
   python manage.py runserver
3. Access the application at:
    [http://127.0.0.1:8000](..)

---

## Database Design
### Collections
1. Users: Stores user information like name, email, and hashed passwords.
2. Evidence: Manages evidence files and associated metadata.
3. Cases: Tracks cases linked to evidence and investigators.

---

## Technologies Used
1. Frontend: HTML, CSS, JavaScript
2. Backend: Django
3. Database: MongoDB
4. Server: Django Development Server
5. Tools: Python, GridFS

---

## License
This project is licensed under the [MIT License](https://github.com/ifrahnz26/EvidenSecure/blob/main/LICENSE).
