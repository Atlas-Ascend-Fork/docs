# API Calling Process

If synchronization in the asynchronous scenario is involved, your app must contain the related code logic. For details about the API call sequence, see the following figure.

**Figure 1** Synchronization flowchart in the callback scenario
![](figures/synchronization-flowchart-in-the-callback-scenario.png)

The key APIs are described as follows:

1. Create a callback function in advance to obtain and process the model inference or operator execution result.
2. Create a thread and customize a thread function in advance. Once `acl.rt.process_report` is called in the thread function to set the timeout interval, `acl.rt.launch_callback` will deliver a callback task after a specified period of time.
3. Call `acl.rt.subscribe_report` to specify the thread for processing the callback function in the stream. This thread must be consistent with that in the previous step.
4. Call `acl.mdl.execute_async` for asynchronous inference.

    Also call `acl.rt.synchronize_stream` to wait for the stream tasks to complete.

    You can obtain the asynchronous inference results of all images at once after the `acl.rt.synchronize_stream` call. However, if the image data volume is large, the wait time could be long. In this case, you can deliver a callback task at a specified interval to obtain the asynchronous inference result of the previous period.

5. Call `acl.rt.launch_callback` to deliver a callback task in the task queue of the stream. When the callback task is executed in the system, it is also executed in the thread subscribed to the stream (`acl.rt.subscribe_report`). The callback function must be the same as that in step 1.

    Each time `acl.rt.launch_callback` is called, a callback task is delivered.

6. Call `acl.rt.unsubscribe_report` to unsubscribe from a thread. (The callback function in the stream is no longer processed by the specified thread.)
