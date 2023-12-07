from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Replace these values with your database connection details
dbname = "employee_management"
user = "postgres"
password = "jacob123@"
host = "localhost"
port = 5432

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

# Create tables if not exists
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department_id INTEGER,
            position_id INTEGER,
            project_id INTEGER,
            skill_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id),
            FOREIGN KEY (position_id) REFERENCES positions (id),
            FOREIGN KEY (project_id) REFERENCES projects (id),
            FOREIGN KEY (skill_id) REFERENCES skills (id),
            FOREIGN KEY (role_id) REFERENCES roles (id)
        );
    """)
    conn.commit()

def add_sample_data():
    # Add sample data
    with conn.cursor() as cursor:
        # Add sample departments
        cursor.execute("INSERT INTO departments (name) VALUES ('HR'), ('Finance'), ('IT');")

        # Add sample positions
        cursor.execute("INSERT INTO positions (name) VALUES ('Manager'), ('Developer'), ('Analyst');")

        # Add sample projects
        cursor.execute("INSERT INTO projects (name) VALUES ('Project A'), ('Project B'), ('Project C');")

        # Add sample skills
        cursor.execute("INSERT INTO skills (name) VALUES ('Python'), ('JavaScript'), ('Database Management');")

        # Add sample roles
        cursor.execute("INSERT INTO roles (name) VALUES ('Team Lead'), ('Software Engineer'), ('Business Analyst');")

        # Add sample employees
        cursor.execute("""
            INSERT INTO employees (name, department_id, position_id, project_id, skill_id, role_id)
            VALUES ('John Doe', 1, 1, 1, 1, 1);
        """)
        cursor.execute("""
            INSERT INTO employees (name, department_id, position_id, project_id, skill_id, role_id)
            VALUES ('Jane Smith', 2, 2, 2, 2, 2);
        """)
        cursor.execute("""
            INSERT INTO employees (name, department_id, position_id, project_id, skill_id, role_id)
            VALUES ('Bob Johnson', 3, 3, 3, 3, 3);
        """)
        conn.commit()

# Uncomment the next line if you want to add sample data
#add_sample_data()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees')
def employee_list():
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                employees.id, employees.name,
                departments.name AS department,
                positions.name AS position,
                projects.name AS project,
                skills.name AS skill,
                roles.name AS role
            FROM employees
            JOIN departments ON employees.department_id = departments.id
            JOIN positions ON employees.position_id = positions.id
            JOIN projects ON employees.project_id = projects.id
            JOIN skills ON employees.skill_id = skills.id
            JOIN roles ON employees.role_id = roles.id
        """)
        employees = cursor.fetchall()

    # Sort the employee list based on project name (index 4 in the tuple)
    employees = sorted(employees, key=lambda x: x[4])

    return render_template('employee_list.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department']
        position_id = request.form['position']
        project_id = request.form['project']
        skill_id = request.form['skill']
        role_id = request.form['role']
        
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO employees (name, department_id, position_id, project_id, skill_id, role_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, department_id, position_id, project_id, skill_id, role_id))
            
            conn.commit()
            
        return redirect('/employees')

    # Fetch departments, positions, projects, skills, and roles for the form
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()

        cursor.execute("SELECT * FROM positions")
        positions = cursor.fetchall()

        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()

        cursor.execute("SELECT * FROM skills")
        skills = cursor.fetchall()

        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()

    return render_template('add_employee.html', departments=departments, positions=positions,
                           projects=projects, skills=skills, roles=roles)

@app.route('/edit_employee/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    if request.method == 'POST':
        name = request.form['name']
        department_id = request.form['department']
        position_id = request.form['position']
        project_id = request.form['project']
        skill_id = request.form['skill']
        role_id = request.form['role']
        
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE employees
                SET name = %s, department_id = %s, position_id = %s, project_id = %s, skill_id = %s, role_id = %s
                WHERE id = %s
            """, (name, department_id, position_id, project_id, skill_id, role_id, employee_id))
            
            conn.commit()
            
        return redirect('/employees')

    # Fetch employee details for the form
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                employees.id, employees.name,
                employees.department_id, employees.position_id,
                employees.project_id, employees.skill_id, employees.role_id,
                departments.name AS department,
                positions.name AS position,
                projects.name AS project,
                skills.name AS skill,
                roles.name AS role
            FROM employees
            JOIN departments ON employees.department_id = departments.id
            JOIN positions ON employees.position_id = positions.id
            JOIN projects ON employees.project_id = projects.id
            JOIN skills ON employees.skill_id = skills.id
            JOIN roles ON employees.role_id = roles.id
            WHERE employees.id = %s
        """, (employee_id,))
        employee = cursor.fetchone()

        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()

        cursor.execute("SELECT * FROM positions")
        positions = cursor.fetchall()

        cursor.execute("SELECT * FROM projects")
        projects = cursor.fetchall()

        cursor.execute("SELECT * FROM skills")
        skills = cursor.fetchall()

        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()

    return render_template('edit_employee.html', employee=employee, departments=departments, positions=positions,
                           projects=projects, skills=skills, roles=roles)

@app.route('/delete_employee/<int:employee_id>')
def delete_employee(employee_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()

    return redirect('/employees')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
