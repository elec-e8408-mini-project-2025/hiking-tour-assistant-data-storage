#!/bin/bash

# Global variables
VENV="venv"
REQUIREMENTS="requirements.txt"
PYTHON_MINIMUM_MAJOR=3
PYTHON_MINIMUM_MINOR=10


# Colored log statuses for console outputs 
# Bold and Red color
ERROR="\033[1;31mERROR:\033[0m"
# Bold and Blue color
INFO="\033[1;34mINFO: \033[0m"
# Bold and yellow
WARN="\033[1;33mWARN: \033[0m"

# "boolean" indicating whether errors occured
ERRORS=false

DASH_LINE="----------------------------------------------------"
TITL_LINE="             HIKING APP INSTALLER"
INFO_LINE="             INSTALLATION FINISHED"
ERRR_LINE="   INSTALLATION FAILED. SEE OUTPUTS FOR DETAILS"
TITL="$DASH_LINE\n$TITL_LINE\n$DASH_LINE"
FIN_ERROR="$DASH_LINE\n$ERRR_LINE\n$DASH_LINE"
FIN_INFO="$DASH_LINE\n$INFO_LINE\n$DASH_LINE"

# Verify that python is installed and meets requirements
check_python_version() {
    # Get python version
    PYTHON_VERSION=$(python3 --version 2>&1)
    if [[ $? -ne 0 ]]; then
        echo -e "$ERROR: python3 is not installed or in PATH"
        echo "$FIN_ERROR"
        exit 1
    fi

    # Extract major and minor version
    PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info[1])")

    if [[ PYTHON_MINOR -lt 10 ]]; then
        echo -e "$ERROR Python version must be atleast $PYTHON_MINIMUM_MAJOR.$PYTHON_MINIMUM_MINOR"
        echo -e "$FIN_ERROR"
        exit 1
    fi

    echo -e "$INFO Python version validated. Using version $PYTHON_VERSION"
}


# Create virtual env if it does not yet exists in default path
create_virtual_env() {
    if [[ ! -d $VENV ]]; then
        python3 -m venv $VENV
        echo -e "$INFO Virtual environment successfully created at path $VENV"
    else
        echo -e "$WARN Virtual environment $VENV already exists. Skipping."
    fi
}

# Install depedencies from destination defined in REQUIREMENTS
install_dependencies() {    
    
    source $VENV/bin/activate

    # Verify that virtual env is active
    # -z: see "help test"
    # $VIRTUAL_ENV: python env variable set when venv is activated
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo -e "$ERROR Virtual environment is not active.Aborting"
        echo -e "$FIN_ERROR"
        exit 1
    else
        echo -e "$INFO Virtual env activated. Proceeding..."
    fi
    
    if [[ -f $REQUIREMENTS ]]; then
        echo "----------------------------------------------------"
        echo -e "$INFO Installing dependencies from $REQUIREMENTS:"
        pip install -r $REQUIREMENTS
        echo -e "$INFO Done."
        echo -e "$WARN Please check from the output that all installations were successful"
        echo "----------------------------------------------------"
    else
        echo -e "$ERROR $REQUIREMENTS was not found. Aborting."
        deactivate
        echo -e "$FIN_ERROR"
        exit 1
    fi 

    echo -e "$INFO Deactivating virtual environment. Remember to activate it before running the app"
    # Deactivate virtual env
    deactivate  

}

enable_on_startup(){
    SYSTEMD_FILE_PATH="/etc/systemd/system/web-app-hiking-watch.service"
    CURRENT_DIR="$(pwd)"
    echo "[Unit]" > "$SYSTEMD_FILE_PATH"
    echo "Description=Hiking watch web application." >> "$SYSTEMD_FILE_PATH"
    echo "" >> "$SYSTEMD_FILE_PATH"
    echo "[Service]" >> "$SYSTEMD_FILE_PATH"
    echo "Restart=on-failure"
    echo "RestartSec=10s"
    echo "WorkingDirectory=$CURRENT_DIR" >> "$SYSTEMD_FILE_PATH"
    echo "ExecStart=/usr/bin/bash $CURRENT_DIR/start-app.sh" >> "$SYSTEMD_FILE_PATH"
    echo "" >> "$SYSTEMD_FILE_PATH"
    echo "[Install]" >> "$SYSTEMD_FILE_PATH"
    echo "WantedBy=multi-user.target" >> "$SYSTEMD_FILE_PATH"

    systemctl daemon-reload
    systemctl start web-app-hiking-watch.service
    systemctl enable web-app-hiking-watch.service
}

echo -e "$TITL"

# Run functions sequentially
check_python_version
create_virtual_env
install_dependencies

echo "Should we add a service entry and enable the web application on startup? (y/n)"
read 
if [ "$REPLY" == "y" ]; then
    sudo bash -c "$(declare -f enable_on_startup); enable_on_startup"
fi

echo -e "$FIN_INFO"