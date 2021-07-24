Reference Link
 * http://thepythoncorner.com/dev/how-to-create-a-windows-service-in-python/

Steps to install aws cli
* install aws cli
* create an IAM user that has only sync access to the S3 buckets you prefer
* run aws config and set up the IAM user as default profile

Steps to install
* install python
* open system environment variables
* make sure to set python home dir to system path variable
* make sure to set pip home dir to system path variable
* download the code from git 
* open command prompt as admin
* navigate into the code dir and do the following
* run "pip install -r requirements.txt"
* make sure the {PYTHON_HOME}\Lib\site-packages\pywin32_system32\pywintypes{version}.dll
  is copied over to {PYTHON_HOME}\Lib\site-packages\win32
* run "python handler.py install" {Installing service handler.py Service installed}
* run "python handler.py update" {Changing service configuration Service updated}

Run as Service
* open services (run services.msc)
* select the Service - properties
* startup type - Automatic
* Log on - Select this account , use your logon account and password

Debug Service 
* "python handler.py debug"
* logs can be found in the service root dir 
  * run services.msc
  * double click on the service
  * "Path to executable" is where the logs are afound under 
    the name info.log and error.log

Delete Service
* Find out the pid of the service and kill
  * sc queryex servicename
  * taskkill /F /PID servicepid
* sc delete servicename