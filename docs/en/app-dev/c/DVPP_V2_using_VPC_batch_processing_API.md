# Using VPC Batch Processing APIs to Reduce Latency and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:58:43.623Z pushedAt=2026-10-21T09:51:09.142Z nl=2 -->

## Background

When performing operations such as cropping and resizing on images, the media data processing module provides the following two types of APIs:

- Process one image at a time, for example, the **hi\_mpi\_vpc\_crop\_resize\_make\_border** API.

    In this mode, if there are multiple input images, a **for** loop is generally used to call the **hi\_mpi\_vpc\_crop\_resize\_make\_border** API once for each image.

- Process multiple images at a time (that is, the batch processing API), for example, the **hi\_mpi\_vpc\_batch\_crop\_resize\_make\_border** API.

    In this mode, if there are multiple input images, you only need to call the **hi\_mpi\_vpc\_batch\_crop\_resize\_make\_border** API once.

The following table lists the correspondence between the two types of APIs.

| Single-Image Processing API | Batch Image Processing API |
| --- | --- |
| hi_mpi_vpc_crop_resize_paste (cropping, resizing, and pasting) | hi_mpi_vpc_batch_crop_resize_paste (batch cropping, resizing, and pasting) |
| hi_mpi_vpc_crop_resize_make_border (cropping, resizing, and padding) | hi_mpi_vpc_batch_crop_resize_make_border (batch cropping, resizing, and padding) |

## Basic Principles

The AI processor has a built-in image processing unit called Digital Video Pre-Processing (DVPP). In DVPP, there are multiple Vision Preprocessing Core (VPC) modules that handle tasks such as image cropping, resizing, and format conversion.

When a batch API is called, the batch tasks are evenly distributed to multiple VPC modules and processed in parallel, which reduces the processing latency of the batch API and improves performance.

## Usage Example

The following uses batch cropping, resizing, and padding as an example to describe how to call the multi-function combination API **hi\_mpi\_vpc\_batch\_crop\_resize\_make\_border**.

You can click [sample\_comm\_vpc\_batchCropResizeMakeBorder](https://gitee.com/ascend/samples/blob/master/cplusplus/level1_single_api/7_dvpp/vpc_sample/src/common/sample_comm_vpc_batchCropResizeMakeBorder.cpp) to obtain the sample code.
