# Using VPC Multi-Function Combination APIs to Reduce System Scheduling Pressure and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:59:52.207Z pushedAt=2026-10-22T00:42:08.886Z nl=2 -->

## Background

When performing operations such as cropping, resizing, pasting, and padding on images, the media data processing module provides the following APIs for implementing these functions:

- A single API performs only one operation (that is, a single-function API), for example, **hi\_mpi\_vpc\_crop, hi\_mpi\_vpc\_resize** and **hi\_mpi\_vpc\_copy\_make\_border**.

    In this mode, to implement multiple functions, for example, cropping + resizing + padding, you need to call the preceding three APIs.

- A single API performs multiple operations (that is, a multi-function combination API), for example, **hi\_mpi\_vpc\_batch\_crop\_resize\_paste** and **hi\_mpi\_vpc\_batch\_crop\_resize\_make\_border**.

    In this mode, to implement multiple functions, for example, cropping + resizing + padding, you only need to call one API **hi\_mpi\_vpc\_batch\_crop\_resize\_make\_border**.

The following table lists the mapping between single-function APIs and multi-function combination APIs.

| Single-Function API | Multi-Function Combination API |
| --- | --- |
| - hi_mpi_vpc_crop (cropping)<br>  - hi_mpi_vpc_resize (resizing) | - hi_mpi_vpc_crop_resize (cropping and resizing)<br>  - hi_mpi_vpc_crop_resize_paste (cropping, resizing, and pasting), hi_mpi_vpc_batch_crop_resize_paste (batch cropping, resizing, and pasting) |
| - hi_mpi_vpc_crop (cropping)<br>  - hi_mpi_vpc_resize (resizing)<br>  - hi_mpi_vpc_copy_make_border (padding) | hi_mpi_vpc_crop_resize_make_border (cropping, resizing, and padding) or hi_mpi_vpc_batch_crop_resize_make_border (batch cropping, resizing, and padding) |

## Basic Principles

An API involves multiple task interactions between the host and device, and each interaction incurs latency. If you call multiple APIs for multiple functions such as cropping and resizing, the number of task interactions between the host and device increases, and so does the latency.

By using a multi-function combination API, you can call a single API to complete multiple functions. Although multiple functions are involved, they are processed as a single operation on the device (the hardware execution time of a multi-function combination API is the same as that of a single-function API). Compared with calling multiple single-function APIs, this approach reduces the number of scheduling operations between the host and device and the number of processing operations on the device, significantly improving scheduling and performance. Consider this approach during performance optimization.

## Usage Example

The following uses batch cropping, resizing, and padding as an example to describe how to call the multi-function combination API **hi\_mpi\_vpc\_batch\_crop\_resize\_make\_border**.

You can click [sample\_comm\_vpc\_batchCropResizeMakeBorder](https://gitee.com/ascend/samples/blob/master/cplusplus/level1_single_api/7_dvpp/vpc_sample/src/common/sample_comm_vpc_batchCropResizeMakeBorder.cpp) to obtain the sample code.
