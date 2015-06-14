
# Databridge Agent Script

This agent script is the agent code that runs inside the worker node that process the job requests. This script will enter an infinite loop and exit only if a black-hole effect is detected.  

## Usage

This script requires some Basic HTTP Authentication credentials in order to communicate with the DataBridge server. The username and password for the Basic-HTTP-Auth are specified as the first two command-line parameters.

Optionally, you can define the databridge URL to use as a third parameter:

```
databridge-agent "username" "password" [ "http://url/to/databridge" ]
```

## Input an Output format

If you are using the `databridge-server-sync` as your databridge server, you will need to conform with it's requirements regarding the format of the input and output job files.

The input job __MUST__ be an executable file, that being a binary application or a shell script. The actual executable bit is not required to be set in the file itself. This file will be executed by the agent and is the bootstrap to your real job.  

It's recommended to store only the job metadata in the input file and provide the application binaries and libraries through CVMFS. If your data change too frequently, you could also use DataBridge itself for storing your dependencies.

## Black-Hole Protection

The agent script protects the queue from a basic black-hole effects. Such effect can occur when the job is unable to initialise properly exits right away (or after a short delay). If left unattended, these 'fast' workers will consume the entire queue, returning junk outputs. 

The agent script requires each job to take __at least 5 minutes__. If for any reason it exits earlier, it will increase the delay for the next job exponentially. If a critical threshold is reached, the worker is considered to be in invalid state and will force a reboot.

Be aware that this, like any other client-side measures, __do NOT__ protect against malicious abuse of server resources. Therefore the Databridge end-point must also be equipped with an appropriate mechanism.

## License

DataBridge-Interface is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

DataBridge-Interface is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with DataBridge-Interface. If not, see http://www.gnu.org/licenses/.

Developed by Ioannis Charalampidis, 2015
