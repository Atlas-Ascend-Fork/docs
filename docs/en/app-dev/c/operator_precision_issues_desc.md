# Issue Description

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:23:40.139Z pushedAt=2026-10-22T07:03:35.422Z nl=2 -->

Inference results that do not meet standards include the following two cases:

- Incorrect inference results caused by operator precision: The full-network inference function has been debugged successfully, but the inference results are incorrect. For example, the MAP results of an object detection network are all 0, or the cosine similarity is 0 when the inference results of the OM model are compared with those of the benchmark network.
- Inference accuracy that does not meet standards caused by operator precision: The full-network inference function has been debugged successfully, and the cosine similarity is above 95% when the inference results of a single OM model are compared with those of the benchmark network, but the dataset inference accuracy differs slightly from the benchmark data. For example:
    - For a classification network OM model, the Top-1/Top-5 accuracy is 0.90/0.70, while that of the benchmark network is 0.92/0.71.
    - For a detection network OM model, the MAP accuracy is 0.54, while that of the benchmark network is 0.55.
