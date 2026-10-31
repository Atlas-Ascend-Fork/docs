# Selecting the Right VDEC Video Decoding Output Format and Resolution for Better Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:54:32.864Z pushedAt=2026-10-21T09:40:46.676Z nl=2 -->

## Background

If you need to use DVPP for video decoding and want to obtain RGB images, on some AI processors the current video decoding API **hi\_mpi\_vdec\_send\_stream** supports output in YUV420SP or RGB888 format, and supports image resizing during decoding. Therefore, from a performance perspective, you can optimize the code logic to directly call the video decoding API **hi\_mpi\_vdec\_send\_stream** to output the RGB888 format.

**Figure 1**  Combined scenarios of VDEC decoding output  
![](figures/VDEC_output_V2.png "Combined scenarios of VDEC decoding output")

## Basic Principles

On some AI processors, the video decoding API **hi\_mpi\_vdec\_send\_stream** supports output in YUV420SP or RGB888 format. You can set API parameters to output different formats, eliminating the need to call **hi\_mpi\_vpc\_convert\_color** for format conversion and reducing the number of API calls.

If the resolution of the video stream differs from that of the model input image, the decoded image needs to be resized. You can also set the output image resolution in the video decoding API **hi\_mpi\_vdec\_send\_stream** to complete image resizing during decoding, eliminating the need to call the resizing API separately and reducing the number of API calls.

In summary, you can complete decoding, resizing, and color space conversion in the video decoding API **hi\_mpi\_vdec\_send\_stream**, reducing the number of API calls and improving performance.

## Usage Example

You can click [vdec\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/vdec_sample) to obtain the sample code.
