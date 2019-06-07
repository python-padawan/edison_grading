# Title - TBD
# Description - TBD

# File Dependencies - TBD

# Revision 1 - Corey Smith April 20, 2019
# Initial draft of script


'''
Notes for the script overall
1. Initially, bring in student first and last names, Team ID, Team Names.
2. Bring in student grades from reviewers
3. Compute student grades individually
4. Compute student grades as team
5. Return student grades in text format
6. Return team grades in text format
7. Pull in student and team grades from text format
8. Repeat 2 thru 7
'''

StudentList = [['Wells', 'David', 'US1', 'BlockBusters'], ['Applegate', 'Lucy', 'US2', 'Aviators'], ['Li', 'Vrushali', 'US3', 'MythBusters'], ['Yu', 'Ping', 'US4', 'HappyFeets']]



class Student:
    def __init__(self, firstname, lastname, teamid, teamname):
        #self.log("Account created!")
        self.firstname = firstname
        self.lastname = lastname
        self.teamid = teamid
        self.teamname = teamname
        
#     def getStudentGrade(self, firstname, lastname, teamname, grade = "Overall"):
#         self.log("Balance checked at " + str(self.balance))
#         return self.balance
    
#     def setStudentGrade(self, firstname, lastname, teamname, grade):
#         self.balance += amount
#         self.log("+" + str(amount) + ": " + str(self.balance))
  
        
    def log(self, firstname, lastname, grade): #Logging method
        filename = firstname + "_" + lastname + "Grades.txt"
        outputFile = open(filename, "a")
        print(grade, file = outputFile)
        outputFile.close()
        
# myBankAccount = BankAccount("David Joyner")
# myBankAccount.deposit(20.0)
# print(myBankAccount.getBalance())
# myBankAccount.withdraw(10.0)
# print(myBankAccount.getBalance()) 