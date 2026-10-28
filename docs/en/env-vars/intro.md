# Introduction

<!-- md-trans-meta sourceCommit=96217e9acd4da744a739b8f94b020fbe0cc7fcca translatedAt=2026-10-16T07:28:28.038Z pushedAt=2026-10-20T07:59:38.327Z nl=2 -->

This document describes the environment variables that developers can use when building AI applications and services based on CANN.

Environment variables can be set through commands, APIs, and configurations, including the **export** command, the **putenv**/**getenv**/**setenv**/**unsetenv**/**clearenv** functions, **os.environ**, and **os.getenv**. It is recommended that you set environment variables before the application process is started. Otherwise, access conflicts on environment variables may occur, causing program exceptions.
