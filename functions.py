import sqlite3
import json

def get_db():
    return sqlite3.connect("students.db")

def get_subjects():
    with open("school.json","r") as file:
        data = json.load(file)

    list_subjects = data["subjects"]
    return list_subjects

def get_grades():
    with open("school.json","r") as file:
        data = json.load(file)

    list_grades = data["grades"]
    return list_grades

def get_classes():
    with open("school.json","r") as file:
        data = json.load(file)

    list_classes = data["classes"]
    return list_classes

def validate(fname,lname,og_grades,grade,og_subjects,subjects,og_classes,myclass):
    try:
        grade = int(grade)
    except ValueError:
        return False, "Invalid grade received"

    if grade not in og_grades:
        return False,"Invalid grade received"

    if len(subjects) == 0:
        return False,"No subject selected"
    for subject in subjects:
        if subject not in og_subjects or subject == "":
            return False,"Invalid subject received"




    if (not fname.isalpha()) or (not lname.isalpha()):
        if fname == "" or lname == "":
            return False, "A student's name can't be blank"
        else:
            return False,"Names should be only alphabetical"
    if myclass not in og_classes:
        return False,"Invalid class received"

    return True,f"{fname} was added to the database"

def safely_add_subjects(subjects):
    num_subjects = len(subjects)
    counter = 0
    placeholder = ""
    for _ in subjects:
        counter+=1
        if counter == num_subjects:
            placeholder+="?"
        else:
            placeholder+="?,"

    return placeholder

def update_subject_database():
    subjects = get_subjects()
    subjects.sort()

    with get_db() as con:
        c = con.cursor()

        for subject in subjects:
            try:
                c.execute('''
                    INSERT INTO subjects (subjectname) VALUES (?) 
                    ''',(subject,))
            except sqlite3.IntegrityError:
                continue

        con.commit()

def display_students(user_id):
    with get_db() as con:
        c = con.cursor()
        c.execute('''
            SELECT studentID,firstname,lastname,grade,class
            FROM students WHERE teacherID = ?;
        ''',(user_id,))

        students_rows = c.fetchall()

        if not students_rows: #If fetchall returned nothing it means the teacher has not students
            return 1

        students_db = [] #Should be a 2D list when finished
        temp_students_db = []

        for student in students_rows:
            temp_students_db.append(list(student))
            student_id = int(student[0])

            c.execute('''
            SELECT subjectname FROM subjects WHERE subjectID IN 
            (SELECT subjectID FROM students_subjects WHERE studentID = ?);
            ''',(student_id,))

            subject_names = c.fetchall()

            if not subject_names: #Added this though it should be impossible for this to even happen
                return 2

            subject_names = list(subject_names)
            new_subject_names = []
            for subject in subject_names:
                subject = subject[0]
                new_subject_names.append(subject)

            temp_students_db.append(new_subject_names)

            students_db.append(temp_students_db)

            temp_students_db = [] #Empties temp_students_db for next iteration

    return students_db




