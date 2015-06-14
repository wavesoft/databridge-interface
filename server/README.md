
# Databridge Synchronization Script

This script is designed to be a drop-in replacement for co-pilot setups when smimple file-based queue is used. It operates on two folders: an `input` folder from which job files are picked and placed on databridge, and an `output`, where the job outputs are stored.

The script is meant to run periodically, usually via a cron job. Upon execution, it will try to download as many job results as possible from the databridge server and then push a configurable number of new job descriptions in the queue.

## Input an Output format

If you are using the `databridge-agent` as your databridge agent, you will need to conform with it's requirements regarding the format of the input and output job files.

The input job __MUST__ be an executable file, that being a binary application or a shell script. The actual executable bit is not required to be set in the file itself. This file will be executed by the agent and is the bootstrap to your real job.  

It's recommended to store only the job metadata in the input file and provide the application binaries and libraries through CVMFS. If your data change too frequently, you could also use DataBridge itself for storing your dependencies.

## Configuration

The default location of databridge server configuration is `/etc/databridge/server.conf`, however this can be override from the command-line. 

The mandatory configuration parameters that you will have to tune are the following:

```bash
# [DATABRIDGE_INPUT_DIR] 
#
# Specify the directory from which to read the job files and
# place them on DataBridge queue.
#
DATABRIDGE_INPUT_DIR="/opt/databridge/input"

# [DATABRIDGE_OUTPUT_DIR] 
#
# Specify the directory where to place the output files that
# come from the DataBridge queue.
#
DATABRIDGE_OUTPUT_DIR="/opt/databridge/output"

# [DATABRIDGE_BASE_URL]
#
# The base URL from which the Queue and DynFed input/output queues
# are derrived.
#
DATABRIDGE_BASE_URL="https://t4t-data-bridge.cern.ch"
```

### SSL Certificates

In order to connect to the Databridge instance you will need an HTTP client certificate. You can specify the location of your certificate and private key through the following parameters:

```bash
# [DATABRIDGE_SSL_CERT] 
#
# Path to the client SSL certificate to use for authentication
# to the DataBridge queue.
#
DATABRIDGE_SSL_CERT="/etc/databridge/keys/client-cert.pem"

# [DATABRIDGE_SSL_KEY] 
#
# Path to the client SSL private key to use for authentication
# to the DataBridge queue.
#
DATABRIDGE_SSL_KEY="/etc/databridge/keys/client-key.pem"
```

### Limits and rates

Depending on how frequently you will be running the synchronization script, you will need to tune the following parameters:

```bash
# [DATABRIDGE_UPLOAD_BULK_SIZE] 
#
# Specify how many jobs to upload to the DataBridge on a
# single upload event.
#
DATABRIDGE_UPLOAD_BULK_SIZE=1000

# [DATABRIDGE_MAX_QUEUE_SIZE] 
#
# The maximum number of jobs (taking in account the local
# reflection of pending jobs) to keep in the queue.
#
# Set to '0' to disable this check and push excactly
# DATABRIDGE_UPLOAD_BULK_SIZE jobs on every sync.
#
DATABRIDGE_MAX_QUEUE_SIZE=1000
```

### Callbacks

In order to offer interoperability with other applications, the `databridge-server-sync` script provide a callback mechanism through external application invocation. To specify your handling application, just define the appropriate configuration parameters:

```bash
# [DATABRIDGE_CB_SCHEDULED] 
#
# An application to run as a callback when a job description
# is about to be placed in the queue.
#
# The first argument is the full path to the job input file.
# The second argument is the databridge slot unique ID.
#
DATABRIDGE_CB_SCHEDULED=""

# [DATABRIDGE_CB_COMPLETED] 
#
# An application to run as a callback to handle a file that
# was just downloaded.
#
# The first argument to the application is the full path to 
# the downloaded job output file.
# The second argument is the databridge slot unique ID.
#
DATABRIDGE_CB_COMPLETED=""
```

## License

DataBridge-Interface is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

DataBridge-Interface is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with DataBridge-Interface. If not, see http://www.gnu.org/licenses/.

Developed by Ioannis Charalampidis, 2015
