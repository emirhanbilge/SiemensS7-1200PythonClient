#!/bin/bash


echo "Ebb Simple Snap-7 Requirements Installation"
echo " Python installation starting .."
sudo apt-get install python3.6
echo "Python installed version 3.6 , If you use snap-7 , you have"
echo " to python version 3.6+ version"
sudo apt-get update
sudo apt-get upgrade
echo "snap-7 repository adapted"
sudo apt-get repository ppa:gijzelaar/snap7
sudo apt-get update
echo "library , dll installation "
sudo apt-get install libsnap7-1 libsnap-dev
echo "pip configuration starting ..."
sudo apt-get install python3-pip
echo "python snap7 modules installation start"
python3 pip install python-snap7
echo "successfully"