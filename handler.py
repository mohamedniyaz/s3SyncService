import time
import boto3
import psutil
import sys
import logging
from subprocess import Popen, PIPE
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
        try:
            pid = None
            for proc in psutil.process_iter():
                if proc.name() == 'aws.exe':
                    pid = proc.pid
                    log.info(f' -- kill aws cli pid {pid}')
                    proc.kill
                    log.info(f' -- kill aws cli pid {pid} complete')
            process = psutil.win_service_get(self._svc_name_)
            pid = None
            pid = process.pid()
            p = psutil.Process(pid)
            if p is not None:
                log.info(f' -- kill the s3SyncService pid {pid}')
                p.kill()
                log.info(f' -- kill the s3SyncService pid complete {pid}')
        except Exception as err:
            log.error(f' -- s3SyncService error {err}')
            sys.exit(-1)
            log.info(f' -- Stopping the s3SyncService')

    def main(self):
        try:
            while self.isrunning:
                log.info(f' -- s3SyncService started syncing files')
                for path in local_path:
                    log.info(f' -- Syncing  {path}')
                    sync_cmd = 'aws s3 sync ' + path + ' ' + s3_path
                    log.info(f' -- {sync_cmd}')
                    run = True
                    command = Popen(sync_cmd, stdout=PIPE, shell=True)
                    while run is True:
                        output = command.stdout.readline()
                        if not output and command.poll() is not None:
                            run = False
                        if output:
                            log.info(f' -- Syncing  completed {output}')

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
