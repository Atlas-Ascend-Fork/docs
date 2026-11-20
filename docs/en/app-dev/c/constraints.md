# Constraints

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:38:33.653Z pushedAt=2026-10-21T06:26:10.317Z nl=2 -->

## About Low Power Consumption

Before the system enters sleep mode, ensure that no AI inference, media data processing, or other related services are delivered, or exit the service processes. After the system wakes up successfully, continue to deliver services or restart the service processes.

## About Processes

- The use of the fork function and functions that encapsulate fork (such as system and posix_spawnp) to create multiple child processes, and the scenario of calling ACL APIs in a process, are not supported. Otherwise, errors or hangs may occur when the process runs.
<!-- npu="910" id7 -->
- For Atlas training products, in a physical machine scenario, a device can support at most 64 user processes, and a host can support at most (number of devices × 64) processes. In a virtual machine scenario, a device can support at most 32 user processes, and a host can support at most (number of devices × 32) processes.
<!-- end id7 -->
<!-- npu="310p" id6 -->
- For Atlas inference products, in a physical machine scenario, a device can support at most 64 user processes, and a host can support at most (number of devices × 64) processes. In a virtual machine scenario, a device can support at most 32 user processes, and a host can support at most (number of devices × 32) processes.
<!-- end id6 -->
<!-- npu="310b" id5 -->
- For Atlas 200I/500 A2 inference products, a device can support at most 64 user processes, and a host can support at most (number of devices × 64) processes.
<!-- end id5 -->
<!-- npu="910b" id4 -->
- For Atlas A2 training products/Atlas A2 inference products, a device can support at most 63 user processes, and a host can support at most (number of devices × 63) processes.
<!-- end id4 -->
<!-- npu="A3" id3 -->
- For Atlas A3 training products/Atlas A3 inference products, a device can support at most 63 user processes, and a host can support at most (number of devices × 63) processes.
<!-- end id3 -->
<!-- npu="950" id2 -->
- For Ascend 950PR/Ascend 950DT, a device can support at most 64 user processes, and a host can support at most (number of devices × 64) processes.
<!-- end id2 -->

## About Creation and Destruction APIs

- For creation APIs (for example, **aclrtCreateStream**, **aclrtCreateEvent**, and **aclCreateDataBuffer**), after a user calls such an API to create the corresponding resource and finishes using the resource, it is recommended that the user promptly call the corresponding destruction API (for example, **aclrtDestroyStream**, **aclrtDestroyEvent**, and **aclDestroyDataBuffer**). Otherwise, the program may run abnormally.
- For destruction APIs (for example, **aclrtDestroyStream**, **aclrtDestroyEvent**, **aclrtFree**, and **aclDestroyDataBuffer**), after a user calls such an API, the user cannot continue to use the released or destroyed resource. It is recommended that the user set the related resource to an invalid value (for example, **NULL**) after calling the destruction API.

## About Memory

<!-- npu="310p" id8 -->
- When developing applications on Atlas inference products, avoid having multiple operations write data to the same memory address, as this may cause hardware exceptions.
<!-- end id8 -->
- Do not use fork or functions that encapsulate fork, such as system and posix_spawnp, during asynchronous memory operations such as **aclrtMemcpyAsync** and **aclrtMemsetAsync**. Otherwise, runtime errors or even unpredictable errors such as process hangs may occur.
- After allocating memory using a memory allocation API (for example, **aclrtMalloc**), to ensure that the memory does not contain dirty data, you are advised to call **aclrtMemset** or **aclrtMemsetAsync** to clear the memory before using it, for example, **aclrtMemset(devBufferPtr, devBufferSize, 0, devBufferSize)**.
  <!-- npu="310p" id9 -->
- In Ascend RC mode, if an application involves memory allocation APIs such as **aclrtMalloc**, **acldvppMalloc**, and **hi_mpi_dvpp_malloc**, when the application runs on the device, by default it may hang and wait for memory resources when memory is insufficient. You can choose to enable certain configurations provided by the operating system (for example, **enable_oom_killer**) based on actual requirements, so that when memory is insufficient, the application exits automatically instead of waiting indefinitely. To enable **enable_oom_killer**, log in to the device and, as the **root** user, enable **enable_oom_killer** in the **/proc/sys/vm** directory. The following is an example command, where **1** indicates enabled and **0** indicates disabled:

  ```bash
  echo 1 > enable_oom_killer
  ```
  <!-- end id9 -->

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
## Application Migration from an Earlier AI Processor Version to a Newer AI Processor Version

You must reconvert the model and recompile the application on the migrated AI processor version. Otherwise, the application may run abnormally.
<!-- end id1 -->
