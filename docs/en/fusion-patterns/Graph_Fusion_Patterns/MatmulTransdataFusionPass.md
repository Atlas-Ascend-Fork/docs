# MatmulTransdataFusionPass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:48:27.042Z pushedAt=2026-11-16T06:27:04.369Z nl=2 -->

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

None.
