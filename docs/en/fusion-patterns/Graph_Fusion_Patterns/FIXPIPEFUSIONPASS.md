# FIXPIPEFUSIONPASS

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:46:30.547Z pushedAt=2026-10-15T12:44:18.330Z -->

## Description

On hardware with FixPipe support, when a cube operator has `support_fixpipe_ability` configured in [FixPipeAbilityProcessPass](FixPipeAbilityProcessPass.md), it will sequentially attempt to match the convert, activation, and transform units as shown in the figure below. If at least one of these units exists (nonexistent units are skipped), the matched operators will be fused into a FixPipe operator.

- convert unit: format conversion unit, which is typically a quant or cast operator.
- activation unit: activation unit, which is typically a ReLU operator.
- transform unit: format conversion unit for converting ND to NZ, which is typically a TransData operator.

![](../figures/FIXPIPEFUSIONPASS_1.png)

## Constraints

- Only static networks are supported.
- This fusion pattern cannot be disabled.

## Applicable Products

<!-- npu="910b" id1 -->
Atlas A2 products
<!-- end id1 -->
