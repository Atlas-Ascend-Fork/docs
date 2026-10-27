# PoolingFusionPass

<!-- md-trans-meta sourceCommit=5202b44fe050523341d3692a32123046bf708403 translatedAt=2026-10-09T06:51:18.447Z pushedAt=2026-10-15T12:44:18.420Z -->

## Description

![](../figures/PoolingFusionPass_1.png)

After:

![](../figures/PoolingFusionPass_2.png)

## Constraints

- Dynamic shapes are not supported.
- The static fusion data type can only be float16 or int8.
- The fusion pattern takes effect for AVG Pooling only. If the network of AVG Pooling has been int8 quantized, that is, the `pool` attribute is set to `AVG` in the prototxt file, the fusion pattern must be enabled.
