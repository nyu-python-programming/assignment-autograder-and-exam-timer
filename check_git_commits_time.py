#!/usr/bin/env python3

import argparse
import datetime
import os
import re
import shutil
import time
import pandas as pd

ALLOWED_TIME_IN_SECONDS = 12600  # 3.5 * 3600


def run_command(base_path, inter_path):
    """
    Runs the git log command in each of the students' repository and logs that output to a directory
    :param base_path: Path where you have cloned repositories of a particular assignment from Github classroom
    :param inter_path: Path where you will have logs of running the tests from the cloned repositories of all
    assignments from Github classroom
    :return:
    """
    dirs = sorted(os.listdir(base_path))

    if not os.path.exists(inter_path):
        os.makedirs(inter_path)

    for _dir in dirs:
        if (_dir != "test_output_files") and (_dir != "git_log_output_files"):
            folder = os.path.join(base_path, _dir)
            print(folder)
            os.chdir(folder)
            # runs the git log command by going to that directory
            os.system("git log --format='%at' > git_log_{}.out".format(_dir))
            # copies the logs to a single directory for later use
            shutil.copy("git_log_{}.out".format(_dir), inter_path)


def generate_csv(inter_path, output_path):
    """
    Generates csv with names of each student who took more time from the logs of the command that were run in run_command
    :param inter_path: Path where you will have logs of running the tests from the cloned repositories of all
    assignments from Github classroom
    :param output_path: Path to the output csv file
    :return:
    """
    names = []
    files = sorted(os.listdir(inter_path))
    for _file in files:
        if _file.startswith("git_log_"):  # to handle the case of file .pytest_cache
            try:
                filepath = os.path.join(inter_path, _file)
                print(filepath)
                student_record = {
                    "github_username": _file.replace("git_log_", "").replace(".out", ""),
                    "time_taken": 0,
                    "remarks": ""
                }
                with open(filepath, 'r') as fp:
                    content = fp.read().strip().split('\n')

                last_commit_timestamp = int(content[0])
                first_commit_timestamp = int(content[-1])

                last_commit_datetime = datetime.datetime.fromtimestamp(last_commit_timestamp)
                first_commit_datetime = datetime.datetime.fromtimestamp(first_commit_timestamp)

                time_taken = last_commit_datetime - first_commit_datetime
                time_taken_str = str(time_taken)

                if (time_taken.total_seconds() > ALLOWED_TIME_IN_SECONDS):
                    student_record["time_taken"] = time_taken_str
                    student_record["remarks"] = "You took {} time to complete the assignment".format(time_taken_str)
                    names.append(student_record)
            except Exception as ex:
                print("=================== Exception for {} ===================".format(_file))

    df = pd.DataFrame(names)
    df.to_csv(output_path, index=False)


def parse_args():
    """
    Parses the commmand line arguments to check_git_commits_time.py
    :return:
    parsed command line arguments
    """
    parser = argparse.ArgumentParser(description="Grading Intro to Programming (Python) assignments")
    parser.add_argument("-b", "--base_path", type=str, required=True,
                        help="Path where you have cloned repositories of exam from Github classroom")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    inter_path = os.path.join(args.base_path, "git_log_output_files")
    output_path = os.path.join(inter_path, "students.csv")
    run_command(args.base_path, inter_path)
    generate_csv(inter_path, output_path)
