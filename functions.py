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
    except:
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
