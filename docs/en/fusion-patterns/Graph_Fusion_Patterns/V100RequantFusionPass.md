# V100RequantFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:52:17.882Z pushedAt=2026-11-16T06:27:04.472Z nl=2 -->

## Description

Optimizes the quantization nodes in inference tasks.

Inserts the RequantHostCpuOpV2 operator into the input of AscendDequant based on the following structures.

- **Scenario 1**

  ![](../figures/V100RequantFusionPass_01.png)

- **Scenario 2**

  ![](../figures/V100RequantFusionPass_02.png)

- **Scenario 3**

  ![](../figures/V100RequantFusionPass_03.png)

## Constraints

If there are multiple AscendDequant operators, the scale values of all AscendDequant operators must be the same.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->
