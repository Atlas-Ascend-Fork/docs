# App Debugging

## Application Running
<!-- npu="910,310p,310b" id1 -->
For details about how to run an application, see [Image Classification with Caffe ResNet-50 (Synchronous Inference)](https://gitee.com/ascend/samples/tree/master/python/level2_simple_inference/1_classification/resnet50_imagenet_classification).
<!-- end id1 -->
**Pay attention to the following points:**

1. For details about model conversion, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).
2. Before running an executable file, upload the directories of the initialization configuration file (`acl.json`), test image, and \*.om file to the same directory on the host.

    If no parameter is passed to the `acl.init` API during [initialization](initialization_and_deinitialization.md), you do not need to upload the directory of the initialization configuration file (`acl.json`) to the host.

3. To run the code, directly run the corresponding Python script. For example:

    ```python
    python3 main.py
    ```

## Troubleshooting

If an error occurs at application run time, obtain the log file by referring to the [Log Reference](https://hiascend.com/en/document/redirect/CannCommunitylogref) and check out the error details. Take the following steps to fix the error:

- If the error is caused by an API call sequence, adjust your API call sequence by referring to the [general restrictions](constraints.md) and the API-specific restrictions.
