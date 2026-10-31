# Setting a Proper Queue Depth to Reduce Hardware Resource Waste and Improve Performance

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:56:33.824Z pushedAt=2026-10-21T09:45:07.974Z nl=2 -->

## Background

The media data processing V2 APIs can be used to configure the VPC queue depth, which is in the range \[10, 350\]. When the user service submits tasks, if the VPC queue is full, backpressure is applied to block task submission, affecting performance.

## Basic Principles

Properly increasing the VPC queue depth can mitigate the impact of performance fluctuations between user business task submission and VPC internal task processing.

- If the user submits more tasks than the VPC channel can process in a short period, the excess tasks are buffered in the queue, so the user is not blocked from continuing to submit tasks.
- If the user submits fewer tasks in a short period, the VPC can process the tasks buffered in the queue, avoiding idle time and hardware resource waste.

You can adjust the queue depth based on the task submission speed of the service and the processing performance of a single VPC channel:

- If the user service creates one channel and uses multiple threads to submit tasks to the same channel, and the number of submitted tasks exceeds the reference performance of a single channel above, it is recommended that the queue depth be set larger.
- If the user service creates one channel and only one thread submits tasks to the channel, submitting one task and obtaining one result at a time in serial execution, tasks do not accumulate in the channel. In this case, the queue depth does not need to be increased and can remain at the default value.

## Usage

When calling the **hi\_mpi\_vpc\_create\_chn** API or the **hi\_mpi\_vpc\_sys\_create\_chn** API to create a VPC channel, set the queue depth through the **attr** parameter in the **hi\_vpc\_chn\_attr** structure.

You can click [vpc\_sample](https://gitee.com/ascend/samples/tree/master/cplusplus/level1_single_api/7_dvpp/vpc_sample) to obtain the sample code. For the sample code of VPC queue depth setting, see the **queue\_len** parameter in **sample\_vpc.cpp**.
