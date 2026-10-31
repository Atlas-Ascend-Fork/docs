# HDMI OPEN Failure

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:08:18.280Z pushedAt=2026-10-23T08:38:06.148Z nl=2 -->

## Application Scenario

- Service scenario: display over the HDMI
- Applicable processors: Atlas 200I/500 A2 inference products
- Processor forms: EP and RC

## Symptom

When the HDMI display is enabled, the following user-mode error indicating the HDMI OPEN failure is printed in the log:

```bash
[ERROR] DSS(4808,vo_test_nvr_hdmi_hi_test):YYYY‑MM‑DD‑HH:MM:SS.fff.uuu [mpi_hdmi_com.c:338][lib_hdmi][mpi_hdmi_com_open]:HDMI device not init
```

## Possible Cause

**hi\_mpi\_hdmi\_init**  is not called before calling  **hi\_mpi\_hdmi\_open**.

## Solution

1. Check the calling sequence of  **hi\_mpi\_hdmi\_open**  and  **hi\_mpi\_hdmi\_init**  in the test case and correct the test case.
2. Execute the HDMI display test case again.
