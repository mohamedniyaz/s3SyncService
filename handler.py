import time

import boto3
import schedule
import sys
import os
import logging
from windowsService import SMWinservice
from config import logging_config, local_path, s3_path, sync_time
from logging.config import dictConfig
dictConfig(logging_config)
log = logging.getLogger('my.package')
s3 = boto3.client('s3')


class S3Service(SMWinservice):
    _svc_name_ = "S3SyncService"
    _svc_display_name_ = "S3 Sync Service"
    _svc_description_ = "Service to Sync files to S3"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False


    def main(self):
        try:
            while self.isrunning:
                log.info(f' -- s3SyncService started syncing files')
                for path in local_path:
                    log.info(f' -- Syncing  {path}')
                    sync_cmd = 'aws s3 sync ' + path + ' ' + s3_path
                    log.info(f' -- {sync_cmd}')
                    os.system(sync_cmd)
                    log.info(f' -- Syncing  completed {path}')
                log.info(f' -- s3SyncService completed syncing files')
                time.sleep(sync_time)
        except Exception as err:
            log.error(f' -- s3SyncService error {err}')
            sys.exit(-1)



# entry point of the module: copy and paste into the new module
# ensuring you are calling the "parse_command_line" of the new created class
if __name__ == '__main__':
    try:
        log.info(f' -- parse command line()')
        S3Service.parse_command_line()
    except Exception as err:
        log.error(f' -- s3SyncService error {err}')
        sys.exit(-1)

