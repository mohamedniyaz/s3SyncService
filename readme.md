Reference Link
 * http://thepythoncorner.com/dev/how-to-create-a-windows-service-in-python/


Steps to install
* install python
* python handler.py install {Installing service handler.py Service installed}
* python handler.py update {Changing service configuration Service updated}

Run as Service
* Open services (run services.msc)
* Select the Service - properties
* Startup type - Automatic
* Log on - Select this account , use your logon account and password


Delete Service
* sc delete servicename