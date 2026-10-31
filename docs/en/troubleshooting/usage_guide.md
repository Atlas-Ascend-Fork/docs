# Usage

<!-- md-trans-meta sourceCommit=9a4145a6f4dafa0b548a7e069df6bb09fd46f1ab translatedAt=2026-10-16T07:09:29.759Z pushedAt=2026-10-23T08:38:06.152Z nl=2 -->

An error code is represented as a 6-character string, for example, **E10035**, where:

- **The first character indicates the level**, which can be **E** (error), **W** (warning), or **I** (information).
- **The second character indicates the module**:
    - 1: GE
    - 2: FE
    - 3: AI CPU
    - 4: TE Fusion
    - 7: Vector operator plugin
    - 8: Vector operator
    - B: TBE Pass compilation tool
    - C: Auto Tune
    - D: RLTune
    - E: Runtime
    - F: LxFusion&AutoDeploy
    - G: AOE
    - H: ACL
    - I: HCCL
    - J: HCCP
    - K: Profiling
    - L: Driver
    - M: Queue scheduling
    - N: DVPP
    - O: AMCT
    - P: Dump
    - Z: Common operator error codes and operator API execution error codes (for example, aclnn operator APIs)

- **The remaining 4 characters indicate the error code.** 0000 to 8999 are user errors, and 9000 to 9999 are internal error codes.

Because scenarios, use cases, and fault causes differ, the printed error code information varies. Therefore, in this document, the **\[%s\]** variable is used to replace the actual printed logs, and the actual logs replaced by **\[%s\]** are subject to the screen output. For example, the **E10035** error code information is represented in the manual as follows:

The \[--dynamic\_batch\_size\], \[--dynamic\_image\_size\], or \[--dynamic\_dims\] argument has \[%s\] profiles, which is less than the minimum \[%s\].

The following shows an example of the actual error reported on the user interface, where the **\[%s\]** variable is replaced with the actual information:

The \[--dynamic\_batch\_size\], \[--dynamic\_image\_size\], or \[--dynamic\_dims\] argument has \[_1_\] profiles, which is less than the minimum \[_2_\].

>**Note:**
>
>- In asynchronous task execution scenarios, for example, when multiple operator execution tasks are submitted consecutively, multiple operators may report errors, and the error information may contain errors from multiple operators. You need to start troubleshooting from the first operator that reports an error.
>- Generally, **E\*9\*\*\*** indicates an internal error code of the system. For internal error codes, contact technical support for troubleshooting. You can obtain the logs and then click [here](https://www.hiascend.com/support) to contact technical support.
>- The error code information described in this document is fully displayed when an error is reported on the screen, including possible causes and solutions. Therefore, the related content is listed here only for reference.
