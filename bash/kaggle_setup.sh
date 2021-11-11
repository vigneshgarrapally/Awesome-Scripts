#!/bin/bash
error_handler() {
  echo "******* FAILED *******" 1>&2
  echo "Make sure kaggle.json is in the present directory and install kaggle module using pip install kaggle"
  echo "Open script and uncomment to debug"
  exit 1
}
trap error_handler ERR
pip install --upgrade --force-reinstall --no-deps kaggle
mkdir -p ~/.kaggle
#echo "directory created"
cp kaggle.json ~/.kaggle/
#echo "copied"
chmod 600 ~/.kaggle/kaggle.json
#echo "permissions has been setup"
echo "Kaggle Setup has been done"
echo "Download datasets using Kaggle API command"
echo "e.g 'kaggle competitions download -c plant-pathology-2020-fgvc7'"
