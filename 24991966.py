"""
Student ID: 24991966
Student Name: Elvis Chi Hin Suen
Date: 28/3/2025
Project description: CITS1401 project 1

"""
def main(csvfile_1, csvfile_2, age, sa2_1, sa2_2):
    
    OP1 = op1(csvfile_2,age)
    OP2 = op2_testing_1(csvfile_1,csvfile_2, age, sa2_1, sa2_2, OP1)
    OP3 = op3_testing_1(csvfile_1,csvfile_2, age, OP1)
    OP4 = op4_testing(csvfile_2,sa2_1, sa2_2)
    
    return OP1,OP2,OP3,OP4
#Output 1
def op1(csvfile_2,age):
    csvfile_2_a = open(csvfile_2,"r")
    reading_list_population = []
    string_all_age_group = []
    
    #only read and take out the heading of the data 
    for i in range (1):
        readlines_population = csvfile_2_a.readline()
        reading_line_population = readlines_population.split(",")
    #print(reading_line_population[2:])
    # to get each element in the group to remove not require string and make them into the form that is required
    for k in range(2,int(len(reading_line_population))):
        string_age_group = reading_line_population[k]

        string_age_group = string_age_group.replace("Age ","")
        string_age_group = string_age_group.replace(" and over\n","")
        string_age_group = string_age_group.split("-")
       
        #have to deal with the last element which need a None vaule as a range 
        if k != int(len(reading_line_population))-1:
            string_age_group_0 = int(string_age_group[0])
            string_age_group_1 = int(string_age_group[1])
            string_agelist = [string_age_group_0,string_age_group_1]
            string_all_age_group = string_all_age_group + [string_agelist]
        else:
            string_age_group_0 = int(string_age_group[0])
            last_element = [int(string_age_group_0),None]
            string_all_age_group = string_all_age_group + [last_element] #last element sytnax
    #print(string_all_age_group)
 
    # to search for the age group using the two number in the age group
    for list_for_looping in string_all_age_group:
        if age >= 0 and age <= 84:
            if age >= list_for_looping[0] and age <= list_for_looping[1]:
                return list_for_looping
        elif age >= 85:
            return string_all_age_group[-1]

#Output 2
def op2_testing_1(csvfile_1, csvfile_2, age, sa2_1, sa2_2, op1):
    
    #to find particular age group and save the position 
    Look_for_age_group = open(csvfile_2,"r")
    
    read_age_group_lines = Look_for_age_group.readline()
    reading_age_group_line = read_age_group_lines.split(",")
    #print(reading_age_group_line)
    
    age_group_look_for = "Age " + str(op1[0]) + "-" + str(op1[1])
    #print(age_group_look_for)
    
    # to deal with the special case of age group 85 and over
    if age_group_look_for == "Age 85-None":
        generalisation_age_group_position = 19
        op1[0] = 85
        op1[1] = float("inf")

    else:
        generalisation_age_group_position = reading_age_group_line.index(age_group_look_for)
   
    
    #print(generalisation_age_group_position)#generalisation of age group position
        
    Look_for_age_group.close()
    
    #open and read the data length to obtain the length
    data_length = open(csvfile_1,"r")
    
    data_length_reference = len(list(data_length))
    #print(data_length_reference)#testing length of data file
    
    data_length.close()
    
    #get the 1st input for input4
    csvfile_1_a = open(csvfile_1,"r")
    
    reading_list = []
    # to get the SA3
    for i in range (data_length_reference):
        readlines = csvfile_1_a.readline()
        reading_line = readlines.split(",")
        #trying to put each column in a row as a element in list
        #print(reading_line,reading_line[4])
        #print(reading_line[2])
        # check the first 5 number
        sa2_1_first_5_number = sa2_1[0:5]
        if reading_line[2] == sa2_1_first_5_number:
            reading_list = reading_list + [reading_line]
    print(sa2_1_first_5_number)#test
    #check the list
    #print(reading_list)
    
    # to get the all SA2 code with the same first 5 number as it is the SA3 code; for input4
    SA2_code = []
    for l in range(0,len(reading_list)):
        SA2_code = SA2_code + [reading_list[l][4]] 
    #print(sa2_1_first_5_number)#test
    #print(SA2_code)#test
    
    #print(reading_list)#test
    #print(reading_list[0][2])#test
    
    #to get the population data from population, and put it into list for input 4 
    csvfile_2_a = open(csvfile_2,"r")
    reading_list_population = []
    
    for i in range (data_length_reference):
        readlines_population = csvfile_2_a.readline()
        reading_line_population = readlines_population.split(",")
        #reading_list = reading_list + [reading_line]
        for p in range(len(SA2_code)): 
            if reading_line_population[0] == SA2_code[p]:
                reading_list_population = reading_list_population +[reading_line_population]
    #print(reading_list_population)#test
    
    #input4 calculation on mean and sample SD
    population_g1 = []
    population_g1_a = []
    
    if age >= op1[0] and age <= op1[1]:#
        for ages_position in range(len(SA2_code)):
            #print(reading_list_population[ages_position])
            population_g1.append(int(reading_list_population[ages_position][generalisation_age_group_position]))#
        #print(population_g1)
        average_population_g1 = sum(population_g1)/len(population_g1)
        #print(average_population_g1)#test
        
        sum1 = 0 
        for ages_position in range(len(SA2_code)):
            population_g1_a.append(int(reading_list_population[ages_position][generalisation_age_group_position]))
            #print(population_g1_a)#test
            #print(reading_list_population[ages_position][2])#test
            sum1 = sum1 + ((float(reading_list_population[ages_position][generalisation_age_group_position]) - average_population_g1 ) ** 2) 
            #print(sum1)#
        sample_SD = f"{(sum1/(len(SA2_code) - 1)) ** 0.5:0.4f}"
        sample_SD = float(sample_SD)
        #print(sample_SD)#
        
        
        answer = [sa2_1_first_5_number,average_population_g1,sample_SD]
        #print(answer)
        csvfile_1_a.close()
        csvfile_2_a.close()
        
        
     
    #2nd input from input5
    csvfile_1_a = open(csvfile_1,"r")
    reading_list_2nd = []
        
    
    # to get the SA3
    for i in range (data_length_reference):
        readlines_2nd = csvfile_1_a.readline()
        reading_line_2nd = readlines_2nd.split(",")
        #trying to put each column in a row as a element in list
        #print(reading_line_2nd,reading_line_2nd[4])
        #print(reading_line_2nd[0])
        # check the first 5 number
        sa2_1_first_5_number_2nd = sa2_2[0:5]
        
        if reading_line_2nd[2] == sa2_1_first_5_number_2nd:
            reading_list_2nd = reading_list_2nd + [reading_line_2nd]
    #print(reading_list_2nd)#
    csvfile_1_a.close()
    
    # to get the all SA2 code with the same first 5 number as it is the SA3 code; for input5
    SA2_code_2nd = []
    for l in range(0,len(reading_list_2nd)):
        SA2_code_2nd = SA2_code_2nd + [reading_list_2nd[l][4]] 
    #print(sa2_1_first_5_number)#
    #print(SA2_code)#
    #print(SA2_code_2nd)#
    #print(reading_list)#
    #print(reading_list[0][2])#
    
    #to get the population data from population, and put it into list for input 5
    csvfile_2_a = open(csvfile_2,"r")
    reading_list_population_2nd = []
    
    for i in range(data_length_reference):
        readlines_population_2nd = csvfile_2_a.readline()
        reading_line_population_2nd = readlines_population_2nd.split(",")
       
        for p in range(len(SA2_code_2nd)): 
            if reading_line_population_2nd[0] == SA2_code_2nd[p]:
                reading_list_population_2nd = reading_list_population_2nd +[reading_line_population_2nd]
    #print(reading_list_population)#
    
    #input5 calculation on mean and sample SD
    population_g1_2nd = []
    population_g1_a_2nd = []
    if age >= op1[0] and age <= op1[1]:
        for ages_position_2nd in range(len(SA2_code_2nd)):
            population_g1_2nd.append(int(reading_list_population_2nd[ages_position_2nd][generalisation_age_group_position]))
        
        average_population_g1_2nd = sum(population_g1_2nd)/len(population_g1_2nd)
        #print(average_population_g1_2nd)#test
        
        sum1_2nd = 0 
        for ages_position_2nd in range(len(SA2_code_2nd)):
            population_g1_a_2nd.append(int(reading_list_population_2nd[ages_position_2nd][generalisation_age_group_position]))
            #print(population_g1_a_2nd)#test
            #print(reading_list_population_2nd[ages_position_2nd][2])#test
            sum1_2nd = sum1_2nd + ((float(reading_list_population_2nd[ages_position_2nd][generalisation_age_group_position]) - average_population_g1_2nd ) ** 2) 
            #print(sum1_2nd)#test
        sample_SD_2nd = f"{(sum1_2nd/(len(SA2_code_2nd) - 1)) ** 0.5:0.4f}"
        sample_SD_2nd = float(sample_SD_2nd)
        #print(sample_SD_2nd)#test
        
        
        answer2 = [sa2_1_first_5_number_2nd,average_population_g1_2nd,sample_SD_2nd]
        #print(answer2)
        
        
        
        
        
        return [answer,answer2]
       
    
    
    
    csvfile_1_a.close()
    csvfile_2_a.close()


#Output 3
def op3_testing_1(csvfile_1, csvfile_2, age, op1):
    
    #to find particular age group and save the position 
    Look_for_age_group = open(csvfile_2,"r")
    
    read_age_group_lines = Look_for_age_group.readline()
    reading_age_group_line = read_age_group_lines.split(",")
    #print(reading_age_group_line)
    age_group_look_for = "Age " + str(op1[0]) + "-" + str(op1[1])
    #print(age_group_look_for)
    # for debugg documentation
    if age_group_look_for == "Age 85-inf":
        generalisation_age_group_position = 19
        op1[0] = 85
        op1[1] = None

    else:
        generalisation_age_group_position = reading_age_group_line.index(age_group_look_for)
    
    
    #print(generalisation_age_group_position)#generalisation of age group position
        
    Look_for_age_group.close()
    
    #open and read the data length to obtain the length
    data_length = open(csvfile_1,"r")
    
    data_length_reference = len(list(data_length))
    #print(data_length_reference)#testing length of data file#539
    
    data_length.close()
    
    
    
    
    #get the unqiue State code and its length
    data_unique_S_T_code = open(csvfile_1,"r")
    
    unique_S_T_code_list = []
    unique_S_T_code = "S_T code"
    for u in range(data_length_reference):
        read_unique_S_T_code = data_unique_S_T_code.readline()
        reading_unique_S_T_code = read_unique_S_T_code.split(",")
        if unique_S_T_code != reading_unique_S_T_code[0]:
            unique_S_T_code = reading_unique_S_T_code[0]
            unique_S_T_code_addition = unique_S_T_code
            unique_S_T_code_list = unique_S_T_code_list +[unique_S_T_code_addition]
            unique_S_T_code_list.sort()
    #print(unique_S_T_code_list)#string#testing need to reopen
    #print(len(unique_S_T_code_list))#3
    data_unique_S_T_code.close()
    
    data_length_unique_S_T_code = open(csvfile_1,"r")
    
    unique_S_T_code_list_length =[]
    unique_S_T_code = "S_T code"
    for u in range(data_length_reference):
        read_unique_S_T_code = data_length_unique_S_T_code.readline()
        reading_unique_S_T_code = read_unique_S_T_code.split(",")
        
        if unique_S_T_code != reading_unique_S_T_code[0]:
            #print(reading_unique_S_T_code[0])
            unique_S_T_code_list_length = unique_S_T_code_list_length + [reading_unique_S_T_code[0]]
            unique_S_T_code_list_length.sort()
    #print(unique_S_T_code_list_length)#testing need to reopen
           
    
    data_length_unique_S_T_code.close()   
 
    # to get the state name in list 
    csvfile_1_a = open(csvfile_1,"r")
    
    
    state_list = []
    state_name = "S_T name"
    selective_5_digit =[]
    selective_5_digit_list =[]
    
   
    for i in range (data_length_reference):
        readlines = csvfile_1_a.readline()
        reading_line = readlines.split(",")
        #reading_list = reading_list + reading_line
        #trying to put each column in a row as a element in list
        #print(reading_line,reading_line[4])
        #print(reading_line[1])
        if state_name != reading_line[1]:
            state_name = reading_line[1]
            state_name_addation = [state_name.lower()]  #i can add more list
            state_list = state_list + state_name_addation
            #print(state_list)# test for sort in to alphabetic order
            #state_list.sort()
            
    #print(state_list)#testing need to reopen#part of answer!!!!!!!
    
    csvfile_1_a.close()
    
    
    
    
    #length of SA2 and read the data line from population data 
    csvfile_2_a = open(csvfile_2,"r")
    SA2_code = "Area_Code_Level2"
    SA2_code_list = []
    reading_line_sa2_list =[]
    for k in range (data_length_reference):#539
        readlines_2 = csvfile_2_a.readline()
        reading_line_2 = readlines_2.split(",")
        #print(reading_line_2)
        
        if SA2_code != reading_line_2[0]:
            SA2_code = reading_line_2[0]
            SA2_code_addition = [SA2_code]
            SA2_code_list = SA2_code_list + [SA2_code_addition]
            SA2_code_list.sort()
            reading_line_sa2 = reading_line_2
            reading_line_sa2_list = reading_line_sa2_list + [reading_line_sa2]
        
    #print(SA2_code_list)#testing need to reopen
    #print(len(SA2_code_list))#538
    #print(reading_line_sa2_list)#testing need to reopen
    
    csvfile_2_a.close()
    
    
    # to get SA2_code_list_first_5_number 
    csvfile_1_a = open(csvfile_1,"r")
    
    SA2_code_list_first_5_number =[]
    
    for h in range (len(SA2_code_list)):
        readlines = csvfile_1_a.readline()
        reading_line = readlines.split(",")
        #trying to put each column in a row as a element in list
        #print(reading_line,reading_line[4])
        #print(reading_line[2])
        # check the first 5 number
        SA2_code_line_first_5_number = SA2_code_list[h][0][0:5]
        SA2_code_list_first_5_number = SA2_code_list_first_5_number + [SA2_code_line_first_5_number]
    #print(SA2_code_list_first_5_number)
    
       
       
    
    csvfile_1_a.close()
    
    #to get the Unique_sa3 code 
    csvfile_1_a = open(csvfile_1,"r")
    
    Unique_SA3_code_list = []
    Unique_SA3_code = "SA3 code"
    for p in range (data_length_reference):
        readlines_1 = csvfile_1_a.readline()
        reading_line_1 = readlines_1.split(",")
        
        if Unique_SA3_code != reading_line_1[2]:
            Unique_SA3_code = reading_line_1[2]
            Unique_SA3_code_addition = [Unique_SA3_code]
            Unique_SA3_code_list = Unique_SA3_code_list + [Unique_SA3_code_addition]
            Unique_SA3_code_list.sort()
        
    #print(Unique_SA3_code_list)#testing need to reopen
            
    list_age_group = [0] * len(Unique_SA3_code_list)
    #print(list_age_group)
    
    
    
    
    
    
    # to list number of unique state code
    unique_S_T_code = Unique_SA3_code_list[0][0][0]
    number_of_unqiue_SA3code = len(unique_S_T_code_list) 
    length_of_STCODE =[]
    length_of_number_of_4_5_6_etc =[0]
    steps = 0
    listing_number_of_unqiue_STCODE = []
    for b in range(number_of_unqiue_SA3code):
        listing_number_of_unqiue_STCODE.append([])
    #print(listing_number_of_unqiue_STCODE)#testing need to reopen
    for w in Unique_SA3_code_list:
        if w[0][0] == unique_S_T_code:
            listing_number_of_unqiue_STCODE[steps].append(w[0][0])
        else:
            unique_S_T_code = w[0][0]
            steps = steps + 1
            listing_number_of_unqiue_STCODE[steps].append(w[0][0])
    #print(listing_number_of_unqiue_STCODE)#testing need to reopen
    #for c in range(number_of_unqiue_SA3code):
        #length_of_number_of_4_5_6_etc.append([])
    #print(length_of_number_of_4_5_6_etc)
    
    #to find the length of each individual unqiue state code
    total_length_of_listing_number_of_unqiue_STCODE = 0
    listing_total_length = [0]
    for a in range(len(unique_S_T_code_list)):
        length = len(listing_number_of_unqiue_STCODE[a])
        #print(length)
        total_length_of_listing_number_of_unqiue_STCODE = total_length_of_listing_number_of_unqiue_STCODE + length
        #print(total_length_of_listing_number_of_unqiue_STCODE)
        length_of_number_of_4_5_6_etc.append(length)
        listing_total_length.append(total_length_of_listing_number_of_unqiue_STCODE)
        #print(length)#testing need to reopen
    #print(length_of_number_of_4_5_6_etc)#testing need to reopen          
    #print(listing_total_length)#testing need to reopen
    #print(len(unique_S_T_code_list))
    #print(unique_S_T_code_list)
    #print(total_length_of_listing_number_of_unqiue_STCODE)
        
    #print(len(Unique_SA3_code_list))#77
    
    grouped_Unique_SA3_code_list = []
    for i in range(len(unique_S_T_code_list)):
        grouped_Unique_SA3_code_list.append([])
    #print(grouped_Unique_SA3_code_list)
    
    #print(unique_S_T_code_list[0])
    
    grouped_Unique_SA3_code = Unique_SA3_code_list
    for k in range(len(unique_S_T_code_list)): 
        for i in range(len(Unique_SA3_code_list)):
            if grouped_Unique_SA3_code[i][0][0] == unique_S_T_code_list[k]:
                grouped_Unique_SA3_code_list[k].append(grouped_Unique_SA3_code[i])
    #print(grouped_Unique_SA3_code_list)
    grouped_Unique_SA3_code_list = sorted(grouped_Unique_SA3_code_list, key=lambda x: x[0][0][1])        

    
    csvfile_1_a.close()
    
    
    
    #to get the population data from population
    csvfile_2_a = open(csvfile_2,"r")
    
    old_q= Unique_SA3_code_list[0]
    step= 0 #move_forward_across_the_list
    for q in Unique_SA3_code_list:# for each row loop for the number, ie)<40101>1001
        
        
        #print(q,old_q)
        #using the if, else statment and the step to keep the addition in track in filling in the corresponding space.
        #it is merely adding all number with the same first 5 SA3 number together
        # this produce a list of sum of each unique SA3
        if q != old_q:
            step = step +1
        
        for i in range(data_length_reference-1):
            if q == [reading_line_sa2_list[i][0][0:5]]:
                    list_age_group[step] = list_age_group[step] + int(reading_line_sa2_list[i][generalisation_age_group_position])#the '2' is refer to position of the age group
                    #print(list_age_group)
                    
        old_q,q = q,old_q
        #print(q,old_q)#break,#testing need to reopen
    #print(list_age_group)#testing need to reopen
    
    csvfile_2_a.close()
    
    
    # to differentiate unique SA3 code with their state code
    # to group or seperate unique SA3 code using their state code 
    sum_list = []
    sum_the_sum_list = []
    maximum_of_each_state = []
    for c in range(len(listing_total_length)-1):#3
        y = list_age_group[listing_total_length[c]:listing_total_length[c+1]]
        sum_list = sum_list + [y]
    #print(sum_list)# reopen
    
    #print(sum_list[0])
    # find the sum of sum_list, may be unnecessary  
    for t in range(len(listing_total_length)-1):  
        #print(max(sum_list[t]))
        #print(sum(sum_list[t]))#testing need to reopen
        sum_the_sum_list = sum_the_sum_list + [sum(sum_list[t])]
    #print(sum_the_sum_list)
    
    #find maximum in each state
    for o in range(len(listing_total_length)-1):
        maximum = max(sum_list[o])
        maximum_of_each_state = maximum_of_each_state + [maximum]
    
    #print(length_of_number_of_4_5_6_etc)
    #print(maximum_of_each_state)
    
    
    #find maximum index of each ST code
    max_index_list = []
    for s in range(len(listing_total_length)-1):
        max_index = sum_list[s].index(max(sum_list[s]))
        #print(max_index)
        max_index_list = max_index_list + [max_index]
    #print(max_index_list)
    #find maximum index of each ST code
    max_index_list_list = []
    for d in range(len(unique_S_T_code_list)):
        max_index_list_list=max_index_list_list+ [max_index_list[d]]
    #print(max_index_list_list)
    
    #find the location of the maximum in a list by adding them up
    total_length_of_the_maximum_unqiue_SA3code = 0
    sum_the_maximum_unqiue_SA3code =[]
    #print(Unique_SA3_code_list)
    #print(len(Unique_SA3_code_list))
    for d in range(len(unique_S_T_code_list)):#3
        length_of_sum_list = max_index_list_list[d]
        #print(length_of_sum_list)
        total_length_of_the_maximum_unqiue_SA3code = total_length_of_the_maximum_unqiue_SA3code + length_of_sum_list
        sum_the_maximum_unqiue_SA3code.append(total_length_of_the_maximum_unqiue_SA3code)
        
    #print(sum_the_maximum_unqiue_SA3code)
    
    #find the actual SA3 code of those maximum 
    sum_the_maximum_unqiue_SA3code_list = []
    #for i in range(len(unique_S_T_code_list)):
    move_forward_each_time = 0
    for r in max_index_list:
        sum_the_maximum_unqiue_SA3code_list = sum_the_maximum_unqiue_SA3code_list + grouped_Unique_SA3_code_list[move_forward_each_time][r]
        move_forward_each_time = move_forward_each_time + 1
    #print(sum_the_maximum_unqiue_SA3code_list)# show each maximum SA3 code
    
    maximum_population_sum_area = open(csvfile_2,"r")
    
    #count_for_step
    #to get each maximum SA3 code into list within list
    maximum_population_sum_area_line_list= []
    
    for d in range(len(unique_S_T_code_list)):
        maximum_population_sum_area_line_list.append([])
        
    for l in range(data_length_reference):
        if l == data_length_reference-1:
            read_maximum_population_sum_area_lines = maximum_population_sum_area.readline()
            maximum_population_sum_area_line = read_maximum_population_sum_area_lines.split(",")
        else:
            read_maximum_population_sum_area_lines = maximum_population_sum_area.readline()
            maximum_population_sum_area_line = read_maximum_population_sum_area_lines[:-1].split(",")
        #print(maximum_population_sum_area_line)
        for d in range(len(unique_S_T_code_list)):#3
            if maximum_population_sum_area_line[0][0:5] == sum_the_maximum_unqiue_SA3code_list[d]:
                maximum_population_sum_area_line_list[d] = maximum_population_sum_area_line_list[d] + [maximum_population_sum_area_line]
    
    #print(maximum_population_sum_area_line_list)
    #print(len(maximum_population_sum_area_line_list[2]))
    #print(len(unique_S_T_code_list))
    
    #listing all number across all age group for maximum SA3
    total_across_same_SA3 = []
    
    for d in range(len(unique_S_T_code_list)):
        total_across_same_SA3.append([])
   
    for d in range(len(unique_S_T_code_list)):
        #print(3)
        for y in range(len(maximum_population_sum_area_line_list[d])):  
         op = (maximum_population_sum_area_line_list[d][y][2:])
         total_across_same_SA3[d] = total_across_same_SA3[d] + op
         #print(total_across_same_SA3)
         #length_of_max_population_in_unique_SA3 = len(maximum_population_sum_area_line_list[d])
         #print(length_of_max_population_in_unique_SA3)
         #print(maximum_population_sum_area_line_list[d])
    #print(total_across_same_SA3[0])
    #print(total_across_same_SA3[1])
    #print(total_across_same_SA3[2])
    
    # to calculate the sum of each maximum SA3 group
    sum_of_total_across_same_SA3 =[]
    for d in range(len(unique_S_T_code_list)):
        sum_of_total_across_same_SA3.append([])
    
    for d in range(len(unique_S_T_code_list)):
        changing_string_into_int_list = [int(numbers) for numbers in total_across_same_SA3[d]]
        sum_of_total_across_same_SA3[d] = sum_of_total_across_same_SA3[d] + [sum(changing_string_into_int_list)]
    
    #print(sum_of_total_across_same_SA3)
        
    maximum_population_sum_area.close()    

    
    
    
    
    # calculate the sample SD
    percentage_list_of_population =[]
    for m in range(len(listing_total_length)-1):
        percentage = f"{maximum_of_each_state[m]/sum_of_total_across_same_SA3[m][0]:0.4f}"
        percentage_list_of_population = percentage_list_of_population + [float(percentage)]
        
    #print(percentage_list_of_population)# part of the answer!!!!!!       
    
    #find unique SA3 name 
    csvfile_1_a = open(csvfile_1,"r")
    

    SA3_name_list = []
    SA3_header_name = "sa3 name"
     
    selective_5_digit =[]
    selective_5_digit_list =[]
    
   
    for i in range (data_length_reference):
        readlines = csvfile_1_a.readline()
        reading_line = readlines.split(",")
        
        #reading_list = reading_list + reading_line
        #trying to put each column in a row as a element in list
        #print(reading_line,reading_line[4])
        #print(reading_line[3],reading_line[3].lower())
      
        if SA3_header_name != reading_line[3].lower(): #or SA3_header_name_lowercase != reading_line[3].lower():
            SA3_header_name = reading_line[3].lower()
            SA3_name_addation = [SA3_header_name]  #i can add more list
            SA3_name_list = SA3_name_list + SA3_name_addation
            #print(state_list)# test for sort in to alphabetic order
    #print(len(listing_total_length))   
    #print(SA3_name_list)#testing need to reopen#part of answer!!!!!!!
    #print(len(SA3_name_list))
    seperated_SA3_name_list =[]
    three_together_SA3_name_list =[]
    for v in range(len(listing_total_length)-1):
        z = SA3_name_list[listing_total_length[v]:listing_total_length[v+1]]
        seperated_SA3_name_list = seperated_SA3_name_list + [z]
    #print(SA3_name_list[0:28])
    #print(SA3_name_list[28:62])
    #print(SA3_name_list[62:77])
    for times in range(len(listing_total_length)-1):
        three_together_SA3_name_list = three_together_SA3_name_list + [seperated_SA3_name_list[times][max_index_list[times]]]#part of answer!!!!!!!
    
    #print(three_together_SA3_name_list)
    
    #print(state_list)
    #final answer, invovled 3 things,{<state_list>,<three_together_SA3_name_list>,<percentage_list_of_population>}
    final_answer_list = []
    for g in range(len(listing_total_length)-1):
        final_answer_list.append([])
        final_answer_list[g].append(state_list[g])
        final_answer_list[g].append(three_together_SA3_name_list[g])
        final_answer_list[g].append(percentage_list_of_population[g])
    final_answer_list.sort()
        
    return final_answer_list
       
    
    
    
    csvfile_1_a.close()
    
    
    
    
    
    csvfile_1_a.close()
    csvfile_2_a.close()


    

#Output 4 
def op4_testing(csvfile_2, sa2_1, sa2_2):
   
   #find the length of file 
   data_length = open(csvfile_2,"r")
   
   data_length_reference_2 = len(list(data_length))
   #print(data_length_reference_2)#testing length of data file
   
   data_length.close()
   
   #open,read and put the file into a list
   csvfile_2_2 = open(csvfile_2,"r")
   population_data_list =[]
   for i in range(data_length_reference_2):
       
       read_line = csvfile_2_2.readline()
       reading_lines = read_line[:-1].split(",")
       population_data_list = population_data_list + [reading_lines]
   
   #print(population_data_list)
   
   #summtion for x
   x_population_data_list = []
   for a in range(data_length_reference_2):
       if population_data_list[a][0] == sa2_1:
           x_population_data_list = x_population_data_list + population_data_list[a][2:]
   #print(x_population_data_list)#list
   x_population_data_list_number = []
   for k in range(len(population_data_list[a])-2):
       x_population_data_list_number = x_population_data_list_number + [int(x_population_data_list[k])]
    
   #print(x_population_data_list_number)
   
   average_x = sum(x_population_data_list_number)/len(x_population_data_list_number)
   #print(average_x)
   
   sum_x = 0
   for d in range(len(x_population_data_list_number)):
       sum_x = sum_x +((x_population_data_list_number[d] - average_x) ** 2)
   
   #print(sum_x)
   
   #summtion for y
   y_population_data_list = []
   for a in range(data_length_reference_2):
       if  population_data_list[a][0] == sa2_2:
           y_population_data_list = y_population_data_list + population_data_list[a][2:]
   #print(y_population_data_list)#list
   y_population_data_list_number = []
   for k in range(len(population_data_list[a])-2):
       y_population_data_list_number = y_population_data_list_number + [int(y_population_data_list[k])]
   
   #print(y_population_data_list_number)
   
   average_y = sum(y_population_data_list_number)/len(y_population_data_list_number)
   #print(average_y)
   
   sum_y = 0
   for d in range(len(y_population_data_list_number)):
       sum_y = sum_y +((y_population_data_list_number[d] - average_y) ** 2)
   
   #print(sum_y)
   
   #taking the 2 input of SA2 and make them into a list
   z_population_data_list = []
   for a in range(data_length_reference_2):
       if  population_data_list[a][0] == sa2_1 or population_data_list[a][0] == sa2_2:
           z_population_data_list = z_population_data_list + [population_data_list[a][2:]]
   #print(z_population_data_list)
   
   #change the data from string into integer
   z_population_data_list_number = []
   for q in range(2):
       z_population_data_list_number.append([])
       z_population_data_list_number[q] = [int(i)for i in z_population_data_list[q]] 
   
   #print(z_population_data_list_number)
   
   #summation of numerator
   sum_z = 0 
   for p in range(len(z_population_data_list_number[0])):
       sum_z = sum_z + ((z_population_data_list_number[0][p] - average_x) * (z_population_data_list_number[1][p] - average_y))
   
   #print(sum_z)
   
   #final answer
   final_answer_r = sum_z / ((sum_y * sum_x) ** 0.5) 
   final_answer_r = float(f"{final_answer_r:0.4f}")
   #print(final_answer_r)
   return final_answer_r
    
    
    
"""
debug documentation:

Issue 1 (Date 2025 April 4):
- Error Description:
    Unable add the pervious sum for each unique SA3 code into a reserve space for further handling 
- Erroneous Code Snippet:
    From: old_q= Unique_SA3_code_list[0] # line 473
    to:  old_q,q = q,old_q # line 490
    
    The whole part of code start from 471 to 494
- Test Case:
    main('SampleData_Areas.csv','SampleData_Populations.csv', 3, '401011001', '401021003')
- Reflection:
   I was unable to add values to the positions on the reserve list I wanted.
   The pattern of changing the position is moving forward after finishing adding the current unique SA3 code.
   Therefore, I coded it by changing the unique SA3 code after each round of addition. And to check only the
   previous SA3 code is not equal before addition. To ensure each sum of the SA3 code will inherent pattern from
   unique SA3 code.
   
Issue 2 (Date 2025 April 5):
- Error Description:
    Unable to identify the correct header
- Erroneous Code Snippet:
    if SA3_header_name != reading_line[3] # line 648 
- Test Case:
    main('SampleData_Areas.csv','SampleData_Populations.csv', 15, '401011001', '401021003')
- Reflection:
    As the header will not be change in this or any data as assumption,
    I have define the header using the name from the data provided. However,
    I need to consider the code as case-insensitive, I need to convert all string
    into lower case before process. Before notice, it was case-insensitive.
   
Issue 3 (Date 2025 April 8):
- Error Description:
    TypeError: '<=' not supported between instances of 'int' and 'NoneType'
- Erroneous Code Snippet:
    if age >= list_for_looping[0] and age <= list_for_looping[1]: # line 43
- Test Case:
    main('SampleData_Areas.csv','SampleData_Populations.csv', 90, '401011001', '401021003')
- Reflection:
    I realized my code can not handle the special case of [85,None].
    Therefore, I need to put some conditional restrictions to avoid having the code
    try to compare between integer and None. To fix it I have given a conditional to deal with
    the special case independently, by using if,else statement.
    
Issue 4 (Date 2025 April 8):
- Error Description:
    ValueError: 'Age 85-inf' is not in list
- Erroneous Code Snippet:
    generalisation_age_group_position = reading_age_group_line.index(age_group_look_for) # line 255
- Test Case:
    main('SampleData_Areas.csv','SampleData_Populations.csv', 85, '401011001', '401021003')
- Reflection:
     I recognise that the item(name) that I am looking for is the wrong input from Output 1.
    Although Output 1 is [85, None], the actual value from previous code has defined it in a way,
    that it is 'Age 85-inf'. To fix it, I used the if,else statement to redefine the value as [85,None],
    so I can use the age group's position to further reference.  

"""
      
    
   






 
    
  




 
    
  

            



    
