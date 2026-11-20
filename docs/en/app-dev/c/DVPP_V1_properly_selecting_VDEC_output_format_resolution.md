# Selecting a Proper VDEC Video Decoding Output Format and Resolution for Better Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:44:54.742Z pushedAt=2026-10-21T07:38:31.977Z nl=2 -->

## Background

If you need to use DVPP for video decoding and want to obtain RGB images, on some AI processors, the current video decoding API **aclvdecSendFrame** supports output in YUV420SP or RGB888 format, and supports image resizing during decoding. Therefore, to improve performance, you can optimize the code logic to directly call the video decoding API **aclvdecSendFrame** to output the RGB888 format.

**Figure 1**  Combined scenarios of VDEC decoding output  
![](figures/VDEC_output_V1.png "Combined scenarios of VDEC decoding output")

## Basic Principles

On some AI processors, the video decoding API **aclvdecSendFrame** supports output in YUV420SP or RGB888 format. You can set API parameters to output different formats, eliminating the need to call **acldvppVpcConvertColorAsync** for format conversion and reducing API calls.

If the resolution of the video stream differs from that of the model input image, the decoded image needs to be resized. You can also set the output image resolution in the video decoding API **aclvdecSendFrame** to complete image resizing during decoding, eliminating the need to call a separate resize API and reducing API calls.

In summary, the video decoding API **aclvdecSendFrame** can perform three functions at once: decoding, resizing, and color space conversion. This reduces the number of API calls and improves performance.

## Usage Example

You can click [vdec\_resnet50\_classification](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/1_classification/vdec_resnet50_classification) to obtain the sample code.

If video decoding needs to output RGB888 format and also implement resizing, you need to set the image format, width, height, width stride, and height stride in the output parameter (which describes the output image) of the **aclvdecSendFrame** API. For example:

```cpp
// Create the output image description.
acldvppPicDesc picOutputDesc = acldvppCreatePicDesc();

// Define the output image format, width, height, width stride, height stride, and the memory for storing output image data.
uint32_t width = 224;
uint32_t height = 224;
uint32_t widthStride = 224 * 3;
uint32_t heightStride = 224;
uint32_t size = widthStride * heightStride;
void *picOutBufferDev = nullptr;
acldvppMalloc(&picOutBufferDev, size);

// Set the output image format, width, height, width stride, height stride, and the memory for storing output image data.
acldvppSetPicDescData(picOutputDesc, picOutBufferDev);
acldvppSetPicDescSize(picOutputDesc, size);
acldvppSetPicDescFormat(picOutputDesc, PIXEL_FORMAT_RGB_888);
acldvppSetPicDescWidth(picOutputDesc, width);
acldvppSetPicDescHeight(picOutputDesc, height);
acldvppSetPicDescWidthStride(picOutputDesc, widthStride);
acldvppSetPicDescHeightStride(picOutputDesc, heightStride);

// Call the decoding API.
aclvdecSendFrame(channelDesc, picInputDesc, picOutputDesc, nullptr, nullptr);
```
