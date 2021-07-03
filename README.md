# Unit Test-Based Assignment Autograder and Timer

This repository contains two Python scripts to help autograde student work in a Python programming course that uses GitHub Classroom.

Contents:

- a script that runs `pytest`-based unit tests on a batch of student assignemnt submissions and saves the resulting grades into a CSV file.
- a script that checks git logs to determine whether each student pushed their code within a given number of hours after they began (good for timed exams), and saves results into a CSV file.

A few assumptions:

- all student code for a given assignment is placed within sub-directories (one subdirectory per student) of a main directory for the assignment. This matches the way that GitHub Classroom Assistant delivers student submissions.
- unit tests used to evaluate the assignment submissions are placed within each student's directory in a subdirectory named, `tests`.
- work is delivered to students as GitHub Classroom assignments, where new git repositories are generated for students when they "accept" an assignment.

## Grade assignments

The script, [grade_assignments.py](./grade_assignments.py), autogrades student work by running `pytest`-based unit tests.

- Make this script executable and run, `./grade_assignments.py --base_path path_to_main_assignment_directory` or `python3 grade_assignments.py --base_path path_to_main_assignment_directory`, where `path_to_main_assignment_directory` is replaced by your main assignment directory.
- Grades for all students will be saved into a CSV file named, `test_output_files/marks.csv` within the assignment main directory.

## Check time taken to complete assignment or exam

The script, [check_git_commits_time.py](./check_git_commits_time.py), determines whether students pushed their code within a given number of hours after their git repositories were initialized. This is especially useful for exams where students are timed from the moment they begin the exam.

- Make this script executable and run, `./check_git_commits_time.py --base_path path_to_main_assignment_directory` or `python3 check_git_commits_time.py --base_path path_to_main_assignment_directory`, where `path_to_main_assignment_directory` is replaced by your main assignment directory.
- Add an optional `--time_allowed` flag with the number of minutes allowed for the exam. For example, `./check_git_commits_time.py --base_path path_to_main_assignment_directory --time_allowed 120`
- Names and time taken by students over the allowed limit will be saved into a CSV file named, `git_log_output_files/students.csv` within the assignment main directory.
