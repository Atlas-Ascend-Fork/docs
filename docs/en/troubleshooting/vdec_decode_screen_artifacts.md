# Artifacts During VDEC Video Decoding

<!-- md-trans-meta sourceCommit=93775688b9e6e932bf0c768a8472e27a5b4f80b8 translatedAt=2026-10-16T07:10:01.008Z pushedAt=2026-10-23T08:38:06.151Z nl=2 -->

## Symptom

When the input stream is decoded by VDEC, the obtained decoded data is incorrect, causing artifacts, as shown in Figure 1. The log contains information similar to "decode error", "input stream error, can't decode, report to user", "num\_ref\_idx\_l0\_active\(30\) out of range\(0,16\)", "dvpp\_vdec\_vdm\_process failed", and "Chan 0 ErrRatio = 44".

**Figure 1** Video artifacts
![](figures/video_artifacts.png "Video artifacts")

## Possible Cause

Some frame data in the input stream is incomplete or there are bad frames, causing artifacts during hardware decoding.

## Solution

To rectify the fault, perform the following steps:

1. Check the input source stream.

    Use a third-party tool (for example, **eseye_u**) to decode and play the input stream and check whether artifacts occur. If artifacts do not occur, go to step 2. If artifacts occur, replace the input stream.

2. If the source stream is normal, the stream may be damaged when being transmitted to VDEC on the device. In this case, store the stream transmitted to VDEC by using  **fwrite**  before sending the stream.
    - Use a third-party tool to check the stored stream. If the stream is abnormal, check whether a stream has been sent.

    - Decode the stored stream by using the sample of the corresponding version to check whether the verification stream is normal or whether VDEC supports the format.

        If the sample decodes the stream normally, the issue lies in the code logic of your development. You can refer to the "Dedicated Accelerator \> Media Data Processing (DVPP) \> Media Data Processing V1 \> VDEC Video Decoding" or "Dedicated Accelerator \> Media Data Processing (DVPP) \> Media Data Processing V2 \> VDEC Video Decoding" section in [Application Development](../app-dev/c/00_acl_cpp_dev.md) to optimize the code logic.
