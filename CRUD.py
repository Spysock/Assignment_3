import psycopg2 as ps

#Needed Credentials to access the db
DB_NAME = "Assignment3"
DB_USER = "postgres"
DB_PASS = "069359"
DB_HOST = "localhost"
DB_PORT = 5432

def initialize_db():
    #Connecting to DB
    try:
        conn = ps.connect(database=DB_NAME,
                          user=DB_USER,
                          password=DB_PASS,
                          host=DB_HOST,
                          port=DB_PORT)
        print("Successful Connection")

    except Exception as e:
        print("Unsuccessful Connection:", e)
        return None

    #Removes duplicated commit statements 
    conn.autocommit = True
    cur = conn.cursor() #Allows executions to occur

    #Table creation
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id SERIAL PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollment_date DATE
    )
    """)

    #Inserting values
    try:
        cur.execute("""
        INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
        ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
        """)
    except ps.errors.UniqueViolation: #if the unique address rule is broken
        pass

    return cur

def get_all_students():
    #Executes selection and prints out all of the students name
    db.execute("SELECT * FROM students;")
    students = db.fetchall()
    for student in students:
        print(student)

def add_student(first_name, last_name, email, enrollment_date):
    try:
        #I kept getting an error because I added duplicates
        db.execute("SELECT 1 FROM students WHERE email = %s", (email)) #Checks if the row exists
        existing_record = db.fetchone() #Fetchone gets the row
        if existing_record: #if this isn't null it exists
            print(f"Error: Student with email {email} already exists.")
            return

        #Insert new insertion into table
        db.execute("""
        INSERT INTO students (first_name, last_name, email, enrollment_date) 
        VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, email, enrollment_date))
        print(f"Successfully added {first_name} {last_name} with the email: {email}, on {enrollment_date}")
    except Exception as e:
        print("Error:", e)


def update_student_email(student_id, new_email):
    try:
        #Update value in email
        db.execute("""
        UPDATE students SET email = %s WHERE student_id = %s
        """, (new_email, student_id))
        print(f"Successfully Updated {student_id} with the new email: {new_email}")
    except Exception as e:
        print("Error:", e)


def delete_student(student_id):
    try:
        db.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        print(f"Successfully Deleted {student_id}")
    except Exception as e:
        print("Error:", e)


db = initialize_db()


get_all_students()


add_student("Example", "Majeed", "examplemajeed@example.com", "2001-02-05")


get_all_students()


update_student_email(4, "example@gmail.com")


get_all_students()


delete_student(4)


get_all_students()

