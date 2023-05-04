#!/home/halvard/miniconda3/bin/python

import pprint
import subprocess
import sys
import os



GET_RUNNING_KERNELS_SCRIPT = os.environ['HOME'] + '/bin/get_running_kernels.sh'

# use -a to print all kernels, including those without GPUs
args = " ".join(sys.argv[1:])
print_all = args == "-a"

def get_gpu_processes():
    """Gets data of processes using GPU by parsing output of nvidia-smi -q"""
    out = subprocess.run(['nvidia-smi', '-q'], stdout=subprocess.PIPE)
    raw_processes = [s.strip() for s in
             out.stdout.decode("utf-8").split("\n")]
    raw_processes = [s for s in raw_processes if s]

    ind = raw_processes.index("Processes")
    raw_processes = raw_processes[1+ind:]

    processes = []
    process = None
    for line in raw_processes:
        if line.startswith("GPU instance ID"):
            if process is not None:
                processes.append(process)

            process = {}
        else:
            key, val = map(str.strip, line.split(":"))
            process[key] = val
    if process is not None:
        processes.append(process)
    return processes


def match_process_and_jupyter_kernel(processes):
    """using the PID of each python process, extracts jupyter kernel id from
    the command used to run the process"""
    kernel_id_to_process_num = {}
    for i,process in enumerate(processes):
        if "python" in process['Name']:
            cmd = subprocess.run(['ps', '-p', process['Process ID'], '-o',
                            'args'], stdout=subprocess.PIPE
                                ).stdout.decode("UTF-8")
            path = cmd.split()[-1]
            kid = path[7+path.find('kernel'):].split(".")[0]
            kernel_id_to_process_num[kid] = i
    return kernel_id_to_process_num

def get_running_jupyter_sessions():
    sessions = subprocess.run([GET_RUNNING_KERNELS_SCRIPT], stdout=subprocess.PIPE)
    sessions = eval(sessions.stdout.decode("utf-8"))
    return sessions

def print_kernel_GPU_memory_usage(processes, kernel_id_to_process_num, sessions):
    for session in sessions:
        kernel_id = session['kernel']['id']
        if kernel_id in kernel_id_to_process_num:
            process = processes[kernel_id_to_process_num[session['kernel']['id']]]
            mem = process['Used GPU Memory']
        else:
            if not print_all:
                continue
            mem = "No GPU"

        print(f"{mem:10}", session['path'], )


def main():
    gpu_processes = get_gpu_processes()
    kernel_id_to_process_num = match_process_and_jupyter_kernel(gpu_processes)
    jupyter_sessions = get_running_jupyter_sessions()
    print_kernel_GPU_memory_usage(gpu_processes, kernel_id_to_process_num,
                                  jupyter_sessions)

if __name__ == "__main__":
    main()
