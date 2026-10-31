# Using VPC Multi-Function Combination APIs to Reduce System Scheduling Pressure and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:48:05.878Z pushedAt=2026-10-21T08:30:16.935Z nl=2 -->

## Background

When performing operations such as cropping, resizing, pasting, and padding on images, the media data processing module provides the following APIs for implementing these functions:

- An API performs only one operation (that is, a single-function API), for example, **acldvppVpcCropAsync**, **acldvppVpcResizeAsync**, and **acldvppVpcMakeBorderAsync**.

    In this mode, to implement multiple functions, for example, cropping + resizing + padding, you need to call the preceding three APIs.

- An API performs multiple operations (that is, a multi-function combination API), for example, **acldvppVpcBatchCropResizePasteAsync** and **acldvppVpcBatchCropResizeMakeBorderAsync**.

    In this mode, to implement multiple functions, for example, cropping + resizing + padding, you only need to call one API: **acldvppVpcBatchCropResizeMakeBorderAsync**.

The mapping between single-function APIs and multi-function combination APIs is as follows.

| Single-Function API | Multi-Function Combination API |
| --- | --- |
| - acldvppVpcCropAsync (cropping)<br>  - acldvppVpcResizeAsync (resizing) | - acldvppVpcCropResizeAsync (cropping and resizing) or acldvppVpcBatchCropResizeAsync (batch cropping and resizing)<br>  - acldvppVpcCropAndPasteAsync (cropping and pasting) or acldvppVpcBatchCropAndPasteAsync (batch cropping and pasting)<br>  - acldvppVpcCropResizePasteAsync (cropping, resizing, and pasting), acldvppVpcBatchCropResizePasteAsync (batch cropping, resizing, and pasting) |
| - acldvppVpcCropAsync (cropping)<br>  - acldvppVpcResizeAsync (resizing)<br>  - acldvppVpcMakeBorderAsync (padding) | acldvppVpcBatchCropResizeMakeBorderAsync (batch cropping, resizing, and padding) |

## Basic Principles

An API involves multiple task interactions between the host and the device, and each interaction incurs latency. If multiple APIs are called for multiple functions such as cropping and resizing, the number of task interactions between the host and the device increases, and the latency naturally increases accordingly.

By using a multi-function combination API, you can call a single API to complete multiple functions. Although multiple functions are involved, they are processed by the device in a single pass (the hardware execution time of a multi-function combination API is the same as that of a single-function API). Compared with calling multiple single-function APIs, this reduces the number of scheduling operations between the host and the device and the number of processing operations on the device, significantly improving scheduling and performance. You can consider this approach during performance optimization.

## Usage Example

The following uses batch image cropping and resizing as an example to describe how to call the multi-function combination API **acldvppVpcBatchCropResizeAsync**.

You can click [batchcrop](https://gitee.com/ascend/samples/tree/master/cplusplus/level2_simple_inference/0_data_process/batchcrop) to obtain the sample code.
