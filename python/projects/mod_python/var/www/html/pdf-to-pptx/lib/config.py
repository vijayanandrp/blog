import os

current_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def check_dir(path_name):
    if not os.path.exists(path=path_name):
        os.mkdir(path_name)

# directory configurations
data_path = os.path.join(current_dir, 'data')
check_dir(data_path)
upload_path = os.path.join(data_path, 'upload')
check_dir(upload_path)
download_path = os.path.join(data_path, 'download')
check_dir(download_path)

# Python file for execution
pdf_to_ppt = os.path.join(current_dir, 'lib', 'pdf_to_pptx.py')

# logger configurations
log_path = os.path.join(data_path, 'log')
check_dir(log_path)
log_file = os.path.join(log_path, 'convertor.log')


# cache path
tmp_path = '/var/apache_tmp'

# Make sure you create a temp path and configure in  root mode
# check_dir(tmp_path)
# sysctl -w vm.drop_caches=3
# mount -t tmpfs tmpfs /var/apache_tmp/ -o size=100M,noexec,nosuid
# sudo chown www-data:www-data /var/apache_tmp/ -R

