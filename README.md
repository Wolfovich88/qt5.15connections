# qt5.15connections
connections_qt5_15_2.py changes old QML signal handlers syntax in the Connections items to qt5.15 syntax. 
Connections { onSignalName: { do somethink } } to Connections { function signalName() {do somethink}}
Warning: the script doesn't add signal parameters to function args. You must add parameters as signalName(....) arguments manually.
