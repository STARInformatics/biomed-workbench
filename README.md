# Biomedical Knowledge Workbench

## Getting Started

This project resides in [this Github project repository](https://github.com/STARInformatics/biomed-workbench).

Here, we assume that we are using a Debian Linux flavor (like Ubuntu) to run the application. Adjust accordingly to
your preferences.

First, it is generally wise to get the latest releases of your existing software (like python). To do this, you can 
run the followiung:

```
sudo apt update
sudo apt upgrade --autoremove
```

Rebooting the system after such an upgrade is generally advisable.

Next, ensure that you have the git client installed:

``` 
sudo apt install git
```

Next, you should configure git with your Git repository metadata and, perhaps, activate credential management (we use 'cache' mode here to avoid storing credentials in plain text on disk)

``` 
git config --global user.name "your-git-account"
git config --global user.email "your-email"
git config --global credential.helper cache
``` 

Then, you can clone the project. A convenient location for the code is in a folder under **/opt/bkw**:

``` 
cd /opt/bkw
git clone https://github.com/STARInformatics/biomed-workbench
```

It is recommended that you have Python release 3.6.* or higher installed on your system, accessible by the application.
Generally,  we recommend release 3.7.*. This can be obtained as follows:

```  
sudo apt install python3.7 python3.7-venv

```

A Unix-style _Makefile_ is provided to configure and run the workbench web application.

First, check if the _make_ command is installed:

``` 
which make
```

should show you a path something like ```/user/bin/make```. If nothing is returned, then install it:

``` 
sudo apt install make
```

It is recommended to install the Biomedical Workbench within a 
[Python "Virtual Environment"](https://docs.python.org/3/tutorial/venv.html). 
If not provided within your development environment (some IDE's like PyCharm can provide one), 
the following _make_ target can be run once to create one (this target only runs with Python 3.6 or better).

FIrst, you can check your project settings:

```  
make project_settings
```

will likely simply  tell you where your virtual environment is assumed to be located (default 'venv';  see the section 
**Customizing the Build** below, if you wish to change this location). 

If the virtual environment is not already created, you can create it as follows:


``` 
make venv
```


The following _make_ target installs the Python project dependencies into the specified environment:

```
make install
```

## Running the Workbench

After configuring the system, the following command runs the workbench, making it accessible 
at the local URL http://127.0.0.1:5000/:


```
make run
```

##  Publishing the Site to the Outside World

Quite often, the workbench site may not be visible to the outside world. To facilitate access, the
**NGINX** web server may be installed:

``` 
sudo apt install nginx
```

This installation will actually completely set up an NGINX server for regular HTTP (port 80, non-SSL) access.
Assuming that the server's firewall lets this port through, you should see a default NGINX index page now come up.

To override this to point to your new workbench web site, you'll need to add some proxy directives. If you have
a subdomain name to point to your server's public IP address, say **bkw.mydomain.com**,  create the following file
under the /

```
#
# Virtual Host configuration for bkw.mydomain.com
#
# You can move that to a different file under sites-available/ and symlink that
# to sites-enabled/ to enable it.
#
server {
       listen 80;
       listen [::]:80;

       server_name bkw.mydomain.com;

       location / {
       
        proxy_set_header X-Forwarded-Host        $host;
        proxy_set_header X-Forwarded-Server      $host;
        proxy_set_header X-Forwarded-For         $proxy_add_x_forwarded_for;

        proxy_pass       http://localhost:5000/;               
       }
}
                      
```

## Adding HTTPS (SSL) Service


``` 
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe

```

##  Customizing the Build

The default location for the "virtual environment" is _venv_.  To override this default location,
you can set the environment variable **VENV**, namely:

```
# Specify the subdiretory location 'py37' 
# for the Python virtual environment
export VENV=py37
```

before running any of the above _make_ targets. Alternately, you may override the location on each 
of the make targets by adding the environment variable there,  e.g.


```
# Creates and uses the virtual environment under subdirectory 'py36'
make venv -e VENV=py36
make install -e VENV=py36
make run  -e VENV=py36
```
