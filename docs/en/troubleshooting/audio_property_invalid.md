# Invalid Audio Playing Attribute Settings

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:04:53.640Z pushedAt=2026-10-23T08:38:06.141Z nl=2 -->

## Application Scenario

- Service scenario: audio playing
- Applicable processors: Atlas 200I/500 A2 inference products
- Processor forms: EP and RC

## Symptom

The audio playing parameters fail to be initialized, and the error code  **0xa0168003**  or  **0xa016800c**  is returned.

```bash
sample_comm_audio_start_ao: hi_mpi_ao_set_pub_attr(2) failed with 0xa0168003!
```

## Possible Cause

The parameters related to audio playing are incorrectly set.

## Solution

1. Check whether the values of the input parameters (such as the bit width, sampling rate, and number of audio channels) of the Audio API fall within their respective valid value ranges. If the values are not within the value ranges, change them to corresponding ranges.
2. Run the audio playing command again.
