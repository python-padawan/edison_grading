# Collect the student names from the file "student_names.txt"
# The file "student_names.txt" has an order format:
# last_name, first_name, team_id , team_name

def parse_student_file(file_input):
    '''
    This function reads in the text file "student_names.txt" and places the lines
    into a list.
    The list generated is returned by the function.
    '''
    
    working_student_list = []
    student_list = []
    
    input_file = open(file_input, 'r')
    
    for lines in input_file:
        working_student_list.append(lines.strip())
    
    input_file.close()
    
    i = 0
    for i in range(len(working_student_list)):
        last_name_index = working_student_list[i].find(',')
        last_name = working_student_list[i][:last_name_index]
        student_list.append(last_name)
        
        first_name_index = working_student_list[i].find(',', last_name_index + 2)
        first_name = working_student_list[i][last_name_index + 2: first_name_index]
        student_list.append(first_name)
        
        team_id_index = working_student_list[i].find(',', first_name_index + 2)
        team_id = working_student_list[i][first_name_index + 2: team_id_index]
        student_list.append(team_id)
        
        # team_name_index = working_student_list[i].find(',', team_id_index + 2)
        team_name = working_student_list[i][team_id_index + 2:]
        student_list.append(team_name)
    return student_list
   
def create_grade_files(student_list):
    '''
    This function reads in a list and creates text files for each student
    '''
    
    student_dictionary = {}
    i = 0
    n = 4 # Number of columns in the student list
    for i in range(len(student_list)):
        if i % n == 0:
            student_dictionary[student_list[i]] = [student_list[i], 
                                                   student_list[i + 1], 
                                                   student_list[i + 2], 
                                                   student_list[i + 3]]
    
    for keys in student_dictionary.keys():
        file_name = str(student_dictionary[keys][1]) + "_" + str(student_dictionary[keys][0]) + "_grades.txt"
        output_file = open(file_name, 'w')
        output_file.write(str(student_dictionary[keys][1]) + " " + str(student_dictionary[keys][0]) + " Edison B-Course Grades\n")
        output_file.close()
    
    
# Test the file creation
# create_grade_files(parse_student_file("student_names.txt"))
