# Tuning Overview

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:29:44.059Z pushedAt=2026-10-22T07:20:53.680Z nl=2 -->

This chapter focuses on precision and performance tuning for inference applications. Before tuning, ensure that the full-network inference function has been debugged and verified, that the function is not blocked, and that the remaining issues are limited to incorrect inference precision, a small gap between inference precision and benchmark data, or model inference performance that does not meet expectations or needs to be improved.

- **Precision issues in an application** may be caused by concatenation issues between the inference function and other functions, precision issues of the operators themselves in the entire network, and so on. You can refer to the suggestions in this chapter to check API parameter configuration issues during function concatenation, and use tools to obtain detailed data for locating and analyzing the issues.
- **Performance issues in an application** may be caused by operator adaptation or data read/write issues of the model on the AI processor, DVPP API usage issues, and so on. You can refer to the suggestions in this chapter to check API usage issues, use tools to optimize the model, and use tools to obtain detailed data for locating and analyzing the issues.
