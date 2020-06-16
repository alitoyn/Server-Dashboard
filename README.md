# Server-Dashboard

Python program showing stats from connected servers - currently tested on servers running Ubuntu 18.04 LTS

Utilises ssh keys to connect so no need to store passwords!

**Current Functionality:**

* Server uptime, users logged in, load averages
* Root storage capacity + an additional storage location
* F@H user stats and server status
* display last line from user added log files (show backup status etc)
* Show available updates (Ubuntu only)
* Open new terminal window with ssh connection to a selected server
* Setup Program to build config file
* Send commands to servers

**Upcoming Functionality:**

* Network and CPU load graphs
* More details on the F@H stats page
* Password lock application
* Use application to install dependencies on connected servers
* CPU Temp readouts