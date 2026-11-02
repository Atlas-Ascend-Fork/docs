# Constraints

- Before the system enters the hibernation mode, ensure that the running processes such as the AI inference and media data processing exit first. After the system is wakened up successfully, continue to process the services.
- Do not use the `fork` function to create multiple pyacl API caller processes, as this may lead to errors or cause processes to stop responding at runtime.
- Do not use `fork` or `fork`-encapsulated functions (such as `system` and `posix_spawnp`) for asynchronous memory manipulations (by using calls to APIs such as `acl.rt.memcpy_async` and `acl.rt.memset_async`). Doing so will result in unexpected errors at runtime and may possibly cause the process to stop responding.
- For allocation APIs (such as `acl.rt.create_stream`, `acl.rt.create_event`, and `acl.create_data_buffer`), the corresponding destruction APIs (such as `acl.rt.destroy_stream`, `acl.rt.destroy_event`, and `acl.destroy_data_buffer`) must be called to destroy the allocations in a timely manner. Otherwise, the application may not function properly.
- For destruction APIs (such as `acl.rt.destroy_stream`, `acl.rt.destroy_event`, `acl.rt.free`, and `acl.destroy_data_buffer`), the released or destroyed resources are no longer available after these APIs are called. You are advised to set the released or destroyed resources to invalid values (for example, `None`) after calling these APIs.
<!-- npu="910" id1 -->
- **Atlas training products**: For physical machines, a device supports a maximum of 64 user processes, and a host supports a maximum of 64 processes multiplied by the number of devices. For virtual machines, a device supports a maximum of 32 user processes, and a host supports a maximum of 32 processes multiplied by the number of devices.
<!-- end id1 -->
<!-- npu="310p" id2 -->
- **Atlas inference products**: For physical machines, a device supports a maximum of 64 user processes, and a host supports a maximum of 64 processes multiplied by the number of devices. For virtual machines, a device supports a maximum of 32 user processes, and a host supports a maximum of 32 processes multiplied by the number of devices.
<!-- end id2 -->
<!-- npu="310b" id3 -->
- **Atlas 200I/500 A2 inference products**: A device supports a maximum of 64 user processes, and a host supports a maximum of 64 processes multiplied by the number of devices.
<!-- end id3 -->
<!-- npu="910b" id4 -->
- **Atlas A2 products**: A device supports a maximum of 63 user processes, and a host supports a maximum of 63 processes multiplied by the number of devices.
<!-- end id4 -->
<!-- npu="A3" id5 -->
- **Atlas A3 products**: A device supports a maximum of 63 user processes, and a host supports a maximum of 63 processes multiplied by the number of devices.
<!-- end id5 -->
<!-- npu="950" id6 -->
- **Ascend 950PR/950DT products**: A device supports a maximum of 64 user processes, and a host supports a maximum of 64 processes multiplied by the number of devices.
<!-- end id6 -->
- After memory is allocated by a call to the memory allocation API (such as `acl.rt.malloc` or `acl.media.dvpp_malloc`) and before you use the allocated memory, you are advised to call `acl.rt.memset` or `acl.rt.memset_async` to initialize the memory, for example, `acl.rt.memset(dev_buffer_ptr, dev_buffer_size, 0, dev_buffer_size)`.
- In Ascend RC mode, the `acl.rt.malloc`, `acl.media.dvpp_malloc`, and `hi_mpi_dvpp_malloc` memory management APIs are called in the app logic, and the app runs on the device, the app is suspended in the event of memory insufficiency until memory is available. You can activate some configurations (for example, `enable_oom_killer`) provided by the OS as required. In this way, the app automatically exits when the memory is insufficient.

    To activate `enable_oom_killer`, log in to the device, go to the `/proc/sys/vm` directory, and set `enable_oom_killer` as the `root` user. The following is a command example, where, `1` indicates activated, and `0` indicates deactivated.

    ```python
    echo 1 > enable_oom_killer
    ```
