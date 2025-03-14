# Hiking Tour Assistant Data Storage

Initial commit

## Requirements

What is required to install and run this application

## Installation

### Manual installation

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

### Convenience script

Run the installation script with

```bash
./install.sh
```

## Running the application

### Manually

To run the app use 

```bash
flask --app src/app.py run --host=0.0.0.0
```

To debug:

```bash
flask --app src/app.py --debug run
```


### Convenience script

To run the app use 

```bash
./start-app.sh
```

To debug:

```bash
./start-app.sh debug
```


TODO: Quick guide for users to get started