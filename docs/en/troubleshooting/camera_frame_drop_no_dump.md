# No Image Dumped Due to Persistent Camera Frame Loss

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:05:46.117Z pushedAt=2026-10-23T08:38:06.143Z nl=2 -->

## Application Scenario

- Service scenario: The camera outputs images and dumps raw and YUV images at the same time.
- Applicable processors: Atlas 200I/500 A2 inference products
- Processor forms: EP and RC

## Symptom

The message "pipe  _x_  chn  _x_  get buffer fail,hi\_size  _xxxx_" is repeatedly printed on the screen.

## Possible Cause

The allocated pipe depth is less than or equal to the dump raw depth. As a result, no extra buffer is sent to the backend **chn**.

## Solution

1. Check the number of depths and modify related attributes to ensure that the value of  **pipe depth + chn attr depth - dump\_attr depth**  is greater than 0.
2. Start the camera again.
