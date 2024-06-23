# Task Management App

A simple task management application built with Django that allows users to create, update, delete, and filter tasks.


## Features

- User authentication (sign up, log in, log out)
- Create, read, update, delete tasks
- Filter tasks by status and due date
- Use of stored procedures for task operations

## Requirements

- Python 3.7+
- Django 3.0+
- Bootstrap 4 (for frontend styling)
- DataBase (MSSQL)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/task-management-app.git
    cd task-management-app
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Run command for stored procedure:**
    ```sh
    python manage.py storedprocedure # On `TaskApp\management\commands\storedprocedure.py`
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`

## Usage

- **Authentication:** Sign up, log in, and log out functionalities.
- **Homepage:** Displays the list of tasks with options to create, update, delete, and filter tasks.

