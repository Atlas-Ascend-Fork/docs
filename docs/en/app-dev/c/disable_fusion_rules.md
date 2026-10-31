# Disabling Fusion Rules

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:29:29.213Z pushedAt=2026-10-26T03:10:39.419Z nl=2 -->

If you do not specify to disable fusion rules during model conversion, fusion rules are enabled by default. Enabling fusion rules improves computing efficiency and performance, but operators may be fused with each other. Some fused operators may have scenarios that are not considered in their implementation, which affects accuracy. Therefore, when an accuracy issue occurs, you can try disabling fusion rules.

If the accuracy meets the requirement after fusion rules are disabled, you still need to identify the problematic operator and report it to technical support for further analysis and resolution. After the operator issue is resolved, you are advised to keep fusion rules enabled. You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.

1. When using the ATC tool to convert a model, add the advanced parameter **--fusion\_switch\_file**.

    The following is an example of using the parameter:

    ```bash
    --fusion_switch_file=$HOME/module/fusion_switch.cfg
    ```

    The configuration file is named, for example, **_fusion\_switch.cfg_**. The following is a sample configuration file. Upload the configured **_fusion\_switch.cfg_** file to any directory on the server where the ATC tool is located:

    ```json
    {
        "Switch":{
            "GraphFusion":{
                "ALL":"off"
            },
            "UBFusion":{
                "ALL":"off"
             }
        }
    }
    ```

    For details about this parameter, see "Command Line Options \> Advanced Options \> Model Tuning Options \> --fusion\_switch\_file" in [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).

2. Use the converted OM model to perform inference again.

>**Note:** 
>Before contacting technical support, set the **DUMP\_GE\_GRAPH** and **DUMP\_GRAPH\_LEVEL** environment variables, convert the model again, and print the graph description information of each stage during model conversion. For details about the environment variables and graph description information, see "References \> Dump Graph Details" in *Ascend Tensor Compiler (ATC)*.
