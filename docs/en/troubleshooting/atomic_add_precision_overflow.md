# Atomic Add Precision Overflow

<!-- md-trans-meta sourceCommit=93775688b9e6e932bf0c768a8472e27a5b4f80b8 translatedAt=2026-10-16T07:04:58.850Z pushedAt=2026-10-23T08:38:06.142Z nl=2 -->

## Analysis Result

If **info.txt** provides the following conclusion, the AI Core error is caused by precision overflow.

```text
Analysis result: success.
"**********************Root cause conclusion******************"
Atomic add has a precision overflow. Check the operator precision.Note that if tasks are concurrently executed on the NPU, a false warning may be reported.
```

In the device slog log (**report/\*/slog/dev-os-_id_/\[run|debug\]/device-os/device-os\_\*.log**), check whether the **Vm fault failed** keyword appears. If it does not appear, the AI Core error is caused by atomic precision overflow. If it appears, the error is caused by out-of-bounds memory access rather than atomic precision overflow. The following is an example of the slog log, where *YYYY‑MM‑DD‑HH:MM:SS.fff.uuu* (year‑month‑day‑hour:minute:second.millisecond.microsecond) indicates the log output time.

```bash
[EVENT] KERNEL(4128,sklogd):YYYY‑MM‑DD‑HH:MM:SS.fff.uuu [klogd.c:253][2572550.901383] [ascend] [ERROR] [devmm] [devmm_svm_device_fault 438] <kworker/u16:186:9871,9871> Vm fault failed. (hostpid=1885445; devid=0; vfid=0; ret=64; fault_addr=0x1240f1fa0000; start=0x1240f1fa0000)
```

<!-- npu="910b" id1 -->
On Atlas A2 products, due to hardware optimization, atomic add precision overflow does not occur.
<!-- end id1 -->

## Root Cause

This issue occurs because, during operator computation, extreme data encounters an atomic add instruction. If overflow occurs during the atomic add operation, error 0x800000 is reported.

## Solution

This type of issue is generally caused by incorrect input data and should be further located through precision tuning. For example, in an inference scenario, refer to the "Model Inference > Precision/Performance Optimization" section in [Application Development](../app-dev/c/00_acl_cpp_dev.md) to tune the precision.
