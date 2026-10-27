# ZConfusionSoftmaxGradFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:01:38.231Z pushedAt=2026-10-15T12:44:18.575Z -->

## Description

This fusion fuses the Mul + ReduceSumD/ReduceSum (supported only on the Ascend 950PR&950DT product series) + Sub operators that match the graph fusion pattern into the ConfusionSoftmaxGrad operator.

![](../figures/ZConfusionSoftmaxGradFusionPass_1.png)

## Constraints

- The fusion pattern does not take effect for dynamic shapes.
- The fusion pattern does not take effect when the two inputs of the Mul operator have different shapes.
- The fusion pattern does not take effect when the input0 of the Mul operator and the input0 of the Sub operator are from different nodes.
- The fusion pattern does not take effect when input0 is not the first input of the Sub operator.
- This fusion pattern does not take effect when the `axis` attribute of ReduceSumD/ReduceSum is not the tail axis index of the input shape.
- This fusion pattern does not take effect when the last axis of the input shape for ReduceSumD/ReduceSum is greater than 30000.
- The fusion pattern does not take effect when the data type is not supported by the fused operator.
- The data type and format of input0 must be the same as those of input1.
- The fusion pattern does not take effect if the reduce axis is set to `1` and the AReduceSumFusionPass fusion pattern is enabled.
- For Ascend 950PR&950DT products, this fusion pattern does not take effect when the `keep_dims` attribute of ReduceSum is `False`.
- For Ascend 950PR&950DT products, this fusion pattern does not take effect when the input axis of ReduceSum is not a const node.

## Applicable Products

<!-- npu="910b" id3 -->
Atlas A2 products
<!-- end id3 -->

<!-- npu="950" id2 -->
Ascend 950PR&950DT products
<!-- end id2 -->
