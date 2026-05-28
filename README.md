# CustomTkinter Password Manager

A modern, secure Python GUI desktop application built with `customtkinter` that allows users to manage their credentials safely. The application integrates with a local MySQL database for data persistence and features an OTP (One-Time Password) email verification system for secure account creation and login.

---

## 🚀 Features

* **Modern UI:** Built using `customtkinter` for a sleek, responsive desktop interface.
* **Secure Authentication:** User registration and login secured via **Email OTP Verification** to ensure account ownership.
* **Credential Storage:** Securely save, view, and manage website URLs, usernames, and passwords.
* **Password Generator:** Built-in tool to generate strong, random passwords to improve credential security.
* **Database Integration:** Powered by a **MySQL** backend running locally to store and retrieve user credentials reliably.

---

## 🔍 How It Works

The application operates through a structured flow combining the local frontend UI, a local database, and an external email relay:

### 1. Database & Environment Initialization
* When the application starts, it reads configuration details (database credentials, SMTP details) from the local `.env` file.
* It establishes a secure, local connection to your MySQL server (`localhost`) to prepare for user queries.

### 2. User Authentication & Registration (with OTP)
* **Sign Up:** When a new user registers, the application captures their email and generates a unique, time-sensitive **One-Time Password (OTP)** in the backend. 
* **SMTP Relay:** Using Python's built-in email handling libraries, the app securely logs into your configured Gmail SMTP server using an App Password and dispatches the OTP to the user's email.
* **Verification:** The user must enter the exact OTP within the GUI. Once validated, the user's account details are securely saved into the local MySQL `users` database table.

### 3. Password Generation & Vault Management
* **Locker Interface:** Once logged in, users gain access to their personal credentials vault. 
* **Password Generator:** The application includes a utility that uses cryptographic randomness to generate high-strength, customizable passwords (mixing uppercase, lowercase, numbers, and symbols).
* **Data Persistence:** When a user saves a credential (Website URL, Username, Password), the application executes an `INSERT` query to log the entry into the local database, mapping it directly to that specific user's ID.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.8 or higher
* MySQL Server (running on `localhost`)
* A Gmail account (to configure an SMTP App Password for sending verification emails)

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/krishnagupta7884/customtkinter-password-manager.git](https://github.com/krishnagupta7884/customtkinter-password-manager.git)
cd customtkinter-password-manager
```
### 2. Install Dependencies

Install the required Python packages using the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Since this project connects to a local database server, you need to set up the schema on your machine:

1. Open your MySQL terminal or MySQL Workbench.
2. Create the target database:
```sql
CREATE DATABASE password_manager;
USE password_manager;
```
3. Initialize the tables by running your specific database creation queries (e.g., creating tables for user login accounts and the stored credentials vault).

### 4. Environment Setup
1. Copy the template environment file to create your active environment configuration:
```bash
cp .env.example .env
```
2. Open the newly created .env file and fill in your local MySQL root credentials and your Gmail SMTP App Password:

```Code snippet
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

⚠️ Important: Never commit your actual .env file to GitHub. It is already safely listed in your .gitignore.

## 💻 Usage

To launch the password manager interface, run the primary application script:
```bash
python "CS PROJECT CLASS XII.py"
```
1. Sign Up: Create a new account and verify your email address using the dynamic OTP.

2. Log In: Authenticate into your secure locker interface.

3. Manage Vault: Add your custom credentials or utilize the generator for random, secure strings.


## 🛠️ Technologies Used
* Frontend: CustomTkinter

* Backend: Python 3

* Database: MySQL (localhost)

* Protocols: SMTP (Secure email relay for OTP generation)

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.


