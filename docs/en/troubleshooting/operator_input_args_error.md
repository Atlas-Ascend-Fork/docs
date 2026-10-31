# Operator Input args Error

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:09:07.051Z pushedAt=2026-10-23T08:38:06.150Z nl=2 -->

## Symptom

The following error is reported in the host application logs (**log/\[run|debug\]/plog/plog-_pid_\_\*.log**), where *YYYY-MM-DD-HH:MM:SS.fff.uuu* (*year-month-day-hour:minute:second.millisecond.microsecond*) indicates the time when the log is output.

```bash
[ERROR] RUNTIME(85483,python):YYYY‑MM‑DD‑HH:MM:SS.fff.uuu [task_info.cc:1678]85658 PrintErrorInfoForDavinciTask:Aicore kernel execute failed, device_id=0, stream_id=2, report_stream_id=2, task_id=57783, flip_num=3, fault kernel_name=RealDiv_ee98c6628030785f610b924ab1557b31_high_precision_210000000, fault kernel info ext=none, program id=9, hash=10612039229658031084.
[ERROR] RUNTIME(85483,python):YYYY‑MM‑DD‑HH:MM:SS.fff.uuu [task_info.cc:1617]85658 GetArgsInfo:[AIC_INFO] args(0 to 9) after execute:0x4f453840, 0x124201ea7400, 0x12420240cc00, 0x1241c006dc28, 0x124100011000, 0x1, 0x1, 0x1, 0,  
```

## Root Cause

In the error information in the plog log, the **args\(_xxxx_\) after execute** log is critical. Check whether the parameter address at **args after execute** is reasonable. If **0** appears, it can be determined that the error is caused by incorrect address allocation.

<!-- npu="910" id1 -->
On Atlas training products, addresses start with **0x1240**. If an address that does not start with **0x1240** appears, it may be abnormal and needs to be checked. In the preceding error log, on Atlas training products, the information at **args after execute** includes **0x4f453840**, **0x124201ea7400**, **0x12420240cc00**, and **0x1241c006dc28**. The first parameter **0x4f453840** does not start with **0x1240**. It is suspected that this parameter address is a host memory address instead of a device memory address, causing the AI Core to read it incorrectly.
<!-- end id1 -->

<!-- npu="910b" id2 -->
On Atlas A2 products, addresses do not start with **0x1240**. If an address that starts with **0x1240** appears, it may be abnormal and needs to be checked.
<!-- end id2 -->

## Solution

Check the training script. For the places where division is used (for example, where **cpu\_tensor/npu\_tensor** is used), because **cpu\_tensor** is a host memory address while **npu\_tensor** is a device memory address, this causes incorrect reads by the AI Core. Change both to device memory addresses.
