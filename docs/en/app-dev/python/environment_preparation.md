# Environment Setup

**Before developing an application, install the NPU firmware, NPU driver, and CANN software (Toolkit and ops).** For details about how to deploy the environment, see [CANN Software Installation](https://hiascend.com/en/document/redirect/CannCommunityInstSoftware).

- Deploy the development environment, and then you can obtain the dependencies required for calling APIs and run the Python code file.

    For Ascend devices, if the driver and firmware have been installed, the environment can be directly used as the operating environment to execute the Python code file that contains pyacl APIs.

    For non-Ascend devices, the Python code file containing the pyacl APIs cannot be directly executed after the development environment is deployed. After the development is complete, upload the Python code file to the Ascend device environment where the operating environment has been deployed for verification.

- The Python code file can be executed in the operating environment only after the operating environment is deployed.

## Setting the Path for Flushing Generated Files

(Optional) Use environment variables `ASCEND_CACHE_PATH` and `ASCEND_WORK_PATH` to set the flushing path of files generated during the running of the app. ATC model conversion, intelligent AOE model optimization, profile data collection, and log collection functions are involved. Knowledge base files, optimization result files, profile data files, and log files will be flushed.

The following is a configuration example. For details, see [Environment Variables](https://hiascend.com/en/document/redirect/CannCommunityEnvRef).

```bash
export ASCEND_CACHE_PATH=/repo/task001/cache
export ASCEND_WORK_PATH=/repo/task001/172.16.1.12_01_03
```

## pyACL Dependencies

- pyACL does not have the installation dependencies but has the running dependencies. For details, see [this guide](https://hiascend.com/en/document/redirect/CannCommunityInstSoftware).
- The Python version on which the `acl.so` file in the generated pyACL depends ranges from 3.7.5 to 3.13.9.

## Setting Environment Variables After the Installation

**After installing the CANN package, you must configure the environment variables. Otherwise, `import acl` cannot be used.**

<!-- npu="910b,910,310p,310b" id1 -->
If you have installed the CANN Toolkit and ops packages:

```bash
# Install the CANN packages as the root user.
. /usr/local/Ascend/cann/set_env.sh
# Install the CANN packages as a non-root user.
. ${HOME}/Ascend/cann/set_env.sh
```
<!-- end id1 -->
After setting the environment variables, add `import acl` to the Python script. Then, you can use the functions in pyacl.
