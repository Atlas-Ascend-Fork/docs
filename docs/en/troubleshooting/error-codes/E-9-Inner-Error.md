# E\*9\*\*\* Internal error

E\*9\*\*\* indicates an internal system error code. Troubleshoot the issue based on the error information. If the issue persists, collect the logs and click [Link](https://www.hiascend.com/support) to provide feedback.

The error format for internal error codes is as follows:

```text
ErrorCode[PID: xxxxxx] DateTimeMS ErrorMessage [FUNC:FuncName][FILE:FileName][LINE:LineNumber]
```

In the preceding error format, ErrorCode indicates the error code, DateTimeMS indicates the timestamp, ErrorMessage indicates the specific error message, FuncName indicates the name of the function that reports the error, FileName indicates the name of the file that reports the error, and LineNumber indicates the line number that reports the error. The following example shows the error report for internal error code EE9999:

```text
EE9999[PID: 2545712] 2026-03-24-21:23:19:464:314 (EE9999): Failed to obtain the kernel address based on the kernel name, kernel_name=RunCpuKernel, retCode=0x0711000E. [FUNC:StreamLaunchCpuKernel][FILE:aicpu_stars.cc][LINE:224]
```
