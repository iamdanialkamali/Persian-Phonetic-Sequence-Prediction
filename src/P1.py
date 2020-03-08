#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os
import csv
import io

csv_file = open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'in/Entries.csv')), mode='r')
pron_datas = csv.reader(csv_file)
farsi_to_pron_dict = {}
pron_to_farsi_dict = {}
farsi_words_count = {}
final_result = []

def found_word(words,full_prons):
    if(len(full_prons)==0):
        # print(words)
        final_result.append(words)
    word = ""
    new_words = words[:]
    lenght = len(full_prons)
    for index in range(lenght):
        word+=full_prons[index]
        if( word in pron_to_farsi_dict ):
            new_words_for_next_level = new_words[:]
            new_words_for_next_level.append(word)
            found_word(new_words_for_next_level,full_prons[index+1:])


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

found_word([],test_full_pron)

output_file = open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'out/sample_Rec_out.txt')), mode='w')

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