# Description

<!-- md-trans-meta sourceCommit=9a4145a6f4dafa0b548a7e069df6bb09fd46f1ab translatedAt=2026-10-16T07:07:20.556Z pushedAt=2026-10-23T08:38:06.146Z nl=2 -->

An error code consists of six characters, for example, **E10035**.

- **The first character indicates the error level**, which can be E (error), W (warning), or I (information).
- **The second character indicates the module**.
    - 1: GE
    - 2: FE
    - 3: AI CPU
    - 4: TE Fusion
    - 7: Vector operator plugins
    - 8: Vector operators
    - B: TBE Pass compilation tool
    - C: Auto Tune
    - D: RL Tune
    - E: Runtime
    - F: LxFusion and AutoDeploy
    - G: AOE
    - H: ACL
    - I: HCCL
    - J: HCCP
    - K: Profiling
    - L: Driver
    - M: queue scheduling
    - N: DVPP
    - O: AMCT
    - P: Dump
    - Z: common operator error codes and operator API execution error codes (for example, aclnn operator API error codes)

- **The remaining four characters indicate error codes**. Error codes 0000 to 8999 are user error codes, and error codes 9000 to 9999 are internal error codes.

The error code information that is printed varies according to the scenario, use case, and fault cause. In this document, \[%s\] is a variable to denote the actual log. For example, the E10035 error code in this document is displayed in the following format:

The \[--dynamic\_batch\_size\], \[--dynamic\_image\_size\], or \[--dynamic\_dims\] argument has \[%s\] profiles, which is less than the minimum \[%s\].

The following is an example of the error message displayed on the screen. The \[%s\] variable is replaced with the actual information.

The \[--dynamic\_batch\_size\], \[--dynamic\_image\_size\], or \[--dynamic\_dims\] argument has \[_1_\] profiles, which is less than the minimum \[_2_\].

>**Note:**
>
>- In asynchronous task execution scenarios, for example, when multiple operator execution tasks are issued consecutively, multiple operators may report errors, and the error information may contain errors from multiple operators. You need to start troubleshooting from the first operator that reports an error.
>- Generally, E\*9\*\*\* indicates a system internal error code. For internal error codes, contact Huawei for troubleshooting. You can obtain logs and then click [here](https://www.hiascend.com/support) to contact technical support.
>- The error code information described in this document is fully displayed when an error is reported on the screen, including possible causes and solutions. Therefore, the related content is listed here only for reference.
