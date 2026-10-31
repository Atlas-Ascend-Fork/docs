# Media Data Processing Overview

<!-- md-trans-meta sourceCommit=fdf4276c76935b494f8459e5a6e0a3e968866a42 translatedAt=2026-10-23T10:30:09.924Z pushedAt=2026-10-26T03:10:39.419Z nl=2 -->

This chapter describes the specific functions, API call process, and sample code of image/video/audio data processing.

## Typical Functions of Image/Video/Audio Data Processing

<!-- npu="310b" id1 -->
**Figure 1** Image/video data processing  
![](figures/image_video_data_processing.png "Image/video data processing")
<!-- end id1 -->

The functions are described in the following table. For the support status of each media data processing function on each product model, see [Function Support by Different Product Models](functions_supported_status.md). AIPP is supported in all current versions.

| Function | Submodule | Description |
| --- | --- | --- |
| Image data processing | AIPP (Artificial Intelligence Pre-Processing) | AIPP performs artificial intelligence pre-processing on the AI Core. Its main functions include resizing images (cropping, padding, etc.), color gamut conversion (converting image formats), and mean subtraction/coefficient multiplication (changing image pixels).<br>AIPP is classified into static AIPP and dynamic AIPP. You can use only one of them to process images; static AIPP and dynamic AIPP cannot be configured at the same time.<br>  - Static AIPP: During model conversion, set the AIPP mode to static and configure the AIPP parameters. After the model is generated, the AIPP parameter values are saved in the offline model (*.om). Each model inference process uses fixed AIPP pre-processing parameters (which cannot be modified). If static AIPP is used, the same AIPP parameters are shared across multiple batches. The AIPP parameter values are set during model conversion using the ATC tool. For details about the ATC tool, see [Ascend Tensor Compiler (ATC)](https://gitcode.com/cann/ge/blob/9.2.0/docs/en/user_guides/atc_tools/README.md).<br>  - Dynamic AIPP: During model conversion, only set the AIPP mode to dynamic. Before each model inference, set the dynamic AIPP parameter values as required before executing the model, so that different AIPP parameters can be used during model execution. |
| Image/video data processing | Digital Vision Pre-Processing (DVPP) | DVPP is a built-in image processing unit of the AI processor. It provides powerful hardware acceleration for media processing through media data processing APIs. Its main functions are as follows:<br><br>  - Vision Preprocessing Core (VPC): processes images in YUV, RGB, and other formats, including resizing, cropping, image pyramid, and color gamut conversion.<br>  - JPEGD (JPEG Decoder): decodes images from JPEG compressed format to YUV format.<br>  - JPEGE (JPEG Encoder): encodes images from YUV format to JPEG compressed format.<br>  - VDEC (Video Decoder): decodes video streams from H264/H265 format to YUV/RGB format.<br>  - VENC (Video Encoder): encodes video streams from the YUV420SP format to the H264/H265 format.<br>  - PNGD (PNG Decoder): decodes images from the PNG format to the RGB format.<br><br><br>AIPP and DVPP can be used independently or in combination. In combined use cases, DVPP is generally used first to perform basic processing such as decoding, cropping, and resizing on images/videos. However, due to hardware constraints of DVPP, the image format and resolution after DVPP processing may not meet the model requirements. Therefore, AIPP is further used to perform color gamut conversion, cropping, padding, and other processing. |

<!-- npu="310b" id2 -->
<br>

The Atlas 200I/500 A2 inference products also support the following functions:

| Function | Submodule | Description |
| --- | --- | --- |
| Obtain video data | Image Signal Processing (ISP) system control | The system control part is used to register 3A algorithms, register sensor drivers, initialize ISP firmware, run ISP firmware, exit ISP firmware, and configure ISP attributes. |
| Obtain video data | MIPI Rx ioctl command | MIPI Rx is a capture unit that supports multiple differential video input interfaces. It receives data from MIPI/LVDS/sub-LVDS/HiSPi interfaces through combo-PHY. Through different function mode configurations, MIPI Rx can support data transmission requirements of multiple speeds and resolutions and support multiple external input devices. |
| Obtain video data | VI (Video Input) | The VI module captures video images, performs processing such as cropping, color optimization, brightness optimization, and noise removal on them, and outputs image data in YUV or RAW format. |
| Display video data | VO (Video Output) | The VO module receives the output images processed by VPSS, performs processing such as playback control, and finally outputs them to peripheral video devices according to the output protocol configured by the user (currently only HDMI is supported).<br>VO can work with the Two Dimensional Engine (TDE) module and the HiSilicon Framebuffer (HIFB) module to use hardware for graphics drawing and overlay graphics layer management respectively. |
| Display video data | HDMI (High Definition Multimedia Interface) | HDMI is a fully digital image and sound transmission interface that can transmit uncompressed audio and video signals. |
| Display video data | TDE (Two Dimensional Engine) | TDE is a 2D graphics acceleration engine. It uses hardware to provide fast graphics drawing functions for OSD (On Screen Display) and GUI (Graphical User Interface), mainly including fast copy, fast color fill, and pattern fill (currently only Alpha Blending is supported). |
| Display video data | HIFB (HiSilicon Framebuffer) | HIFB is used to manage overlay graphics layers. It not only provides the basic functions of Linux Framebuffer, but also adds extended functions such as modifying the display start position of a layer and inter-layer Alpha on the basis of Linux Framebuffer. |
| Region management | Region | The OSD (On Screen Display) overlaid on the video and the color blocks covering the video are collectively called regions. The region management module is used to manage these region resources in a unified manner, to display specific information on the video (such as channel number and timestamp), or to fill color blocks in the video for occlusion. Currently, this function must be used together with VPSS. |
| Image/video data processing | VPSS (Video Process Sub-System) | The VPSS module supports unified preprocessing of input images, such as denoising, deinterlacing, and cropping, and then processes each channel separately, such as resizing and adding borders. |
| Audio data obtaining and output | AI (Audio Input) | The AI module captures audio data. |
| AO (Audio Output) | For audio data decoded by the ADEC module, the AO module supports audio playback. |  |
| Audio data encoding and decoding | AENC (Audio Encoder) | For audio data obtained by the AI module, the AENC module supports encoding it and outputting audio streams. |
| Audio data encoding and decoding | ADEC (Audio Decoder) | ADEC supports decoding audio streams of protocols such as G.711a and G.711u, and then plays the audio through the AO module. |
<!-- end id2 -->

## Typical Use Cases of DVPP Image/Video Data Processing

If the resolution or format of the source image or video does not meet the model requirements, we can process the source image or video to make it meet the model requirements. The following are examples of **typical use cases**.

- **Video decoding and resizing**

    In the scenario where the Yolov3 model is used for object detection, the input video provided by the user is in H264 encoding format with a resolution of 1920\*1080, but the Yolov3 model requires the input image to be in RGB/YUV format with a resolution of 416\*416. Since the two do not match, the following series of processing can be performed on the video.

    **Figure 2**  Video decoding and resizing use case  
    ![](figures/video_decoding_resizing.png "Video decoding-resizing use case")

- **Image decoding, resizing, and format conversion**

    In the scenario where the Resnet50 model is used for image classification, the input image provided by the user is in JPEG encoding format with a resolution of 1280\*720, but the Resnet50 model requires the input image to be in RGB format with a resolution of 224\*224. Since the two do not match, the following series of processing can be performed on the image.

    **Figure 3**  Image decoding, resizing, and format conversion use case  
    ![](figures/image_decoding_resizing_format_conversion.png "Image decoding-resizing-format conversion use case")

- **Cropping, resizing, and format conversion**

    In the scenario where the Resnet50 model is used for image classification, the input image provided by the user is in YUV420SP format with a resolution of 1280\*720, but the Resnet50 model requires the input image to be in RGB format with a resolution of 224\*224. Since the two do not match, the following series of processing is performed on the image.

    **Figure 4**  Cropping, resizing, and format conversion use case diagram  
    ![](figures/image_crop_resize_format_conversion.png "Crop-resize-format conversion use case diagram")
