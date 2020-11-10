import os
import subprocess

# get root directory
current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

home = subprocess.getstatusoutput('echo $HOME')

# directory configurations
data_path = os.path.join(current_dir, 'data')
if not os.path.exists(data_path):
    os.mkdir(data_path)

logs_path = os.path.join(data_path, 'logs')
if not os.path.exists(logs_path):
    os.mkdir(logs_path)

# Log File
log_file = os.path.join(logs_path, 'defaults.log')

