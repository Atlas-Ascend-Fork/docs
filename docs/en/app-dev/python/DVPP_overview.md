# Basics About Media Data Processing

This section describes the specific functions, API calling processes, and sample code of image/video data processing.

## Typical Functions

CANN provides **AIPP-** and **DVPP-based** image/video data processing modes. This section focuses on DVPP-based image/video data processing.

| Approach| Description|
|---------|------|
| Artificial Intelligence Pre-Processing (AIPP)| AIPP implements functions on the AI Core, including image resizing (such as cropping and padding), CSC, mean subtraction, and factor multiplication (for pixel changing).<br>AIPP supports static and dynamic modes. However, the two modes are mutually exclusive.<br>Static AIPP: During model conversion, set the AIPP mode to static and set the AIPP parameters. After the model is generated, the AIPP parameter values are saved in the offline model (.om). The same AIPP parameter configurations are used in each model inference phase. If the static AIPP mode is used, multiple batches share the same AIPP parameters. The AIPP parameter values are set when the ATC tool is used for model conversion. For details about the tool, see [Ascend Tensor Compiler (ATC)](https://hiascend.com/en/document/redirect/cannCommunityATC).<br>Dynamic AIPP: During model conversion, specify the AIPP mode to dynamic, and set different sets of dynamic AIPP parameters as required. In this way, different sets of parameters can be used for model inference. Dynamic AIPP allows multiple batches to use different sets of AIPP parameters. You can call pyACL APIs to set these parameters. For details, see [Dynamic AIPP Model Inference](dynamic_AIPP_inference.md).|
| Digital Vision Pre-Processing (DVPP)| As an embedded image processing unit of an AI Processor, DVPP provides powerful hardware acceleration capabilities for media processing through media data processing APIs. It delivers the following functions:<br>Vision Preprocessing Core (**VPC**): Processes YUV and RGB images, including resizing, cropping, and CSC.<br>JPEG Decoder (**JPEGD**): Decodes images from JPEG to YUV.<br>JPEG Encoder (**JPEGE**): Encodes images from YUV to JPEG.<br>Video Decoder (**VDEC**): Decodes video streams from H.264/H.265 to YUV/RGB.<br>Video Encoder (**VENC**): Encodes video streams from YUV420SP to H.264/H.265.<br>PNG Decoder (**PNGD**): Decodes images from PNG to RGB.<br>AIPP and DVPP can be used separately or together. In combined applications, DVPP is used first to decode, crop, and resize images or videos. However, due to DVPP hardware restrictions, the image format and resolution after DVPP may not meet the model requirements. Therefore, AIPP is required to further perform color space conversion (CSC), image cropping, and border making.|

## Typical Scenarios

The resolution and format of the source image or video can be processed to meet the model requirements. The following is an **example of a typical scenario**.

- **Video decoding and resizing**

    The input video is in H.264/H.265 encoding format and the resolution is 1920 x 1080. However, the YOLOv3 model for object detection requires an RGB or YUV input image with the resolution of 416 x 416. In this case, you can process the video as follows.

    **Figure 1** Video decoding and resizing
    ![](figures/video-decoding-and-resizing.png)

- **Image decoding, resizing, and format conversion**

    The input image is in JPEG encoding format and the resolution is 1280 x 720. However, the ResNet-50 model for image classification requires an RGB input image with the resolution of 224 x 224. In this case, you can process the image as follows.

    **Figure 2** Image decoding, resizing, and format conversion
    ![](figures/image-decoding-resizing-and-format-conversion.png)

- **Image cropping, resizing, and format conversion**

    The input image is in YUV420SP format and the resolution is 1280 x 720. However, the ResNet-50 model for image classification requires an RGB input image with the resolution of 224 x 224. In this case, you can process the image as follows.

    **Figure 3** Image cropping, resizing, and format conversion
    ![](figures/image-cropping-resizing-and-format-conversion.png)

## Development Workflow of Media Data Processing

**Figure 4** Development process
![](figures/development-workflow-5.png)

1. **Set up the environment.**

    For details, see [Environment Setup](environment_preparation.md).

2. **Create code directories.**

    Before developing an app, you must create directories to store code files, scripts, test images, and model files.

    In the model inference scenario, an offline model (.om file) that adapts to the AI processor is required. For details, see [Model Building](model_construction.md).

    >[!NOTE] NOTE
    >If model inference is involved in an app, you need to build a model.

3. **Develop an app.**

    If model inference is involved, compile the code by referring to [Model Management](model_management.md).

4. **Run the app**. For details, see [App Debugging](app_debug.md).
