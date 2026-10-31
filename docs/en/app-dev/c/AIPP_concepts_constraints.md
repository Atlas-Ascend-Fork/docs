# Concepts and Usage Constraints

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:26:00.941Z pushedAt=2026-10-26T03:10:39.412Z nl=2 -->

## What Is AIPP

Artificial Intelligence Pre-Processing (AIPP) is used to perform image pre-processing on the AI Core, including color space conversion (converting the image format), image normalization (mean subtraction/coefficient multiplication), and cropping (specifying the cropping start point to crop the image to the size required by the neural network).

AIPP is classified into static AIPP and dynamic AIPP. You can use either static AIPP or dynamic AIPP to process images. You cannot configure both static AIPP and dynamic AIPP at the same time.

- Static AIPP: During model conversion, set the AIPP mode to static and configure the AIPP parameters. After the model is generated, the AIPP parameter values are saved in the offline model (\*.om file). Fixed AIPP pre-processing parameters (which cannot be modified) are used in each model inference process.

    If static AIPP is used, the same AIPP parameters are shared by all batches in the multi-batch scenario.

- Dynamic AIPP: During model conversion, set the AIPP mode to dynamic. Before each model inference, set the dynamic AIPP parameter values as required before executing the model, so that different AIPP parameters can be used during model execution.

    If dynamic AIPP is used, different AIPP parameters can be used for different batches in the multi-batch scenario.

## Constraints

- **When dynamic AIPP and dynamic batch are used together**:
    - When calling the **aclmdlCreateAIPP** API to set **batchSize**, set **batchSize** to the maximum batch size.
    - For the data node in the model that requires dynamic AIPP processing, the corresponding input memory size must be allocated based on the maximum batch size.

- **When dynamic AIPP and dynamic resolution are used together**:
    - If cropping, scaling, or padding is enabled when setting dynamic AIPP parameters, dynamic AIPP cannot be used together with dynamic resolution.
    - If cropping, scaling, or padding is not enabled when setting dynamic AIPP parameters, and dynamic AIPP is used together with dynamic resolution, ensure that the width and height set through the **aclmdlSetAIPPSrcImageSize** API are equal to those set through the **aclmdlSetDynamicHWSize** API. Both should be set to the width and height of the maximum dynamic resolution level used during model conversion.
    - For the data node in the model that requires dynamic AIPP processing, the corresponding input memory size must be allocated based on the maximum resolution (width and height).

- **When dynamic AIPP and dynamic shape input (with a shape range set) are used together**, the width and height of the output image of dynamic AIPP must fall within the set shape range.
- For the same model, AIPP (including static AIPP and dynamic AIPP) cannot be used together with dynamic dimensions (ND format).
- In addition to AIPP, there are ACL APIs for media data processing based on the Digital Vision Pre-Processing (DVPP) hardware, including scaling, cropping, format conversion, image encoding/decoding, and video encoding/decoding. These APIs provide richer functions than AIPP, but impose certain constraints on input/output images and memory.

    For details about the media data processing APIs based on DVPP, see [DVPP Media Acceleration Library](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/dvpp/dvpp_03_0000.html).
