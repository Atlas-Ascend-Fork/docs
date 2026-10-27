# ReluFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:52:13.908Z pushedAt=2026-10-15T12:44:18.433Z -->

## Description

In the Caffe framework, the fusion matches the following specific graph structure. After the matching is successful, the fusion is converted into an instruction to complete the computation of the activation function.

**Structure 1**

![](../figures/ReluFusionPass_1.png)

**Structure 2**

![](../figures/ReluFusionPass_2.png)

## Constraints

The input of the Add operator must be Convolution, Activation, FusionBatchNorm, BatchNorm, Pooling, or Eltwise.

The **Mode** attribute of Activation is set to **Relu**.

## Applicable Products

<!-- npu="310b" id3 -->
Atlas 200I/500 A2 inference products
<!-- end id3 -->

<!-- npu="310p" id4 -->
Atlas inference products
<!-- end id4 -->

<!-- npu="910" id5 -->
Atlas training products
<!-- end id5 -->Atlas training products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->
