#!/bin/bash

# Create a virtual environment and install the required packages into it.
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install -r /io/requirements.txt

# Copy the required packages into somewhere to deploy
mkdir python
cp -r venv/lib/python3.6/site-packages/camelot python/.
cp -r venv/lib/python3.6/site-packages/chardet python/.
cp -r venv/lib/python3.6/site-packages/dateutil python/.
cp -r venv/lib/python3.6/site-packages/et_xmlfile python/.
cp -r venv/lib/python3.6/site-packages/openpyxl python/.
cp -r venv/lib/python3.6/site-packages/pdfminer python/.
cp -r venv/lib/python3.6/site-packages/PyPDF2 python/.
cp -r venv/lib/python3.6/site-packages/pytz python/.
cp -r venv/lib/python3.6/site-packages/sortedcontainers python/.
cp -r venv/lib/python3.6/site-packages/six.py python/.
cp -r venv/lib/python3.6/site-packages/jdcal.py python/.
cp -r venv/lib64/python3.6/site-packages/click python/.
cp -r venv/lib64/python3.6/site-packages/Crypto python/.
cp -r venv/lib64/python3.6/site-packages/cv2 python/.
cp -r venv/lib64/python3.6/site-packages/fitz python/.
cp -r venv/lib64/python3.6/site-packages/numpy python/.
cp -r venv/lib64/python3.6/site-packages/pandas python/.

# Delete the superfluous pycache stuff
python3 -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python3 -c "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

# Zip it all up into a layer
zip -r /io/layer.zip python

