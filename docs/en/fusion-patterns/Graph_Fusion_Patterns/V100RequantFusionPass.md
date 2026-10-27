# V100RequantFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:56:57.350Z pushedAt=2026-10-15T12:44:18.506Z -->

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
