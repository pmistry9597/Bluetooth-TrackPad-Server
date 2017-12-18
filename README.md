# Bluetooth TrackPad Server
This is a Python script that allows for an Android device to control a pc that has the Bluetooth TrackPad App installed.
You can find that app on my GitHub and it's called Bluetooth-TrackPad-App. It listens for connections on and keeps listening so
a new client can connect afterwards without script restart.
The only commands it can send is cursor movement and mouse button clicks.

It requires the PyBluez and PyAutoGUI modules. It also requires admin permissions. I overcame this by making a batch script
that calls this file and running that file as Administrator (right click on the batch it and click run as administrator).

If connection fails, you need to restart the script to start listening for connections again.

I may add scrolling and button clicks through the actual trackpad in the app. I might make a GUI version using C++ to make it 
more user-friendly and snappier.

Example batch script to run the Bluetooth Server with administrator permissions (you'll have to tweak it to your environment):
@echo off <br />
cd [YOUR DIRECTORY WITH THE SCRIPT] <br />
C:\Python35\python.exe trackPadServer.py <br />

