# How to Obtain Logs Generated During aclnn API Calls

<!-- md-trans-meta sourceCommit=fe5307907d2087c03797a673819df2784c73d1b4 translatedAt=2026-10-20T07:14:46.186Z pushedAt=2026-10-21T02:33:30.165Z nl=2 -->

During aclnn API calls, if issues such as operator execution failure or precision anomalies occur, you can extract host-side logs to assist in analysis and diagnosis. Generally, the following log information needs to be analyzed:

- Obtaining plog logs:

    After the program finishes running, the logs can be viewed under `$HOME/ascendc/log` by default. The host log file storage path is as follows:

    ```text
    $HOME/ascend/log/debug/plog/plog-pid_*.log
    ```

    Enabling the environment variable **ASCEND\_LOG\_PRINT\_TO\_STDOUT** allows logs to be printed directly to the screen (**1** indicates enabling screen printing, and **0** indicates disabling it). The configuration example is as follows:

    ```bash
    export ASCEND_LOG_PRINT_TO_STDOUT=1
    ```

    For details about logs, see [CANN Log Reference](https://hiascend.com/document/redirect/CannCommunitylogref). For details about environment variables, see [CANN Environment Variables](https://hiascend.com/document/redirect/CannCommunityEnvRef).

- Obtaining aclnn exception error information:

    Use the **aclGetRecentErrMsg** API to obtain exception information during aclnn API calls. The usage is as follows:

    ```cpp
    printf(aclGetRecentErrMsg());
    ```

    The following is an example of the printed error information:

    ```text
    [PID:646612] 2026-01-24-11:53:44.671.727 AclNN_Parameter_Error(EZ1001): Expected a proper Tensor but got null for argument addmmTensor.self.
    ```
