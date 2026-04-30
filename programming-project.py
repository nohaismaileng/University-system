import json
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime as dt

students_data = []
courses_data = []

students_file = "students.json"
courses_file = "courses.json"

if os.path.exists(students_file):
    with open(students_file, "r") as f:
        students_data = json.load(f)
    if not isinstance(students_data, list):
        students_data = []
else:
    students_data = []

if os.path.exists(courses_file):
    with open(courses_file, "r") as f:
        courses_data = json.load(f)
else:
    courses_data = []

def save_students_data():
    with open(students_file, "w") as f:
        json.dump(students_data, f, indent=2)

def save_courses_data():
    with open(courses_file, "w") as f:
        json.dump(courses_data, f, indent=2)

def menu():
    print("1. Add Student Information")
    print("2. Edit Student Information")
    print("3. Remove Student Information")
    print("4. Add Course Information")
    print("5. Edit Course Information")
    print("6. Remove Course Information")
    print("7. Supply Grades")
    print("8. Print Student Result")
    print("9. Generate Bar Chart")
    print("10. Generate Pie Chart")
    print("0. Exit")

def get_valid_birthdate():
    while True:
        birthdate_str = input("Enter student birthdate (YYYY-MM-DD): ")
        try:
            birthdate = dt.strptime(birthdate_str, "%Y-%m-%d").date()
            return birthdate
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")

def add_student_information():
    code = input("Enter student code: ")
    name = input("Enter student name: ")
    birthdate = get_valid_birthdate()

    student = {"code": code, "name": name, "birthdate": birthdate.strftime("%Y-%m-%d")}

    if isinstance(students_data, list):
        students_data.append(student)
        save_students_data()
        print("Student added successfully.")
    else:
        print("Error information")

def edit_student_information():
    code = input("Enter student code to edit: ")
    for student in students_data:
        if student["code"] == code:
            student["name"] = input("Enter new name: ")
            student["birthdate"] = input("Enter new birthdate: ")
            save_students_data()
            print("Student information updated.")
            return
    print("Error! Student is not found.")

def remove_student_information():
    code = input("Enter student code to remove: ")
    for student in students_data:
        if student["code"] == code:
            students_data.remove(student)
            save_students_data()
            print("Student removed successfully.")
            return
    print("Error! Student is not found.")

def add_course_information():
    code = input("Enter course code: ")
    name = input("Enter course name: ")
    max_degree = input("Enter maximum degree: ")

    course = {"code": code, "name": name, "max_degree": max_degree}
    courses_data.append(course)
    save_courses_data()
    print("Course added successfully.")

def edit_course_information():
    code = input("Enter course code to edit: ")
    for course in courses_data:
        if course["code"] == code:
            course["name"] = input("Enter new name: ")
            course["max_degree"] = input("Enter new maximum degree: ")
            save_courses_data()
            print("Course information updated successfully.")
            return
    print("Error! Course is not found.")

def remove_course_information():
    code = input("Enter course code to remove: ")
    for course in courses_data:
        if course["code"] == code:
            courses_data.remove(course)
            save_courses_data()
            print("Course removed successfully.")
            return
    print("Error! Course is not found.")

def supply_grades():
    course_code = input("Enter course code to supply grades: ")
    for course in courses_data:
        if course['code'] == course_code:
            csv_file = f"{course_code}.csv"
            grades_data = []
            for student in students_data:
                grade = input(f"Enter grade for {student['name']} ({student['code']}):")
                grades_data.append({'code': student['code'], 'grade': grade})
            with open(csv_file, 'w', newline='') as f:
                fieldnames = ['code', 'grade']
                write = csv.DictWriter(f, fieldnames=fieldnames)
                write.writeheader()
                write.writerows(grades_data)
            print("Grades supplied and saved successfully!")
            return
    print("Error! Course not found.")

def calculate_results(course_code):
    csv_file = f"{course_code}.csv"
    results_data = []
    total_credit_hours = 0
    total_weighted_grade = 0

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            student_code = row["code"]
            grade = float(row["grade"])

            max_degree = None
            credit_hours = None
            for course in courses_data:
                if course["code"] == course_code:
                    max_degree = float(course["max_degree"])
                    credit_hours = float(course.get("credit_hours", 1))
                    break

            if max_degree is not None and credit_hours is not None:
                percentage = int((grade / max_degree) * 100)

                if percentage in range(90, 101):
                    gpa = 4.0
                elif percentage in range(80, 90):
                    gpa = 3.7
                elif percentage in range(70, 80):
                    gpa = 2.7
                elif percentage in range(60, 70):
                    gpa = 2.0
                elif percentage < 60:
                    gpa = 0.0
                else:
                    return "Invalid input"

                total_credit_hours += credit_hours
                total_weighted_grade += gpa * credit_hours

                results_data.append({"code": student_code, "result": grade, "gpa": gpa})

    overall_gpa = total_weighted_grade / total_credit_hours if total_credit_hours > 0 else 0.0
    return results_data, overall_gpa




def generate_bar_chart(course_code, result_data):
    codes = [result["code"] for result in result_data]
    results = [result["result"] for result in result_data]
    plt.bar(codes, results)
    plt.xlabel("Student Code")
    plt.ylabel("Result")
    plt.title(f"Result for Course {course_code}")
    plt.savefig(f"{course_code}_bar_chart.png")
    plt.show()

def generate_pie_chart():
    course_counted_data = {course["code"]: 0 for course in courses_data}
    for student in students_data:
        for course in courses_data:
            csv_file = f"{course['code']}.csv"
            if os.path.exists(csv_file):
                with open(csv_file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row["code"] == student["code"]:
                            course_counted_data[course["code"]] += 1
    course_symbols = list(course_counted_data.keys())
    course_counts_values = list(course_counted_data.values())
    plt.pie(course_counts_values, labels=course_symbols, autopct='%1.1f%%')
    plt.title("Course Registration")
    plt.savefig("course_registration_pie_chart.png")
    plt.show()

def print_student_result():
    student_code = input("Enter student code to print result: ")
    student_name = None
    overall_gpa = 0.0
    for student in students_data:
        if student["code"] == student_code:
            student_name = student["name"]
            break
    if student_name is None:
        print("Student not found!")
        return

    result_data, overall_gpa = calculate_results("C001")  # Replace with the actual course code
    generate_result_html(student_name, student_code, result_data, overall_gpa)

def generate_result_html(student_name, student_code, result_data, overall_gpa):
    with open("result_template.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Result</title>
    <!-- Include Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
    <div class="container mt-5">
        <h1 class="mb-4">Student Result</h1>
        <div class="row">
            <div class="col-md-6">
                <h2>Personal Information</h2>
                <ul class="list-group">
                    <li class="list-group-item"><strong>Student Code:</strong> {student_code}</li>
                    <li class="list-group-item"><strong>Birthdate:</strong> <!-- Add birthdate if available --></li>
                </ul>
            </div>
            <div class="col-md-6">
                <h2>Result Details</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Course Code</th>
                            <th>Result</th>
                            <th>GPA</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- Replace the following block with your actual result data -->
                        {generate_result_table(result_data)}
                        <!-- End of result data block -->
                    </tbody>
                </table>
                <p><strong>Overall GPA:</strong> {overall_gpa}</p>
            </div>
        </div>
    </div>
    <!-- Include Bootstrap JS and jQuery -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>""")

def generate_result_table():
    print("\n======= Student Information System Menu =======")
    print("1. Add Student Information")
    print("2. Edit Student Information")
    print("3. Remove Student Information")
    print("4. Add Course Information")
    print("5. Edit Course Information")
    print("6. Remove Course Information")
    print("7. Supply Grades")
    print("8. Print Student Result")
    print("9. Generate Bar Chart")
    print("10. Generate Pie Chart")
    print("0. Exit")

def get_user_choice():
    return input("Enter your choice (0-10): ")

def main():
    while True:
        generate_result_table()
        choice = get_user_choice()

        if choice == "1":
            add_student_information()
        elif choice == "2":
            edit_student_information()
        elif choice == "3":
            remove_student_information()
        elif choice == "4":
            add_course_information()
        elif choice == "5":
            edit_course_information()
        elif choice == "6":
            remove_course_information()
        elif choice == "7":
            supply_grades()
        elif choice == "8":
            print_student_result()
        elif choice == "9":
            course_code = input("Enter course code for bar chart: ")
            result_data, _ = calculate_results(course_code)
            generate_bar_chart(course_code, result_data)
        elif choice == "10":
            generate_pie_chart()
        elif choice == "0":
            print("Exiting the Student Information System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 10.")

if __name__ == "__main__":
    main()
