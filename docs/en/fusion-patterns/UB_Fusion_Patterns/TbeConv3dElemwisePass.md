# TbeConv3dElemwisePass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T07:04:32.722Z pushedAt=2026-10-15T12:44:18.629Z -->

## Description

Performs UB fusion on Conv3D and Elemwise in a subgraph that meets the following patterns.

![](../figures/TbeConv3dElemwisePass_1.png)

Or

![](../figures/TbeConv3dElemwisePass_2.png)

Or

![](../figures/TbeConv3dElemwisePass_3.png)

Or

![](../figures/TbeConv3dElemwisePass_4.png)

## Constraints

Dynamic shapes are not supported.

Four patterns are supported, corresponding to the scenarios shown in the preceding four figures.

1. Fuses two Elemwise operators. The first operator supports only Add, and the second operator supports only ReLU.
2. Fuses an Elemwise operator that has another input. The Elemwise operator type is not restricted. AscendDequant and AscendRequant are supported.
3. Fuses an Elemwise operator that has only one input. Only ReLU is supported..
4. Fuses three Elemwise operators. The first supports only AscendDequant, the second only Add, and the third only Relu. This use case is supported only on Atlas inference products.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="910" id2 -->
Atlas training products
<!-- end id2 -->
