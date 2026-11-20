# Properly Using VDEC Decoding Frame Skipping to Reduce Memory Allocation, Relieve VPC Pressure, and Achieve Better Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:58:09.560Z pushedAt=2026-10-21T09:47:03.238Z nl=2 -->

## Background

In the video decoding + model inference scenario, if a video has a large number of frames and not every frame requires inference, for frames that do not require inference, it is recommended that you set the current frame output to not be displayed and not output the decoding result when calling the **hi\_mpi\_vdec\_send\_stream** API for decoding.

## Basic Principles

Video decoding requires continuous data, and the decoded data must be output in YUV format. Therefore, after each frame is decoded, VDEC internally performs decompression, resizing, and format conversion through VPC.

If you do not want to obtain the decoding result of a frame, set the current frame output to not be displayed when calling the **hi\_mpi\_vdec\_send\_stream** API for decoding. In this way, no output memory needs to be allocated, and VDEC does not perform decompression, resizing, and format conversion through the VPC module. This reduces memory allocation and relieves the processing pressure on VPC, thereby improving performance.

## Usage

For details, see the description of the **need\_display** parameter in the **hi\_vdec\_stream** structure of the **hi\_mpi\_vdec\_send\_stream** API.
