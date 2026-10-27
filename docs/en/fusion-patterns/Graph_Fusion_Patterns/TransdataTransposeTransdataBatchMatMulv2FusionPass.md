# TransdataTransposeTransdataBatchMatMulv2FusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:56:09.529Z pushedAt=2026-10-15T12:44:18.496Z -->

## Description

Deletes redundant nodes such as TransData and Transpose between the two BatchMatMulV2 nodes.

Pattern 1:

![](../figures/TransdataTransposeTransdataBatchMatMulv2FusionPass_1.png)

Pattern 2:

![](../figures/TransdataTransposeTransdataBatchMatMulv2FusionPass_2.png)

Pattern 3:

![](../figures/TransdataTransposeTransdataBatchMatMulv2FusionPass_3.png)

## Constraints

The output data type of the first TransData must be float16.

All nodes can only be referenced once.

The perm list of Transpose can only be `[0,2,1,3]`, and the last dimension must be exactly divided by 16.

The last three dimensions of the input shape of the first TransData must be the same as those of the output shape of the second TransData.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
