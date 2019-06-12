# coding: utf-8
'''
Collect the grades from the reviewers in the format from the file <deliverable_name>_grades.txt:
TeamID, TeamName, Grades, Reviewer Name
'''

import reviewer_grades
import input_student_names


class Student:
    def __init__(self, lastname, firstname, teamid, teamname):
        self.lastname = lastname
        self.firstname = firstname
        self.teamid = teamid
        self.teamname = teamname

    def PrintName(self):
        print("my name is", self.firstname, self.lastname)

    def GetTeamDeliverable(self, teamdeliverable, teamscore):
        self.teamdeliverable = teamdeliverable
        self.teamscore = teamscore

    def GetIndividiualDeliverable(self, indydeliverable, indyscore):
        self.indydeliverable = indydeliverable
        self.indyscore = indyscore

    def PrintStudentScore(self):
        print(str(self.lastname), "grade is", self.indyscore)

# class TeamGrades:
#         def __init__(self, deliverable, score = "100.0!"):
#             self.deliverable = deliverable
#             self.score = score
#
#         def printScore(self):
#             print("my grade is", self.deliverable, self.score)
#
# class IndividualGrades:
#         def __init__(self, deliverable, score = "101.0!"):
#             self.deliverable = deliverable
#             self.score = score
#
#         def printScore(self):
#             print("my grade is", self.deliverable, self.score)


#     def log_individual(self, lastname, firstname, deliverable, grade): #Logging method
#         self.deliverable = deliverable
#         self.grade = grade
#         filename = firstname + "_" + lastname + "_grades.txt"
#         try:
#             outputFile = open(filename, "a")
#             outputFile.write(str(deliverable) + " : " + grade)
#         except (IOError, EOFError) as e:
#             print("Testing multiple exceptions. {}".format(e.args[-1]))
#         finally:
#             outputFile.close()

#     def log_team(self, teamname, deliverable, grade): #Logging method
#         self.deliverable = deliverable
#         self.grade = grade
#         filename = firstname + "_" + lastname + "_grades.txt"
#         try:
#             outputFile = open(filename, "a")
#             outputFile.write(str(deliverable) + " : " + grade)
#         except (IOError, EOFError) as e:
#             print("Testing multiple exceptions. {}".format(e.args[-1]))
#         finally:
#             outputFile.close()





# Return dictionary of current B-Course Class
# students = input_student_names.parse_student_file("student_names.txt")
# print(Students)


if __name__  == '__main__':
    Wells = Student("David", "Wells", "US1", "BlockBusters")
    Wells.GetIndividiualDeliverable("USConOps", "51.0")
    Wells.PrintStudentScore()

# Bring in the files from the text file "file_list"


US_ConOps_grades = reviewer_grades.two_grades("Blockbusters", "US1", "ConOps")
# print(US_ConOps_grades)
# input_student_names.create_grade_files(input_student_names.parse_student_file("student_names.txt"))
