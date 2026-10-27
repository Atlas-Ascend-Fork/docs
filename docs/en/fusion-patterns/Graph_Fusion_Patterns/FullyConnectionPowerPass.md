# FullyConnectionPowerPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:46:39.617Z pushedAt=2026-10-15T12:44:18.333Z -->

## Description

Fuses the FullyConnection+Power operators into the FullyConnectionPower operator.

![](../figures/FullyConnectionPowerPass_1.png)

After:

![](../figures/FullyConnectionPowerPass_2.png)

## Constraints

- The number of FC weights cannot be less than 2.
- The input data type of FC cannot be int8 or uint8.
