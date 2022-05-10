#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json


class Course(object):
    """The Course class.
    """

    def __init__(self, course_id, course_name, department, credits, time, location):
        """The initialization for the object.

        Args:
            course_id (str): The course id.
            course_name (str): The course name.
            department (str): The department.
            credits (int): The credits.
            time (dict): The time.
            location (str): The location.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.department = department
        self.credits = credits
        self.time = time
        self.location = location

    def export_object(self):
        """Export the object to a json file.
        """

        # Convert the object's information into the dict format.
        objectInformation = {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'department': self.department,
            'credits': self.credits,
            'time': self.time,
            'location': self.location
        }

        if os.path.exists('./Courses/'):
            # The directory exists.
            pass
        else:
            # The directory doesn't exist.
            os.mkdir('./Courses/')

        # Check whether the file is existed.
        if os.path.exists('./Courses/{course_id}.json'.format(course_id=self.course_id)):
            # If the file is existed, we remove it.
            os.remove(
                './Courses/{course_id}.json'.format(course_id=self.course_id))
        with open('./Courses/{course_id}.json'.format(course_id=self.course_id), 'w') as f:
            json.dump(objectInformation, f)
        # Convert the object to a json file.

        # Note, we plan to set the time of the course with the dict object.
        # {'Lesson-1': {'Weekday': 'Monday', 'StartTime': '08:30', 'EndTime': '09:30'}, 'Lesson-2': {'Weekday': 'Monday', 'StartTime': '09:30', 'EndTime': '10:30'}}


class CourseManager(object):

    def __init__(self):
        if os.path.exists('courses.json'):
            print("Initialize the course manager from the json data file.")
            self.load_courses_file()
        else:
            print("Initialize the course manager.")
            self.courses = {}

    def add_courses(self, course):
        """Add the course into the courses dict.

        Args:
            course (Course): The Course object.
        """
        # We set the template of the record in course manager object like below:
        # {'Information': {'Name': course.course_name, 'Department': course.department, 'Credits': course.credits, 'Time': course.time, 'Location': course.location}, 'Registration': {'StudentId': {'Name': StudentName, 'Grade': StudentGrade, 'Department': StudentDept, 'Gender': StudentGender}, 'StudentId': {'Name': StudentName, 'Grade': StudentGrade, 'Department': StudentDept, 'Gender': StudentGender}, 'StudentId': {'Name': StudentName, 'Grade': StudentGrade, 'Department': StudentDept, 'Gender': StudentGender}}}
        self.courses[course.course_id] = {'Information': {'Name': course.course_name, 'Department': course.department,
                                                          'Credits': course.credits, 'Time': course.time, 'Location': course.location},
                                          'Registration': {}}
        print("The course is added into the courses dict.")

    def remove_courses(self, course_id):
        """Remove the course with the course id given.

        Args:
            course_id (str): The id of the course.
        """

        # First, we check whether the course is in the courses list.
        if course_id in self.courses.keys():
            # If the course is in the courses list, we remove the course.
            del self.courses[course_id]
            print("The course is removed.")
        else:
            print(
                "The course is not in the courses list, so you can't remove the course.")

    def add_students(self, course_id, student_information):
        """Add the student into the course.

        Args:
            course_id (str): The course id.
            student_information (dict): The student information.
        """

        # First, we check whether the course is in the courses list.
        if course_id in self.courses.keys():
            # If the course is in the courses list, we add the student into the course.
            # The grade is initialized to -1.
            self.courses[course_id]['Registration'][student_information['Student_id']] = {
                'Name': student_information['Name'], 'Grade': -1, 'Department': student_information['Department'], 'Gender': student_information['Gender']}
        else:
            print("The course is not in the courses list, so you can't add the student.")

    def remove_student(self, course_id, student_id):
        """Remove the student with the course id and student id given.

        Args:
            course_id (str): The id of the course.
            student_id (str): The id of the student.
        """

        # First, we check whether the course is in the courses list.
        if course_id in self.courses.keys():
            # Next, we check whether the student is in this course.
            if student_id in self.courses[course_id]['Registration'].keys():
                # If the student is in the course, we remove the student.
                del self.courses[course_id]['Registration'][student_id]
            else:
                print("The student is not in the course.")
        else:
            print(
                "The course is not in the courses list, so you can't remove the student.")

    def sync_selected_courses(self, student):
        """Sync the courses with the student.

        Args:
            student (Student): The student object.
        """
        # First, we clear the existed selected courses.
        student.selected_courses.clear()

        # Sync the new selected courses.
        for course_id in self.courses.keys():
            if student.student_id in self.courses[course_id]['Registration'].keys():
                student.selected_courses[course_id] = {'Information': self.courses[course_id]['Information'],
                                                       'Grade': self.courses[course_id]['Registration'][student.student_id]['Grade']}

    def set_course_grade(self, course_id, student_id, grade):
        """Set the grade with course id and student id given.

        Args:
            course_id (str): The id of the course.
            student_id (str): The id of the student.
            grade (float): The grade.
        """
        # First, we check whether the course is in the courses list.
        if course_id in self.courses.keys():
            # Next, we check whether the student is in this course.
            if student_id in self.courses[course_id]['Registration'].keys():
                # If the student is in the course, we set the grade for the student.
                self.courses[course_id]['Registration'][student_id]['Grade'] = grade
            else:
                print("The student is not in the course.")
        else:
            print("The course is not in the courses list, so you can't set the grade.")

    def save_courses_file(self):
        """Save the courses into json file.
        """
        with open('courses.json', 'w') as f:
            json.dump(self.courses, f)

    def load_courses_file(self):
        """Load the courses from json file.
        """
        with open('courses.json', 'r') as f:
            self.courses = json.load(f)

    def get_registrant_information(self, student_id):
        """Get the registrant information with the student id given.

            Args:
                student_id (str): The id of the student.
        """

        # First, we check whether we can really get some information.
        if len(self.courses.keys()) <= 0:
            # That means, no course is in the courses list.
            print("Nothing in the courses list.")
        else:
            # There do exists something in the courses list.

            # Record important information.
            total_score = 0
            total_courses = 0

            # Find all the courses that the student is in.
            for course_id in self.courses.keys():
                if student_id in self.courses[course_id]['Registration'].keys():
                    # If the student is in the course, we display the information.
                    print(
                        "The student named {name} is in course {course_id}, with grade {grade}.".format(name=self.courses[course_id]['Registration'][student_id]['Name'], course_id=course_id, grade=self.courses[course_id]['Registration'][student_id]['Grade']))
                    total_score += self.courses[course_id]['Registration'][student_id]['Grade']
                    total_courses += 1

            # Check whether the student is in any course.
            if total_courses == 0:
                print(
                    "The student is not in any course, then no information is displayed.")
            else:
                # Calculate the average score.
                average_score = total_score / total_courses
                print("The average score is {average_score}.".format(
                    average_score=average_score))


class Person(object):
    """The Person class(An abstract class).
    """

    def __init__(self, last_name, first_name, gender, birthday):
        """The initialization for the object.

        Args:
            last_name (str): The last name.
            first_name (str): The first name.
            gender (str): The gender.
            birthday (datetime): The birthday.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.birthday = birthday


class Student(Person):
    """The Student class(Inherited from the Person class).

    Args:
        Person (class): The inherited class.
    """

    def __init__(self, student_id, last_name, first_name, gender, birthday, department):
        """The initialization for the object.

        Args:
            student_id (str): The student id.
            last_name (str): The last name.
            first_name (str): The first name.
            gender (str): The gender.
            birthday (datetime): The birthday.
            department (str): The department.
        """
        super().__init__(last_name, first_name, gender, birthday)
        self.student_id = student_id
        self.department = department
        self.selected_courses = {}

    def export_object(self):
        """ Export the data into the json file with the dictionary format.
        """

        # Convert the object's information into the dict format.
        objectInformation = {
            'student_id': self.student_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'gender': self.gender,
            'birthday': self.birthday.strftime("%Y-%m-%d"),
            'department': self.department,
        }

        if os.path.exists('./Students/'):
            # The directory exists.
            pass
        else:
            # The directory doesn't exist.
            os.mkdir('./Students/')

        # Check whether the file is existed.
        if os.path.exists('./Students/{student_id}.json'.format(student_id=self.student_id)):
            os.remove(
                './Students/{student_id}.json'.format(student_id=self.student_id))
        with open('./Students/{student_id}.json'.format(student_id=self.student_id), 'w') as f:
            json.dump(objectInformation, f)

    def get_selected_courses(self, CourseManager):
        """Get the selected courses for the student.

        Args:
            CourseManager (class): The CourseManager class.
        """
        # Sync the data.
        CourseManager.sync_selected_courses(self)

        # Check whether the student is in any course.
        if len(self.selected_courses.keys()) == 0:
            print("The student is not in any course.")
        else:
            # There do exists something in the selected courses.

            print("The selected courses for student {student_id} named {student_name}:".format(
                student_id=self.student_id, student_name=("{} {}".format(self.first_name, self.last_name))))

            for course_id in self.selected_courses:
                print(
                    "##########################################################################")
                print("The course {course_id} is named {course_name}.".format(
                    course_id=course_id, course_name=self.selected_courses[course_id]['Information']['Name']))
                print("The department is {department}.".format(
                    department=self.selected_courses[course_id]['Information']['Department']))
                print("The location is {location}.".format(
                    location=self.selected_courses[course_id]['Information']['Location']))
                for values in self.selected_courses[course_id]['Information']['Time'].values():
                    print("The time is from {start} to {end} on {weekday}".format(
                        start=values['StartTime'], end=values['EndTime'], weekday=values['Weekday']))
                print(
                    "##########################################################################")

    def get_gpa(self, CourseManager):
        """Get the GPA score of the student.

        Args:
            CourseManager (class): The CourseManager class.
        """
        # Sync the data.
        CourseManager.sync_selected_courses(self)

        # First, we check whether the student has selected any course.
        if len(self.selected_courses) <= 0:
            # That means, no course is selected.
            print("The student has not selected any course.")
        else:
            # There do exists something in the selected courses list.

            # Record important information.
            total_score = 0
            total_credits = 0
            for course_id in self.selected_courses:
                total_score += self.selected_courses[course_id]['Grade'] * \
                    self.selected_courses[course_id]['Information']['Credits']
                total_credits += self.selected_courses[course_id]['Information']['Credits']
            gpa_score = total_score / total_credits
            print("The GPA score is {gpa_score} with total credits {credits}.".format(
                gpa_score=gpa_score, credits=total_credits))

    def get_grade_credits_for_courses(self, CourseManager):
        """Get the grade and credits for the courses.

        Args:
            CourseManager (class): The CourseManager class.
        """
        # Sync the data.
        CourseManager.sync_selected_courses(self)

        # First, we check whether the student has selected any course.
        if len(self.selected_courses) <= 0:
            # That means, no course is selected.
            print("The student has not selected any course.")
        else:
            # There do exists something in the selected courses list.
            print("The grades for the selected courses:")
            for course_id in self.selected_courses:
                print("The course with name {course_name} and {credit} credit(s) has grade {grade}.".format(
                    course_name=self.selected_courses[course_id]['Information']['Name'], credit=self.selected_courses[course_id]['Information']['Credits'], grade=self.selected_courses[course_id]['Grade']))

    def save_selected_courses(self, CourseManager):
        """Save the selected courses.

        Args:
            CourseManager (class): The CourseManager class.
        """
        # Sync the data.
        CourseManager.sync_selected_courses(self)
        # First, we check whether the selected courses is empty.
        if len(self.selected_courses) <= 0:
            # That means, no course is selected.
            print("No course is selected.")
        else:
            # There do exists something in the selected courses.
            if os.path.exists('./Selected_Courses/'):
                # The directory exists.
                pass
            else:
                os.mkdir('./Selected_Courses/')
            with open("./Selected_Courses/selected_courses_{student_id}.json".format(student_id=self.student_id), "w") as f:
                # Write the selected courses into the file.
                json.dump(self.selected_courses, f)

    def print_schedule(self, CourseManager):
        """Print the schedule.

        Args:
            CourseManager (class): The CourseManager class.
        """
        # Sync the data.
        CourseManager.sync_selected_courses(self)
        # First, we check whether the student has selected any course.
        if len(self.selected_courses) <= 0:
            # That means, no course is selected.
            print("The student has not selected any course.")
        else:
            # There do exists something in the selected courses list.
            print("The schedule for student {student_id} named {student_name}:".format(
                student_id=self.student_id, student_name=("{} {}".format(self.first_name, self.last_name))))

            # Print the schedule.
            for course_id in self.selected_courses:
                print(
                    "##########################################################################")
                print("Course Information")
                print("Course name: {course_name}".format(
                    course_name=self.selected_courses[course_id]['Information']['Name']))
                print("Course Time:")
                for values in self.selected_courses[course_id]['Information']['Time'].values():
                    print("{weekday} from {start} to {end}".format(
                        weekday=values['Weekday'], start=values['StartTime'], end=values['EndTime']))
                print("Course Location: {course_location}".format(
                    course_location=self.selected_courses[course_id]['Information']['Location']))
                print(
                    "##########################################################################")

    def modify_course(self, CourseManager, mode):
        """Modify the selected courses.

        Args:
            CourseManager (class): The CourseManager class.
            mode (int): The mode. 1 is for add, 2 is for delete.
        """

        # Sync the data.
        CourseManager.sync_selected_courses(self)

        if mode == 1:
            # Add a course.
            course_id = input("Please input the course id to add:")
            if course_id in CourseManager.courses.keys():
                # That means, the course exists.
                student_information = {'Student_id': self.student_id, 'Name': ("{} {}".format(self.first_name, self.last_name)),
                                       'Department': self.department, 'Gender': self.gender}
                CourseManager.add_students(course_id, student_information)
            else:
                print("The course is not available!")
        else:
            # Delete a course.
            course_id = input("Please input the course id to delete:")
            if course_id in self.selected_courses.keys():
                # That means, the course exists.
                CourseManager.remove_student(course_id, self.student_id)
            else:
                print("The course is not available!")

        # Sync the selected courses.
        CourseManager.sync_selected_courses(self)

        # Print the schedule.
        self.print_schedule(CourseManager)
