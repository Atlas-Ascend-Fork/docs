# Configuring the Precision Mode

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:28:23.238Z pushedAt=2026-10-26T03:10:39.417Z nl=2 -->

If the precision mode of the network model or operators is not specified during mode conversion, the fp16 (float16) data type is used for computation by default.

After the model high-precision mode is configured, inference precision can be improved, but inference performance may be affected. If you need to maintain performance while meeting the precision requirement, you can configure some operators to retain the data types in the original network.

## Configuring the High-Precision Mode for the Network Model

1. When converting a model using the ATC tool, add the advanced parameter **--precision\_mode** to specify the precision mode.

    The parameter is set as follows, indicating that if an operator in the network model supports fp32 (float32), fp32 is used; if the operator does not support fp32, fp16 (float16) is used.

    ```bash
    --precision_mode=allow_fp32_to_fp16
    ```

    For details about this parameter, see "Command Line Options \> Advanced Options \> Operator Tuning Options \> --precision\_mode" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

2. Perform inference again using the converted OM model.

## Configuring Some Operators to Retain the Data Types in the Original Network

1. When converting a model using the ATC tool, add the advanced parameter **--keep\_dtype** (specifies that some operators retain the original data types of the network during computation) and **--precision\_mode** (specifies the precision mode of the network model).

    The following is an example of using the parameters:

    ```bash
    --keep_dtype=$HOME/exceptionlist.cfg --precision_mode=force_fp16
    ```

    The configuration file is named **_exceptionlist.cfg_**, for example. The following is a sample configuration file. Each line in the file is the name of an operator. Upload the configured **_exceptionlist.cfg_** file to any directory on the server where the ATC tool is located:

    ```text
    Opname1 
    Opname2 
    …
    ```

    For details about this parameter, see "Command Line Options \> Advanced Options \> Operator Tuning Options \> --keep\_dtype" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

2. Perform inference again using the converted OM model.
