import os 

print(os.listdir("text"))

list_file = os.listdir("text")

start_ = []
end_ = []
name_ = []

classify = ['sekolah', 'nama', 'mata_pelajaran', 'nilai']

start = 1
line = ''

for clas in classify:
    name_.append(clas)
    start_.append(start)
    start += 5
    end_.append(start)
    start += 2

for file in list_file:
    print(file)
    f = open("text/"+str(file), "r")
    text = f.read()
    text = text.replace("\n", " ") 
    f.close()   

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
    #print(tmp)

    line += tmp
    line += '\n'
    print(line)

f = open("demo.jsonl", "w")
f.write(line)
f.close()

"""f = open("text/"+list_file[0], "r")
text = f.read()
text = text.replace("\n", " ")

start_ = []
end_ = []
name_ = []

classify = ['sekolah', 'nama', 'mata_pelajaran', 'nilai']

start = 1
line = ''

for clas in classify:
    name_.append(clas)
    start_.append(start)
    start += 5
    end_.append(start)
    start += 2
    print(clas)

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
    print(tmp)

    line += tmp
    line += '\n'
    line

f = open("demo.jsonl", "w")
f.write(line)
f.close()

print(name_)
print(start_)
print(end_)"""





