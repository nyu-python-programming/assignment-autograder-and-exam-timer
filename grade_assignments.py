import argparse
import os
import re
import shutil
import time
import pandas as pd


def run_tests(base_path, inter_path):
    """
    Runs the pre-defined tests in each of the students' repository and logs that output to a directory
    :param base_path: Path where you have cloned repositories of a particular assignment from Github classroom
    :param inter_path: Path where you will have logs of running the tests from the cloned repositories of all
    assignments from Github classroom
    :return:
    """
    dirs = sorted(os.listdir(base_path))

    if not os.path.exists(inter_path):
        os.makedirs(inter_path)

    for _dir in dirs:
        if _dir != "test_output_files":
            folder = os.path.join(base_path, _dir)
            print(folder)
            os.chdir(folder)
            # runs the tests by going to that directory
            os.system("python3 -m pytest tests/ > test_{}.out".format(_dir))
            # copies the logs to a single directory for later use
            shutil.copy("test_{}.out".format(_dir), inter_path)


def generate_csv(inter_path, output_path):
    """
    Generates csv with grades for each student from the logs of the tests that were run in run_tests
    :param inter_path: Path where you will have logs of running the tests from the cloned repositories of all
    assignments from Github classroom
    :param output_path: Path to the output csv file with marks
    :return:
    """
    grades = []
    files = sorted(os.listdir(inter_path))
    for _file in files:
        if _file.startswith("test_"):  # to handle the case of file .pytest_cache
            try:
                filepath = os.path.join(inter_path, _file)
                print(filepath)
                student_grade = {
                    "github_username": _file.replace("test_", "").replace(".out", ""),
                    "total_points": 0,
                    "remarks": ""
                }
                with open(filepath, 'r') as fp:
                    content = fp.readlines()

                # Handles the case where we encounter error running the test cases which implicitly means that the
                # underlying code has errors and so 0 marks for that
                if "ERRORS" in "".join(content):
                    student_grade["remarks"] = "Error running the test cases"
                    grades.append(student_grade)
                    continue

                remarks = ""
                total_tests = int(content[3].replace("collected ", "").replace(" items", ""))
                passed_tests = 0

                test_result_finds = re.findall(r"(\d)*\s+(failed|passed)", content[-1])
                for _result in test_result_finds:
                    if _result[1] == "passed":
                        passed_tests = int(_result[0])

                remarks += "Out of {} tests, your code passed {} and failed {}.".format(total_tests, passed_tests,
                                                                                        total_tests - passed_tests)

                # Adds the brief summary of test cases if any one of them has failed
                if " short test summary info " in "".join(content):
                    remarks += " Specific areas that were not completely correct were the functions named, "
                    failed_messages_list = "".join(content).split(" short test summary info ")[1].split("\n")[1:-2]
                    for message in failed_messages_list:
                        remarks += "{}, ".format(message.split("Tests::")[1].split(" - ")[0])
                remarks = remarks.strip(", ")

                # the marks are given with an assumption that each test has an equal weightage to the final marks
                student_grade["total_points"] = passed_tests * (100 / total_tests)
                student_grade["remarks"] = remarks.strip()
                grades.append(student_grade)
            except Exception as ex:
                print("=================== Exception for {} ===================".format(_file))

    df = pd.DataFrame(grades)
    df.to_csv(output_path, index=False)


def parse_args():
    """
    Parses the commmand line arguments to grade_assignments.py
    :return:
    parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Grading Intro to Programming (Python) assignments")
    parser.add_argument("-b", "--base_path", type=str, required=True,
                        help="Path where you have cloned repositories of a particular assignment from Github classroom")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    inter_path = os.path.join(args.base_path, "test_output_files")
    output_path = os.path.join(inter_path, "marks.csv")
    run_tests(args.base_path, inter_path)
    generate_csv(inter_path, output_path)
