# Environment Variables Automatically Configured After Installation

<!-- md-trans-meta sourceCommit=c14717642ba24270f72de4d02bcb447c5802b043 translatedAt=2026-10-16T07:28:03.327Z pushedAt=2026-10-20T07:59:38.328Z nl=2 -->

This section describes the basic environment variables related to program compilation and execution that are configured by default through the **set_env.sh** script after the CANN software installation is complete, as well as the environment variables related to the installation packages that need to be manually configured during subsequent program compilation and execution.

After the CANN software installation is complete, the basic environment variables required for program compilation and execution are automatically configured by default. However, these environment variables become invalid after the user process ends. You can also configure them with one click by using the following environment variable scripts.

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
```bash
# Example of environment variable configuration for installation as the root user:
# When installing the Toolkit package
source /usr/local/Ascend/cann/set_env.sh
# When installing the ATB acceleration library of the NNAL package
source /usr/local/Ascend/nnal/atb/set_env.sh
# When installing the SiP acceleration library of the NNAL package
source /usr/local/Ascend/nnal/asdsip/set_env.sh
```

```bash
# Example of environment variable configuration for installation as a non-root user:
# When installing the Toolkit
source ${HOME}/Ascend/cann/set_env.sh
# When installing the ATB acceleration library of the NNAL package
source ${HOME}/Ascend/nnal/atb/set_env.sh
# When installing the SiP acceleration library of the NNAL package
source ${HOME}/Ascend/nnal/asdsip/set_env.sh
```
<!-- end id1 -->
<!-- @ref: docs/res/zh/env-vars/install_res.md#id1 -->

Users can also set permanent environment variables by modifying the **\~/.bashrc** file. The procedure is as follows:

1. As the running user, run the **vi \~/.bashrc** command in any directory to open the **.bashrc** file, and add the preceding content after the last line of the file.
2. Run the **:wq!** command to save the file and exit.
3. Run the source **\~/.bashrc** command to make the settings take effect immediately.

<!-- npu="950,A3,910b,910,310p,310b" id3 -->
## Environment Variable Description

See the following for detailed descriptions of the environment variables.

- **Toolkit**
  - **PATH**: executable file search path.
  - **LD_LIBRARY_PATH**: dynamic library search path.
  - **PYTHONPATH**: Python search path.
  - **ASCEND_OPP_PATH**: root directory of the operator library.
  - **ASCEND_AICPU_PATH**: installation path of the AI CPU component.
  - **TOOLCHAIN_HOME**: installation path of the toolchain.
  - **ASCEND_HOME_PATH**: same as **ASCEND_TOOLKIT_HOME**, representing the storage path of files after Toolkit software installation.
  - **ASCEND_TOOLKIT_HOME**: storage path of files after the Toolkit software package is installed.
  - **CMAKE_PREFIX_PATH**: built-in environment variable of CMake, used to specify the path of CMake library configuration files for retrieval by commands such as **find_package ()**.

- **ATB acceleration library in the Neural Network Acceleration Library (NNAL)**
  - **ATB_HOME_PATH**: storage path of files after the ATB software package is installed.
  - **LD_LIBRARY_PATH**: list of search paths for loading dynamic libraries in the Linux system.
  - **PATH**: adds the path of the **bin** directory of the ATB software package to the system environment variable **PATH**. The default path is recommended.
  - **ATB_STREAM_SYNC_EVERY_KERNEL_ENABLE**: used to locate problems and determine the kernel where an error occurs. When this variable is set to **1**, stream synchronization is performed when the execution of each kernel ends.
  - **ATB_STREAM_SYNC_EVERY_RUNNER_ENABLE**: used to locate problems and determine the runner where an error occurs. When this variable is set to **1**, stream synchronization is performed when each runner is executed.
  - **ATB_STREAM_SYNC_EVERY_OPERATION_ENABLE**: used to locate problems and determine the operation where an error occurs. When this variable is set to **1**, synchronization is performed when each operation is executed.
  - **ATB_OPSRUNNER_KERNEL_CACHE_LOCAL_COUNT**: number of slots in the local kernelCache.
    - When the number of slots increases: the cache hit rate increases, but the retrieval efficiency decreases.
    - When the number of slots decreases: the retrieval efficiency improves, but the cache hit rate decreases.
  - **ATB_OPSRUNNER_KERNEL_CACHE_GLOBAL_COUNT**: number of slots in the global kernelCache.
    - When the number of slots increases: the cache hit rate increases, but the retrieval efficiency decreases.
    - When the number of slots decreases: the retrieval efficiency improves, but the cache hit rate decreases.
  - **ATB_WORKSPACE_MEM_ALLOC_ALG_TYPE**: selects the workspace memory allocation algorithm. Depending on the environment variable configuration, ATB selects different algorithms to calculate the workspace size and workspace allocation. Users can test the workspace allocation by selecting different algorithms.
  - **ATB_COMPARE_TILING_EVERY_KERNEL**: after each kernel runs, compares whether the tiling content on the NPU changes before and after the run. It is generally used to check whether tiling memory corruption occurs.
  - **ATB_SHARE_MEMORY_NAME_SUFFIX**: shared memory naming suffix. When multiple users use communication operators simultaneously, this value must be set to distinguish the shared memory.
  - **ATB_MATMUL_SHUFFLE_K_ENABLE**: enables Shuffle-K. The accumulation order at different positions of the result matrix in matrix multiplication is consistent/inconsistent. It affects the internal accumulation order of the matmul operator.
  - **LCCL_DETERMINISTIC**: whether the LCCL deterministic AllReduce (order-preserving addition) is enabled. Note that the enabled function takes effect only when **rankSize<=8**. After it is enabled, the following impacts occur:
    - Affects the performance of some communication operators.
    - Affects the accumulation order of LCCL communication operators.
  - **LCCL_PARALLEL**: This function cannot be enabled together with deterministic computation. **LCCL_DETERMINISTIC** must be set to **0** or **false**.
    - After the multi-communicator parallel function is used, **LCCL_PARALLEL** must be set back to **false**. Otherwise, the performance of basic scenarios will degrade. Modification during running is not supported.
    <!-- npu="910b" id2 -->
    - This environment variable can be used only in the AllReduce multi-thread concurrent scenario, and supports only the Atlas A2 products with 8 devices and a data size of less than 100 MB.
    <!-- end id2 -->

- **SiP acceleration library in the Neural Network Acceleration Library (NNAL)**
  - **ASDSIP_HOME_PATH**: storage path of files after the SiP software package is installed.
  - **LD_LIBRARY_PATH**: list of search paths for loading dynamic libraries in the Linux system.

<!-- end id3 -->
