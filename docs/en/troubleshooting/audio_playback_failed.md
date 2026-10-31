# Abnormal Audio Playing

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:04:53.739Z pushedAt=2026-10-23T08:38:06.140Z nl=2 -->

## Application Scenario

- Service scenario: audio playing
- Applicable processors: Atlas 200I/500 A2 inference products
- Processor forms: EP and RC

## Symptom

The audio cannot be played normally, and the error code  **0xa0168009**  is returned.

```bash
sample_comm_audio_start_ao: hi_mpi_ao_set_pub_attr(2) failed with 0xa0168009!
```

## Possible Cause

The audio-related KO file is not inserted.

## Solution

1. Run the  **lsmod**  command to check whether the KO file is inserted.
2. Run the following command to re-insert the AO-related  KO file:

    ```bash
    insmod /var/davinci/driver/drv_ao.ko
    ```

3. Run the audio playing command again.
