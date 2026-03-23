def main(csvfile_1, csvfile_2):
    try:
        if not csvfile_1.endswith('.csv') or not csvfile_2.endswith('.csv'):
            return 'Files not in proper CSV format, please try again'
    
        if 'Invalid data(header missing):' in cleaningdata_2(csvfile_2):
            return(cleaningdata_2(csvfile_2))
        elif 'Invalid data(header missing): No age group' in cleaningdata_2(csvfile_2):
            return('Invalid data(header missing): No age group')
        elif 'Invalid data(empty file)' in cleaningdata_2(csvfile_2):
            return('Invalid data(empty file)')
    
        if 'Invalid data(Handling missing), missing:' in cleaningdata_1(csvfile_1):
            return(cleaningdata_1(csvfile_1))
        
        if len(cleaningdata_2(csvfile_2)) <= 1 or len(cleaningdata_1(csvfile_1)) <= 1:
            return('Invalid data(empty file)')
        
        
        cleanfile_csv_1,cleanfile_csv_2 = crosscheckfile_for_missing(csvfile_1,csvfile_2)
        
        OP1 = op1(csvfile_1,csvfile_2,cleanfile_csv_1,cleanfile_csv_2)
        OP2 = op2(csvfile_1,csvfile_2,cleanfile_csv_1,cleanfile_csv_2)
        OP3 = op3(csvfile_1,csvfile_2,cleanfile_csv_1,cleanfile_csv_2)
        #print(op1_1)
        #print(op2_1)
        #print(op3_1)
        
    except FileNotFoundError:
        return "Invalid file names or non-existent files, please try again"
    
    return OP1,OP2,OP3
def cleaningdata_2(csvfile_2):
    #find the length of the file for read line reference
    data_length = open(csvfile_2,"r")
    data_length_reference = len(list(data_length))
    #print(data_length_reference)#testing length of data file #dynamic number #stanard -> 539
    data_length.close()
    #end
    
    #remove title that is not relevant
    find_vaild_title = open(csvfile_2,"r")
    find_title_line = find_vaild_title.readline() 
    title_line = find_title_line.lower()
    title_line = title_line.split(',')
    title_line[-1] = title_line[-1].strip()
    #print(title_line)#
    find_vaild_title.close()
    #end
    
    #handling Handling missing
    must_have_title = ['area_code_level2', 'area_name_level2']
    missing = []
    for needed in must_have_title: 
        if needed not in title_line:
            missing.append(needed)
    if len(missing) > 0:
        return 'Invalid data(header missing):',missing
        #return
    #end
    
    #find vaild title index
    vaild_title_index_list = []
    for title in title_line:
        if title.startswith('age'):
            vaild_title_index_list.append(title_line.index(title))
        elif 'area_code_level2' == title:
            vaild_title_index_list.append(title_line.index(title))
        elif 'area_name_level2' == title:
            vaild_title_index_list.append(title_line.index(title))
    #print(vaild_title_index_list)
    #end
    
    #what if there is not age group
    if len(vaild_title_index_list) < 3:
        return 'Invalid data(header missing): No age group'
    #end
    
    
    #case insensitive by lowercase
    csvfile_2_a = open(csvfile_2,"r")
    SampleData_Populations_P2_list_c = []
    
    for i in range (data_length_reference):
        readlines = csvfile_2_a.readline()
        reading_line = readlines.lower()
        reading_line = reading_line.split(",")
        reading_line[-1] = reading_line[-1].strip()
        #SampleData_Populations_P2_list.append(reading_line)
        for k in vaild_title_index_list:
            SampleData_Populations_P2_list_c.append(reading_line[k])
    #print(SampleData_Populations_P2_list_c)
    #end
            
    #structure the 'SampleData_Populations_P2_list_c' in nested list to seperate between row 
    temp_list = []
    SampleData_Populations_P2_list = []
    checker = 0
    for i in SampleData_Populations_P2_list_c:
        temp_list.append(i)
        checker = checker + 1
        if checker/len(vaild_title_index_list) == 1.0:
            SampleData_Populations_P2_list.append(temp_list)
            checker = 0
            temp_list = []
    #print(SampleData_Populations_P2_list)
    csvfile_2_a.close()
    #end
    
    
    #sort the 'SampleData_Populations_P2_list' in in order(small to big)
    #the title will be the last, because it's letter, reorder it and put it first
    SampleData_Populations_P2_list = sorted(SampleData_Populations_P2_list, key=lambda x:x[0])
    SampleData_Populations_P2_list.insert(0,SampleData_Populations_P2_list[-1])
    SampleData_Populations_P2_list.pop(-1)
    #print(SampleData_Populations_P2_list)
    #end
    
    #reodering the column and spread it to every row
    header_line = sorted(SampleData_Populations_P2_list[0])
    standard_header_line = header_line.copy()
    standard_header_line.insert(0,standard_header_line.pop(-1))
    standard_header_line.insert(0,standard_header_line.pop(-1))
#     print('')
#     print(standard_header_line)
#     print('')
#     print(len(SampleData_Populations_P2_list))
#     print('')
#     print(SampleData_Populations_P2_list)
    
    header = SampleData_Populations_P2_list[0]
    reorder_index = [header.index(p) for p in standard_header_line]
    
    reordered_data = [standard_header_line]
    for row in SampleData_Populations_P2_list[1:]:
        reordered_row = [row[i] for i in reorder_index]
        reordered_data.append(reordered_row)
    
    SampleData_Populations_P2_list = reordered_data
    #end
    
    
    
    #cleaning duplicated rows
    # 1.find duplicated row
    Sample_Data_Populations_P2_list = []
    duplicated_sa2_list = []
    marker = ''
    for lines in SampleData_Populations_P2_list:
        if marker == lines[0]:
            duplicated_sa2_list.append(lines[0])
        Sample_Data_Populations_P2_list.append(lines)
        marker = lines[0]
    #print(Sample_Data_Populations_P2_list)
    #print(duplicated_sa2_list)
    
    # 2.remove all rows with the duplicated sa2 code
    removing_duplicate_list = []
    for row in Sample_Data_Populations_P2_list:
        if row[0] not in duplicated_sa2_list:
            removing_duplicate_list.append(row)
                #print(row)
    Sample_Data_Populations_P2_list = removing_duplicate_list
    #print(Sample_Data_Populations_P2_list)
    #end
    
    #use it to identity number, only number '0-9' give True
    counts = 0
    error_number_list = []
    for rows in Sample_Data_Populations_P2_list:
        if counts > 0:
            for r in rows[2:]:
                if r.isdecimal() == False:
                    error_number_list.append(rows)
                    Sample_Data_Populations_P2_list.remove(rows)
                    break 
        counts = counts + 1           
                    
         
        
    #print(len(Sample_Data_Populations_P2_list))%
    #print(len(error_number_list))%
    #end
    
    #coverting popultion into integer
    count = 0
    for n in range(len(Sample_Data_Populations_P2_list)):
        if count > 0: 
            Sample_Data_Populations_P2_list[n][2:] = map(int,Sample_Data_Populations_P2_list[n][2:])
            #x = Sample_Data_Populations_P2_list[n][2:].isdecimal()
            #print(x)
        count = count + 1
    
    
    #print(len(Sample_Data_Populations_P2_list))%
    #print(Sample_Data_Populations_P2_list)%
    csvfile_2_a.close()
    #print(Sample_Data_Populations_P2_list[-1])
    #end
    
    return Sample_Data_Populations_P2_list
#cleaningdata_2('SamplePopulations_tcase7.csv')
    
def cleaningdata_1(csvfile_1):
    #find the length of the file for read line reference
    data_length_1 = open(csvfile_1,"r")
    data_length_reference_1 = len(list(data_length_1))
    #print(data_length_reference_1)#testing length of data file #dynamic number #stanard -> 539
    data_length_1.close()
    #end
    
    #set out a desired hard code title and case sensitive by lowercase  
    hard_coded_title = ['s_t code', 's_t name', 'sa2 code', 'sa2 name', 'sa3 code', 'sa3 name']
    find_vaild_title = open(csvfile_1,"r")
    finding_title_line = find_vaild_title.readline()
    title_line = finding_title_line.lower()
    title_line = title_line.split(',')
    title_line[-1] = title_line[-1].strip()
    #print(title_line)
    find_vaild_title.close()
    #end
    
    #handling Handling missing
    missing = []
    for needed in hard_coded_title:
        if needed not in title_line:
            missing.append(needed)
    if len(missing) > 0:
        return'Invalid data(header missing), missing:',missing
        #return 
    #end
    
    
    #find out the index position of vaild title
    vaild_title_index_list = []
    for title in title_line:
        if title in hard_coded_title:
            vaild_title_index_list.append(title_line.index(title))
    #print(vaild_title_index_list)
    #end
            
    #testing pull out desired column and case insensitive by lowercase         
    csvfile_1_a = open(csvfile_1,"r")
    SampleData_Areas_P2_list_c = []
    
    for i in range(data_length_reference_1):
        readlines_1_c = csvfile_1_a.readline()
        reading_line_1_c = readlines_1_c.lower()
        reading_line_1_c = reading_line_1_c.split(",")
        reading_line_1_c[-1] = reading_line_1_c[-1].strip()
        for k in vaild_title_index_list:
            SampleData_Areas_P2_list_c.append(reading_line_1_c[k])
    #print(SampleData_Areas_P2_list_c)
    #end
            
    #structure the 'SampleData_Areas_P2_list_c' in nested list to seperate between row  
    temp_list = []
    SampleData_Areas_P2_list = []
    checker = 0
    for i in SampleData_Areas_P2_list_c:
        temp_list.append(i)
        checker = checker + 1
        if checker/len(vaild_title_index_list) == 1.0:
            SampleData_Areas_P2_list.append(temp_list)
            checker = 0
            temp_list = []
    #print(SampleData_Areas_P2_list)%
    csvfile_1_a.close()
    #end

    
    #sort the 'SampleData_Populations_P2_list' in in order(small to big)
    #the title will be the last, because it's letter, reorder it and put it first
    SampleData_Areas_P2_list = sorted(SampleData_Areas_P2_list, key=lambda x:x[0])
    #print(SampleData_Areas_P2_list)
    SampleData_Areas_P2_list.insert(0,SampleData_Areas_P2_list[-1])
    SampleData_Areas_P2_list.pop(-1)
    #print(SampleData_Areas_P2_list)%
    #end
    
    #reodering the column and spread it to every row
    header_line_1 = sorted(SampleData_Areas_P2_list[0])
    standard_header_line_1 = header_line_1.copy()
    #print(standard_header_line_1)%
    
    header_1 = SampleData_Areas_P2_list[0]
    reorder_index_1 = [header_1.index(p) for p in standard_header_line_1]
    
    reordered_data_1 = [standard_header_line_1]
    for row in SampleData_Areas_P2_list[1:]:
        reordered_row_1 = [row[i] for i in reorder_index_1]
        reordered_data_1.append(reordered_row_1)
    
    SampleData_Areas_P2_list = reordered_data_1
    #print(Sample_Data_Area_P2_list)%
    #end
    
    #cleaning duplicated rows
    # 1.find duplicated row
    Sample_Data_Area_P2_list = []
    duplicated_sa2_list = []
    marker = ''
    for lines in SampleData_Areas_P2_list:
        if marker == lines[2]:
            duplicated_sa2_list.append(lines[2])
        Sample_Data_Area_P2_list.append(lines)
        marker = lines[2]
    #print(Sample_Data_Area_P2_list)
    #print(duplicated_sa2_list)
    
    # 2.remove all rows with the duplicated sa2 code
    removing_duplicate_list = []
    for row in Sample_Data_Area_P2_list:
        if row[2] not in duplicated_sa2_list:
            removing_duplicate_list.append(row)
                #print(row)
    Sample_Data_Area_P2_list = removing_duplicate_list
    #print(Sample_Data_Area_P2_list)
    #print(len(Sample_Data_Area_P2_list))
    #end
    
    # remove inconsistent relationships between sa3 code, sa2 code, st code
    # 1.remove row that the sa3 code and sa2 code, sa3 code and st code is not matching, 
    only_if_sa3_and_sa2_or_st_match_list = [Sample_Data_Area_P2_list[0]]
    for row in Sample_Data_Area_P2_list[1:]:
        sa3 = row[4]
        if sa3 == row[2][0:5] and sa3[0] == row[0]:
            only_if_sa3_and_sa2_or_st_match_list.append(row)
    #print(only_if_sa3_and_sa2_or_st_match_list)
    #print(len(only_if_sa3_and_sa2_or_st_match_list))
    Sample_Data_Area_P2_list = only_if_sa3_and_sa2_or_st_match_list
    # 2.remove row that sa2 code and st code is not matching
    # seem unnecessary, if sa3=sa2 and sa3=st, then sa2=sa3=st, deduce sa2=st
#     only_if_sa2_and_st_match = [only_if_sa3_and_sa2_or_st_match_list[0]]
#     for row in only_if_sa3_and_sa2_or_st_match_list[1:]:
#         sa2 = row[2][0]
#         if sa2 == row[0]:
#             only_if_sa2_and_st_match.append(row)
#     print(only_if_sa2_and_st_match)
#     print(len(only_if_sa2_and_st_match))
     #end 
    
    
    
    
    
    
    csvfile_1_a.close()
    return Sample_Data_Area_P2_list


#cleaningdata_1('SampleAreas_tcase2.csv')

def crosscheckfile_for_missing(csvfile_1,csvfile_2):
    clean_Populations_Data = cleaningdata_2(csvfile_2)
    clean_Areas_Data = cleaningdata_1(csvfile_1)
    #print(clean_Populations_Data)#
    #print(clean_Areas_Data)#
    
    #check if SA2code from population data in Area data, if yes, put it into a new list,
    #because remove the missing will affect the original list(clean_Populations_Data)
    filtering_population_data = [clean_Populations_Data[0]] # establish a new list 
    check_step = 0
    for row in clean_Populations_Data[1:]:
        #print(row[0])
        found = False
        for line in clean_Areas_Data[1:]:
            #print(line)
            if row[0] in line:
                found = True
                check_step = check_step + 1 # should be len(clean_Areas_Data)-1
                #print(check_step)
                break
        if found == True:
            filtering_population_data.append(row)
    #print(filtering_population_data)
    #print(len(filtering_population_data))
    
    #check if SA2code from Area data in population data, if yes, put it into a new list,
    #because remove the missing will affect the original list(clean_Areas_Data)
    filtering_area_data = [clean_Areas_Data[0]]
    check_step = 0
    for row in clean_Areas_Data[1:]:
        #print(row)
        found = False
        for line in clean_Populations_Data[1:]:
            #print(line)
            if row[2] in line:
                found = True
                check_step = check_step + 1 # should be len(clean_Areas_Data)-1
                #print(check_step)
                break
        if found == True:
            filtering_area_data.append(row)
    #print(' ' )
    #print(filtering_area_data)
    #print(filtering_population_data)
    return filtering_area_data, filtering_population_data
    
#crosscheckfile_for_missing('SampleData_Areas_P2.csv','SamplePopulations_tcase7.csv')

def op1(csvfile_1,csvfile_2,cleanfile_csv_1,cleanfile_csv_2):
    #cleanfile_csv_1,cleanfile_csv_2 = crosscheckfile_for_missing(csvfile_1,csvfile_2)
    #print(cleanfile_csv_1)
    #print(cleanfile_csv_2)
    data_length_reference = len(cleanfile_csv_2)
    
    
#     #only read and take out the heading of the data and construct a dictionary with [] as vaule
#     largest_population_dictionary = {}
#     reading_line_population = cleanfile_csv_2[0].copy()
#     print(reading_line_population)
#     reading_line_population[-1] = reading_line_population[-1].strip()
#     reading_line_population.remove('area_code_level2')
#     reading_line_population.remove('area_name_level2')
# 
#     
#     for l in range(len(reading_line_population)):
#         string_age_group = reading_line_population[l]
#         string_age_group = string_age_group.replace('age ','')
#         reading_line_population[l]= string_age_group.replace(' and over','-None')
#     
#     reading_line_population = sorted(reading_line_population)    
#     
#     print(reading_line_population)
#     
#     for l in range(len(reading_line_population)):
#         largest_population_dictionary[reading_line_population[l]] = []
#     print(largest_population_dictionary)
    
   
    
    
    #starting point of start using cleanfile_csv_2 
    #find the position of the age group
    position_dictionbary = {}
    readlines = cleanfile_csv_2[0]
    age_position_index_list = []
    
    for i in readlines:
        if i in readlines:
            age_position = readlines.index(i)
            age_position_index_list.append(age_position)
    #print(age_position_index_list)
    
    for i in range(len(readlines)):
        position_dictionbary[readlines[i]] = age_position_index_list[i]
    #print(position_dictionbary)#
    
    
        
            
     
    #find the maxiumm in age group in SA2 # get position key
    max_list = []
    
    position_key = readlines.copy()
    
    position_key.pop(0)
    position_key.pop(0)
    
    #print(position_key)#
    for i in range(len(position_key)):
        max_list.append([])
    #print(max_list)
    step = 0
    for k in position_key:
        if k != position_key[0]:
            step = step + 1
        for i in range(data_length_reference):#539
            max_list[step].append(cleanfile_csv_2[i][0:position_dictionbary[k]+1])
            #print(max_list)
#         max_list_10_to_19.append(cleanfile_csv[i][0:position_dictionbary['Age 10-19']+1])
#         max_list_20_to_29.append(cleanfile_csv[i][0:position_dictionbary['Age 20-29']+1])
#         max_list_30_to_39.append(cleanfile_csv[i][0:position_dictionbary['Age 30-39']+1])
#         max_list_40_to_49.append(cleanfile_csv[i][0:position_dictionbary['Age 40-49']+1])
#         max_list_50_to_59.append(cleanfile_csv[i][0:position_dictionbary['Age 50-59']+1])
#         max_list_60_to_69.append(cleanfile_csv[i][0:position_dictionbary['Age 60-69']+1])
#         max_list_70_to_79.append(cleanfile_csv[i][0:position_dictionbary['Age 70-79']+1])
#         max_list_80_to_more.append(cleanfile_csv[i][0:position_dictionbary['Age 80 and over']+1])
    #print(max_list)
    #print(len(max_list))
#     print(max_list_10_to_19)
#     print(max_list_20_to_29)
#     print(max_list_30_to_39)
#     print(max_list_40_to_49)
#     print(max_list_50_to_59)
#     print(max_list_60_to_69)
#     print(max_list_70_to_79)
#     print(max_list_80_to_more)
#     #max_list = [max_list_0_to_9, max_list_10_to_19, max_list_20_to_29, max_list_30_to_39, max_list_40_to_49, max_list_50_to_59, max_list_60_to_69, max_list_70_to_79, max_list_80_to_more]
#     number_list0 = []
#     number_list1 = []
#     number_list2 = []
#     number_list3 = []
#     number_list4 = []
#     number_list5 = []
#     number_list6 = []
#     number_list7 = []
#     number_list8 = []
    number_list = []
    for i in range(len(max_list)):
        number_list.append([])
    #print(number_list)    
    for l in range(len(max_list)):
        for i in range(1,len(max_list[l])):
            number_list[l].append(max_list[l][i][-1])
    #print(number_list) 
#     for i in range(1,len(max_list_10_to_19)):
#         number_list1.append(max_list_10_to_19[i][-1])
#     
#     for i in range(1,len(max_list_20_to_29)):
#         number_list2.append(max_list_20_to_29[i][-1])
#     
#     for i in range(1,len(max_list_30_to_39)):
#         number_list3.append(max_list_30_to_39[i][-1])
#     
#     for i in range(1,len(max_list_40_to_49)):
#         number_list4.append(max_list_40_to_49[i][-1])
#     
#     for i in range(1,len(max_list_50_to_59)):
#         number_list5.append(max_list_50_to_59[i][-1])
#     
#     for i in range(1,len(max_list_60_to_69)):
#         number_list6.append(max_list_60_to_69[i][-1])
#     
#     for i in range(1,len(max_list_70_to_79)):
#         number_list7.append(max_list_70_to_79[i][-1])
#     
#     for i in range(1,len(max_list_80_to_more)):
#         number_list8.append(max_list_80_to_more[i][-1])

    ans0_list = []
    for i in range(len(number_list)):
        #print(max(number_list[i]),number_list[i].index(max(number_list[i])))
        ans0 = cleanfile_csv_2[number_list[i].index(max(number_list[i]))+1][1]
        ans0_list.append(ans0)
    #print('this is part(last column) of ans:',ans0_list)#op1(3)
        
#     
#     print('')
#     print(max(number_list0),number_list0.index(max(number_list0)))#4814 at 381 position, correct
#     print(cleanfile_csv[number_list0.index(max(number_list0))+1])
#     ans0 = cleanfile_csv[number_list0.index(max(number_list0))+1][1]
#     print(ans0)
    
#     print('')
#     print(max(number_list1),number_list1.index(max(number_list1)))#4812 at 381 position, correct
#     print(cleanfile_csv[number_list1.index(max(number_list1))+1])
#     ans1 = cleanfile_csv[number_list1.index(max(number_list1))+1][1]
#     print(ans1.lower())
#     
#     print('')
#     print(max(number_list2),number_list2.index(max(number_list2)))#8104 at 1 position, correct
#     print(cleanfile_csv[number_list2.index(max(number_list2))+1])
#     ans2 = cleanfile_csv[number_list2.index(max(number_list2))+1][1]
#     print(ans2.lower())
#     
#     print('')
#     print(max(number_list3),number_list3.index(max(number_list3)))#5194 at 36 position, correct
#     print(cleanfile_csv[number_list3.index(max(number_list3))+1])
#     ans3 = cleanfile_csv[number_list3.index(max(number_list3))+1][1]
#     print(ans3.lower())
#     
#     print('')
#     print(max(number_list4),number_list4.index(max(number_list4)))#4118 at 381 position, correct
#     print(cleanfile_csv[number_list4.index(max(number_list4))+1])
#     ans4 = cleanfile_csv[number_list4.index(max(number_list4))+1][1]
#     print(ans4.lower())
#     
#     print('')
#     print(max(number_list5),number_list5.index(max(number_list5)))#3955 at 286 position, correct
#     print(cleanfile_csv[number_list5.index(max(number_list5))+1])
#     ans5 = cleanfile_csv[number_list5.index(max(number_list5))+1][1]
#     print(ans5.lower())
#     
#     print('')
#     print(max(number_list6),number_list6.index(max(number_list6)))#3096 at 59 position, correct
#     print(cleanfile_csv[number_list6.index(max(number_list6))+1])
#     ans6 = cleanfile_csv[number_list6.index(max(number_list6))+1][1]
#     print(ans6.lower())
#     
#     print('')
#     print(max(number_list7),number_list7.index(max(number_list7)))#3664 at 151 position, correct
#     print(cleanfile_csv[number_list7.index(max(number_list7))+1])
#     ans7 = cleanfile_csv[number_list7.index(max(number_list7))+1][1]
#     print(ans7.lower())
#     
#     print('')
#     print(max(number_list8),number_list8.index(max(number_list8)))#1933 at 151 position, correct
#     print(cleanfile_csv[number_list8.index(max(number_list8))+1])
#     ans8 = cleanfile_csv[number_list8.index(max(number_list8))+1][1]
#     print(ans8.lower())
    
#     ans0 = cleanfile_csv[number_list0.index(max(number_list0))+1][1].lower()
#     ans1 = cleanfile_csv[number_list1.index(max(number_list1))+1][1].lower()
#     ans2 = cleanfile_csv[number_list2.index(max(number_list2))+1][1].lower()
#     ans3 = cleanfile_csv[number_list3.index(max(number_list3))+1][1].lower()
#     ans4 = cleanfile_csv[number_list4.index(max(number_list4))+1][1].lower()
#     ans5 = cleanfile_csv[number_list5.index(max(number_list5))+1][1].lower()
#     ans6 = cleanfile_csv[number_list6.index(max(number_list6))+1][1].lower()
#     ans7 = cleanfile_csv[number_list7.index(max(number_list7))+1][1].lower()
#     ans8 = cleanfile_csv[number_list8.index(max(number_list8))+1][1].lower()

    
    
    #find the maximum in age group in SA3 code
    cleanfile_csv_0 = cleanfile_csv_2.copy()
    sample = ''
    unique_sa3_code = []
    cleanfile_csv_0.pop(0)
    #print(cleanfile_csv_0)
    #print(cleanfile_csv_2)
    for i in cleanfile_csv_0:
        if i[0][0:5] != sample:
            sample = i[0][0:5]
            unique_sa3_code.append(i[0][0:5])
    #print(unique_sa3_code)#
   
#     unique_sa3_code_population = []
#     for i in range(len(unique_sa3_code)):#77
#         unique_sa3_code_population.append([])
#     
#     unique_sa3_code_population_summing = []
#     for i in range(len(unique_sa3_code)):#77
#         unique_sa3_code_population_summing.append([])
#     
    
   
    check = ''
    step = 0
    steps = 0
    max_sa3_code_list = []
    for k in position_key: #(position_dictionbary[k])#may want to write a error report to explain it, if need one
        unique_sa3_code_population = []
        for i in range(len(unique_sa3_code)):#77
            unique_sa3_code_population.append([])
    
        unique_sa3_code_population_summing = []
        for i in range(len(unique_sa3_code)):#77
            unique_sa3_code_population_summing.append([])
        
        #print(position_dictionbary[k])#
        #if k != position_key[0]:
            #steps = steps + 1
             
        for l in range(len(unique_sa3_code)):
            for i in cleanfile_csv_0:
                if i[0][0:5] == unique_sa3_code[l]:
                    unique_sa3_code_population[l].append(i[position_dictionbary[k]])#change the number '2'
                    unique_sa3_code_population_summing[l].append(sum(unique_sa3_code_population[l]))
                
        #print(unique_sa3_code_population)#
        #print(unique_sa3_code_population_summing)#
    
        unique_sa3_code_population_sum = []
        for i in unique_sa3_code_population_summing:
            unique_sa3_code_population_sum.append(i[-1])
        #print(unique_sa3_code_population_sum)#
        #print(unique_sa3_code_population_sum.index(max(unique_sa3_code_population_sum)))#
        temp = unique_sa3_code[unique_sa3_code_population_sum.index(max(unique_sa3_code_population_sum))]
        #print(temp)#
        max_sa3_code_list.append(temp)
    #print(max_sa3_code_list)#use the SA3 code to find SA3 name
    #print(cleanfile_csv_1)
    
    #take the SA3 name out from the Area data,
    #using the 'max_sa3_code_list' as reference,
    #because these are Max population, using SA3 code to represent   
    step_s = 0
    max_sa3_name_list = []
    for times in range(len(cleanfile_csv_1)): 
        for row in cleanfile_csv_1[1:]:
            if step_s >= len(max_sa3_code_list):
                break
            if max_sa3_code_list[step_s] in row:
                #print(row)#
                max_sa3_name_list.append(row[-1])
                #print(step_s)
                step_s = step_s + 1
    #print('this is part(middle column) of ans:',max_sa3_name_list)#op1(2)
                
    #find the maximum in age group in State code
    cleanfile_csv_01 = cleanfile_csv_2.copy()
    sample = ''
    unique_ST_code = []
    cleanfile_csv_01.pop(0)
    #print(cleanfile_csv_01)
    #print(cleanfile_csv_2)
    for i in cleanfile_csv_01:
        if i[0][0] != sample:
            sample = i[0][0]
            unique_ST_code.append(i[0][0])
    #print(unique_ST_code)#
    max_ST_code_list = []
    for k in position_key:
        unique_ST_code_population = []
        for i in range(len(unique_ST_code)):
            unique_ST_code_population.append([])
        
        unique_ST_code_population_summing = []
        for i in range(len(unique_ST_code)):
            unique_ST_code_population_summing.append([])
        
        for l in range(len(unique_ST_code)):
            for i in cleanfile_csv_01:
                if i[0][0] == unique_ST_code[l]:
                    unique_ST_code_population[l].append(i[position_dictionbary[k]])
                    #print(unique_ST_code_population)
                    unique_ST_code_population_summing[l].append(sum(unique_ST_code_population[l]))
    
        #print(unique_ST_code_population)#
        #print(unique_ST_code_population_summing)#
        
        unique_ST_code_population_sum = []
        for i in unique_ST_code_population_summing:
            unique_ST_code_population_sum.append(i[-1])
            
        temper = unique_ST_code[unique_ST_code_population_sum.index(max(unique_ST_code_population_sum))]
        #print(temper)#
        max_ST_code_list.append(temper)
    #print(max_ST_code_list)#use the ST code to find the ST name
    
    #take the ST name out from the Area data,
    #using the 'max_ST_code_list' as reference,
    #because these are Max population, using ST code to represent
    steps_s = 0 
    max_ST_name_list = []
    for times in range(len(cleanfile_csv_1)):
        for row in cleanfile_csv_1[1:]:
            if steps_s >= len(max_ST_code_list):
                break
            if max_ST_code_list[steps_s] in row:
                #print(row)#
                max_ST_name_list.append(row[1])
                #print(step_s)#
                steps_s = steps_s + 1
    #print('this is part(first column) of ans:',max_ST_name_list)
    
    #formating answer, format is [max_ST_name_list,max_sa3_name_list,ans0_list]
    op1_formating_list = []    
    for i in range(len(ans0_list)):
        format1 = [max_ST_name_list[i],max_sa3_name_list[i],ans0_list[i]]
        op1_formating_list.append(format1)
    #print(op1_formating_list)
    #only read and take out the heading of the data and construct a dictionary with [] as vaule
    largest_population_dictionary = {}
    reading_line_population = cleanfile_csv_2[0].copy()
    #print(reading_line_population)
    reading_line_population[-1] = reading_line_population[-1].strip()
    reading_line_population.remove('area_code_level2')
    reading_line_population.remove('area_name_level2')

    
    for l in range(len(reading_line_population)):
        string_age_group = reading_line_population[l]
        string_age_group = string_age_group.replace('age ','')
        reading_line_population[l]= string_age_group.replace(' and over','-None')
    
    reading_line_population = sorted(reading_line_population)    
    
    #print(reading_line_population)
    
    for l in range(len(reading_line_population)):
        largest_population_dictionary[reading_line_population[l]] = op1_formating_list[l]
    #print(largest_population_dictionary)
        
#     if len(max_ST_name_list) == len(max_sa3_name_list) and len(max_sa3_name_list) == len(ans0_list) and len(ans0_list) == len(reading_line_population):
#         print(True, len(max_ST_name_list))
    
    return largest_population_dictionary

def op2(csvfile_1,csvfile_2,cleanfile_csv_1,cleanfile_csv_2):
    #cleanfile_csv_1,cleanfile_csv_2 = crosscheckfile_for_missing(csvfile_1,csvfile_2)
    #print(cleanfile_csv_1)
    #print(cleanfile_csv_2)
    data_length_reference = len(cleanfile_csv_2)
    
    #find all unqiue SA3 code
    cleanfile_csv_0 = cleanfile_csv_2.copy()
    sample = ''
    unique_sa3_code = []
    cleanfile_csv_0.pop(0)
    #print(cleanfile_csv_0,id(cleanfile_csv_0))
    #print(cleanfile_csv_2,id(cleanfile_csv_2))
    for i in cleanfile_csv_0:
        if i[0][0:5] != sample:
            sample = i[0][0:5]
            unique_sa3_code.append(i[0][0:5])
    #print(unique_sa3_code)#
    
    #find all unqiue SA2 code
    cleanfile_csv_find_sa2 = cleanfile_csv_2.copy()
    sample = ''
    unique_sa2_code = []
    cleanfile_csv_find_sa2.pop(0)
    #print(cleanfile_csv_find_sa2,id(cleanfile_csv_find_sa2))
    #print(cleanfile_csv_2,id(cleanfile_csv_2))
    for i in cleanfile_csv_find_sa2:
        if i[0] != sample:
            sample = i[0]
            unique_sa2_code.append(i[0])
    #print(unique_sa2_code)#
    #print(len(unique_sa2_code))#
    
    #group all the population with the same unique SA2 code together
    step = 0
    unique_sa2_code_population = []
    for row in cleanfile_csv_2[1:]:
        #print(row)
        if row[0] == unique_sa2_code[step]:
            #print(step)
            #print(row[2:])
            sum_num = 0 
            for num in row[2:]:
                sum_num = sum_num + num
            unique_sa2_code_population.append(sum_num)
            step = step + 1
            
    #print(unique_sa2_code_population)

    #put the SA2 population data with the same SA3 code together
    unique_sa3_code_population = []
    for i in range(len(unique_sa3_code)):#77
            unique_sa3_code_population.append([])
    #print(unique_sa3_code_population)
    
    steps = 0 
    for l in range(len(unique_sa2_code)):
        while steps < len(unique_sa3_code) and unique_sa2_code[l][0:5] != unique_sa3_code[steps]:
            steps = steps + 1
        
        if steps < len(unique_sa3_code):
            unique_sa3_code_population[steps].append(unique_sa2_code_population[l])
        
    #print(steps)
    #print(unique_sa3_code_population)#
    
    #put the SA2 code with the same SA3 code together
    unique_sa3_code_grouping_sa2 = []
    for i in range(len(unique_sa3_code)):#77
            unique_sa3_code_grouping_sa2.append([])
    #print(unique_sa3_code_grouping_sa2)
    
    steps = 0 
    for l in range(len(unique_sa2_code)):
        while steps < len(unique_sa3_code) and unique_sa2_code[l][0:5] != unique_sa3_code[steps]:
            steps = steps + 1
        
        if steps < len(unique_sa3_code):
            unique_sa3_code_grouping_sa2[steps].append(unique_sa2_code[l])
    
    #print(unique_sa3_code_grouping_sa2)#

    
    #sum the population of each SA3 code
    sum_of_unique_sa3_code_population = []
    for row in unique_sa3_code_population:
        sum_s = 0 
        for num in row:
            sum_s = sum_s + num
        sum_of_unique_sa3_code_population.append(sum_s)
    #print(sum_of_unique_sa3_code_population)#
    #print(len(sum_of_unique_sa3_code_population))#
    
    #find SA3 code with population >= 150000(15萬)
    SA3_code_index_population_greater_than_150k = []
    for i in sum_of_unique_sa3_code_population:
        if i >= 150000:
            index_num = sum_of_unique_sa3_code_population.index(i)
            SA3_code_index_population_greater_than_150k.append(index_num)
    #print(SA3_code_index_population_greater_than_150k)#
    
#     print('the sa3 group',unique_sa3_code_grouping_sa2[15])
#     print('corresponding population',unique_sa3_code_population[15])
#     print('max',max(unique_sa3_code_population[15]))
#     p = unique_sa3_code_population[15].index(max(unique_sa3_code_population[15]))
#     print(p)
#     print(unique_sa3_code_grouping_sa2[15][p])

   
    # try to find the maximum of SA2 for each SA3, while SA3 >= 150k
    maximum_sa2_in_sa3 = []
    for i in range(len(SA3_code_index_population_greater_than_150k)):
            maximum_sa2_in_sa3.append([])
    #print(maximum_sa2_in_sa3)
    
    clean_file_csv = cleanfile_csv_2.copy()
#     print(id(clean_file_csv))
#     print(id(cleanfile_csv_2))
    #print(clean_file_csv)
    stepps = 0 
    for index in SA3_code_index_population_greater_than_150k:
        SA2_population_list = unique_sa3_code_population[index]
        #print(SA2_population_list)
        sa2_list = unique_sa3_code_grouping_sa2[index]
        #print(sa2_list)
        max_sa2_population = max(SA2_population_list)
        #print(max_population)
        
        #find out all sa2 code that have the population same as the maximum
        maxi_sa2_list = []
        for i in range(len(SA2_population_list)):
            if SA2_population_list[i] == max_sa2_population:
                maxi_sa2_list.append(sa2_list[i])

        #find the smallest sa2 code
        smallest_sa2 = maxi_sa2_list[0]
        for sa2 in maxi_sa2_list:
            if smallest_sa2 > sa2:
                selected_sa2 = sa2

        #print(smallest_sa2)
        maximum_sa2_in_sa3[stepps].append(smallest_sa2)
        maximum_sa2_in_sa3[stepps].append(max_sa2_population)
        
        for row in clean_file_csv[1:]:
            if row[0] == smallest_sa2:
                if len(row[2:]) > 1:
                    #print(row[2:])#
                    avg = sum(row[2:])/len(row[2:])
                    #print(avg)#
                
                    sum_result = 0 
                    for num in row[2:]:
                        sum_1 = (num - avg) ** 2
                        sum_result = sum_result + sum_1
                    #print(sum_result)#
                
                    Variance =(1/(len(row[2:])-1))*(sum_result)
                    #print(Variance)#
                    SD = Variance ** 0.5
                    #print(SD)#
                    SD = float(f"{SD:0.4f}")
                    #print(SD)#
                else:
                    SD = 0
                maximum_sa2_in_sa3[stepps].append(SD)
                break 
        stepps = stepps + 1
        #print(max_sa2_in_sa3)
        #print(c_max)
    #print(maximum_sa2_in_sa3)#
    
    # find unqiue ST code and make dictionary to represent
    cleanfile_csv_01 = cleanfile_csv_2.copy()
    sample = ''
    unique_ST_code = []
    cleanfile_csv_01.pop(0)
    #print(cleanfile_csv_01)
    #print(cleanfile_csv_2)
    for i in cleanfile_csv_01:
        if i[0][0] != sample:
            sample = i[0][0]
            unique_ST_code.append(i[0][0])
    #print(unique_ST_code)#
    
    #make mutiple independent inner dictionary within a dictionary
    max_dictionary = {} 
    for l in range(len(unique_ST_code)):
        inner_dictionary = {}
        #print(id(inner_dictionary))
        max_dictionary[unique_ST_code[l]] = inner_dictionary
    #print(max_dictionary)
    
    #put the data in the dictionary with the concept of
    #mutiple layer of inner dictionary can be put into a dictionary at once   
    for i in maximum_sa2_in_sa3:
       max_dictionary[i[0][0]][i[0][0:5]] = i  
                    
                
                    
    
    #print(max_dictionary)
    return max_dictionary

def op3(csvfile_1,csvfile_2,cleanfile_csv_1,cleanfile_csv_2):
    #cleanfile_csv_1,cleanfile_csv_2 = crosscheckfile_for_missing(csvfile_1,csvfile_2)
    #print(cleanfile_csv_1)
    #print(cleanfile_csv_2)
    
    #put all sa3 and sa2 code in a dictionary
    sa3_sa2_dictionary = {}
    marker = 0
    for sa3code in cleanfile_csv_2[1:]:
        #print(sa3code)
        if marker != sa3code[0][0:5]:
            sa3_sa2_dictionary.setdefault(sa3code[0][0:5],[])
            sa3_sa2_dictionary[sa3code[0][0:5]].append(sa3code)
            marker = sa3code[0][0:5]
        elif marker == sa3code[0][0:5]:
            sa3_sa2_dictionary[sa3code[0][0:5]].append(sa3code)
    
    #print(sa3_sa2_dictionary)
    #find all sa3 with 15 or more sa2 code and put them in dictionary
    clean_data_csv_2 = cleanfile_csv_2.copy()
    #print(id(cleanfile_csv_2))
    #print(id(clean_data_csv_2))
    sa3_sa2_length_is_15_or_more_dictionary = {}
    for k in sa3_sa2_dictionary:
        if len(sa3_sa2_dictionary[k]) >= 15:
            sa3_sa2_length_is_15_or_more_dictionary[k] = sa3_sa2_dictionary[k]
    #print(sa3_sa2_length_is_15_or_more_dictionary)
    
    #nested list making
    sa3__nested_sa2_list = []
    for key in sa3_sa2_length_is_15_or_more_dictionary:
        sa3__nested_sa2_list.append([])
        #print(key)
    
    #print(sa3__nested_sa2_list)


    #make a nested list that have all the information satisfy the condition of sa3 with 15 or more sa2 code
    step = 0
    mark_list = []
    for sa3 in sa3_sa2_length_is_15_or_more_dictionary.keys():
        mark_list.append(sa3)
    marker = mark_list[0]
    #print(marker)
    for key in sa3_sa2_length_is_15_or_more_dictionary:
        #print(key)
        for value in sa3_sa2_length_is_15_or_more_dictionary[key]: 
            if marker != key:
                step = step + 1
                marker = key 
            #print(value)
            sa3__nested_sa2_list[step].append(value)
    #print(sa3__nested_sa2_list)
    
    # find all combination of sa2 code and process from there
    sa2_sa2_cosine_similarity_dictionary = {}
    steps = 0 
    for nestlist in sa3__nested_sa2_list:
        #print(nestlist)
        for i in range(len(nestlist)):
            for j in range(i+1,len(nestlist)):
                list1 = nestlist[i]
                list2 = nestlist[j]
                #print(list1,list2)#
                
                #calculate cosine similarity part
                #calculate dot product
                dot_product = 0 
                for x, y in zip(list1[2:], list2[2:]):
                    dot_product = dot_product + x * y
                #print(dot_product)

                #calculate the two magnitude  
                sum1 = 0 
                for p in list1[2:]:
                    sum1 = sum1 + p * p 
                magnitudeA = sum1 ** 0.5
                #print(magnitudeA)

                sum2 = 0
                #print(list2[2:])
                for q in list2[2:]:
                    sum2 = sum2 + q * q 
                magnitudeB = sum2 ** 0.5
                #print(magnitudeB)

                #calculate cosine similarity
                if magnitudeA != 0 and magnitudeB != 0:
                    cosine_similarity = dot_product / (magnitudeA * magnitudeB)
                    #print(cosine_similarity)
                else:
                    cosine_similarity = 0
                #print(cosine_similarity)#
                sa2_sa2_cosine_similarity_dictionary[list1[0],list2[0]] = cosine_similarity 

    #print(sa2_sa2_cosine_similarity_dictionary)
    #print(sa2_sa2_cosine_similarity_dictionary.values())
    # make nested list base on number of unqiue ST code
    # put the cosine_similarity in group in term of SA3
    sa2_sa2_cosine_similarity_list = []
    sample_num = ''
    step_s = 0
    for i in sa2_sa2_cosine_similarity_dictionary:
        if i[0][0:5] != sample_num:
            sa2_sa2_cosine_similarity_list.append([])
            sample_num = i[0][0:5]
            if len(sa2_sa2_cosine_similarity_list) >= 2:
                step_s = step_s + 1
        #print([i[0][0:5],i,sa2_sa2_cosine_similarity_dictionary[i]])
        element = [i[0][0:5],i,sa2_sa2_cosine_similarity_dictionary[i]]
        sa2_sa2_cosine_similarity_list[step_s].append(element)  


    #print(sa2_sa2_cosine_similarity_list)
    #print(len(sa2_sa2_cosine_similarity_list))
    
    #find the maximum of cos similarity 
    max_cos_similarity_list = [] 
    for i in sa2_sa2_cosine_similarity_list:
        #print(i[1],i[1][2],'start')
        tempmax = sorted(i, key=lambda x:x[2], reverse=True)
        #print(tempmax[0],'max')
        max_cos_similarity_list.append(tempmax[0])
    #print(max_cos_similarity_list)
    
    # name?
    clean_file_csv_1 = cleanfile_csv_1.copy()
#     print(id(cleanfile_csv_1))
#     print(id(clean_file_csv_1))
    name_dictionary = {}
    for ele in max_cos_similarity_list: 
        #print(ele)
        for i in clean_file_csv_1[1:]:
            if ele[0] in i:
                sa3_name = i
                #print(sa3_name[-1])#
                break # one is enough
        for j in clean_file_csv_1[1:]:
            if ele[1][0] in j:
                sa2_name1 = j
                #print(sa2_name1[3])#
                break # one is enough
        for k in clean_file_csv_1[1:]:
            if ele[1][1] in k:
                sa2_name2 = k
                #print(sa2_name2[3])#
                break # one is enough
        if sa2_name1[3] > sa2_name2[3]:
            sa2_name1[3],sa2_name2[3] = sa2_name2[3],sa2_name1[3]
        
        cos_sim = float(f"{ele[2]:.4f}")
        name_dictionary[sa3_name[-1]] = [sa2_name1[3],sa2_name2[3],cos_sim]
    #print(name_dictionary)
    return name_dictionary    
        
    



    

main('SampleData_Areas_P2.csv','SamplePopulations_tcase0.csv')

    

