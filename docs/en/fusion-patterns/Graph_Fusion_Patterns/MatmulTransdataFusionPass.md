# MatmulTransdataFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:50:16.487Z pushedAt=2026-10-15T12:44:18.400Z -->

## Description

Reduces the number of Transdata operators in the graph from 2 to 1 through equivalent replacement.

![](../figures/MatmulTransdataFusionPass_1.png)

After:

![](../figures/MatmulTransdataFusionPass_2.png)

When the Cast operator is absent:

![](../figures/MatmulTransdataFusionPass_3.png)

After:

![](../figures/MatmulTransdataFusionPass_4.png)

## Constraints

None
