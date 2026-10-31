# No Camera Found

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:05:46.374Z pushedAt=2026-10-23T08:38:06.143Z nl=2 -->

## Application Scenario

- Service scenario: camera image output

- Applicable processors: Atlas 200I/500 A2 inference products
- Processor forms: EP and RC

## Symptom

The message  "open ISP device error!"  is displayed. The error code  **0xa01c8040**  is returned.

## Possible Cause

The ISP KO file is not inserted.

## Solution

1. Run the  **lsmod**  command to check whether the KO file is inserted.
2. Run the following command to re-insert the AO-related  KO file:

    ```bash
    insmod /var/davinci/driver/drv_isp.ko
    ```

3. Perform the camera service again.
