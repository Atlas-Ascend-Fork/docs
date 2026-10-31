# Recommendations for Increasing the Calibration Set

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:14:09.523Z pushedAt=2026-10-22T03:25:35.142Z nl=2 -->

During accuracy-based automatic quantization, you can manually modify **batch\_num** in the quantization configuration based on the batch size and the number of images required for quantization, so as to adjust the amount of data used for calibration. **batch\_num** controls the number of batches of data used for quantization, where **batch\_num** = **total\_nums** / **batch\_size**. Here, **total\_nums** indicates the total number of images, and **batch\_size** indicates the number of images used in each batch.

**In general**:

The larger the **batch\_num**, the more data samples are used during quantization and the smaller the accuracy loss after quantization. However, excessive data does not improve accuracy; instead, it consumes more memory, reduces the quantization speed, and may cause insufficient memory, video memory, or thread resources. Therefore, it is recommended that **batch\_num** × **batch\_size** be set to **16** or **32**.
