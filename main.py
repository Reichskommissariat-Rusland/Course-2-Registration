#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from assistant_func import *
from time import sleep

courses_dict = {}
students_dict = {}

manager = CourseManager()


def student_registration():
    """Register a new student.

    Returns:
        student (Student): The Student object that registered.
    """

    student_id = input("$ Please give the student ID(Q\q for quit): ")
    student_last_name = input(
        "$ Please give the student's last name(Q\q for quit): ")
    student_first_name = input(
        "$ Please give the student's first name(Q\q for quit): ")
    student_gender = input(
        "$ Please give the student's gender(Q\q for quit): ")
    try:
        student_birthday = input(
            "$ Please give the student's birth year(Like format: YYYY-MM-DD, Q\q for quit): ")
    except ValueError as e:
        print("$ Birthday invalid! Exiting to the menu...")
        return
    student_department = input(
        "$ Please give the student department(Q\q for quit): ")

    student_birthday = datetime.datetime.strptime(
        student_birthday, '%Y-%m-%d')

    if 'q' not in [student_id, student_last_name, student_first_name, student_gender, student_birthday, student_department]:

        return Student(student_id, student_last_name, student_first_name, student_gender, student_birthday, student_department)
    else:
        return


def initialize():
    """Initialize the data.
    """

    for file_name in os.listdir('./Courses/'):
        course = init_course('./Courses/' + file_name)
        courses_dict[course.course_id] = course

    for file_name in os.listdir('./Students/'):
        student = init_student('./Students/' + file_name)
        students_dict[student.student_id] = student


def exit_system():
    """Exit the system.
    """

    # Back the data of the current status into external files.
    print("$ Backing up the data...")

    for course in courses_dict.values():
        course.export_object()

    for student in students_dict.values():
        student.save_selected_courses(manager)
        student.export_object()

    print("$ Data backed up.")

    print("$ Exiting the system...")
    exit()


def menu():
    """Display the menu.

    Returns:
        choice (int): The choice for the process.
    """

    print("############################################################################")
    print("#               Welcome to our course registration system                  #")
    print("############################################################################")
    print("#                   1. Course registration for new user                    #")
    print("#                   2. Modify user course registration                     #")
    print("#                   3. Course management                                   #")
    print("#                   4. Print selected course schedule                      #")
    print("#                   5. Query grades and credits                            #")
    print("#                   6. Exit                                                #")
    print("############################################################################")

    choice = int(input("$ Please give your choice: "))
    while choice not in [1, 2, 3, 4, 5, 6]:
        print("$ Please give a valid choice.")
        choice = int(input("$ Please give your choice: "))

    return choice


def control_sequence(choice):
    """Control the sequence of the program.

    Args:
        choice (int): The choice for the process.
    """

    if choice == 1:
        # Course registration for new user.
        student_id = input("$ Please enter the ID for check(Q\q for quit):")
        if student_id in students_dict.keys():
            # Already in registration.
            print("This student has already been in registration!")
            return
        else:
            # Start registration.
            student = student_registration()
            students_dict[student.student_id] = student
        sleep(3)
    elif choice == 2:
        # Modify the course registration for the user.

        student_id = input(
            "$ Please give the student ID for modification(Q\q for exit): ")

        while student_id not in students_dict.keys():
            if student_id == 'Q' or student_id == 'q':
                return
            print("$ Student is not the registrant in the system.")
            student_id = input(
                "$ Please give the student ID for modification(Q\q for exit): ")

        student = students_dict[student_id]

        mode = input(
            "$ Please give your mode(1 is for add, 2 is for remove, and Q\q for exit): ")

        while mode not in ['1', '2', 'q', 'Q']:
            print("$ Please give a valid mode.")
            mode = input(
                "$ Please give your mode(1 for add, 2 for remove, Q\q for exit): ")

        if mode == '1' or mode == '2':
            # Modify the course registration for the user.
            student.modify_course(manager, int(mode))
        else:
            print("$ Exiting to the main menu...")
            return
        sleep(3)
    elif choice == 3:
        # Course management.

        mode = input(
            "$ Course management mode(1 for add, 2 for remove, 3 is for score modification, and Q\q for exit):")

        while mode not in ['1', '2', '3', 'q', 'Q']:
            print("$ Please give a valid mode.")
            mode = input(
                "$ Please give your mode(1 for add, 2 for remove, Q\q for exit): ")

        if mode == '1':
            # Add a course.
            course_id = input(
                "$ Please give the course ID to add(Q\q for exit): ")
            while course_id not in courses_dict.keys():
                if course_id == 'q' or course_id == 'Q':
                    return
                print("$ Please give a valid course ID.")
                course_id = input(
                    "$ Please give the course ID to add (Q\q for exit): ")
            course = courses_dict[course_id]
            manager.add_courses(course)

        elif mode == '2':
            # Delete a course.
            course_id = input(
                "$ Please give the course ID to remove(Q\q for exit): ")
            while course_id not in courses_dict.keys():
                if course_id == 'q' or course_id == 'Q':
                    return
                print("$ Please give a valid course ID.")
                course_id = input(
                    "$ Please give the course ID to remove (Q\q for exit): ")
            manager.remove_courses(course_id)
        elif mode == '3':
            # Modify the score of a course.
            student_id = input("$ Please give the student ID(Q\q for exit): ")
            while student_id not in students_dict.keys():
                if student_id == 'Q' or student_id == 'q':
                    print("$ Exiting to the main menu...")
                    return
                print("$ Please give a valid student ID.")
                student_id = input(
                    "$ Please give the student ID(Q\q for exit): ")

            course_id = input(
                "$ Please give the course ID to add(Q\q for exit): ")
            while course_id not in courses_dict.keys():
                if course_id == 'q' or course_id == 'Q':
                    return
                print("$ Please give a valid course ID.")
                course_id = input(
                    "$ Please give the course ID to add (Q\q for exit): ")

            score = input("$ Please give the score(Q\q for exit): ")
            if score == 'Q' or score == 'q':
                return
            else:
                while float(score) > 100 or float(score) < 0:
                    print("$ Please give a valid score.")
                    score = input("$ Please give the score: ")

            manager.set_course_grade(course_id, student_id, float(score))

        else:
            print("$ Exiting to the main menu...")
            return
        sleep(3)
    elif choice == 4:
        # Print the selected course schedule.
        student_id = input("$ Please give the student ID(Q\q for exit): ")
        while student_id not in students_dict.keys():
            if student_id == 'Q' or student_id == 'q':
                print("$ Exiting to the main menu...")
                return
            print("$ Please give a valid student ID.")
            student_id = input("$ Please give the student ID(Q\q for exit): ")
        student = students_dict[student_id]
        # Print the schedule for the student.
        student.print_schedule(manager)
        sleep(3)
    elif choice == 5:
        # Query the grades and credits.
        student_id = input("$ Please give the student ID(Q\q for exit): ")
        while student_id not in students_dict.keys():
            if student_id == 'Q' or student_id == 'q':
                print("$ Exiting to the main menu...")
                return
            print("$ Please give a valid student ID.")
            student_id = input("$ Please give the student ID(Q\q for exit): ")
        student = students_dict[student_id]
        # The grades and the credits of the current student.
        student.get_grade_credits_for_courses(manager)
        # The gpa.
        student.get_gpa(manager)
        sleep(3)
    else:
        # Exit the system.
        exit_system()


def main():
    initialize()
    while True:
        choice = menu()
        control_sequence(choice)


if __name__ == '__main__':
    main()
