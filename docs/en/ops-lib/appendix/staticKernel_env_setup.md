# Environment Setup

<!-- md-trans-meta sourceCommit=96217e9acd4da744a739b8f94b020fbe0cc7fcca translatedAt=2026-10-20T07:16:57.532Z pushedAt=2026-10-21T02:33:30.167Z nl=2 -->

## Installing the Software Packages

1. Prepare the software packages based on the following software package list.

    **Table 1** Software package list

    | Component | Introduction |
    | --- | --- |
    | Toolkit | Toolkit for development, debugging, and tuning. It mainly includes operator tools, model tools, and application tools. |
    | Firmware | Firmware package. It contains basic firmware such as UEFI on the device. This package is usually flashed into the device during production, but it can also be installed later to upgrade the firmware version. |
    | Driver | Driver package. It carries the interaction, scheduling, and transmission between the host and the device, including the device management and query driver, graph execution task scheduling driver, training data transmission preprocessing driver, and AI CPU operator loading and execution driver. |
    | PyTorch (optional) | When you use the Python APIs of PyTorch for programming, install the software related to the PyTorch framework.<br> Note: You can download the latest PyTorch software from the [Ascend/pytorch](https://gitcode.com/Ascend/pytorch/releases) repository. The recommended version is v5.0.rc2.1-pytorch1.11.0 or later. Otherwise, the subsequent capability of dumping operator JSON files will be affected. |

2. Install the software packages. For details about how to install the driver, firmware, and the Ascend-cann-toolkit development suite package, see [CANN Software Installation](https://hiascend.com/document/redirect/CannCommunityInstSoftware).

3. Configure the environment variables.

    CANN provides process-level environment variable setting scripts for users to reference in processes, so that environment variables are set automatically. The following shows example commands. The examples use the default installation paths for both root and non-root users. Replace them with the actual installation paths.

    ```bash
    # Configure environment variables after installing the toolkit package as the root user.
    source /usr/local/Ascend/cann/set_env.sh
    # Configure environment variables after installing the toolkit package as a non-root user.
    source ${HOME}/Ascend/cann/set_env.sh
    ```

## Obtaining the Tool

The tool is located in the `${INSTALL_DIR}/bin/op_compiler` directory.

Replace **\$\{INSTALL\_DIR\}** with the file storage path after CANN software installation. For example, if you install the software as the **root** user, the default storage path is `/usr/local/Ascend/cann`.
