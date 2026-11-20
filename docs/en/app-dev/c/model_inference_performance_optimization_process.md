# Model Inference Performance Tuning

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:17:46.311Z pushedAt=2026-10-22T03:56:29.025Z nl=2 -->

During full-network inference, the model inference performance may not meet expectations due to issues such as operator adaptation and data read/write of the model on the AI processor. You can refer to the content in this section to learn about the performance tuning process for model inference. Since this is a tuning process, before tuning, ensure that functional debugging of full-network inference has been completed and that functionality is not blocked. Only the model inference performance does not meet expectations and needs to be improved.

In the performance tuning process shown in the following figure, the key tools involved in tuning are the model tuning tool Ascend Optimization Engine (AOE) and the model compression tool Ascend Model Compression Toolkit (AMCT). During the tuning process, when operations such as converting models, recording model inference time, and analyzing performance bottlenecks are involved, the model conversion tool ATC, performance data collection tools, and accuracy comparison tools are also used as auxiliary tools.

![](figures/image_0000001594647953.png)
