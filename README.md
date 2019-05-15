# Biomedical Knowledge Workbench

### Scripts

- `python scripts/fix_sbgn.py`: fixes the sub-component relations between nodes in the Reactome SBGN files.
- `python scripts/build_id_mapping_csv.py`: builds up a CSV mapping names of Reactome elements (which are used as the labels of nodes in the SBGN files) to identifiers.

## Getting Started

This project resides in [this Github project repository](https://github.com/STARInformatics/biomed-workbench).

Here, we assume that we are using a Debian Linux flavor (like Ubuntu) to run the application. Adjust the commands
accordingly to your chosen operating system (e.g. Microsoft Windows procedures will be slightly different).
Note that under Linux, you may need to use _sudo_ to run some of these package installation commands.

First, some software may need to be updated and installed. In preparation, update your local package index as follows:

```
sudo apt update
```

It is recommended that you have Python release 3.6.* or higher installed on your system, accessible by the application.
Install it if necessary (Ubuntu Linux often already has it installed).

Ensure that **pip3** is installed:

```
# check where pip3 is installed
command -v pip3
```


If the previous command returns an empty result then under Ubuntu Linux, you can:

```
sudo apt-get install python3-pip
```

Under Windows, you may need to run something like this:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

Ensure that **virtualenv** is installed:

```
# check where virtualenv is installed
command -v virtualenv

# if the previous command returns an empty result then...you may need 'sudo' if installed centrally
pip3 install virtualenv
```

Optionally, under Linux, package installation may also be used:

```
sudo apt install virtualenv
```

Next, ensure that you have the **git** client installed:

```
# check where git is installed
command -v  git

# if the previous command returns an empty result then...
sudo apt install git
```

Next, ensure that you have the **curl** software installed.  Some operating  systems have it;  others, maybe not by  default:

```
# check where git is installed
command -v curl

# if the previous command returns an empty result then...
sudo apt install curl
```

A Unix-style _Makefile_ is provided to configure and run the workbench web application.
Thus, you need to ensure that you have a version of the Unix **make** installed:

```
# check where make is installed
command -v  make

# if the previous command returns an empty result then...
sudo apt install make
```

Finally, ensure that you have **npm** installed:

```
# check where make is installed
command -v npm

# if the previous command returns an empty result then...
sudo apt install npm
```

It is generally wise to get all of the latest releases of your existing software (like python). To do this, you can
run the following:

```
sudo apt upgrade --autoremove
```

Rebooting the system after such an upgrade is generally advisable. Afterwards, log back into the system to continue.

## Building the Project

Configure git with your Git repository metadata and, perhaps, activate credential management (we use 'cache' mode here to avoid storing credentials in plain text on disk)

```
git config --global user.name "your-git-account"
git config --global user.email "your-email"
git config --global credential.helper cache
```

Then, you can clone the project. A convenient location for the code is in a folder under **/opt/bkw**:

```
cd /opt
sudo mkdir bkw
sudo chown ubuntu:ubuntu bkw     # substitute your username on the system, if not ubuntu
cd bkw
git clone https://github.com/STARInformatics/biomed-workbench
```

### Python Virtual Environment

Here, we recommend that the Biomedical Workbench back end service be install and run within a
[Python "Virtual Environment"](https://docs.python.org/3/tutorial/venv.html).

If not already configured within your development environment (some IDE's like PyCharm can deploy one), then you
will need to create one.

The default subdirectory name for the "virtual environment" is _venv_.  To override this default location,
you can set the environment variable **VENV**.  For example, to specify the virtual environment location 'py36':

```
export VENV=py36
```

before running any of the system _make_ targets. Alternately, you may override the location of the Python
virtual environment location the 'install' and 'service' make targets (Note: target 'web' doesn't use the environment)

```
make install -e VENV=py36
make service  -e VENV=py36
make web
```

To create a Python virtual environment, run the following:

```
virtualenv -p python3.6 ${VENV}
```

The virtual environment needs to be activated before proceeding further with the building and operation of the system:

```
source ${VENV}/bin/activate
```

The virtual environment may be deactivated as follows:

```
deactivate
```

### Configuring to Run the Application Behind a Hostname

If you are planning to host the application behind a web service proxy (see NGINX discussion below) configured to point to a specified hostname and using a preferred internet protocol, then it will be necessary to  communicate the site particulars to the application. In particular, the following environment variables should be set (exported?) to the anticipated hostname and service API path _before_ fully configuring the system:

* `REACT_APP_FRONTEND_URL` defaults to http://localhost:3000
* `REACT_APP_SERVICE_URL` defaults to http://localhost:5000

These values may be changed. For example, setting them as follows:

```
export REACT_APP_FRONTEND_URL=https://bkw.mydomain.com
export REACT_APP_SERVICE_URL=https://bkw.mydomain.com/service
```

will indicate that the web application root page is hosted at *https://bkw.mydomain.com* and that the web
service API will be found at *https://bkw.mydomain.com/service*.  Follow the directives of your particular OS
to ensure that these environment variables are persistently visible whenever you start up the application.

Alternately, if you don't want to export environment variables, you can edit [frontend/.env](frontend/.env). Setting environment variables will overwrite what is in this `.env` file.

You can confirm your project settings at anytime by the following:

```
make project_settings
```

## Configuring the System

The following _make_ target configures the build environment (as necessary) and installs the project library
dependencies into that environment:

```
make install
```

## Running the Workbench

### Configuration of Data

The system depends on a local cache of core data which must be downloaded first before running the system, as follows:

```
make data
```

### Back End Data and Analysis Service

After configuring the system and downloading the core data, the following command runs the back end data service as a background process.

```
make service
```

After which it is accessible by default at the URL http://127.0.0.1:5000/).
The log stored in  ```logs/service_<datestamp>.log```.

Once running, REST URL's can access the data, e.g. perform a keyword search for MONDO identifiers:

[http://localhost:5000/api/disease/uteri%20cancer?size=10](http://localhost:5000/api/disease/uteri%20cancer?size=10)

The service can also return several other data types:

```
http://localhost:5000/api/disease-to-gene/MONDO:0009401
http://localhost:5000/api/gene-to-pathway/HGNC:406
http://localhost:5000/api/pathway-to-sbgn/R-HSA-389661
http://localhost:5000/api/pathway-to-png/R-HSA-389661
```

### Front End Web Application

The following command runs the front end web application as a background process
at the local URL http://127.0.0.1:3000/ (with error log stored in  ```logs/web_<datestamp>.log```)

```
make web
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
in a file the /etc/nginx/sites-available/bkw (you may need to use 'sudo' to create this file. It is ok to
leave it owned by 'root').  

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

       # Points to the React node.js web application
       location / {
            proxy_set_header X-Forwarded-Host        $host;
            proxy_set_header X-Forwarded-Server      $host;
            proxy_set_header X-Forwarded-For         $proxy_add_x_forwarded_for;

            proxy_pass http://localhost:3000/;               
       }

       # OPTIONAL: points to the web services on the Python Flask back end
       # A "sample" set of services is posted on the default index.html page
       location /service/ {
            proxy_set_header X-Forwarded-Host        $host;
            proxy_set_header X-Forwarded-Server      $host;
            proxy_set_header X-Forwarded-For         $proxy_add_x_forwarded_for;

            proxy_pass http://localhost:5000/;               
       }
}

```

Note that the NGINX Location /service/ configuration is optional and
resolves to a page of sample backend web service API calls:

```
API workflow example:
http://localhost:5000/api/disease/diabetes mellitus
http://localhost:5000/api/disease-to-gene/MONDO:0009401
http://localhost:5000/api/gene-to-pathway/HGNC:406
http://localhost:5000/api/pathway-to-sbgn/R-HSA-389661
http://localhost:5000/api/pathway-to-png/R-HSA-389661
```

for which you need to change 'localhost:5000' to your actual hostname, namely, something like:

```
http://bkw.mydomain.com/service/api/disease/diabetes%20mellitus
```

Once you have created the above NGINX configuration file in sites-available, symlink it into 'sites-enabled':

```
cd /etc/nginx/sites-enabled
ln -s ../sites-available/bkw bkw

# Sanity check: make sure NGINX can read it without error
sudo nginx -t
```

then restart the nginx daemon process:

```
sudo systemctl restart nginx
```

Note that after making this change to the default hostname, you need to ensure that the *BKW_BASE_URL* and
*BKW_API_PATH* environment variables are reset accordingly (see above).

## Adding HTTPS (SSL) Service

The 'Certbot' tool maybe used to apply HTTPS to a running NGINX HTTP-enabled web site
(see https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx). The software may be installed as follows:

```
sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot python-certbot-nginx
```

After installing the software, it may be run (assuming that we've already set up the NGINX, as described above):

```
sudo certbot --nginx
```
