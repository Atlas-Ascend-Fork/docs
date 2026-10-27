# InplaceAddRmsNormFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:48:46.359Z pushedAt=2026-10-15T12:44:18.370Z -->

## Description

Scenario 1: Converts AddRmsNorm to InplaceAddRmsNorm by reusing the x1 input address as the y output address and the x2 input address as the x output address.

![](../figures/InplaceAddRmsNormFusionPass_1.png)

Scenario 2: Fuses AddRmsNorm and Cast into the AddRmsNormCast operator if the output y of AddRmsNorm is connected to only two outputs and the first output is connected to the Cast operator (to cast the output y from float16/bfloat16 to float32).

![](../figures/InplaceAddRmsNormFusionPass_2.png)

## Constraints

- This fusion pattern applies only to inference tasks.
- For the fusion into AddRmsNormCast:
  - The input x1 can only be of the float16 or bfloat16 type.
  - Only casting from float16 or bfloat16 to float32 is supported.
  - The output must not contain rstd either before or after fusion.

- Constraint for fusion into InplaceAddRmsNorm: In use cases other than Ascend 950PR&950DT products, the second output of AddRmsNorm must have no successor node.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->

<!-- npu="A3" id2 -->
Atlas A3 products
<!-- end id2 -->

<!-- npu="310p" id3 -->
Atlas inference products
<!-- end id3 -->

<!-- npu="950" id4 -->
Ascend 950PR&950DT products
<!-- end id4 -->
