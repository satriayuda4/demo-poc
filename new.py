import os
from tkinter import Y 

list_file = os.listdir("text")
#print(list_file)

line = ''
clas = ['sekolah', 'nama', 'mata_pelajaran', 'nilai']
start_list = [52, 80, 87, 93]
end_list = [71, 85, 90, 97]

for i in range(len(list_file)):
    #print(list_file[i])
    file = "text/" + list_file[i]
    #print(file)
    f = open(file, "r", encoding="utf-8")
    text = f.read()
    text = text.replace("\n", " ")
    f.close()
    #print(text)
    condition = True
    start_ = []
    end_ = []
    name_ = []
    for i in range(4):
        #start = int(input("input start "))
        #end = int(input("input end "))
        start = start_list[i]
        end = end_list[i]
        #print("input start", start)
        #print("input end", end)
        #print("The text is:",text[start:end])
        #ask_satisfied = input("Satisfied? (y/n)")
        ask_satisfied = "y"
        #print("Satisfied? (y/n)", ask_satisfied)
        if ask_satisfied == "y" or ask_satisfied == 'Y':
            #name = input('Display name: ')
            name = clas[i]
            #name = "sekolah"
            name_.append(name)
            start_.append(start)
            end_.append(end)
        elif ask_satisfied == "n" or ask_satisfied == 'N':
            """ask_exit = input("exit? (y/n)")
            if ask_exit == 'y':
                condition = False
                break"""
            continue
    
    start_text = '{"annotations": ['
    end_text = '],"text_snippet": {"content": "' + text + ' " }}'
    tmp = ''
    for i in range(len(start_)):
        start = start_[i]
        end = end_[i]
        name = name_[i]
        mid_txt = '{"text_extraction": {"text_segment": {"end_offset": ' + str(end) + ',"start_offset": ' + str(start) + '}}, "display_name": "' + name + '"}'
        tmp += mid_txt
        if i+1 < len(start_):
            tmp += ','
    tmp = start_text + tmp + end_text

    line += tmp
    line += '\n'

print(line)

f = open("demo-new.jsonl", "w",encoding="utf-8")
f.write(line)
f.close()