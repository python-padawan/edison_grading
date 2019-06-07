'''
Collect the grades from the reviewers in the format from the file <deliverable_name>_grades.txt:
TeamID, TeamName, Grades, Reviewer Name
'''

import reviewer_grades
import input_student_names

US_ConOps_grades = reviewer_grades.two_grades("Blockbusters", "US1", "ConOps")
print(US_ConOps_grades)
input_student_names.create_grade_files(input_student_names.parse_student_file("student_names.txt"))