#!/bin/bash

# Initializes Python virtual environment
# for use in AI experiments.

# Activate module venv and install Python3.11 in directory ~/software/python/venv3.11
# The intent is to run Jupiter notebooks for AI stuff and Jypiter;
# All commands in notebooks will use the venv3.11,
#   ASSUMING the ipykernel is forced to use it - see below

PYTHON_VERSION=3.6
VENV_DIRNAME=venv${PYTHON_VERSION}-for-ai-rocm
VENV_PATH=~/software/python/${VENV_DIRNAME}
python${PYTHON_VERSION} -m venv ${VENV_PATH}
# Check that venv has python3.6
source  ${VENV_PATH}/bin/activate

# AFTER ACTIVATE, PYTHON, PYTHON3 AND PYTHON3.6 ARE THE SAME. SO JUST USE PYTHON.
#    SAME FOR PIP
# ALL BELOW IS INSTALLED AND DONE IN the venv3.6--for-ai-rocm

# Update pip, although this is optional, like AppStore update
python -m pip install --upgrade pip

# IMPORTANT: INSIDE VENV, install then run module ipykernel,
#            tell it to install itself with name ${VENV_DIRNAME}
#            The name will show in Jupiter lab as a kernel name,
#            and should be set as 'preferred kernel'.

pip install ipykernel # also install jupyter
python -m ipykernel install --user --name=${VENV_DIRNAME} # ==> Installed kernelspec in /home/mzimmermann/.local/share/jupyter/kernels/venv3.6-for-ai-rocm

# Install also jupyter-lab
pip install jupyterlab

# Deactivate and reactivate. This seems needed before Jypiter for kernel to work
deactivate
source  ${VENV_PATH}/bin/activate

echo If you want to start Jupiter lab, enter any key, otherwise Ctrl-C:

read -r

# Once in jupyter in the browser, click Kernel -> Change kernel.
# The list SHOULD SHOW KERNEL ${VENV_DIRNAME}, select it.
jupyter-lab train-bert-on-yelp-local.ipynb
