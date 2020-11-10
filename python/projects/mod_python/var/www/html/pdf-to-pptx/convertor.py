from mod_python import apache, util
import os
import sys
import shutil
import uuid

current_dir = os.path.dirname(os.path.realpath(__file__))
for paths, dirs, files in os.walk(current_dir):
    if 'lib' in paths:
        sys.path.append(paths)

from config import upload_path, check_dir, download_path, tmp_path, pdf_to_ppt
from logger import Logger
from pdf_to_pptx import PdfToPpt

random_string = ''


class Storage(file):
    def __init__(self, file_name):
        global random_string
        file_name = [check for check in file_name.split('\\') if '.pdf' in check]
        self.fname = file_name[0]
        self.logger = Logger.defaults('Storage - convertor.py ')
        self.file_path = '%s/%s' % (upload_path, random_string)
        check_dir(self.file_path)
        self.file_path = '%s/%s' % (self.file_path, self.fname)
        self.download_path = ''
        self.tmp_path = tmp_path
        self.ret_ok = False
        self.md5sum = ''
        try:
            super(Storage, self).__init__(self.file_path, 'w+b')
            self.ret_ok = True
        except:
            pass

    def close(self):
        super(Storage, self).close()
        self.make_setup()

    def make_setup(self):
        self.logger.info('Filename = %s ', self.file_path)
        if not '.pdf' in self.file_path:
            self.logger.info('Make sure correct pdf file is uploaded ..')
            return
        # self.md5sum = hashlib.md5(self.file_path).hexdigest()
        self.md5sum = random_string
        self.logger.info('Random String is %s ' % self.md5sum)
        self.download_path = os.path.join(download_path, self.md5sum)
        check_dir(self.download_path)
        self.tmp_path = os.path.join(tmp_path, self.md5sum)
        check_dir(self.tmp_path)
        shutil.copy(self.file_path, self.tmp_path)
        ppt_file = os.path.join(self.download_path, self.fname)
        shutil.copy(self.file_path, ppt_file)
        pdf_file = os.path.join(self.tmp_path, self.fname)
        self.logger.debug('Reached here ----<<<<>>>>>>------ \n %s  \n %s \n' % (pdf_file, ppt_file))
        PdfToPpt(pdf_file=pdf_file, ppt_file=ppt_file).execute()


def handler(req):
    global random_string
    log = Logger.defaults('Main Handler')
    log.info('$'*80)
    random_string = str(uuid.uuid4()).replace('-', '')
    req.content_type = 'text/plain'
    strIP = req.get_remote_host(apache.REMOTE_NOLOOKUP)
    if req.method != 'POST':
        return apache.HTTP_BAD_REQUEST
    request_data = util.FieldStorage(req, keep_blank_values=True, file_callback=Storage)
    log.info('Client IP - %s' % strIP )
    req.write(random_string)
    return apache.OK
