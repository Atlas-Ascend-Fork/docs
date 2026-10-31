# Issue Locating Process

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:41:03.739Z pushedAt=2026-10-26T03:10:39.442Z nl=2 -->

**Figure 1** Locating process  
![](figures/operator_precision_issues_positioning_process.png "Locating process")

<a id="li1678610773511"></a>

1. The inference result is incorrect. To locate the issue later, perform inference again to obtain the dump data of the model.

    To obtain the dump data of the model, call the ACL API to enable dump. For details, see the *Precision Debugging Tool*.

2. Configure the precision mode.
    1. Configure the high-precision mode of the model and then perform inference to obtain the dump data of the model. After inference, if the precision meets the standard, proceed to step [2.b](#li108141712131710); if the precision does not meet the standard, proceed to step [3](#li34501246181412).

        Performing inference after configuring the high-precision mode of the model may affect inference performance. If you need to maintain performance while the precision meets the standard, execute [2.b](#li108141712131710)\ to [2.d](#li5846847198) to configure some operators to retain the data types in the original network.

        To configure the high-precision mode of the model, see [Configuring the High-Precision Mode of a Network Model](config_precision_mode.md).
    <a id="li108141712131710"></a>
    2. Use the precision comparison tool to compare the dump data in the high-precision mode with the dump data obtained in [1](#li1678610773511).

        For details about how to use the tool, see [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html).

    3. Identify the operators with computation differences based on the comparison result in the previous step.

        Generally, identify one different operator at a time (the first operator with a low cosine similarity, for example, lower than 0.95). After the different operator is found, perform inference and obtain dump data during inference. Then compare the dump data with that in the high-precision mode to find the next different operator.

        Repeat this step until no different operator exists.
    <a id="li5846847198"></a>
    4. For the operators with differences, configure this part of operators to retain the data types in the original network, and then perform inference again.

        For details about how to configure the high-precision mode for some operators, see [Configuring Some Operators to Retain Data Types in the Original Network](config_precision_mode.md).
<a id="li34501246181412"></a>
3. Disable data cache optimization.
    1. After restoring the original precision mode of the model, disable data cache optimization and perform inference. If the precision meets the standard, go to step [3.b](#li168541437153611). If the precision does not meet the standard, go to step [4](#li2215195581410).

        Data cache optimization is enabled by default. Enabling data cache optimization improves computation efficiency and performance. However, some operators may have scenarios that are not considered in their implementation, which affects precision. Therefore, when a precision issue occurs, you can try to disable data cache optimization. If the precision meets the standard after data cache optimization is disabled, you still need to identify the problematic operator and then contact technical support for further analysis and resolution. After the operator issue is resolved, you are advised to keep data cache optimization enabled. You can obtain logs and click [here](https://www.hiascend.com/support) to contact technical support.

        For details about how to disable data cache optimization, see [Disabling Data Cache Optimization](disable_data_cache_optimization.md).
    <a id="li168541437153611"></a>
    2. Use the precision comparison tool to compare the dump data obtained after disabling the data cache optimization function with the dump data obtained in [1](#li1678610773511).

        For details about how to use the tool, see [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html).

    3. Identify the operators with computation differences based on the comparison result in the previous step.
    4. Contact technical support and provide the operators with differences for further analysis. You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.
<a id="li2215195581410"></a>
4. Disable the fusion rule function.
    1. Re-enable the data cache optimization function, disable the fusion rule function, and then perform inference. If the precision meets the standard, proceed to step [4.b](#li1649922517388). If the precision does not meet the standard, proceed to step [5](#li295816232513).

        Fusion rules are enabled by default. Enabling fusion rules improves computation efficiency and performance, but operators may be fused with each other. Some fused operators may have scenarios that are not considered in their implementation, which affects precision. Therefore, when a precision issue occurs, you can try to disable fusion rules. If the precision meets the standard after the fusion rule function is disabled, you still need to identify the problematic operators and report them to technical support for further analysis and resolution. After the operator issues are resolved, it is recommended that you keep the fusion rule function enabled. You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.

        For details about how to disable the fusion rule function, see [Disabling Fusion Rules](disable_fusion_rules.md). Disabling certain fusion rules may cause functional issues. Therefore, after fusion rules are configured to be disabled, the system disables only some fusion rules without affecting functions, rather than all fusion rules.
    <a id="li1649922517388"></a>
    2. Use the precision comparison tool to compare the dump data obtained after disabling fusion rules with the dump data obtained in [1](#li1678610773511).

        For details about how to use the tool, see [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html).

    3. Based on the comparison result in the previous step, identify the operators with computation differences.
    4. Contact technical support and provide the operators with differences for further analysis. You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.
<a id="li295816232513"></a>
5. Check data processing or configuration.

    Inference precision not meeting the standard may be caused by differences in the dataset, AIPP, or post-processing method. You need to troubleshoot these factors step by step. After re-enabling the fusion rule function, check data processing or configuration. For details, see [Checking Data Processing or Configuration](check_configuration.md).

    If there is a problem with the data processing logic or data configuration, modify it and perform inference again. If there is no problem with the data processing logic or data configuration, proceed to step 6.

6. Compare with benchmark computation data.
    1. Use the precision comparison tool to compare the dump data of the model with the dump data of the benchmark network.

        For details about how to use the tool, see [Precision Debugging Tool](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/devaids/ModelAccuracyAnalyzer/atlasaccuracy_16_0001.html).

    2. Based on the comparison results from the previous step, identify the operators with computation differences.
    3. Contact technical support and provide the operators with differences for further analysis. You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.
