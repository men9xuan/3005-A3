import psycopg2

# Define connection parameters
dbname = 'a3q1'
user = 'postgres'
password = 'postgres'
host = '127.0.0.1'  
port = '5432'  

# helper function to connect to postgres server
def connect_db():
    try:
        # connect to server with psycopg2
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection
    # catch error and print out 
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

# CURD functions
# Get all students records 
def getAllStudents():
    # connect to pg server 
    connection = connect_db()
    if connection:
        try:
            # execute query
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students ORDER BY student_id;")
            students = cursor.fetchall()
            for student in students:
                print(student)
        # catch error and print out          
        except psycopg2.Error as e:
            print("Error retrieving students:", e)
        # close connection
        finally:
            cursor.close()
            connection.close()
    else: 
        print('Failed to connect to the database')        

# Add student to database
def addStudent(first_name, last_name, email, enrollment_date):
    # connect to pg server 
    connection = connect_db()
    if connection:
        try: 
            # execute query
            cursor = connection.cursor()
            cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s);",
                           (first_name, last_name, email, enrollment_date))
            connection.commit()
            print("Successfully added student to the record")

        # catch error and print out 
        except psycopg2.Error as e:
            print("Error adding student:", e)
        finally:
            cursor.close()
            connection.close()
    else: 
        print('Failed to connect to the database')        

# Update student email by student id
def updateStudentEmail(student_id, new_email):
    connection = connect_db()
    if connection:
        try: 
            # execute query
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
            # check if student record exists in database
            if not cursor.fetchone():
                print("Error: student with id {} does not exist.".format(student_id))
                return
            # execute query
            cursor.execute("UPDATE students SET email = %s WHERE student_id = %s;",
                           (new_email, student_id))
            connection.commit()
            print("Successfully updated student email to the record")
        # catch error and print out     
        except psycopg2.Error as e:
            print("Error updating student email:", e)
        # close connection
        finally:
            cursor.close()
            connection.close()
    else: 
        print('Failed to connect to the database')        

# Delete student record by student id
def deleteStudent(student_id):
    connection = connect_db()
    if connection:
        try: 
            # execute query
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM students WHERE student_id = %s;", (student_id,))
            # check if student record exists in database
            if not cursor.fetchone():
                print("Error: student with id {} does not exist.".format(student_id))
                return
            # execute query
            cursor.execute("DELETE FROM students WHERE student_id = %s;",
                           (student_id,))
            connection.commit()
            print("Successfully deleted student id {} from the record".format(student_id))
        except psycopg2.Error as e:
            print("Error deleting student:", e)
        # close connection
        finally:
            cursor.close()
            connection.close()
    else: 
        print('Failed to connect to the database')        

# Optional function : initialize the supplied table definition by one function 
def initialize():
    connection = connect_db()
    if connection:
        try: 
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS students;")
            cursor.execute("CREATE TABLE students (\
    student_id SERIAL PRIMARY KEY,\
    first_name TEXT NOT NULL,\
    last_name TEXT NOT NULL,\
    email TEXT NOT NULL UNIQUE,\
    enrollment_date DATE\
);")
            connection.commit()
            print("Successfully initialized students table")
        except psycopg2.Error as e:
            print("Error deleting student:", e)
        # close connection
        finally:
            cursor.close()
            connection.close()
    else: 
        print('Failed to connect to the database')   

# Optional function : insert the supplied sample entries by one function 
def insertSample():
    connection = connect_db()
    if connection:
        try: 
            cursor = connection.cursor()
            cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES\
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),\
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),\
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');")
            connection.commit()
            print("Successfully inserted sample students")
        except psycopg2.Error as e:
            print("Error deleting student:", e)
        finally:
            cursor.close()
            connection.close()
    else: 
        print('Failed to connect to the database')   

# Optional function : provide simple instruction for the command line interface
def help():
    print("Usage: \n\
getAllStudents -------------------------------------------- get all student records\n\
addStudent first_name last_name email enrollment_date ----- add studnet record\n\
updateStudentEmail student_id new_email ------------------- update student email\n\
deleteStudent studentId ----------------------------------- delete student record\n\
help ------------------------------------------------------ print usage description\n\
** ADVANCED FUNCTION **\n\
initialize ------------------------------------------------ initialize students table\n\
insertSample ---------------------------------------------- insert sample students to the table\n\
note: use YYYY-MM-DD for date format \n\n")

# Map of supported functions
functions = {
    "addStudent": addStudent,
    "getAllStudents" : getAllStudents,
    "updateStudentEmail": updateStudentEmail,
    "deleteStudent": deleteStudent,
    "help" : help,
    "initialize": initialize,
    "insertSample" : insertSample
}

# Main function
def start():
    print("Welcome to the STUDENT RECORD MANAGEMENT SYSTEM\n")
    help()
    
    while True:
        user_input = input("Enter function name and argument or 'q' to quit: ").strip().split()
        if user_input is None or len(user_input) == 0:
            print("No input detected. Please try again.")
            continue

        cmd = user_input[0]
        args = user_input[1:]

        if cmd == 'q':
            exit()

        if cmd in functions:
            functions[cmd](*args)
            print()
        else:
            print("Function not found. Enter 'help' for help")

if __name__ == "__main__":
    start()