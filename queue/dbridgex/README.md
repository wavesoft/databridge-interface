
# DataBridge-X Queue

DataBridge-X Queue is an implementation of DataBridge that takes into account additional requirements frequently met in job queue interfaces. 

**Note**: This document and implementation even though is working is just a *proof of concept* and should be thoroughly tested before used in production.

## Description

The DataBridge-X Queue is an elaborate FIFO queue that takes into account additional requirements that some experiments might need:

 * __Modular Storage Back-End:__ DataBridge-X provides a modular abstracting to the storage element used for keeping the queue data. In principle any key/value store can be used.
 * __Feature Matching:__ DataBridge-X offers the means to send jobs only to a particular subset of volunteers that fulfill a set of requirements. Such a feature is useful when more than one projects or project versions are using the same queue.
 * __Real-Time Notifications:__ DataBridge-X broadcasts real-time notifications to one or more target machines in order to gauge it's operation. This provides the means for responding in critical changes to the queue. 

## Usage

In the following examples you can see in practice how to use the `dbridgex` module:

```python
from dbridgex import DataBridgeQueue, REDISStore

# Create an instance of databridge queue
queue = DataBridgeQueue(
    "name-of-the-queue",    # The ID of this queue
    REDISStore(             # The interface to the back-end key/value store
        host="localhost",
        port=6379,
        db=0
        )
    )
```

The second parameter to the `DataBridgeQueue` constructor is an instance of a back-end key/value store interface, used for accessing the database. This is expected to be a subclass of `dbridgex.store.StoreBase`.

`REDISStore` is a performant back-end that comes with with DataBridge-X. It uses REDIS for it's implementation.

DataBridgeQueue behaves like a simple FIFO queue if no feature-matching is enabled. For example, you can enqueue and dequeue job IDs in the queue like this:

```python
queue.push( 'job-id-1' )
queue.push( 'job-id-2' )
...
job = queue.pop()
```

If there are no more jobs in the queue `None` is returned.

### Feature Matching

You can benefit from more powerful features if you enable feature matching. To do so, you will need to specify which feature-matching algorithm to use. 

DataBridge-X offers a reference implementation of a *Micro-Job Description Language* that matches some basic job/agent features. In order to use this, pass an instance of the `MJDLFactory` as a third parameter in the DataBridgeQueue constructor:

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

Now you define a dictionary of features each job **requires** like this:

```python
queue.push( 'job-id-for-x86', { "platform": "Linux-i386" })
queue.push( 'another-job-id-for-x86', { "platform": "Linux-i386" })
queue.push( 'job-id-for-x64', { "platform": "Linux-x86_64" })
```

MJDL Also provides priorities. A job with a higher priority is preferred when the rest of the features match. Unless specified, job priority defaults to `0`. For example:

```python
queue.push( 'priority-job-id-for-x64', { "platform": "Linux-x86_64", "priority": 1 })
```

When you pop a job, you can specify what features each entity **offers** like this:

```python
job = queue.pop({ "platform": "Linux-i386" })
print job
# Displays: 'job-id-for-x86'
```

As mentioned before, jobs with higher priority will be selected first:

```python
job = queue.pop({ "platform": "Linux-x86_64" })
print job
# Displays: 'priority-job-id-for-x64'
job = queue.pop({ "platform": "Linux-x86_64" })
print job
# Displays: 'job-id-for-x64'
```

You can implement your own job matching logic by subclassing the four base classes found in the `dbridgex.features` module: `FeatureRequirement`, `FeatureOffer`, `FeatureMatcher` and `FeatureFactory`.

The `FeatureFactory` is responsible for instancing the appropriate flavor of your classes. Check the `dbridgex.features.mjdl` for a reference implementation.

### Notifications

You can broadcast notifications via UDP messages to one or more hosts by configuring the queue accordingly:

```python
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
        <th>Description</th>
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

## API Reference

The following methods are exposed by the `DataBridgeQueue` class:

### DataBridgeQueue( `queueName`, `storeBackend`, `featureFactory=None` )

The constructor of DataBridge Queue. 

<table>
    <tr>
        <th>Argument</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    <tr>
        <th>queueName</th>
        <td><code>str</code></td>
        <td>The name of the DataBridge Queue in operation.</td>
    </tr>
    <tr>
        <th>storeBackend</th>
        <td><code>dbridgex.store.StoreBase</code></td>
        <td>An instance of <code>dbridgex.store.StoreBase</code> that will be used for accessing the storage element.</td>
    </tr>
    <tr>
        <th>featureFactory</th>
        <td><code>dbridgex.features.FeatureFactory</code></td>
        <td>An instance of <code>dbridgex.features.FeatureFactory</code> that will be used for constructing the appropriate feature-matching classes.</td>
    </tr>
</table>

### push( `jobid`, `feats=None` )

Push an job ID in the DataBridge-X queue.

<table>
    <tr>
        <th>Argument</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    <tr>
        <th>jobid</th>
        <td><code>str</code></td>
        <td>The job ID</td>
    </tr>
    <tr>
        <th>feats</th>
        <td><code>dict</code></td>
        <td>A dictionary with the <em>required</em> features this job needs in order to run.</td>
    </tr>
</table>

### pop( `feats=None` )

Fetch the next job ID from the DataBridge-X queue.

This function returns a string with the job ID pending in the queue, or `None` if there are no elements left.

<table>
    <tr>
        <th>Argument</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    <tr>
        <th>feats</th>
        <td><code>dict</code></td>
        <td>A dictionary with the <em>offered</em> features the remote entity provides.</td>
    </tr>
</table>

### config( `parm`, `value=None` )

Get or Set a persistent configuration parameter.

This function offers a simple read/write interface to queue-specific persistent parameters. These parameters are kept in the storage back-end.

If the argument `value` is missing this function will return the contents of the configuration parameter `param`. If the parameter is missing, this function will return `None`.

<table>
    <tr>
        <th>Argument</th>
        <th>Type</th>
        <th>Description</th>
    </tr>
    <tr>
        <th>param</th>
        <td><code>string</code></td>
        <td>The name of the configuration parameter to access.</td>
    </tr>
    <tr>
        <th>value</th>
        <td><code>string</code></td>
        <td>The value to store in the configuration parameter. If this argument is missing, the contents of the configuration parameter is returned.</td>
    </tr>
</table>

## License

This project is released under the GNU GPL v2 license:

>  DataBridge-X Queue Implementation
>  Copyright (C) 2014-2015  Ioannis Charalampidis, PH-SFT, CERN
> 
>  This program is free software; you can redistribute it and/or
>  modify it under the terms of the GNU General Public License
>  as published by the Free Software Foundation; either version 2
>  of the License, or (at your option) any later version.
> 
>  This program is distributed in the hope that it will be useful,
>  but WITHOUT ANY WARRANTY; without even the implied warranty of
>  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
>  GNU General Public License for more details.
> 
>  You should have received a copy of the GNU General Public License
>  along with this program; if not, write to the Free Software
>  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, SA.


