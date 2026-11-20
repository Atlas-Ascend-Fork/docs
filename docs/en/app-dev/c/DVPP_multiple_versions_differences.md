# Differences Between Media Data Processing API Versions

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:41:53.812Z pushedAt=2026-10-23T09:53:30.832Z nl=2 -->

The following describes each set of media data processing APIs. The API sets must not be used in mixed mode.

- Media data processing operator API set: This API set is more suitable for AI frameworks. Its input data and output data are based on tensor parameters, support asynchronous execution on a stream, and can work with Neural Network (NN) operators on the same stream.
- Media data processing V2 API set: This API set is suitable for computer vision processing applications. Its input data and output data are based on image parameters, support multiple image formats such as YUV420 and RGB, and provide richer and more flexible parameter configuration capabilities.
- Media data processing V1 API set: This API set contains legacy media APIs and is no longer evolving. Use the preceding two API sets instead.
