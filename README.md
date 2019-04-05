# Biomedical Knowledge Workbench

## Getting Started

It is recommended that you have Python release 3.6.* or higher installed on your system, accessible by the application.

A Unix-style _Makefile_ is provided to configure and run the workbench web application.

### Configuration

It is recommended to install the Biomedical Workbench within a 
[Python "Virtual Environment"](https://docs.python.org/3/tutorial/venv.html). 
If not provided within your development environment (some IDE's like PyCharm can provide one), 
the following _make_ target can be run once to create one (this target only runs with Python 3.6 or better)


``` 
make venv
```

will create the virtual environment in  'venv' by default (see below for build customization)


### Installation

The following _make_ target installs the system dependencies:

```
make install
```

### Running the Workbench

The following command runs the workbench at the local URL http://127.0.0.1:5000/:


```
make run
```

###  Customizing the Build

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
