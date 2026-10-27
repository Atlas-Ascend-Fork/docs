# BatchMatMulNonAlignedFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:41:46.784Z pushedAt=2026-10-15T12:44:18.262Z -->

## Description

Applies to non-aligned BatchMatMul.

Pattern 1:

![](../figures/BatchMatMulNonAlignedFusionPass_1.png)

After:

![](../figures/BatchMatMulNonAlignedFusionPass_2.png)

Pattern 2:

![](../figures/BatchMatMulNonAlignedFusionPass_3.png)

After:

![](../figures/BatchMatMulNonAlignedFusionPass_4.png)

## Constraints

The M dimension of the BatchMatMul input must be a multiple of 16, and the K dimension must not be a multiple of 16.

The `perm` values in `transpose` are subject to the following constraints:

1\. When add\_2 is absent, all values of `transpose.perm` are \{0,2,1,3\}.

2\. When add\_2 is present, the value of `transpose_1.perm` is \{0,2,1,3\}, and the value of `transpose_2.perm` is \{0,2,3,1\}.
