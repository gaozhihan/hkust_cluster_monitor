from subprocess import check_output
import os
import re

gpu_clients = ["client108", "client109", "client110", "client111", "client112",
               "client113", "client114"]

def get_gpu_info_bash(client_name):
    str =\
r"""#!/bin/csh
# specify where the output file should be put
#$ -o ./
#$ -e ./

# specify the working path
#$ -wd ./

#$ -l h={}
#$ -N gpu_info

setenv PATH "/usr/local/cuda-8.0/bin:$PATH"
nvidia-smi""".format(client_name)
    return str

info_str = ""
regex = "Your job (\d+)"
pattern = re.compile(regex)
for name in gpu_clients:
    info_str += "# GPU Info {}".format(name)
    print("Submitting the job for", get_gpu_info_bash(name))
    f = open("gpu_status_temp.sh", "w")
    f.write(get_gpu_info_bash(name))
    out = check_output(['qsub', '-q', 'all.q', 'gpu_status_temp.sh'])
    print(pattern.findall(out)[0])
    f.close()
os.remove("gpu_status_temp.sh")
