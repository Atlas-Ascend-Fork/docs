# ConvWeightCompressFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:45:11.988Z pushedAt=2026-11-16T06:27:04.291Z nl=2 -->

## Description

For Cube operators, the filter is compressed by inserting a compression operator or sparsified by inserting a 2:4 structured sparsity operator. This pass performs compression or 2:4 structured sparsity based on the user-defined parameters.

Cube operators support Conv2D, FullyConnection, and MatMulV2.

![](../figures/ConvWeightCompressFusionPass_1.png)

After:

![](../figures/ConvWeightCompressFusionPass_2.png)

## Constraints

The first node (Conv2D/FullyConnection/MatMulV2) must meet the following conditions:

- The data type of the input with index 0 must be int8 or uint8.
- AI Core must be supported.
- The value of groups must not be greater than 1.
- Weight compression or 2:4 structured sparsity must be supported.

## Applicable Products

The effectiveness of this pass depends on whether the target platform supports the corresponding operator types. For details, see [Ascend IR Operator Specifications](https://www.hiascend.com/document/detail/en/CANNCommunityEdition/latest/API/aolapi/docs/en/ops-lib/ascendIR_spec_intro.md) in the operator library.
