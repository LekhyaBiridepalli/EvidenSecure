# **EvidenSecure: Secure Digital Evidence Management Platform**

EvidenSecure is a robust web-based platform designed for law enforcement agencies to securely manage digital evidence. This project ensures the confidentiality, integrity, and security of evidence while providing advanced features such as immutable evidence, secure file storage, and role-based user authentication.

---

## **Contributors**

- [Ifrah Naaz](https://github.com/ifrahnz26)  - 1MS22CS064
- [Lekhya Biridapalli](https://github.com/LekhyaBiridepalli)  - 1MS22CS079
- [Ishika Mohol](https://github.com/justishika)  - 1MS22CS069

---

## **Features**

### **General Features**
- **Evidence Management**: Secure upload and storage of evidence files using MongoDB GridFS.  
- **Immutable Evidence**: Ensures that evidence cannot be altered after submission; additional details can only be appended.  
- **User Authentication**: Implements role-based login for admins and investigators.

### **Implemented CNS Aspects**
1. **Encryption of Sensitive Data**:  
   - Utilizes AES (Advanced Encryption Standard) in CBC (Cipher Block Chaining) mode to encrypt evidence and case details.

2. **Immutable Evidence**:  
   - Protects evidence integrity by preventing modifications to original files while allowing appending additional details.

3. **Password Hashing**:  
   - Employs Django’s `make_password` method to hash passwords and verifies them using `check_password`.

4. **Secure File Storage**:  
   - Uses MongoDB GridFS to store large forensic files securely with encryption.

5. **CSRF Protection**:  
   - Prevents unauthorized access using Django’s built-in CSRF protection mechanism.

---

## **Screenshots**
<img width="300" height ="200" alt="Screenshot 2025-01-12 at 6 22 59 PM" src="https://github.com/user-attachments/assets/a2e24a52-f88a-42bd-bace-300b832a9913" />
<img width="300" height ="200" alt="Screenshot 2025-01-12 at 6 23 20 PM" src="https://github.com/user-attachments/assets/89788f6a-4ca2-404d-a3f6-884dbc48f485" />
<img width="300" height ="200"  alt="Screenshot 2025-01-12 at 6 23 41 PM" src="https://github.com/user-attachments/assets/8bf511cd-9415-42da-bb66-7588491b57e5" />
<img width="300" height ="200" alt="Screenshot 2025-01-12 at 6 40 43 PM" src="https://github.com/user-attachments/assets/30160d16-947a-44f1-a039-989afa0f026f" />
<img width="300" height ="200" alt="Screenshot 2025-01-12 at 6 35 43 PM" src="https://github.com/user-attachments/assets/c3beac41-29ab-4a37-a5e3-24d6d0712046" />
<img width="300" height ="200" alt="Screenshot 2025-01-12 at 6 40 28 PM" src="https://github.com/user-attachments/assets/a30d2c60-075e-4738-99f8-5ae9d2a7cac1" />

---

## **Prerequisites**

- **Python** 3.8+  
- **MongoDB** 4.4+  
- **Django** 4.0+  
- **pip** (Python package manager)  

---

## **Project Setup**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/ifrahnz26/evidensecure.git
```

### **Step 2: Install Required Dependencies**
1. Install the required dependencies using the `requirements.txt` file:  
   ```bash
   pip install -r requirements.txt
   ```

2. If the `requirements.txt` file is unavailable, generate it:  
   ```bash
   pip freeze > requirements.txt
   ```

### **Step 3: Set Up the Database**
1. Start MongoDB:  
   ```bash
   mongod
   ```

2. Connect to MongoDB using the following settings:  
   - **Database Name**: `EvidenSecure_db`  
   - Example Python connection:  
     ```python
     from pymongo import MongoClient
     client = MongoClient('mongodb://localhost:27017/')
     db = client['EvidenSecure_db']
     ```

### **Step 4: Run the Application**
1. Apply migrations:  
   ```bash
   python manage.py migrate
   ```

2. Start the development server:  
   ```bash
   python manage.py runserver
   ```

3. Access the application at:  
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## **Database Design**

### **Collections**
- **Users**: Stores user details such as name, email, and hashed passwords.  
- **Evidence**: Manages evidence files and associated metadata.  
- **Cases**: Tracks cases and their linkage to evidence and investigators.  


---

## **Technologies Used**

### **Frontend**  
- HTML  
- CSS  
- JavaScript  

### **Backend**  
- Django  

### **Database**  
- MongoDB  

### **Server**  
- Django Development Server  

### **Tools**  
- Python  
- GridFS  

---

## **License**

This project is licensed under the [MIT License](LICENSE).  

---
