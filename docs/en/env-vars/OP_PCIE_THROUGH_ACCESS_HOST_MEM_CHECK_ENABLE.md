# OP_PCIE_THROUGH_ACCESS_HOST_MEM_CHECK_ENABLE

<!-- md-trans-meta sourceCommit=fe5307907d2087c03797a673819df2784c73d1b4 translatedAt=2026-10-16T07:30:36.781Z pushedAt=2026-10-20T07:59:38.329Z nl=2 -->

## Function Description

PCIe through is an Ascend NPU hardware capability that allows device-side operators to directly access host memory through the PCIe bus, thereby reducing data movement overhead.

This environment variable is used to enable address checking for the PCIe through feature: after it is configured and takes effect, the data address of each tensor is checked during single-operator execution to determine whether it falls within the PCIe address segment range. Operators whose addresses hit the PCIe address segment will enable the PCIe through feature.

The value can be:

- **1**: enables address checking for the PCIe through feature.
- Other values (including 0) or not configured: disables the feature (disabled by default).

## Configuration Example

```bash
export OP_PCIE_THROUGH_ACCESS_HOST_MEM_CHECK_ENABLE=1
```

## Constraints

Interconnection requirement: This feature takes effect only when the host and device are interconnected through PCIe. If they are not interconnected through PCIe (for example, HCCS or UB), the feature does not take effect even if this environment variable is configured.

Operator support: Only two memory access instructions in the Ascend NPU chip natively support PCIe through access. After this environment variable is enabled, operators that support PCIe through automatically select the compute templates corresponding to these two instructions to ensure that the memory access path meets hardware requirements. Currently, the PCIe through feature is supported by only some operators. If the operator used is not within the supported range, an AI Core error may occur during operator execution even if this environment variable is enabled. It is recommended that you confirm whether the target operator has been adapted to this feature before use.

Performance tips: Enabling address checking introduces additional memory check overhead, which may increase the performance burden on the host side. Use it only when needed.

Function tips: DataDump does not yet support the PCIe through scenario. Therefore, DataDump is not supported after PCIe through is enabled.

## Supported Models

<!-- npu="950" id1 -->
Ascend 950PR&950DT products
<!-- end id1 -->
