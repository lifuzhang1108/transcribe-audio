import os
from subprocess import PIPE, run
from multiprocessing import Process, cpu_count


def transcribe_file(i):
    path=file_list[i]
    print('process:',path)
    fn=path[0:-3].split("/")[-1]+'txt'
    if fn in txt_list:
        print("skipped")
        return
    command = ["deepspeech", "--model", "deepspeech-0.7.4-models.pbmm", "--scorer","kenlm.scorer","--audio",path]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if len(result.stdout)>0:
        text_file = open(fn, "w")
        n = text_file.write(result.stdout)
        text_file.close()
        print('done')


file_list=[]
for root, dirs, files in os.walk("../wav"):
    for file in files:
        if file.endswith(".wav"):
            file_list.append(os.path.join(root, file))
print(file_list)

txt_list=[]
for root, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".txt"):
            txt_list.append(os.path.join( file))
                

for i in range(len(file_list)):
    p = Process(target=transcribe_file, args=(i,))
    p.start()
    p.join()
    print('Transcribed file {} : {} '.format(i + 1,  file_list[i]))







# for i in file_list:
#     print('process:',i)
#     fn=i[0:-3]+'txt'
#     command = ["deepspeech", "--model", "deepspeech-0.7.4-models.pbmm", "--scorer","kenlm.scorer","--audio",i]
#     result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
#     text_file = open(fn, "w")
#     n = text_file.write(result.stdout)
#     text_file.close()
#     print('done')
