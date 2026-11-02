# Model Building

It is not yet supported to directly run networks trained under open-source frameworks (such as Caffe and TensorFlow) on the AI processor. ATC is provided to convert such a network into an AI processor-adapted offline model (\*.om file).

The following uses the ResNet-50 network under the ONNX framework as an example to describe how to use ATC to convert a model. For details, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).

1. Log in to the development environment as the running user.
2. Convert the model.

    Run the following command to convert the original model into a *.om model that can be identified by the AI processor. Note that the running user must have the read and write permissions on the related files specified in the command. Replace `<SAMPLE_DIR>` in the following command with the actual directory where the sample package is stored. Replace "<soc\_version\>" with the actual AI processor version.

    ```bash
    cd <SAMPLE_DIR>/MyFirstApp_ONNX/model
    wget https://obs-9be7.obs.cn-east-2.myhuaweicloud.com/003_Atc_Models/resnet50/resnet50.onnx
    atc --model=resnet50.onnx --framework=5 --output=resnet50 --input_shape="actual_input_1:1,3,224,224"  --soc_version=<soc_version>
    ```

    Parameters are listed below. For details about the constraints, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).

    - --`model`: path of the ResNet-50 model file.
    - --`framework`: source framework type. `5` indicates ONNX.
    - --`output`: path of the `resnet50.om` model file. Record this path for future use during app development.
    - --`input_shape`: input shape.
    - --`soc_version`: specifies the Ascend AI Processor version.

        >[!NOTE]
        >If you cannot determine the `soc_version` of the current device, perform the following steps:
        >- For the following products: Run the `npu-smi info` command on the server where the AI processor is installed to obtain the `Name` information. The actual configuration value is AscendName. For example, if the value of `Name` is `_xxxyy_`, the actual configuration value is `Ascend_xxxyy_`.
        > Atlas A2 products
        > Atlas 200I/500 A2 inference products
        > Atlas inference products
        > Atlas training products
        >- For Atlas A3 products, run the `npu-smi info -t board -i id -c chip_id` command on the server where the AI processor is installed to obtain the chip name and NPU name. The actual value is represented by `Chip name_NPU name`. For example, if the chip name is `Ascendxxx` and the NPU name is `1234`, the actual value is `Ascendxxx_1234`. Where:
            >- `id`: Device ID, namely the NPU ID queried by the `npu-smi info -l` command.
            >- `chip_id`: chip ID, which is the same as the chip ID obtained by running the `npu-smi info -m` command.
            >- For Ascend 950PR/950DT products, run the `npu-smi info -t board -i id` command on the server where the AI processor is installed to obtain the chip name and NPU name. The actual value is represented by `Chip name_NPU name`. For example, if the chip name is `Ascendxxx` and the NPU name is `1234`, the actual value is `Ascendxxx_1234`.
            > id indicates the device ID, which is the NPU ID obtained by running the npu-smi info -l command.

>[!NOTE]
>
>- During model conversion, if a message is displayed indicating that some operators are not supported, develop custom operators first by referring to [Ascend C Operator Development Guide](https://hiascend.com/en/document/redirect/CannCommunityOpdevAscendC), and then convert the model again.
>- During model conversion, if a message is displayed, indicating that an operator compilation error occurs, but the message cannot help you locate the error, contact technical support. (After obtaining the logs, click [here](https://www.hiascend.com/support) to contact technical support.) You need to set the `DUMP_GE_GRAPH`and `DUMP_GRAPH_LEVEL`environment variables, convert your model again, and collect graphs in each phase during model conversion. For details about the environment variables and dump graphs, see "See Also > Dump Graph Details" in [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).
>- For details about the building and inference of models with a dynamic input shape, see [Model Inference with Dynamic-Shape Inputs](dynamic_shape_model_inference.md).
>- If the existing network does not meet your requirements, you can use the operators supported by the AI processor and call the graph construction API to build your own network, and then compile the network into an .om offline model file. For details, see *Graph Development*.
