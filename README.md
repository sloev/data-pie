data-pie
========

puredata + raspberry pi + pots and ports


a python launcher lets the user choose a patch htrough rotating a wheel.
pots lets the user change variables in the pure data patch
audio out / in lets the standalone box function as effect or source

Libpd and python on Raspberry pi
--------------------------------
This tutorial assumes you are running raspbian on your pi
and that you have your pi connected to the internets

To get libpd working on raspberry pi:
Dont install pure-data or pd-extended beforehand. 
Libpd comes with included pure-data vanilla which it prefers.

In your ssh session with your pi go to home directory.
Clone the libpd git repo:
'''$ git clone https://github.com/libpd/libpd'''
cd into the directory of libpd
'''$ make'''
wait for 5 to 10 minutes
done

Install python stuff to be able to run libpd python examples:
'''$ sudo apt-get install python-dev python-pyaudio'''
cd into the python examples directory 
'''$ make 
$ make install'''
run python example with included pd patch
'''$ python test.py'''