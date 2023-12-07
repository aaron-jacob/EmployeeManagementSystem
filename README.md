# Employee Management System

## Overview

Employee Management System is a simple web application built using Flask and PostgreSQL. It allows you to manage employee information, including details like name, department, position, project, skill, and role.

## Features

- View a list of employees.
- Add new employees to the system.
- Edit existing employee information.
- Delete employees from the system.

## Technologies Used

- Flask: A web framework for building the backend.
- PostgreSQL: A relational database for storing employee and related data.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/employee-management.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your PostgreSQL database. Update the database connection details in `app.py`:

    ```python
    # Replace these values with your database connection details
    dbname = "your_database_name"
    user = "your_database_user"
    password = "your_database_password"
    host = "your_database_host"
    port = "your_database_port"
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the Employee Management System.

## Database Structure

The application uses the following database tables:

- `departments`: Stores department information.
- `positions`: Stores position information.
- `projects`: Stores project information.
- `skills`: Stores skill information.
- `roles`: Stores role information.
- `employees`: Stores employee information with foreign keys to the above tables.

## Sample Data

If you want to add sample data to your database, uncomment the `add_sample_data()` function in `app.py` and run the application again.


