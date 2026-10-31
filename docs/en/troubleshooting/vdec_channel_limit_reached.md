# Failure in Creating a VDEC Channel Due to the Upper Limit in the Ascend Virtualization Instance Scenario

<!-- md-trans-meta sourceCommit=6cd29bdd84cdddc273ad662dd3b2784d5ad66033 translatedAt=2026-10-16T07:09:40.828Z pushedAt=2026-10-23T08:38:06.151Z nl=2 -->

## Symptom

Once the number of channels reaches a certain level, no more VDEC channels can be created.

A device log example is as follows:

```bash
pid 0 usr chn 0 device 0 chn 0 vf_id 1 has created chn num(27) is full, max chn num = 27
```

>**Note:** 
>In EP mode, after running the decoding process, log in to the host and run the  **msnpureport -a**  command in the directory on which you have the read, write, and execute permissions to export the device log.
>In RC mode, log in to the board environment and run the  **cat /proc/umap/vdec**  command to export decoding information.

## Possible Cause

Different computing power templates have different upper limits on the total number of channels. If the number of channels exceeds the upper limit, no more channels can be created.

## Solution

1. Query VDEC resource information in the used computing power template.

    **Table 1** **Ascend virtualization instance configuration** (Atlas inference products)

    | Name (of Compute Group) | Specification | AIC Core Count | Memory (GB) | AI CPU (device_aicpu Count) | VPC | JPEGD | JPEGE | VENC | VDEC |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | Total resources | 1 | 8 | The value is the same as the value of **memory_size** obtained by calling **dsmi_get_memory_info**. | 7 | 12 | 16 | 8 | 3 | 12 |
    | vir04 | 1/2 | 4 | memory_size/2 | 4 | 6 | 8 | 4 | 2 | 6 |
    | vir04_3c | 1/2 | 4 | memory_size/2 | 3 | 6 | 8 | 4 | 1 | 6 |
    | vir04_4c_dvpp | 1/2 | 4 | memory_size/2 | 4 | 12 | 16 | 8 | 3 | 12 |
    | vir04_3c_ndvpp | 1/2 | 4 | memory_size/2 | 3 | 0 | 0 | 0 | 0 | 0 |
    | vir02 | 1/4 | 2 | memory_size/4 | 2 | 3 | 4 | 2 | 1 | 3 |
    | vir02_1c | 1/4 | 2 | memory_size/4 | 1 | 3 | 4 | 2 | 0 | 3 |
    | vir01 | 1/8 | 1 | memory_size/8 | 1 | 1 | 2 | 1 | 0 | 1 |

2. Calculate the upper limit of the total number of channels based on the VDEC resource information.

    Upper limit of the total number of  decoding channels = \(JPEGD + VDEC\) / \(16 + 12\) × 256.

    For example, in the  **vir01**  template, the maximum number of decoding channels is calculated as follows \(2 + 1\) / \(16 + 12\) × 256 = 27.
