

def two_grades(teamName, teamID, deliverable):
    '''
    This function reads in the text file, "<team_id>_<deliverable>_grades.txt", and places the lines 
    into a manageable list.
    The list generated is returned by the function.
    The text file will have the format:
    "TeamName, Grade1, Grade2 ReviewerFirstName"
    '''
    
    file_name = teamID + '_' + deliverable + "_grades.txt"
    input_file = open(file_name, 'r')
    working_grades_list = []
    master_list = []
    grade_1_list = []
    grade_2_list = []
    
    for items in input_file:
        working_grades_list.append(items.strip())
    
    input_file.close()

    i = 0
    for i in range(len(working_grades_list)):
        team_name_index = working_grades_list[i].find(',')
        team_name = working_grades_list[i][:team_name_index]
        master_list.append(team_name)
        
        grade_1_index = working_grades_list[i].find(',', team_name_index + 2)
        grade_1 = working_grades_list[i][team_name_index + 2:grade_1_index]
        master_list.append(grade_1)
        grade_1_list.append(grade_1)
        
        grade_2_index = working_grades_list[i].find(',', grade_1_index + 2)
        grade_2 = working_grades_list[i][grade_1_index + 2:grade_2_index]
        master_list.append(grade_2)
        grade_2_list.append(grade_2)
        
        #reviewer_index = working_grades_list[i].find(',', grade_2_index + 2)
        reviewer = working_grades_list[i][grade_2_index + 2:]
        master_list.append(reviewer)
        
    grade_1_avg = 0       
    for grades in grade_1_list:
        grade_1_avg += int(grades)
    grade_1_avg /= len(grade_1_list)

    grade_2_avg = 0       
    for grades in grade_2_list:
        grade_2_avg += int(grades)
    grade_2_avg /= len(grade_2_list)
    
    return [teamID, deliverable, grade_1_avg, grade_2_avg]



def three_grades(teamName, teamID, deliverable):
    '''
    This function reads in the text file, "<team_id>_<deliverable>_grades.txt", and places the lines 
    into a manageable list.
    The list generated is returned by the function.
    The text file will have the format:
    "TeamName, Grade1, Grade2, Grade3 ReviewerFirstName"
    '''
    
    file_name = teamID + '_' + deliverable + "_grades.txt"
    input_file = open(file_name, 'r')
    working_grades_list = []
    master_list = []
    grade_1_list = []
    grade_2_list = []
    grade_3_list = []
    
    for items in input_file:
        working_grades_list.append(items.strip())
    
    input_file.close()

    i = 0
    for i in range(len(working_grades_list)):
        team_name_index = working_grades_list[i].find(',')
        team_name = working_grades_list[i][:team_name_index]
        master_list.append(team_name)
        
        grade_1_index = working_grades_list[i].find(',', team_name_index + 2)
        grade_1 = working_grades_list[i][team_name_index + 2:grade_1_index]
        master_list.append(grade_1)
        grade_1_list.append(grade_1)
        
        grade_2_index = working_grades_list[i].find(',', grade_1_index + 2)
        grade_2 = working_grades_list[i][grade_1_index + 2:grade_2_index]
        master_list.append(grade_2)
        grade_2_list.append(grade_2)
        
        grade_3_index = working_grades_list[i].find(',', grade_2_index + 2)
        grade_3 = working_grades_list[i][grade_2_index + 2:grade_3_index]
        master_list.append(grade_3)
        grade_3_list.append(grade_3)
        
        #reviewer_index = working_grades_list[i].find(',', grade_3_index + 2)
        reviewer = working_grades_list[i][grade_3_index + 2:]
        master_list.append(reviewer)
        
    grade_1_avg = 0       
    for grades in grade_1_list:
        grade_1_avg += int(grades)
    grade_1_avg /= len(grade_1_list)

    grade_2_avg = 0       
    for grades in grade_2_list:
        grade_2_avg += int(grades)
    grade_2_avg /= len(grade_2_list)
    
    grade_3_avg = 0       
    for grades in grade_3_list:
        grade_3_avg += int(grades)
    grade_3_avg /= len(grade_3_list)

    return [teamID, deliverable, grade_1_avg, grade_2_avg, grade_3_avg]



def four_grades(teamName, teamID, deliverable):
    '''
    This function reads in the text file, "<team_id>_<deliverable>_grades.txt", and places the lines 
    into a manageable list.
    The list generated is returned by the function.
    The text file will have the format:
    "TeamName, Grade1, Grade2, Grade3, Grade4, ReviewerFirstName"
    '''
    
    file_name = teamID + '_' + deliverable + "_grades.txt"
    input_file = open(file_name, 'r')
    working_grades_list = []
    master_list = []
    grade_1_list = []
    grade_2_list = []
    grade_3_list = []
    grade_4_list = []
    
    for items in input_file:
        working_grades_list.append(items.strip())
    
    input_file.close()

    i = 0
    for i in range(len(working_grades_list)):
        team_name_index = working_grades_list[i].find(',')
        team_name = working_grades_list[i][:team_name_index]
        master_list.append(team_name)
        
        grade_1_index = working_grades_list[i].find(',', team_name_index + 2)
        grade_1 = working_grades_list[i][team_name_index + 2:grade_1_index]
        master_list.append(grade_1)
        grade_1_list.append(grade_1)
        
        grade_2_index = working_grades_list[i].find(',', grade_1_index + 2)
        grade_2 = working_grades_list[i][grade_1_index + 2:grade_2_index]
        master_list.append(grade_2)
        grade_2_list.append(grade_2)
        
        grade_3_index = working_grades_list[i].find(',', grade_2_index + 2)
        grade_3 = working_grades_list[i][grade_2_index + 2:grade_3_index]
        master_list.append(grade_3)
        grade_3_list.append(grade_3)
        
        grade_4_index = working_grades_list[i].find(',', grade_3_index + 2)
        grade_4 = working_grades_list[i][grade_3_index + 2:grade_4_index]
        master_list.append(grade_4)
        grade_4_list.append(grade_4)
        
        #reviewer_index = working_grades_list[i].find(',', grade_4_index + 2)
        reviewer = working_grades_list[i][grade_4_index + 2:]
        master_list.append(reviewer)
        
    grade_1_avg = 0       
    for grades in grade_1_list:
        grade_1_avg += int(grades)
    grade_1_avg /= len(grade_1_list)

    grade_2_avg = 0       
    for grades in grade_2_list:
        grade_2_avg += int(grades)
    grade_2_avg /= len(grade_2_list)
    
    grade_3_avg = 0       
    for grades in grade_3_list:
        grade_3_avg += int(grades)
    grade_3_avg /= len(grade_3_list)

    grade_4_avg = 0       
    for grades in grade_4_list:
        grade_4_avg += int(grades)
    grade_4_avg /= len(grade_4_list)
    
    return [teamID, deliverable, grade_1_avg, grade_2_avg, grade_3_avg, grade_4_avg]



def five_grades(teamName, teamID, deliverable):
    '''
    This function reads in the text file, "<team_id>_<deliverable>_grades.txt", and places the lines 
    into a manageable list.
    The list generated is returned by the function.
    The text file will have the format:
    "TeamName, Grade1, Grade2, Grade3, Grade4, Grade5, ReviewerFirstName"
    '''
    
    file_name = teamID + '_' + deliverable + "_grades.txt"
    input_file = open(file_name, 'r')
    working_grades_list = []
    master_list = []
    grade_1_list = []
    grade_2_list = []
    grade_3_list = []
    grade_4_list = []
    grade_5_list = []
    
    for items in input_file:
        working_grades_list.append(items.strip())
    
    input_file.close()

    i = 0
    for i in range(len(working_grades_list)):
        team_name_index = working_grades_list[i].find(',')
        team_name = working_grades_list[i][:team_name_index]
        master_list.append(team_name)
        
        grade_1_index = working_grades_list[i].find(',', team_name_index + 2)
        grade_1 = working_grades_list[i][team_name_index + 2:grade_1_index]
        master_list.append(grade_1)
        grade_1_list.append(grade_1)
        
        grade_2_index = working_grades_list[i].find(',', grade_1_index + 2)
        grade_2 = working_grades_list[i][grade_1_index + 2:grade_2_index]
        master_list.append(grade_2)
        grade_2_list.append(grade_2)
        
        grade_3_index = working_grades_list[i].find(',', grade_2_index + 2)
        grade_3 = working_grades_list[i][grade_2_index + 2:grade_3_index]
        master_list.append(grade_3)
        grade_3_list.append(grade_3)
        
        grade_4_index = working_grades_list[i].find(',', grade_3_index + 2)
        grade_4 = working_grades_list[i][grade_3_index + 2:grade_4_index]
        master_list.append(grade_4)
        grade_4_list.append(grade_4)
        
        grade_5_index = working_grades_list[i].find(',', grade_4_index + 2)
        grade_5 = working_grades_list[i][grade_4_index + 2:grade_5_index]
        master_list.append(grade_5)
        grade_5_list.append(grade_5)
        
        #reviewer_index = working_grades_list[i].find(',', grade_5_index + 2)
        reviewer = working_grades_list[i][grade_5_index + 2:]
        master_list.append(reviewer)
        
    grade_1_avg = 0       
    for grades in grade_1_list:
        grade_1_avg += int(grades)
    grade_1_avg /= len(grade_1_list)

    grade_2_avg = 0       
    for grades in grade_2_list:
        grade_2_avg += int(grades)
    grade_2_avg /= len(grade_2_list)
    
    grade_3_avg = 0       
    for grades in grade_3_list:
        grade_3_avg += int(grades)
    grade_3_avg /= len(grade_3_list)

    grade_4_avg = 0       
    for grades in grade_4_list:
        grade_4_avg += int(grades)
    grade_4_avg /= len(grade_4_list)
    
    grade_5_avg = 0       
    for grades in grade_5_list:
        grade_5_avg += int(grades)
    grade_5_avg /= len(grade_5_list)
    
    return [teamID, deliverable, grade_1_avg, grade_2_avg, grade_3_avg, grade_4_avg, grade_5_avg]



def six_grades(teamName, teamID, deliverable):
    '''
    This function reads in the text file, "<team_id>_<deliverable>_grades.txt", and places the lines 
    into a manageable list.
    The list generated is returned by the function.
    The text file will have the format:
    "TeamName, Grade1, Grade2, Grade3, Grade4, Grade5, Grade6, ReviewerFirstName"
    '''
    
    file_name = teamID + '_' + deliverable + "_grades.txt"
    input_file = open(file_name, 'r')
    working_grades_list = []
    master_list = []
    grade_1_list = []
    grade_2_list = []
    grade_3_list = []
    grade_4_list = []
    grade_5_list = []
    grade_6_list = []
    
    for items in input_file:
        working_grades_list.append(items.strip())
    
    input_file.close()

    i = 0
    for i in range(len(working_grades_list)):
        team_name_index = working_grades_list[i].find(',')
        team_name = working_grades_list[i][:team_name_index]
        master_list.append(team_name)
        
        grade_1_index = working_grades_list[i].find(',', team_name_index + 2)
        grade_1 = working_grades_list[i][team_name_index + 2:grade_1_index]
        master_list.append(grade_1)
        grade_1_list.append(grade_1)
        
        grade_2_index = working_grades_list[i].find(',', grade_1_index + 2)
        grade_2 = working_grades_list[i][grade_1_index + 2:grade_2_index]
        master_list.append(grade_2)
        grade_2_list.append(grade_2)
        
        grade_3_index = working_grades_list[i].find(',', grade_2_index + 2)
        grade_3 = working_grades_list[i][grade_2_index + 2:grade_3_index]
        master_list.append(grade_3)
        grade_3_list.append(grade_3)
        
        grade_4_index = working_grades_list[i].find(',', grade_3_index + 2)
        grade_4 = working_grades_list[i][grade_3_index + 2:grade_4_index]
        master_list.append(grade_4)
        grade_4_list.append(grade_4)
        
        grade_5_index = working_grades_list[i].find(',', grade_4_index + 2)
        grade_5 = working_grades_list[i][grade_4_index + 2:grade_5_index]
        master_list.append(grade_5)
        grade_5_list.append(grade_5)
        
        grade_6_index = working_grades_list[i].find(',', grade_5_index + 2)
        grade_6 = working_grades_list[i][grade_5_index + 2:grade_6_index]
        master_list.append(grade_6)
        grade_6_list.append(grade_6)
        
        #reviewer_index = working_grades_list[i].find(',', grade_6_index + 2)
        reviewer = working_grades_list[i][grade_6_index + 2:]
        master_list.append(reviewer)
        
    grade_1_avg = 0       
    for grades in grade_1_list:
        grade_1_avg += int(grades)
    grade_1_avg /= len(grade_1_list)

    grade_2_avg = 0       
    for grades in grade_2_list:
        grade_2_avg += int(grades)
    grade_2_avg /= len(grade_2_list)
    
    grade_3_avg = 0       
    for grades in grade_3_list:
        grade_3_avg += int(grades)
    grade_3_avg /= len(grade_3_list)

    grade_4_avg = 0       
    for grades in grade_4_list:
        grade_4_avg += int(grades)
    grade_4_avg /= len(grade_4_list)
    
    grade_5_avg = 0       
    for grades in grade_5_list:
        grade_5_avg += int(grades)
    grade_5_avg /= len(grade_5_list)

    grade_6_avg = 0       
    for grades in grade_6_list:
        grade_6_avg += int(grades)
    grade_6_avg /= len(grade_6_list)
    
    return [teamID, deliverable, grade_1_avg, grade_2_avg, grade_3_avg, grade_4_avg, grade_5_avg, grade_6_avg]


