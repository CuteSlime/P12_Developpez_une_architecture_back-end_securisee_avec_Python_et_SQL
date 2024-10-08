
# P12_Developpez_une_architecture_back-end_securisee_avec_Python_et_SQL

Projet numéro 12 du parcour OpenClassrooms "développeur d'application python"

This is a Command Line Interface for a CRM application built with Python, using the SQLAlchemy ORM with a MySQL database. made as a project for OpenClassroom.

## Features

- **Database Management**: Manage customer data using a MySQL database.
- **Secure Authentication**: Utilizes JWT tokens and password hashing for secure user authentication.
- **Interactive Menus**: Provides an interactive CLI interface with `questionary` for user inputs (Keyboard controle).
- **Error Tracking**: Integrates Sentry for error tracking. (for dev)

## Table of Contents

- [P12\_Developpez\_une\_architecture\_back-end\_securisee\_avec\_Python\_et\_SQL](#p12_developpez_une_architecture_back-end_securisee_avec_python_et_sql)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [Dependencies](#dependencies)
  - [Development](#development)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/CuteSlime/P12_Developpez_une_architecture_back-end_securisee_avec_Python_et_SQL.git
   cd P12_Developpez_une_architecture_back-end_securisee_avec_Python_et_SQL
   ```

2. **Install Dependencies**

   This project uses `pipenv` to manage dependencies. Ensure you have `pipenv` installed, then run:

   ```bash
   pipenv install
   ```

   This will install all the necessary dependencies and create the virtual environement if needed, add `--dev` to also get development dependencies.

3. **Create and Configure the `.env` File**

   Create a `.env` file in the root directory and populate it with your environment variables:

   ```env
   DB_USER = "<your_db_user>"
   DB_PWD = "<your_db_password>"
   DB_HOST = "<your_db_host>"
   DB_PORT = "<your_db_port>"
   DB_NAME = "<your_db_name>"

   SECRET_KEY = "<your_secret_key>"
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 20

   SENTRY_DSN = "<your_sentry_dsn>"
   ```

   Replace the placeholders with your actual credentials.

## Configuration

- **Database**: The application uses a MySQL database. Configure the database connection in the `.env` file.
- **JWT Authentication**: A `SECRET_KEY` an `ALGORITHM` and `ACCESS_TOKEN_EXPIRE_MINUTES` are required for generating and verifying JWT tokens.
- **Error Tracking**: Configure `SENTRY_DSN` for error tracking. (for dev)

## Usage

1. **Activate Virtual Environment**

   Before running the application, activate the virtual environment:

   ```bash
   pipenv shell
   ```

2. **Run the Application**

   Run the main script:

   ```bash
   python run.py
   ```

   This will initialize the database tables and start the CLI application.
   
   if the Database don't have any User yet, then a manager type of User will be created,
   the username and password will be `Admin`, after creating another manager you will be able to delete the Admin user,
   please, at most change the password if you keep this account.

## Dependencies

The application uses the following dependencies:

- **SQLAlchemy**: ORM for database interaction
- **PyMySQL**: MySQL database connector
- **argon2-cffi**: Password hashing library
- **python-dotenv**: Manage environment variables
- **Alembic**: Database migrations
- **PyJWT**: JWT tokens for authentication
- **questionary**: Interactive user prompts
- **sentry-sdk**: Error tracking and monitoring

## Development

To run tests and check code quality:

1. **Run Tests**

   ```bash
   pytest
   ```

2. **Check Code Quality**

   ```bash
   flake8 --output-file=flake8_report.txt 
   ```

3. **Calculate Test Coverage**

   ```bash
   coverage run -m pytest
   coverage html
   ```
