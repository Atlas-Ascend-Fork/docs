# Development Process

**Figure 1** Development process
![](figures/development-workflow-2.png)

1. Set up the development environment and operating environment.
2. Create code directories.

    Before developing an app, you must create directories to store code files, test images, and model files. The following is an example:

    ```text
    ├App name
    ├── caffe_model      # Directory of the configuration file and model file for model conversion
    │   ├── xxx.cfg
    │   ├── xxx.prototxt
    ├── data
    │   ├── xxx.jpg     # Test data
    │
    ├── model
    │   ├── xxx.om      # Model file generated after conversion
    │
    ├── xxx.py           # Python script
    ├── xxx.py
    ```

3. Develop an application.
    1. Perform initialization. For details, see [Initialization and Deinitialization](initialization_and_deinitialization.md).

        Before using the pyACL API to develop an application, you must call `acl.init` to initialize the application. Otherwise, errors may occur during the initialization of internal system resources, causing exceptions in other services.

    2. Allocate runtime resources. For details, see [Runtime Resource Allocation and Deallocation](runtime_resource_allocation_and_release.md).
    3. Data transfer:
    4. Perform model inference. For details, see [Model Management](model_management.md).

        After the model inference is complete, destroy the allocations.

        Perform data postprocessing as required. For example, for an image classification app, identify the class indexes with the highest confidence values in data postprocessing.

    5. After all data is processed, release runtime resources in a timely manner. For details, see [Runtime Resource Allocation and Deallocation](runtime_resource_allocation_and_release.md).
    6. Perform deinitialization. For details, see [Initialization and Deinitialization](initialization_and_deinitialization.md).

4. Run the app, including model conversion and application script execution. For details, see [App Debugging](app_debug.md).
