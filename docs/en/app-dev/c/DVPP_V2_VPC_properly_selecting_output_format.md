# Selecting a Proper Output Format for VPC Processing to Reduce Memory Allocation and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:00:37.996Z pushedAt=2026-10-22T00:43:53.897Z nl=2 -->

The VPC image processing function supports output in YUV400 format (grayscale image). If the input image for model inference is a grayscale image, directly use the VPC function without AIPP color space conversion.

## Basic Principles

Directly using the VPC function to output the YUV400 format (grayscale image) eliminates the need for AIPP color space conversion, reducing the load on the AI Core unit and improving performance at the hardware level.

## Usage

For sample code of the VPC function, see [Typical VPC Image Processing Functions](DVPP_V2_VPC.md).
