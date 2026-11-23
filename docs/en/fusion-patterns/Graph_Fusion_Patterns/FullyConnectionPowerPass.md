# FullyConnectionPowerPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:46:14.568Z pushedAt=2026-11-16T06:27:04.314Z nl=2 -->

## Description

Fuses the FullyConnection+Power operators into the FullyConnectionPower operator.

![](../figures/FullyConnectionPowerPass_1.png)

After:

![](../figures/FullyConnectionPowerPass_2.png)

## Constraints

- The number of FC weights cannot be less than 2.
- The input data type of FC cannot be int8 or uint8.
