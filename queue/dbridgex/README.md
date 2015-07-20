
# DataBridge-X Queue

DataBridge-X Queue is an implementation of DataBridge that takes into account additional requirements frequently met in job queue interfaces. 

**Note**: This document and implementation even though is working is just a *proof of concept* and should be thoroughly tested before used in production.

## Description

The DataBridge-X Queue is an elaborate FIFO queue that takes into account additional requirements that some experiments might need.

## Example

In the following examples you can see in practice how to use the `dbridgex` module:

```python
from dbridgex import DataBridgeQueue, REDISStore, MJDLFactory

# Create an instance of databridge queue
queue = DataBridgeQueue(
    "name-of-the-queue",    # The ID of this queue
    REDISStore(             # The interface to the back-end key/value store
        host="localhost",
        port=6379,
        db=0
        ),
    MJDLFactory()           # The feature-matching factory instance
    )
```

DataBridgeQueue behaves like a simple FIFO queue
if no feature-matching information are specified:

```python
queue.push( 'job-id-1' )
queue.push( 'job-id-2' )
...
job = queue.pop()
```

However you can benefit from it's feature-matching internals
if you specify the feature specifications you require:

```python
queue.push( 'job-id-for-x86', { "arch": "x86" } )
queue.push( 'another-job-id-for-x86', { "arch": "x86" } )
...
job = queue.pop({ "arch": "x86_64" })
```
