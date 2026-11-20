# Precision Improvement Overview

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:19:10.239Z pushedAt=2026-10-22T04:01:22.359Z nl=2 -->

This document describes the precision tuning process, related configurations, and typical cases in full-network inference scenarios. As this is a tuning process, before tuning, ensure that the full-network inference function has been debugged and verified, that the function is not blocked, and that only the inference precision is incorrect or slightly deviates from the benchmark data.

During full-network inference, incorrect or substandard inference precision may be caused by the following reasons:

- Chaining issues between the inference function and other functions: A typical case is the chained use of DVPP + AIPP + model inference. This scenario is mainly caused by incorrect parameter configuration in the APIs and incorrect AIPP configuration during model conversion.

    If DVPP, AIPP, and model inference are used in a chained manner, it is recommended that you troubleshoot these issues first. Otherwise, you can skip this step and directly troubleshoot the precision issues of the operators themselves.

- Precision issues of the operators themselves in the entire network: For such issues, you can use the precision comparison tool to obtain various types of data by following the specific issue locating process described below, and then compare and analyze the data to determine whether the issue is caused by configuration or operator implementation, and resolve the issues one by one. This chapter describes how to compare and analyze data based on specific comparison and analysis cases.

**Figure 1**  Inference precision issues  
![](figures/model_inference_precision_issues.png "Inference precision issues")

**Note:**

- In this document, "inference" is currently limited to the scenario where inference is performed using OM offline model files.
<!-- npu="950,A3,910b,910,310p,310b" id1 -->
- The operator precision issues mentioned in this document refer to the precision issues of operators in the entire network. For custom operators, if precision issues are found during running and verification, see the *Ascend C Operator Development Guide*.
<!-- end id1 -->
