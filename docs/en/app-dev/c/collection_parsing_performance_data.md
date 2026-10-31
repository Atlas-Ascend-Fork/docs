# Collecting & Parsing Performance Data

<!-- md-trans-meta sourceCommit=723a4cff0d4aa189e3bfd192b64fea3be4c0ffc9 translatedAt=2026-10-23T10:27:46.386Z pushedAt=2026-10-26T03:10:39.416Z nl=2 -->

This section describes the basic method of collecting and parsing performance data using the **msprof command line** in the **inference** scenario, and analyzing performance bottlenecks through the generated result files. **Before using the msprof command line**, you need to refer to [Performance Tuning Tool](https://gitcode.com/cann/docs/blob/9.2.0/docs/en/profiling/profiling_menu.md) to prepare the environment, understand the usage constraints, and learn the basic parameter usage.

## Collecting, Parsing, and Exporting Performance Data

1. Log in to the running environment where the toolkit package is installed and run the following command to collect, parse, and export performance data in one click:

    ```bash
    msprof --output=/home/HwHiAiUser/profiling_output /home/HwHiAiUser/HIAI_PROJECTS/MyAppname/out/main
    ```

    **Table 1** Parameters

    | Parameter | Description | Optional/Required |
    | --- | --- | --- |
    | --output | Storage path of the collected Profiling data. The default value is the directory where the AI task file resides. The path cannot contain the following special characters: "\n", "\f", "\r", "\b", "\t", "\v", "\u007F". | Optional |

    After the command is executed, a **PROF_\__XXX** directory is generated in the directory specified by **--output** to store the automatically parsed performance data (only the performance data is shown below).

    ```bash
    ├── device_{id}   // Stores the raw data. Users do not need to pay attention to it.
    │    └── data
    └── mindstudio_profiler_output
          ├── msprof_{timestamp}.json
          ├── step_trace_{timestamp}.json
          ├── xx_*.csv
           ...
          └── README.txt
    ```

2. Go to the **mindstudio\_profiler\_output** directory to view the performance data files. \* indicates the timestamp.

    **Table 2** Performance data files collected by msprof with the default configuration

    | File Name | Description |
    | --- | --- |
    | msprof_*.json | Timeline data summary table. |
    | step_trace_*.json | Iteration trace data, including the duration of each iteration. This performance data file is not generated in the single operator scenario. |
    | op_summary_*.csv | AI Core and AI CPU operator data. |
    | op_statistic_*.csv | Statistics on the call count and duration of AI Core and AI CPU operators. |
    | step_trace_*.csv | Iteration trace data. This performance data file is not generated in the single operator scenario. |
    | task_time_*.csv | Task Scheduler task scheduling information. |
    | fusion_op_*.csv | Information before and after operator fusion in the model. This performance data file is not generated in the single-operator scenario. |
    | api_statistic_*.csv | Statistics on the API execution duration at the CANN layer. |
    | prof_rule_0_*.json | Tuning suggestions. |

    - To view a JSON file, enter **chrome://tracing** in the Chrome browser and drag the file to the blank area to open it. Use the keyboard shortcuts (**w**: zoom in, **s**: zoom out, **a**: move left, **d**: move right). This file allows you to view the timing information of the current AI task execution, such as the API call timeline during running, as shown in Figure 1.

        **Figure 1**  Viewing the JSON file
        ![](figures/view_json_file.png "Viewing the JSON file")

    - The CSV file can be opened directly. Through this file, you can view the software and hardware data during AI task execution, such as the running duration of each operator on the AI processor software and hardware. You can quickly find the required information through field sorting, as shown in Figure 2.

        **Figure 2**  Viewing the CSV file
        ![](figures/view_csv_file.png "Viewing the CSV file")

## Performance Analysis

As described above, there are many performance data files and the analysis methods are flexible. The following describes several important files and their analysis methods.

- Through the **msprof\_\*.json** file, view the timing information of AI task execution from an overall perspective, and then analyze possible bottleneck points.

    **Figure 3**  msprof\_\*.json file example
    ![](figures/msprof_json_example.png "msprof_-json file example")

    - Area 1: CANN layer data, which mainly contains the duration data of components such as Runtime and nodes (operators).
    - Area 2: underlying NPU data, which mainly contains the duration data and iteration trace data of each stream task flow under Ascend hardware, as well as AI processor system data.
    - Area 3: displays the detailed information of each operator and API in the timeline (displayed by clicking each timeline color block).

    From the preceding figure, you can roughly identify the APIs, operators, and task flows with long durations, and identify the corresponding dispatch relationships based on the arrow directions. Then analyze the lower-layer tasks with long durations during inference execution, view the APIs and operators with long durations in area 3, and perform quantitative analysis in combination with the CSV file to locate the specific performance bottleneck.

- Analyze the total call time and total call count of each type of operator through the **op\_statistic\_\*.csv** file to check whether a certain type of operator takes a long time in total, and then analyze whether this type of operator can be optimized.

    **Figure 4**  op\_statistic\_\*.csv file example
    ![](figures/op_statistic_csv_file_example.png "op_statistic_-csv file example")

    You can sort by **Total Time** to find out which type of operator takes a long time.

- Analyze the information and time consumption of a specific operator through the **op\_summary\_\*.csv** file to identify time-consuming operators, and then analyze whether the operator can be optimized.

    **Figure 5**  op\_summary\_\*.csv file example
    ![](figures/op_summary_csv_file_example.png "op_summary_-csv file example")

    The **Task Duration** field indicates the time consumption of an operator. You can sort by **Task Duration** to identify time-consuming operators, or sort by **Task Type** to view time-consuming operators running on different cores (AI Core and AI CPU).
