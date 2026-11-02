# Basic Principles

## Synchronization Mechanism

The following synchronization mechanisms are supported:

- `acl.rt.synchronize_event` waits for an event to complete.
- `acl.rt.synchronize_stream` waits until all tasks in the given stream are completed.
- `acl.rt.stream_wait_event` blocks the execution of a specified stream until the specified event is completed. It allows multiple streams to wait on the same event. For details about the API call sequence, see [Synchronous Wait of Tasks Between Streams (Implemented Using Events)](synchronous_waiting_Implemented_via_Event.md).
- `acl.rt.synchronize_device` waits until the device has completed all requested tasks. If there are multiple devices, this API is called to wait for the device corresponding to the current context.
