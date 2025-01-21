#!/bin/bash

VENV="venv"
APP="src/app.py"

# Colored log statuses for console outputs 
# Bold and Red color
ERROR="\033[1;31mERROR:\033[0m"
# Bold and Blue color
INFO="\033[1;34mINFO: \033[0m"
# Bold and yellow
WARN="\033[1;33mWARN: \033[0m"



DASH_LINE="----------------------------------------------------"
TITL_LINE="             HIKING APP"
ERRR_LINE=" STARTING THE APP FAILED. PLEASE REVIEW CONSOLE OUTPUT FOR DETAILS"
INFO_LINE="             SHUTTING DOWN"
TITL="$DASH_LINE\n$TITL_LINE\n$DASH_LINE"
FIN_ERROR="$DASH_LINE\n$ERRR_LINE\n$DASH_LINE"
FIN_INFO="$DASH_LINE\n$INFO_LINE\n$DASH_LINE"


# Verify that virtual env exists
verify_venv() {
    source $VENV/bin/activate
    # -z: see "help test"
    # $VIRTUAL_ENV: python env variable set when venv is activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo -e "$ERROR Virtual environment not found. Aborting. Have you installed the application?"
        echo -e "$FIN_ERROR"
        exit 1
    else
        echo -e "$INFO Virtual env activated. Proceeding..."
    fi
}


# Run application either with debug disabled or enabled
run_app() {
    if [[ -n $1 && "$1" == "debug" ]]; then
        echo -e "$INFO Running flask in debug mode"
        flask --app $APP --debug run
    else
        echo -e "$INFO Running flask with debug mode off"
        echo -e "$INFO Hint: add argument 'debug' after script to activate debug mode"
        flask --app $APP run
    fi
}


echo -e "$TITL"

# Call functions. Note that the first positional argument is passed to the function.
verify_venv
run_app $1


# deactivate venv (not necessary as script runs in sub shell. Just a precaution.)
deactivate

echo -e "\n $FIN_INFO"