# Incorrect Camera Image Output Effect

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:06:30.788Z pushedAt=2026-10-23T08:38:06.145Z nl=2 -->

## Application Scenario

- Service scenario: camera image output and dump
- Applicable processors: Atlas 200I/500 A2 inference products
- Processor forms: EP and RC

## Symptom

The image is blurred after being dumped.

## Possible Cause

Check whether the pixel format is the same as that of the image viewing tool and whether the resolution is the same.

## Solution

1. Check the pixel formats of the image and the image viewing tool. For example, if the pixel format is YUV420, select the corresponding 420 format and resolution.
2. Start the camera again after the settings are complete.
