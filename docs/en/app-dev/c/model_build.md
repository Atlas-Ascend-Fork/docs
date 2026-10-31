# Model Compilation

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:38:52.996Z pushedAt=2026-10-26T03:10:39.437Z nl=2 -->

Log in to the development environment as the running user. Use the ATC tool to compile a network model from an open-source framework (such as ONNX or TensorFlow) into an \*.om model file.

The following uses ONNX model conversion as an example to provide a command example. The user who executes the command must have read and write permissions on the relevant paths in the command.

```bash
atc --model=$HOME/module/resnet50*.onnx --framework=5 --output=$HOME/module/out/onnx_resnet50 --soc_version=<soc_version>
```

The parameters are described as follows. For details about the value ranges and constraints, see [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

- **--model**: path of the model file of the ResNet-50 network.
- **--framework**: type of the original framework. **5** indicates ONNX.
- **--output**: path of the **resnet50.om** model file. Note that you need to record the path where the OM model file is saved, because it will be used in subsequent application development.
- **--soc\_version**: version of the AI processor. Replace **_<soc\_version\>_** with the actual value.

**Note:**

<!-- npu="950,A3,910b,910,310p,310b" id1 -->
- If the model conversion reports unsupported operators, develop the custom operators by referring to [Ascend C Operator Development Guide](https://gitcode.com/cann/asc-devkit/blob/9.2.0/docs/zh/guide/index.md) first, and then recompile the model.
<!-- end id1 -->
- If the model conversion reports operator compilation issues but the error message is insufficient to locate the problem and you need to contact technical support (you can obtain the logs and click [here](https://www.hiascend.com/support) to contact technical support), set the **DUMP\_GE\_GRAPH** and **DUMP\_GRAPH\_LEVEL** environment variables, and then convert the model again to collect the graph description information of each stage during model conversion. For details about the environment variables and graph description information, see "References \> Dump Graph Details" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).
