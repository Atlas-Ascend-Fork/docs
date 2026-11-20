# Disabling Data Cache Optimization

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:40:47.585Z pushedAt=2026-10-21T06:32:12.797Z nl=2 -->

If you do not disable data cache optimization during model conversion, it is enabled by default. Enabling data cache optimization improves computing efficiency and performance. However, some operators may not cover all scenarios in their implementation, which affects precision. Therefore, you can try disabling data cache optimization when precision issues occur.

If the precision meets the requirement after data cache optimization is disabled, you still need to identify the problematic operator and report it to technical support for further analysis and resolution. (You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.) After the operator issue is resolved, you are advised to keep data cache optimization enabled.

1. When using the ATC tool to convert a model, add the advanced parameter **--buffer\_optimize** to disable data cache optimization.

    The parameter is set as follows:

    ```bash
    --buffer_optimize=off_optimize
    ```

    For details about this parameter, see "Command Line Options \> Advanced Options \> Model Tuning Options \> --buffer\_optimize" in [Ascend Tensor Compiler (ATC)](https://hiascend.com/document/redirect/cannCommunityATC).

2. Perform inference again using the converted OM model.

>**Note:** 
>Before contacting technical support, set the **DUMP\_GE\_GRAPH** and **DUMP\_GRAPH\_LEVEL** environment variables, convert the model again, and print the graph description information of each stage during model conversion. For details about the environment variables and graph description information, see "References \> Dump Graph Details" in the *Ascend Tensor Compiler (ATC)*.
