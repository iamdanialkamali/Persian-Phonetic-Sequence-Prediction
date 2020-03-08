#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv
import os

csv_file = open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'in/Entries.csv')), mode='r')
pron_datas = csv.reader(csv_file)
farsi_to_pron_dict = {}
pron_to_farsi_dict = {}
farsi_words_count = {}
final_result = []
words_series = []
def found_word(full_prons,index):
    word = ""
    goal_reached = False
    if(index==len(full_prons)):
        return True
    elif(words_series[index] !=1):    
        lenght = len(full_prons[index:])
        for word_index in range(lenght):
            word+=full_prons[index+word_index]
            if( word in pron_to_farsi_dict ):
                
                if(len(words_series[index + word_index+1])==0 ):
                    if(found_word(full_prons ,index + word_index+1)):
                        words_series[index].append(word)
                        goal_reached = True
                else:
                    words_series[index].append(word)
                    
            

        if(goal_reached):
            return True
    elif(words_series[index]==1):
        return False
    # else:             
    #     words_series[index].append(words_series[index+l])



for row in pron_datas:
    # print(row)
    if( row[1] in farsi_words_count and  (row[0] in pron_to_farsi_dict) == True ):
        farsi_words_count[row[1]] = int(farsi_words_count[row[1]]) + 1
    else:
         farsi_words_count[row[1]] = 1
    
    farsi_to_pron_dict[row[1]] = row[0]
    pron_to_farsi_dict[row[0]] = row[1]
csv_file.close()

test = open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'in/in_1.txt')), mode='r') 
test_line = test.readline()
test_words = test_line.split(' ')
# print(test_words)
test_prons = []
for word in test_words:
    test_prons.append(farsi_to_pron_dict[word])
test_full_pron = ''.join(test_prons)
# print(test_prons)
# print(test_full_pron)
words_series = [[] for i in range(len(test_full_pron)+1)]
found_word(test_full_pron,0)

total_count = 0
for i in range(len(words_series)):
    total_count *= len(words_series[i])

final_result = [ [] for i in range(total_count-1) ]    
words_series2 = [i[:] for i in words_series]
delete_count = [0 for i in words_series]
for first_list_index in range(len(words_series)):
    moved = False
    first_list_lenght = len(words_series[first_list_index])
    if(first_list_lenght>0):
        for first_list_word_index in range(first_list_lenght):
            last_word_lenght =  len(words_series[first_list_index][first_list_word_index].split('-')[-1])
            second_list_index =  first_list_index + last_word_lenght
            second_list_lenght = len(words_series2[second_list_index])
            second_list = words_series2[second_list_index][:]
            
            for second_list_words_index in range(second_list_lenght):
                second_list = words_series2[second_list_index][:]
                moved = True
                words_series[second_list_index].append(words_series[first_list_index][first_list_word_index]+"-" +second_list[second_list_words_index % second_list_lenght])
                if(delete_count[second_list_index]<len(words_series2[second_list_index])):
                    del words_series[second_list_index][0]
                    delete_count[second_list_index]+=1

        if(moved):
            words_series[first_list_index] = []
for i in words_series:
    if(len(i)>0):
        for j in i:
            final_result.append(j.split('-'))

output_file = open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'out/sample_DP_out.txt')), mode='w')

for sentece in final_result:
        new_sentece = []
        count  = 1
        for word in sentece:
            temp_count = int(farsi_words_count[pron_to_farsi_dict[word]])
            count *= temp_count
        
        for word in sentece:
            new_sentece.append(pron_to_farsi_dict[word])

        for i in range(count):
            output_file.writelines("-".join(new_sentece))
output_file.close()