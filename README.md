# Biomedical Knowledge Workbench

## Getting Started

This project resides in [this Github project repository](https://github.com/STARInformatics/biomed-workbench).

First, ensure that you have the git client installed (here we assume a Debian-based Linux distribution like Ubuntu):

``` 
sudo apt update
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

A Unix-style _Makefile_ is provided to configure and run the workbench web application.

It is recommended to install the Biomedical Workbench within a 
[Python "Virtual Environment"](https://docs.python.org/3/tutorial/venv.html). 
If not provided within your development environment (some IDE's like PyCharm can provide one), 
the following _make_ target can be run once to create one (this target only runs with Python 3.6 or better)

``` 
make venv
```

will create the virtual environment in  'venv' by default (see below for build customization)


The following _make_ target installs the system dependencies:

```
make install
```

## Running the Workbench

The following command runs the workbench at the local URL http://127.0.0.1:5000/:


```
make run
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
