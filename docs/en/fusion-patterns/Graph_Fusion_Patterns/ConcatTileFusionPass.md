# ConcatTileFusionPass

<!-- md-trans-meta sourceCommit=00b1ca60d898edc2a59d7bd6065c20592117dbdc translatedAt=2026-10-09T06:42:20.744Z pushedAt=2026-10-15T12:44:18.273Z -->

## Description

Concatenates multiple identical contiguous inputs to fuse Tile operators.

**Pattern 1**

![](../figures/ConcatTileFusionPass_1.png)

**Pattern 2**

![](../figures/ConcatTileFusionPass_2.png)

## Constraints

- Only Tile/TileD+Concat operators are supported.
- Concat[ConcatD/ConcatV2/ConcatV2D] and Tile/TileD support only one output.
- `concat_dim` of Concat cannot be the same as the broadcast axis of Tile/TileD.
- Concat supports only data edges. Control edges can exist only in the input of Tile nodes.
- Only static scenarios are supported.
- The multiple inputs of Tile/TileD must be the same and contiguous in Concat. The number of contiguous Tile/TileD must be greater than 2.
- The product of the input tensor shape dimensions of Tile/TileD must be less than or equal to `shape_limited_`.

    shape\_limited\_ = vector\_calculate\_size \* 2 \* vector\_core\_num/data\_type\_size .

    `data_type_size` indicates the data size of the output tensor of Concat[ConcatD/ConcatV2/ConcatV2D].

    To view the values of `vector_calculate_size` and `vector_core_num`, perform the following steps:

    View the platform information file in the `${INSTALL_DIR}/${arch}/data/platform_config` folder and search for the keyword `vec_calc_size` or `vector_core_cnt` to obtain the values of `vector_calculate_size` and `vector_core_num`. Replace `${INSTALL_DIR}` with the actual file storage path after the CANN software is installed. For example, if the installation is performed as the `root` user, the default file storage path after the installation is `/usr/local/Ascend/cann`.

## Applicable Products

<!-- npu="310p" id1 -->
Atlas inference products
<!-- end id1 -->

<!-- npu="310b" id2 -->
Atlas 200I/500 A2 inference products
<!-- end id2 -->

<!-- npu="910" id3 -->
Atlas training products
<!-- end id3 -->

<!-- npu="910b" id4 -->
Atlas A2 products
<!-- end id4 -->

<!-- npu="A3" id5 -->
Atlas A3 products
<!-- end id5 -->
