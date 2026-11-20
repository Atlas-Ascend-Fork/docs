# Selecting an Appropriate Output Format During VPC Processing to Reduce Memory Allocation and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:48:45.720Z pushedAt=2026-10-21T08:32:01.969Z nl=2 -->

## Background

The VPC image processing function supports output in the YUV400 format (grayscale image). If the input image for model inference is a grayscale image, use the VPC function directly without using the AIPP color space conversion function.

## Basic Principles

Directly using the VPC function to output the YUV400 format (grayscale image) eliminates the need for AIPP color space conversion, reducing the load on the AI Core unit and improving performance at the hardware level.

## Usage

With support for the YUV400 format, you can directly set the output format to YUV400 and set the memory size to a value not less than **widthStride\*heightStride**, thereby saving memory.

For sample code of the VPC function, see [Typical VPC Image Processing Functions](DVPP_V1_VPC.md).
