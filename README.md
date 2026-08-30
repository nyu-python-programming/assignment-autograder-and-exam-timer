# Assignment Autograder and Exam Timer

This repository contains two Python scripts to help autograde student work in a Python programming course that distributes assignments and exams as GitHub repositories.

Contents:

- a script that runs `pytest`-based unit tests on a batch of student assignemnt submissions and saves the resulting grades into a CSV file.
- a script that checks `git log` to determine whether each student pushed their code within the allowed time (good for timed exams), and saves results into a CSV file.

A few assumptions:

- all student code for a given assignment is placed within sub-directories (one subdirectory per student) of a main directory for the assignment. Cloning each student's fork into a single directory produces this layout.
- `pytest`-based unit tests used to evaluate the assignment submissions are placed within each student's directory.
- work is delivered to students as GitHub repositories, which students `fork` into their own accounts and then push their work to.

> Note: the exam timer measures the time between the creation of a repository and the final push. A fork inherits the full history of the repository it was forked from, so this measurement is not meaningful for forked repositories and needs to be reworked to measure from the student's first own commit instead.

## Install dependencies

Install all dependencies with `pipenv`, i.e. `pipenv install`. Then activate the virtual environment with `pipenv shell`.

Alternatively, if you prefer, you can use `pip`, i.e. `pip install -r requirements.txt` (or `pip3 install -r requirements.txt`)

## Grade assignments

The script, [grade_assignments.py](./grade_assignments.py), autogrades student work by running `pytest`-based unit tests.

- Make this script executable and run, `./grade_assignments.py --base_path path_to_main_assignment_directory` or `python3 grade_assignments.py --base_path path_to_main_assignment_directory`, where `path_to_main_assignment_directory` is replaced by your main assignment directory.
- Grades for all students will be saved into a CSV file named, `test_output_files/marks.csv` within the assignment main directory.

## Check time taken to complete assignment or exam

The script, [check_git_commits_time.py](./check_git_commits_time.py), identifies students who took longer than allowed to complete an exam or assignment. This is especially useful for exams where students can start at a time of their choosing, but are timed from the moment they begin.

- Make this script executable (i.e. `chmod u+x *.py`) and run, `./check_git_commits_time.py --base_path path_to_main_assignment_directory` or `python3 check_git_commits_time.py --base_path path_to_main_assignment_directory`, where `path_to_main_assignment_directory` is replaced by your main assignment directory.
- Add an optional `--time_allowed` flag with the number of minutes allowed for the exam. For example, `./check_git_commits_time.py --base_path path_to_main_assignment_directory --time_allowed 120`. The allowed time defaults to `3.5` hours.
- Names and time taken by students over the allowed limit will be saved into a CSV file named, `git_log_output_files/students.csv` within the assignment main directory.
