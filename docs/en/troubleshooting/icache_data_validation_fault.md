# icache Data Verification Fault

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:08:53.640Z pushedAt=2026-10-23T08:38:06.149Z nl=2 -->

## Symptom

The event log (**slog/dev-os-_id_/run/event/event\_\*.log**) of the device contains the **event\_id=0x80C98000** keyword.

<!-- npu="910b" id1 -->
On Atlas A2 products, the trace log (stored in the **$HOME/ascend/atrace/** directory by default) contains the **stars\_print\_error\_pc\_icache\_and\_hbm\_info** error keyword. *YYYY-MM-DD-HH:MM:SS.fff.uuu* (*year-month-day-hour:minute:second.millisecond.microsecond*) indicates the time when the log is output.

```bash
2024-04-22-09-06-17/hisi_logs/device-2/******/log/ts.log:5177:[ERROR] TSCH(-1,null):YYYY‑MM‑DD‑HH:MM:SS.fff.uuu 35906 (dieid:0,cpuid:0) aicore.c:767 stars_print_error_pc_icache_and_hbm_info: stat for dump pc start, aiv_id=47, icache_miss_num=8161, hbm_miss_num=0, compare_num=32, compare_fail_num=0
```
<!-- end id1 -->

<!-- npu="310p" id2 -->
On Atlas inference products, the trace log (stored in the **$HOME/ascend/atrace/** directory by default) contains the **check\_error\_pc\_icache\_and\_hbm\_info** error keyword. *YYYY-MM-DD-HH:MM:SS.fff.uuu* (*year-month-day-hour:minute:second.millisecond.microsecond*) indicates the time when the log is output.

```bash
[ERROR] TSCH(-1,null):YYYY‑MM‑DD‑HH:MM:SS.fff.uuu 438 (dieid:0,cpuid:0) aicore_icache_plat.c:848 check_error_pc_icache_and_hbm_info: stat for dump pc start, aic_id=1, icache_miss_num=8176, hbm_miss_num=0, compare_num=17, compare_fail_num=0  
```
<!-- end id2 -->

## Root Cause

At the error keyword, check the **compare\_fail\_num** print information. If the **compare\_fail\_num** value is not **0**, an iCache memory bit-flip hardware fault exists.

## Procedure

Click [Health Management Error Definition](https://support.huawei.com/enterprise/en/ascend-computing/ascend-hdk-pid-252764743) to obtain the manual of the corresponding version. The iCache memory bit-flip fault is described as follows (some key fields are listed):

|  |  |
| --- | --- |
| Event ID | 0x80C98000 |
| Fault event name | AI Core instruction data verification failed. |
| Fault description/possible cause | The iCache data is inconsistent with the GM verification. Possible causes include:<br><br>  1. iCache data bit flip.<br>  2. GM data is overwritten. |
| Fault impact | The current AI task fails. If the AI Core does not recover, subsequent AI tasks also fail. |
| Fault self-processing mode | 1. TSFW reports the fault to fault management through TSDrv.<br>  2. TSFW records the error log.<br>  3. TSFW returns task failure through the service plane.<br>  4. TSFW resets the AIC. If the reset succeeds, TSFW reports recovery through TSDrv. If the reset fails, TSFW performs core isolation (after the core is isolated, service scheduling no longer uses this core) and records the error log. |
| System processing suggestion | 1. It is recommended that the AI training task exit and be re-executed, or the inference request be re-initiated.<br>  2. If the AI task still fails after re-execution, it is recommended to reset the SoC. If the fault persists, it is recommended to return the device to the factory for repair. |
