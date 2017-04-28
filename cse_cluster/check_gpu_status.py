from subprocess import check_output
import os
import re
import time

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

/usr/bin/nvidia-smi
sleep 10s""".format(CURRENT_DIR, CURRENT_DIR, CURRENT_DIR, client_name)
    return str

info_str = ""
regex = "Your job (\d+)"
pattern = re.compile(regex)
job_ids = []
for name in gpu_clients:
    print("Submitting the job for", get_gpu_info_bash(name))
    f = open("gpu_status_temp.sh", "w")
    f.write(get_gpu_info_bash(name))
    f.close()
    out = check_output(['qsub', '-q', 'all.q', 'gpu_status_temp.sh'])
    out = str(out)
    job_ids.append(pattern.findall(out)[0])
os.remove("gpu_status_temp.sh")
for name, id in zip(gpu_clients, job_ids):
    output_filename = "gpu_info.o{}".format(id)
    error_filename = "gpu_info.e{}".format(id)
    while not os.path.exists(output_filename):
        time.sleep(1)
    info_str += "# GPU Info {}\n\n".format(name)
    f = open(output_filename, 'r')
    info_str += "```"
    info_str += "".join(f.readlines()[2:])
    info_str += "```"
    f.close()
    info_str += "\n"
    os.remove(output_filename)
    os.remove(error_filename)
f = open("gpu_info.md", 'w')
f.write(info_str)
f.close()
