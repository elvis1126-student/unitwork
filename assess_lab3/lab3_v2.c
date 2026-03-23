# include <stdio.h>
# include <stdlib.h>
# include <string.h>
#include <stdbool.h>
#include <limits.h>
// using least recently used algorithm to move page out 

// student name: Chi Hin Elvis Suen
// student number: 24991966
// this is submission for lab3



# define TEST "sample.txt"
# define OUT "sample_out.txt"
struct accounting_data{
    /* data */
    // note, can not set inital value in structure, set in declaring
    int cputime;
    int counting_quantum;
    bool finished;
    int total_process_time;
};

struct status_data{
    /* data */
    int process_name_to_id;
    int *memory_frame; // store which frame a page is located in RAM, range of 0-15
    
    int next_used_pageNo;
    char *name; // use malloc()
    int finish_time;
    int IO_count;
    int *IO_request_time; // use malloc()
    int *IO_run_time; // use malloc()
    int IO_key;
    int length;
   
};

struct main_memory{
    int process_id;
    int page_number; // accessed page number, which belongs to the process of <process_id>
    int last_accessed_time; //time 
};

// define the struct as type - tracking_data/ status_data
typedef struct accounting_data tracking_data;
typedef struct status_data status_datas;
typedef struct main_memory memories;

// I am skeptical about no making that static, although they should be allocate memory space at heap
/* define a pointer for each struture, at the start point to NULL first, 
because we don't know where it should point to at this moment, we have not allocate memory space using malloc(), 
so set these pointer to null first to make it point as something that allow us to have controll */

static status_datas *status = NULL; // malloc ()
static tracking_data *tracking = NULL; //malloc ()
static memories memory_data[16] = {0}; 

int print_check(){
    printf("table:\n");
    for(int l = 0; l < status[0].length; l = l + 1){
        printf("process %d:%d,%d,%d,%d\n",l,status[l].memory_frame[0],status[l].memory_frame[1],status[l].memory_frame[2],status[l].memory_frame[3]); 
    }
    printf("-------\n");
                    
    printf("RAM:\n");
    for(int l = 0; l < 16; l = l + 1){
        printf("Frame %d: %d;%d;%d\n",l,memory_data[l].process_id,memory_data[l].page_number,memory_data[l].last_accessed_time);
    }
    printf("-------\n");
    return 0;
}

bool linear_search(int target, int array[], int length){ 
    if(length == 0){
        return false;
    }
    for(int i = 0; i < length ; i = i + 1){
        if(target == array[i]){
            return true;
        }
    }
    return false;
}

int local_remove_by_least_access_process(int process_location_x){
    
    //find the process with least time and having a same process id between remove and import page
    int minimum_time = INT_MAX;
    int swap_out_frame_location;

    
    for(int i = 0; i < 16; i = i + 1){
        if(memory_data[i].last_accessed_time < minimum_time && status[process_location_x].process_name_to_id == memory_data[i].process_id){
            
            // update the minimum value
            minimum_time = memory_data[i].last_accessed_time;
            swap_out_frame_location = i; // i is the frame
            
        }
    }

    
    //record and mark as not in ram
    status[memory_data[swap_out_frame_location].process_id].memory_frame[memory_data[swap_out_frame_location].page_number] = 99;

    //check record of mark as not in ram
    /*
            printf("--------\n");
            printf("removed processNo:\n");
            
            printf("processNO:%d\n",memory_data[swap_out_frame_location].process_id);
        
            printf("--------\n");
    */
    

    //remove and free space in the ram; re-initalisation
    memory_data[swap_out_frame_location].process_id = 0;
    memory_data[swap_out_frame_location].page_number = 0;
    memory_data[swap_out_frame_location].last_accessed_time = 0;

    /*
    printf("removed check\n");
    print_check();
    */

    return swap_out_frame_location;
}

int global_remove_by_least_access_process(int process_location_x){
    
   //find the process with least time 
    int minimum_time = INT_MAX;
    int swap_out_frame_location;

    
    for(int i = 0; i < 16; i = i + 1){
        if(memory_data[i].last_accessed_time < minimum_time){
            
            // update the minimum value
            minimum_time = memory_data[i].last_accessed_time;
            swap_out_frame_location = i; // i is the frame
            
        }
    }
    
    //record and mark as not in ram
    status[memory_data[swap_out_frame_location].process_id].memory_frame[memory_data[swap_out_frame_location].page_number] = 99;


    //check record of mark as not in ram
    /*
    printf("--------\n");
    printf("removed processNo:\n");
            
    printf("processNO:%d\n",memory_data[swap_out_frame_location].process_id);
        
    printf("--------\n");
    */

    //remove and free space in the ram; re-initalisation
    memory_data[swap_out_frame_location].process_id = 0;
    memory_data[swap_out_frame_location].page_number = 0;
    memory_data[swap_out_frame_location].last_accessed_time = 0;

    /*
    printf("removed check\n");
    print_check();
    */
    return swap_out_frame_location; 
}

int processes(){
    
    //struct status_data status[10] = {0};
    //struct accounting_data tracking[10] = {0};

    int counting_quantum = 0;
    // set the value at here
    
    int total_time = 0;
    // need atoi() to make number in ASCII to int, (maybe not)
    int number_of_finished_process = 0;
    int initaled_number_of_processes_to_memory_frame = 0;
    int next_available_import_frameNo = 0;
    bool non_linear_memory_count_flag = false; 
    bool run_flag;
    bool have_same_process_in_ram;
    bool same_page_already_in_ram_flag;
    // If a process is scheduled to run, you can just add 10 to cpuTime
    // should be just repeat in following for 10 process, and change the position
    //printf("start cputime = %d\n", tracking[9].cputime);
    while(number_of_finished_process < status[0].length){ // change the number for the cputime

        // if make an I/O request add n to cpuTime and the process is blocked
        
        for(int x = 0; x < status[0].length; x = x + 1){

            // printf("x=%d, before cputime=%d, counting_quantum=%d\n",x, tracking[x].cputime, tracking[x].counting_quantum);


            if(tracking[x].cputime > status[x].finish_time && tracking[x].finished == true){ 
                
                continue;
            }
             
             //if(binary_search(tracking[x].counting_quantum, int array[], sizeof )), binary_search(int target, int array[], int length)
            tracking[x].counting_quantum = tracking[x].counting_quantum + 1;
            
            // load page into memory, initalisation
            /*
            if(initaled_number_of_processes_to_memory_frame < status[0].length){
                
                //ram information
                memory_data[next_available_import_frameNo].process_id = status[x].process_name_to_id;
                memory_data[next_available_import_frameNo].last_accessed_time = total_time;

                //record and update informaiton
                status[x].memory_frame[status[x].next_used_pageNo] = next_available_import_frameNo;
                next_available_import_frameNo = next_available_import_frameNo + 1;
                status[x].next_used_pageNo = status[x].next_used_pageNo + 1;

                printf("initialisation\n");
                print_check();
                

            }
            */
           /*
           if(total_time == 705){
                    printf("in");
            }
            */

            if(linear_search(tracking[x].counting_quantum, status[x].IO_request_time, status[x].IO_count)){
                // I/O interruption handle
                for(int i = 0; i < status[x].IO_run_time[status[x].IO_key]; i = i + 1){ // change the number 5 into dynamic number from data 
                    if(tracking[x].cputime < status[x].finish_time){
                        tracking[x].cputime = tracking[x].cputime + 1;
                        total_time = total_time + 1; 
                    
                    }
                }
                // PageNo cycle, possible no. is 0,1,2,3, back to 0 if not in range[0,1,2,3] 
                if(status[x].next_used_pageNo > 3){ 
                    
                    status[x].next_used_pageNo = 0;
                }

                /*
                if(status[x].process_name_to_id == 7){
                    printf("in");
                }
                */

                // I/O request page import
                if(status[x].next_used_pageNo < 4 && next_available_import_frameNo < 16 && non_linear_memory_count_flag == false && tracking[x].cputime < status[x].finish_time){
                    //ram have space
                    //ram organisation
                    memory_data[next_available_import_frameNo].process_id = status[x].process_name_to_id;
                    memory_data[next_available_import_frameNo].page_number = status[x].next_used_pageNo;
                    memory_data[next_available_import_frameNo].last_accessed_time = total_time; 
                    //record
                    status[x].memory_frame[status[x].next_used_pageNo] = next_available_import_frameNo;
                    next_available_import_frameNo = next_available_import_frameNo + 1;
                    status[x].next_used_pageNo = status[x].next_used_pageNo + 1;
                    
                    //check
                    //printf("-page import check-\n");
                    //print_check();
                    

                }else if(status[x].next_used_pageNo < 4 && tracking[x].cputime < status[x].finish_time){ 
                    //full ram
                    non_linear_memory_count_flag = true;

                    
                    // find the least used page of same process
                    have_same_process_in_ram = false; 
                    for(int l = 0; l < 16; l = l +1){
                        if(status[x].process_name_to_id == memory_data[l].process_id){
                            have_same_process_in_ram = true;
                            break; 
                        }
                    }
                    
                    //if found same process id and same next_used_pageNo in ram do no action
                    same_page_already_in_ram_flag = false;
                    
                    for(int l = 0; l < 16; l = l +1){
                        if(status[x].next_used_pageNo == memory_data[l].page_number && status[x].process_name_to_id == memory_data[l].process_id){
                            same_page_already_in_ram_flag = true;
                            status[x].next_used_pageNo = status[x].next_used_pageNo + 1;
                            break;
                        }
                    }
                    
                    
                    if(same_page_already_in_ram_flag == false){
                        if(have_same_process_in_ram == true){
                            next_available_import_frameNo = local_remove_by_least_access_process(x);
                        }else{
                            next_available_import_frameNo = global_remove_by_least_access_process(x);
                        }
                    

                        //ram organisation
                        memory_data[next_available_import_frameNo].process_id = status[x].process_name_to_id;
                        memory_data[next_available_import_frameNo].page_number = status[x].next_used_pageNo;
                        memory_data[next_available_import_frameNo].last_accessed_time = total_time; 
                    
                        //record and mark as in the ram
                        status[x].memory_frame[status[x].next_used_pageNo] = next_available_import_frameNo;
                        status[x].next_used_pageNo = status[x].next_used_pageNo + 1;
                        
                        //check
                        //printf("-non liear check-\n");
                        //print_check();
                    }
                }
                status[x].IO_key = status[x].IO_key + 1;
                
            }else{
                // normal running
                for(int i = 0; i < 10; i = i + 1){
                    if(tracking[x].cputime < status[x].finish_time){
                        tracking[x].cputime = tracking[x].cputime + 1;
                        total_time = total_time + 1; 
               
                    }
                }
                
            }
            //testing line
            //printf("name: %s, x=%d, after cputime=%d, counting_quantum=%d, total_process_time=%d\n",status[x].name, x, tracking[x].cputime, tracking[x].counting_quantum, total_time);
            
            /* if (tracking[9].counting_quantum == 1 && x == 9){
               printf("-----------------\n");
            }*/
            if(tracking[x].cputime >= status[x].finish_time && tracking[x].finished == false){ // change the number for the cputime
                tracking[x].total_process_time = total_time;
                tracking[x].finished = true;
                number_of_finished_process = number_of_finished_process + 1;
                
                // printf("name : %s, total time:%d\n",status[x].name,tracking[x].total_process_time);
                
                //printf("%s completed at time %d\n",status[x].name,tracking[x].total_process_time);

                 
                continue; // ?
            }

            if(initaled_number_of_processes_to_memory_frame < status[0].length){
                initaled_number_of_processes_to_memory_frame = initaled_number_of_processes_to_memory_frame + 1;
            }
                
        }
    
    //testong line
    //printf("-----------------\n");


    }

    //finish print
    /*
    printf("-------\n");
    printf("finish print:table\n");
    print_check();
    */
    return tracking[0].cputime;
}




int reading(char *argvalue[]){

    // find out how many line in the file
    FILE *p_number_of_line = fopen(argvalue[1],"r"); // argvalue[1] //TEST
    int number_of_lines = 0;
    size_t single_character = 2;
    char *character = malloc(single_character * sizeof(char));

    while(fgets(character, single_character, p_number_of_line) != NULL){
        
        if(strcmp(character,"\n") == 0){ /* '==0' mean true */
            number_of_lines = number_of_lines + 1;
            // printf("character : %d\n",character);
            // printf("number_of_lines :%d\n",number_of_lines);
        }
    } 

    if(number_of_lines != 0 && strcmp(character,"\n") != 0){
        number_of_lines = number_of_lines + 1;
        //printf("(exit) number_of_lines :%d\n",number_of_lines);
    }else{
        printf("empty file, please try again\n");
        fclose(p_number_of_line);
        return 0;
    }

    //printf("number_of_lines (exited): %d\n",number_of_lines);
    //printf("last_character (exited): %s\n",character);
    free(character);
    fclose(p_number_of_line); 

    // first test out the maximum by guess, because read te file need a inital line length  
    int counting_number_of_lines = 0;
    size_t suggested_max_length = 10; // the number must be greater than 1, it can not read anything when = 1  
    bool value = false;
    //printf("number_of_lines : %d\n", number_of_lines);
    while(number_of_lines != counting_number_of_lines){ // some issue with the condition (infinite looping), check and revisit
        counting_number_of_lines = 0;
        /* if the counting_number_of_lines != number_of_lines once again, 
        value == true, then increase the memory size being allocated */

        if(value == true){
            suggested_max_length = suggested_max_length + 10; // maybe more than 1, but 1 is fine
            //printf("extended\n");
        }

        // open, read and test part
        FILE *p_memory_length_size = fopen(argvalue[1],"r"); // argvalue[1] //TEST

        char *open_line_length = malloc(suggested_max_length * sizeof(char));
    
        // error handle
        if(p_memory_length_size == NULL){
            printf("unable to open file, please try again\n");
            fclose(p_memory_length_size);
            return 0;
        }
    
        // read the file 
        size_t line_length;
        while(fgets(open_line_length, suggested_max_length, p_memory_length_size)!= NULL){
            counting_number_of_lines = counting_number_of_lines + 1;
            line_length = strlen(open_line_length);
            //printf("%zu\n",line_length);
        }

        /* when the var(counting_number_of_lines) is counted to the correct number of line 
        and  only if the read line_length is bigger than inital guess; the second condition 
        prevent the max length reduce */
        if(counting_number_of_lines == number_of_lines && suggested_max_length < line_length){
                suggested_max_length = line_length; // trying to give only the max length as a line present in the file 
        }
        value = true;

        //test
        /*
        printf("-----------\n");
        printf("suggested_max_length : %zu\n",suggested_max_length);
        printf("%d\n",counting_number_of_lines);
        printf("-----------\n");
        fclose(p_memory_length_size);
        */
    }
    
    // until here i check the line length, use the variable -> suggested_max_length, because it is checked

    /* initialized the array length dynamicly, similar to status_datas status[n] = {0},
    but in dynamic memory allocation, i need to used calloc to achieve the same thing */  
    status = calloc(number_of_lines, sizeof(status_datas));
    tracking = calloc(number_of_lines, sizeof(tracking_data));
     
    //printf("allocated: %zu\n",suggested_max_length);
    FILE *p_document = fopen(argvalue[1],"r"); // argvalue[1] //TEST
    size_t real_length = suggested_max_length + 1;
    //printf("real_length: %zu\n",real_length);
    
    char *p_line = malloc(real_length * sizeof(char)); // malloc() // notice, change the number of memory byte allocate will greatly affect
    char *p_word = malloc(real_length * sizeof(char)); // malloc()

    if(p_document == NULL){
        printf("unable to open file, please try again\n");
        return 0;
    }
    
    int i = 0;
    
    
    char *word2 = malloc(real_length * sizeof(char)); // malloc()
    char *time_t = malloc(real_length * sizeof(char)); // malloc()
    
    // actually reading lines
    
    while(fgets(p_line, real_length, p_document) != NULL){ // 50 need to be change into suggested_max_length as well 
        
        status[0].length = status[0].length + 1;
        
        size_t line_length = strlen(p_line);
        //printf("standard answer\n");
        //printf("%zu\n",line_length);
        /*if(line_length > 50){
        realloc(line,line_length * sizeof(line_length));}*/
        status[i].process_name_to_id = i;
        status[i].name = malloc(real_length * sizeof(char));
        status[i].IO_request_time = malloc(real_length * sizeof(int));
        status[i].IO_run_time = malloc(real_length * sizeof(int));
        status[i].memory_frame = malloc(4 * sizeof(int));
        status[i].next_used_pageNo = 0;
        
        for(int k = 0; k < 4; k = k + 1){
            /*if(k == 0){
            tracking[i].memory[k] = 0;
            }
            else{
                tracking[i].memory[k] = 99;
            }*/
           status[i].memory_frame[k] = 99;
        }

        status[i].process_name_to_id = i;
        sscanf(p_line,"%s",status[i].name);
        int n = strlen(status[i].name) + 1;
        sscanf(p_line + n, "%d",&status[i].finish_time);
        sprintf(p_word,"%d",status[i].finish_time);
        int m = strlen(p_word) + 1;
        
        int move = 0;
        int move2 = 0;
        int l = 0;
        // char *word2 = malloc(real_length * sizeof(char)); // malloc()
        // char *time_t = malloc(real_length * sizeof(char)); // malloc()
        while(line_length > n + m + move + move2){ // hate it, 2h debug
            if(sscanf(p_line + n + m + move + move2, "%d",&status[i].IO_request_time[l]) == 1){
                sprintf(word2,"%d",status[i].IO_request_time[l]);
                move = move + strlen(word2) + 1;
                status[i].IO_count = status[i].IO_count + 1; 
                
            }else{
                break;}

            if(sscanf(p_line + n + m + move + move2, "%d",&status[i].IO_run_time[l]) == 1){
                sprintf(time_t,"%d",status[i].IO_run_time[l]);
                move2 = move2 + strlen(time_t) + 1;

            }else{
                break;}


            l = l + 1;
        }
        
        i = i + 1; 
    }
    fclose(p_document);

    free(word2);
    free(time_t);
    free(p_line);
    free(p_word);
    return 0;
}

int write_out(char *writing_out[]){

    FILE *f_write = fopen(writing_out[2],"w"); // writing_out[1] //OUT

    //finish write out
    //printf("-------\n");
    //printf("finish print:table\n");
    fprintf(f_write,"Page table:\n");
    for(int l = 0; l < status[0].length; l = l + 1){
       fprintf(f_write,"Process %d: %d %d %d %d\n",l,status[l].memory_frame[0],status[l].memory_frame[1],status[l].memory_frame[2],status[l].memory_frame[3]); 
    }
    //printf("-------\n");
    fprintf(f_write,"\n");
    //printf("finish print:RAM\n");
    fprintf(f_write,"RAM:\n");
    for(int l = 0; l < 16; l = l + 1){
        fprintf(f_write,"Frame %d: %d, %d, %d;\n",l,memory_data[l].process_id,memory_data[l].page_number,memory_data[l].last_accessed_time);
    }
    //printf("-------\n");

    fclose(f_write);

    return 0;

}




int main(int argcount, char *argvalue[]){
if(argcount < 3){
    printf("no or insuffient file name\n");
    return 0;
}
reading(argvalue); // use argvalue after complete
processes();
write_out(argvalue);


for(int i = 0; i < status[0].length; i = i + 1){
    free(status[i].name);
    free(status[i].IO_request_time);
    free(status[i].IO_run_time);
}
free(status);
free(tracking);


return 0;
}
