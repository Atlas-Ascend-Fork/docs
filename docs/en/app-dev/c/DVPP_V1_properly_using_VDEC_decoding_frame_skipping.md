# Properly Using VDEC Decode Frame Skipping to Reduce Memory Allocation, Relieve VPC Load, and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:46:12.318Z pushedAt=2026-10-21T07:40:16.769Z nl=2 -->

## Background

In the video decoding + model inference scenario, if a video has a large number of frames and not every frame requires inference, for frames that do not require inference, you are advised to use the **aclvdecSendSkippedFrame** API for decoding without outputting the decoding result.

## Basic Principles

Video decoding requires continuous data, and the decoded data needs to be output in YUV format. Therefore, after each frame is decoded, VDEC internally performs decompression, scaling, and format conversion through VPC.

If you do not want to obtain the decoding result of a frame, you can call the **aclvdecSendSkippedFrame** API. In this case, no output memory needs to be allocated, and VDEC does not perform decompression, scaling, or format conversion through the VPC module. This reduces memory allocation and relieves the processing pressure on VPC, thereby improving performance.

## Usage

For details, see the description of the **aclvdecSendSkippedFrame** API.
