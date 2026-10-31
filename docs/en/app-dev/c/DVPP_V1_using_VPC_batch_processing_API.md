# Using VPC Batch Processing APIs to Reduce Latency and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:46:36.140Z pushedAt=2026-10-21T07:45:23.985Z nl=2 -->

## Background

For image processing such as cropping and resizing, the media data processing module provides the following two types of APIs:

- Process one image at a time, for example, the **acldvppVpcCropAsync** API.

    In this mode, if there are multiple input images, a **for** loop is generally used to call **acldvppVpcCropAsync** once for each image.

- Process multiple images at a time (that is, batch processing APIs), for example, the **acldvppVpcBatchCropAsync** API

    In this mode, if there are multiple input images, you only need to call **acldvppVpcBatchCropAsync** once.

The following table lists the correspondence between the two types of APIs.

| Single-Image Processing API | Batch Image Processing API |
| --- | --- |
| acldvppVpcCropAsync (cropping) | acldvppVpcBatchCropAsync (batch cropping) |
| acldvppVpcCropResizeAsync (cropping and resizing) | acldvppVpcBatchCropResizeAsync (batch cropping and resizing) |
| acldvppVpcCropAndPasteAsync (cropping and pasting) | acldvppVpcBatchCropAndPasteAsync (batch cropping and pasting) |
| acldvppVpcCropResizePasteAsync (cropping, resizing, and pasting) | acldvppVpcBatchCropResizePasteAsync (batch cropping, resizing, and pasting) |
| - | acldvppVpcBatchCropResizeMakeBorderAsync (batch cropping, resizing, and padding) |

## Basic Principles

The AI processor has a built-in image processing unit Digital Video Pre-Processing (DVPP). In DVPP, there are multiple Vision Preprocessing Core (VPC) modules that handle tasks such as image cropping, resizing, and format conversion.

When a batch processing API is called, the batch tasks are evenly distributed to multiple VPC modules and processed in parallel. As a result, the processing latency of the batch API is reduced and the performance is improved.

## Usage Example

The following uses batch image cropping and resizing as an example to describe how to call the batch processing API **acldvppVpcBatchCropResizeAsync**. For the complete code, click [batchcrop](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/0_data_process/batchcrop) to obtain the sample code.
