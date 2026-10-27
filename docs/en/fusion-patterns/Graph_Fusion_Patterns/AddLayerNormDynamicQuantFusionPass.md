# AddLayerNormDynamicQuantFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:36:56.980Z pushedAt=2026-10-15T12:44:18.197Z -->

## Description

Fuses AddLayerNorm and one or two downstream DynamicQuant operators into the AddLayerNormQuant operator.

There may be one or two structures in the dashed-line box.

![](../figures/AddLayerNormDynamicQuantFusionPass_1.png)

When the optional smooth input of DynamicQuant exists, it will be placed in the position corresponding to the scale input of AddLayerNormQuant.

The smooth operation of DynamicQuant can also be expressed by Mul. In this scenario, the optional smooth input of DynamicQuant must be empty.

![](../figures/AddLayerNormDynamicQuantFusionPass_2.png)

## Constraints

- For dtype:
  <!-- npu="950" id3 -->
  - For Ascend 950PR&950DT products, the x1 data type of AddLayerNorm supports fp16, bf16, and fp32.
  <!-- end id3 -->
  <!-- npu="910b" id4 -->
  - For Atlas A2 products, the x1 data type of AddLayerNorm supports fp16 and bf16.
  <!-- end id4 -->
  - The data types of inputs x2, gamma, beta, and bias of AddLayerNorm must be the same as that of x1.
  - The input x of DynamicQuant must be of the same data type as x1 of AddLayerNorm.
  <!-- npu="950" id5 -->
  - For Ascend 950PR&950DT products, if DynamicQuant has `smooth`, the dtype of `smooth` must be the same as the x1 data type of AddLayerNorm.

  <!-- end id5 -->
- For the graph structure:
  - AddLayerNorm can have only one or two fan-outs for its output 0, connecting to a Mul node or a DynamicQuant node.
  - When AddLayerNorm has two fan-outs for its output 0, the two downstream nodes must be both Mul nodes or both DynamicQuant nodes.
  - When a downstream node of output 0 is Mul, it must have exactly one downstream DynamicQuant node, which must not contain the optional `smooth` input.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="950" id2 -->
Ascend 950PR&950DT products
<!-- end id2 -->
