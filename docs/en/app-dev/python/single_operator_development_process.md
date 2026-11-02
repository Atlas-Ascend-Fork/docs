# Development Process

**Figure 1** Development process
![](figures/development-workflow.png)

1. Prepare the environment.

    For details, see [Environment Setup](environment_preparation.md).

2. Create code directories.

    Before developing an app, you must create directories to store code files, scripts, test images, and model files.

3. Prepare operators.

    Generate operator .om files with ATC.

    Construct single-operator description files in \*.json format (describing the inputs, outputs, and attributes of the operators), use ATC to compile the single-operator description files into .om files, and call the pyACL APIs to load the .om files and execute the operators.

    For details about ATC, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).

4. Develop an application.

    For the single-operator API call sequence, see [API Calling Process](single_operator_interface_calling_process.md) and related sample code.

5. Run the app. For details, see [App Debugging](app_debug.md).
