
# DataBridge-X Queue

DataBridge-X Queue is an implementation of DataBridge that takes into account additional requirements frequently met in job queue interfaces. 

**Note**: This document and implementation even though is working is just a *proof of concept* and should be thoroughly tested before used in production.

## Description

The DataBridge-X Queue is an elaborate FIFO queue that takes into account additional requirements that some experiments might need. The following sections explain in details the new features.

### Feature Matching

DataBridge-X offers the means to send jobs only to a particular subset of volunteers that fulfill a set of requirements. Such a feature is useful when more than one projects or project versions are using the same queue.

### Real-Time Notifications

DataBridge-X broadcasts real-time notifications to one or more target machines in order to gauge it's operation. This provides 

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

## Notifications

You can broadcast notifications via UDP messages to one or more hosts by configuring the queue accordingly:

```json
# Configure the 'notify' property, specifying a list
# of comma-separated hosts that will receive real-time
# notifications from the queue operations:
queue.config("notify", "127.0.0.1:11223,192.168.1.1:11223")
```

Each message is a JSON-Encoded object with the property `event` holding the name of the event. For example:

```javascript
{
    // The property 'event' holds the name of the event
    "event": "queue.miss",
    // Everything else are additional parmeters
    "queue": "name-of-the-queue",
    ...
}
```

The events broadcasted are the following:

<table>
    <tr>
        <th>Name</th>
        <th>Description/th>
    </tr>

    <tr>
        <th><code>queue.enqueue</code></th>
        <td>
            <p>
                This event is triggered when an item is placed in a queue bucket. The following parameters are also included:
            </p>
            <table>
                <tr>
                    <th>queue</th>
                    <td>The name of the DataBridge Queue in operation.</td>
                </tr>
                <tr>
                    <th>bucket</th>
                    <td>The ID of the bucket the job was placed.</td>
                </tr>
                <tr>
                    <th>job</th>
                    <td>The ID of the job.</td>
                </tr>
                <tr>
                    <th>size</th>
                    <td>The size of the bucket after the item was enqueued.</td>
                </tr>
            </table>
        </td>
    </tr>

    <tr>
        <th><code>queue.dequeue</code></th>
        <td>
            <p>
                This event is triggered when an item is removed from a queue bucket. The following parameters are also included:
            </p>
            <table>
                <tr>
                    <th>queue</th>
                    <td>The name of the DataBridge Queue in operation.</td>
                </tr>
                <tr>
                    <th>bucket</th>
                    <td>The ID of the bucket the job was placed.</td>
                </tr>
                <tr>
                    <th>job</th>
                    <td>The ID of the job.</td>
                </tr>
                <tr>
                    <th>size</th>
                    <td>The size of the bucket after the item was dequeued.</td>
                </tr>
            </table>
        </td>
    </tr>

    <tr>
        <th><code>queue.empty</code></th>
        <td>
            <p>
                This event is triggered only once when a queue bucket is emptied. The following parameters are also included:
            </p>
            <table>
                <tr>
                    <th>queue</th>
                    <td>The name of the DataBridge Queue in operation.</td>
                </tr>
                <tr>
                    <th>bucket</th>
                    <td>The ID of the bucket the job was placed.</td>
                </tr>
            </table>
        </td>
    </tr>

    <tr>
        <th><code>queue.miss</code></th>
        <td>
            <p>
                This event is triggered when an entity tries to fetch an item from an empty queue. The following parameters are also included:
            </p>
            <table>
                <tr>
                    <th>queue</th>
                    <td>The name of the DataBridge Queue in operation.</td>
                </tr>
                <tr>
                    <th>(offer)</th>
                    <td>When feature matching is enabled, this parameter contains the description of the features the entity offered. This is useful in order to identify the environment and push appropriate type of jobs.</td>
                </tr>
            </table>
        </td>
    </tr>

</table>


