from subprocess import check_output
import os
import re

gpu_clients = ["client108", "client109", "client110", "client111", "client112",
               "client113", "client114"]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
def get_gpu_info_bash(client_name):
    str =\
r"""#!/bin/csh
# specify where the output file should be put
#$ -o {}
#$ -e {}

# specify the working path
#$ -wd {}

#$ -l h={}
#$ -N gpu_info

/usr/bin/nvidia-smi > {}.gpu.txt""".format(CURRENT_DIR, CURRENT_DIR, CURRENT_DIR,
                                           client_name, client_name)
    return str

info_str = ""
regex = "Your job (\d+)"
pattern = re.compile(regex)
for name in gpu_clients:
    info_str += "# GPU Info {}".format(name)
    print("Submitting the job for", get_gpu_info_bash(name))
    f = open("gpu_status_temp.sh", "w")
    f.write(get_gpu_info_bash(name))
    f.close()
    out = check_output(['qsub', '-q', 'all.q', 'gpu_status_temp.sh'])
    out = str(out)
    print(pattern.findall(out)[0])
os.remove("gpu_status_temp.sh")
