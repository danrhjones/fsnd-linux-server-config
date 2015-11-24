Details of Server Configuration Project
========================================

## Connection Details

#### URL
- http://ec2-52-27-144-117.us-west-2.compute.amazonaws.com/

##### IP address
- 52.27.144.117

##### User details and SSH port

Log in with the user 'grader' on port 2200

Use private key provided


## Installed Applications
- Installed the following applications:

- Postgres
- Apache
- php (for Nagois)
- libapache2-mod-wsgi
- Flask
- Flask-Login
- Flask-SeaSurf
- SQLAlchemy
- oauth2client



## Configuration changes made

- Added 'grader' to the sudoers by creating a new user specific file in /etc/sudoers.d/
- Disabled root from ssh login by changing 'PermitRootLogin' to no in /etc/ssh/sshd_config
- Configured the SSH port to 2200 by changing 'Port' to 2200 in /etc/ssh/sshd_config 
- Configured UFW to initially deny all incoming and allow all outgoing, then configured to allow incoming on port 80 (http), port 2200 (for the updated SSH port) and port 123 (NTP)
- Changed the time zone to UTC using 'sudo dpkg-reconfigure tzdata' 
- Create Catalog application folders in /var/www/catalog
- catalogapp.wsgi - the WSGI wrapper
- /catalog - contains all the code for the catalog site

## Changes to the existing code:
- Changed the path to the images folder to be an absolute rather than relative path.
- Changed path to client_secrets.json in google_connect_oauth.py to absolute path
- Updated database URL in db_helper.py



## Monitoring application 
I have used Nagios 4. This has been configured to show the health of the server

Url:

http://ec2-52-27-144-117.us-west-2.compute.amazonaws.com/nagios/

The user name is: nagiosadmin

The password is:  p455w0rd

## Resources used (in no order)
- https://help.ubuntu.com/lts/serverguide/httpd.html
- https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
- http://stackoverflow.com/questions/20627327/invalid-command-wsgiscriptalias-perhaps-misspelled-or-defined-by-a-module-not
- http://stackoverflow.com/questions/338768/python-importerror-no-module-named
- http://askubuntu.com/questions/122330/unable-to-restart-apache-getting-error-apache2-bad-user-name-apache-run-use
- http://flask.pocoo.org/docs/0.10/patterns/packages/
- http://stackoverflow.com/questions/6454564/target-wsgi-script-cannot-be-loaded-as-python-module
- http://stackoverflow.com/questions/7225900/how-to-pip-install-packages-according-to-requirements-txt-from-a-local-directory
- http://stackoverflow.com/questions/23686558/setting-up-psycopg2-for-the-first-time-how-do-you-configure-it-for-some-test-da
- http://docs.sqlalchemy.org/en/latest/core/engines.html#postgresql
- http://stackoverflow.com/questions/31168606/internal-server-error-target-wsgi-script-cannot-be-loaded-as-python-module-and
- http://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session
- http://unix.stackexchange.com/questions/7283/how-can-i-make-a-user-able-to-log-in-with-ssh-keys-but-not-with-a-password
- https://www.digitalocean.com/community/tutorials/how-to-install-nagios-4-and-monitor-your-servers-on-ubuntu-14-04
