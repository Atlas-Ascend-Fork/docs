# AFullyConnectionReshapePass

<!-- md-trans-meta sourceCommit=unknown translatedAt=2026-11-06T09:41:48.515Z pushedAt=2026-11-16T06:27:04.212Z nl=2 -->

## Description

Fuses the FullyConnection+Reshape operators into the AFullyConnectionReshape operator.

![](../figures/AFullyConnectionReshapePass_1.png)

After:

![](../figures/AFullyConnectionReshapePass_2.png)

## Constraints

- The number of output nodes of Reshape cannot exceed 1.
- The FullyConnection node must have the `axis` attribute, and the attribute value must be 1.
- The input and output dimensions of axis 0 of Reshape must be the same, and the output dimension cannot be 0.
