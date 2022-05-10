#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from basic_class import *

import json
import datetime


def init_course(file_name):
    """
    Initialize the Course object with the data from the file.

    Args:
        fileName (str): The name of the file to read.

    Returns:
        course (Course): The Course object that initialized.
    """

    with open(file_name, 'r') as f:
        data = json.load(f)

    course = Course(data['course_id'],
                    data['course_name'], data['department'], data['credits'], data['time'], data['location'])

    return course


def init_student(file_name):
    """
    Initialize the Student object with the data from the file.

    Args:
        fileName (str): The name of the file to read.

    Returns:
        student (Student): The Student object that initialized.
    """

    with open(file_name, 'r') as f:
        data = json.load(f)

    student = Student(data['student_id'], data['last_name'],
                      data['first_name'], data['gender'], datetime.datetime.strptime(data['birthday'], "%Y-%m-%d"), data['department'])

    return student
