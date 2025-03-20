# Hiking Tour Assistant Data Storage

Hiking Tour Assistant Data Storage is part of Hiking Band System, together with the LilyGO T-Watch Hiking application. This project provides a web application that is built to run on Raspberry Pi 3B. 

## How to get started

This project has been released together with the LilyGO T-Watch hiking application. Within the final release are documentation to help get started. 


## Requirements

The Web Application is a Python 3.x application that works on versions 3.10 and greater. The dependencies for the application can be found in [requirements.txt](./requirements.txt), 

## Installation

Installation can be done either by manual installation or by using the convenience script. 

### Option 1: Manual installation

First setup the virtual environment

```bash
python3 -m venv venv
```

Then install dependencies

```bash
pip install -r requirements.txt
```

If you add new dependencies, create an updated `requirements.txt` with the following command:
```
pip freeze > requirements.txt
```

### Option 2: Convenience script

Run the installation script with

```bash
./install.sh
```

## Running the application

The applicatin can also be run either manually or with a convenience script. 

### Option 1: Manually

To run the app use 

```bash
flask --app src/app.py run --host=0.0.0.0
```

To debug:

```bash
flask --app src/app.py --debug run
```


### Option 2: Convenience script

To run the app use 

```bash
./start-app.sh
```

To debug:

```bash
./start-app.sh debug
```
