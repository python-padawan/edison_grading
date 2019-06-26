'''
Details of script...

1. Read in student names from text file
    A. A dictionary is created with Student's last name as key
    B. The dictionary has first name, last name, team id, and team name

2. Check to see if grades already exist
    A. If exists, append, and if not, create and write.
    
3. Read in grades from text file

4. Compute grades
    A. Take average all of grades with grading weights
    B. Return grades in team format
    
5. Output grades
    A. Output grade for individual student
    B. Output grade for team 
    C. Output grade for master file    
'''

import reviewer_grades
import input_student_names
import csv

# US_ConOps_grades = reviewer_grades.two_grades("US1", "ConOps")
# # print(US_ConOps_grades)
student_dict = input_student_names.parse_student_file("student_names.txt")


def calc_grades_from_file(filename, grades_2_score = 2):
    team_id = filename[:filename.find('_')]
    deliverable = filename[filename.find('_') + 1:filename.find('_', filename.find('_') + 2)]
    
    if grades_2_score == 2:
        return reviewer_grades.two_grades(team_id, deliverable)
    elif grades_2_score == 3:
        return reviewer_grades.three_grades(team_id, deliverable)
    elif grades_2_score == 4:
        return reviewer_grades.four_grades(team_id, deliverable)
    elif grades_2_score == 5:
        return reviewer_grades.five_grades(team_id, deliverable)
    elif grades_2_score == 6:
        return reviewer_grades.six_grades(team_id, deliverable)
    
    
def compute_grades(file_list):
    i = 0
    returned_grades = []
    for i in range(len(file_list)):
        returned_grades.append(calc_grades_from_file(file_list[i], 2))
    return returned_grades


class Student:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.teamid = student_dict[self.lastname][2]
        self.teamname = student_dict[self.lastname][3]
        
    def log_team_grade(self, teamid):
        pass
    
        

#     def printName(self):
#         print("My name is", self.firstname, self.lastname, self.teamid, self.teamname)



D_Wells = Student("David", "Wells")
Student.printName(D_Wells) 




# # Text Files to compute grades
US1_Grades = [
    "US1_ConOps_grades.txt", 
    "US1_RFI_grades.txt"
    ]


print(compute_grades(US1_Grades))
