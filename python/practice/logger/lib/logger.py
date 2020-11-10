import logging
import os
from config import log_file, logs_path
from datetime import datetime, timedelta


def date_stamp_with_days_subtraction(fmt='%Y-%m-%d', days_to_subtract=1):
    date_stamp = datetime.now() + timedelta(days=-days_to_subtract)
    date_stamp = date_stamp.strftime(fmt)
    return date_stamp


class Logger(object):
    """ module for logging the executions and statements """

    @staticmethod
    def defaults(name, logfile=log_file, debug_level='DEBUG', output_stream=True, check_log_file=False):
        """ default configuration settings in the method """
        
        if check_log_file:
            """ Backup the old log file with date stamp """
            new_file = "{}_{}".format(date_stamp_with_days_subtraction(), os.path.basename(logfile))
            new_file = os.path.join(logs_path, new_file)
            if not os.path.isfile(new_file):
                os.rename(log_file, new_file)
        
        if debug_level is "INFO":
            debug_level = logging.INFO
        elif debug_level is "DEBUG":
            debug_level = logging.DEBUG
        else:
            debug_level = logging.INFO

        # log file configuration
        logging.basicConfig(
            level=debug_level,
            filename=logfile,
            filemode='a',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')

        if type(output_stream) is bool and output_stream:
            # console output
            console = logging.StreamHandler()
            console.setLevel(debug_level)
            console.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
            logging.getLogger('').addHandler(console)

        return logging.getLogger("%s" % name)


if __name__ == "__main__":
    log = Logger.defaults(__name__, output_stream=True, logfile=log_file)
    log.info("This is info module")
    log.debug(" Debug contents here")
    log.warning("Warning statements here")
    log.critical("Critical contents ")
    log.error("ERROROROR")
    log.exception("See below example ")
    try:
        import excel
    except Exception as error:
        log.error("Import error", exc_info=True)
        log.exception('err')  # default = exc_info = 1
