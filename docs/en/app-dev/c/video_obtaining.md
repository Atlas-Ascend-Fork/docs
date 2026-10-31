# Video Data Obtaining Function

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:36:11.352Z pushedAt=2026-10-22T08:38:52.190Z nl=2 -->

The video obtaining function requires the cooperation of multiple functional modules such as ISP, MIPI Rx, and VI. This section describes the overall API call flow of the video data obtaining function, the API call flow of each functional module, and the precautions.

Currently, the video data obtaining function is implemented through the cooperation of the following functional modules:

- **ISP system control**

    The system control part is used to register 3A algorithms, register sensor drivers, initialize ISP firmware, run ISP firmware, exit ISP firmware, configure ISP attributes, and perform other functions.

- **MIPI Rx ioctl command words**

    MIPI Rx is an obtaining unit that supports multiple differential video input APIs. It receives data from MIPI/LVDS/sub-LVDS/HiSPi APIs through combo-PHY. Through different functional mode configurations, MIPI Rx can support data transmission requirements of various speeds and resolutions, and support multiple external input devices.

- **Video Input (VI)**

    The VI module captures video images, can perform cropping, color optimization, brightness optimization, noise removal, and other processing on them, and outputs image data in YUV or RAW format.

## Overall API Call Process

![](figures/video_data_obtaining_overall_process.png)

The API call process is described as follows:

1. Call **hi\_mpi\_sys\_init** to initialize the media data processing system.
2. Use the MIPI Rx ioctl command word to initialize the MIPI/sensor hardware interconnection information. For the API call process, see [Initializing MIPI/Sensor Hardware Integration Information](#section5234939161715).
3. Use the VI functional API to initialize the VI module. For the API call process, see [Initializing the VI Module](#section140011491810).
4. Use the ISP system control API to initialize and run the ISP module. For the API call process, see [Initializing and Running the ISP Module](#section0926122591813).
5. Use the VI functional API to obtain processed image data. For the API call process, see [Obtaining Processed Image Data](#section13127438161814).
6. Use the ISP functional API to release ISP module resources. For the API call process, see [Releasing ISP Module Resources](#section053155901816).
7. Use the VI functional API to release VI module resources. For the API call process, see [Releasing VI Module Resources](#section1909173011193).
8. Use the MIPI Rx ioctl command word to exit the MIPI/sensor hardware. For the API call flow, see [Exiting the MIPI/Sensor Hardware](#section440174412194).
9. Call the **hi\_mpi\_sys\_exit** API to release the media data processing system resources.

<a id="section5234939161715"></a>

## Initializing MIPI/Sensor Hardware Interconnection Information

![](figures/initializing_MIPI_SENSOR_hardware_interconnection_info.png)

1. Use the **HI\_MIPI\_SET\_HS\_MODE** command word to set the mode.
2. Use the **HI\_MIPI\_ENABLE\_MIPI\_CLOCK** command word to enable the MIPI clock.
3. Use the **HI\_MIPI\_RESET\_MIPI** command word to reset the MIPI connected to the sensor.
4. (Optional) Use the **HI\_MIPI\_CONFIG\_SENSOR\_CLOCK** command word to configure the sensor clock.
5. (Optional) Use the **HI\_MIPI\_ENABLE\_SENSOR\_CLOCK** command word to enable the sensor clock.
6. Use the **HI\_MIPI\_RESET\_SENSOR** command word to reset the sensor.
7. Use the **HI\_MIPI\_SET\_DEV\_ATTR** command word to configure the MIPI Rx/device attributes.
8. Use the **HI\_MIPI\_UNRESET\_MIPI** command word to deassert the MIPI reset.
9. Use the **HI\_MIPI\_UNRESET\_SENSOR** command word to deassert the reset of the sensor.

<a id="section140011491810"></a>

## Initializing the VI Video Input Module

The initialization flow of the VI module varies depending on the data source, data format, and mode.

![](figures/initializing_VI.png)

1. Data is input from the sensor. To obtain YUV-format data, the data is processed through the VI channel in linear mode. The flow is described as follows:

    ![](figures/obtain_YUV_through_VI_linear_mode.png)

    1. Sequentially call the **hi\_mpi\_vi\_set\_dev\_attr** and **hi\_mpi\_vi\_enable\_dev** APIs to configure the attributes of the VI device and enable the VI device.
    2. Call the **hi\_mpi\_vi\_set\_dev\_bind\_pipe** API to set the binding relationship between the device and the PIPE.
    3. Sequentially call the **hi\_mpi\_vi\_create\_pipe** and **hi\_mpi\_vi\_start\_pipe** APIs to create and start the VI PIPE. Set a reasonable **hi\_vi\_pipe\_attr.depth** queue depth. A larger queue depth provides better anti-jitter performance. It is recommended to set the value to **3** or greater.
    4. Sequentially call the **hi\_mpi\_vi\_set\_chn\_attr** and **hi\_mpi\_vi\_enable\_chn** APIs to configure the attributes of the VI channel and enable the VI channel. Set a reasonable **hi\_vi\_chn\_attr.depth** queue depth. In addition to the memory reserved for internal VI processing, the queue depth must also take into account the user's image service processing duration (the time interval from when the user calls the **hi\_mpi\_vi\_get\_chn\_frame** API to take away the image resource to when the user calls the **hi\_mpi\_vi\_release\_chn\_frame** API to return the image resource). Set the queue depth to a reasonable value accordingly.

2. Data is input from the sensor. To obtain YUV-format data, the data is processed through the VI channel in WDR mode. The flow is described as follows:

    ![](figures/obtain_YUV_through_VI_wdr_mode.png)

    Compared with the normal linear mode, in WDR mode, the sensor module simultaneously generates two frames of image data through long and short exposure. VI needs to create two pipe resources and bind the two pipes to the same VI device to receive and process the corresponding long-exposure and short-exposure frame images respectively, and then output the fused image data of the long and short exposures in the channel corresponding to the primary pipe. Therefore, the API call process differs as follows:

    1. Call **hi\_mpi\_vi\_set\_dev\_bind\_pipe** to bind the image data of the same sensor device to two pipes. According to the example figure, bind DEV0 to PIPE0 and PIPE1.
    2. Call the **hi\_mpi\_vi\_create\_pipe** and **hi\_mpi\_vi\_start\_pipe** APIs to create and start two pipes. According to the example figure, PIPE0 and PIPE1 are created, where PIPE0 serves as the primary pipe to receive and process short-exposure frames, and PIPE1 serves as the secondary pipe to receive and process long-exposure frames.

        In WDR mode, PIPE0 and PIPE1 form a group, with PIPE0 as the primary pipe; PIPE1 and PIPE2 form a group, with PIPE1 as the primary pipe.

    3. Only the channel on the primary pipe needs to be started. The channel on the secondary pipe does not need to be started, which saves resources.

3. To obtain RAW-format data, process it through the VI pipe. The flow is described as follows:

    ![](figures/obtain_RAW_through_VI.png)

    1. Call the **hi\_mpi\_vi\_set\_dev\_attr** and **hi\_mpi\_vi\_enable\_dev** APIs to configure the attributes of the VI device and enable the VI device.
    2. Call the **hi\_mpi\_vi\_set\_dev\_bind\_pipe** API to complete the binding relationship settings between the device and the pipe.
    3. Call the **hi\_mpi\_vi\_create\_pipe** API to create a pipe.
        1. If the user only needs to obtain RAW images and does not need the images to be processed and converted by VI, the following operations can be performed when creating a pipe in **hi\_mpi\_vi\_create\_pipe**:
            1. Set **pipe\_bypass\_mode** to **HI\_VI\_PIPE\_BYPASS\_BE** so that the images are not processed by ISP BE.
            2. Set the size of **hi\_vi\_pipe\_attr.depth** to **hi\_vi\_dump\_attr.depth** so that no extra image resources are allocated except for the image queue required for dumping.
            3. Call **hi\_mpi\_vi\_set\_chn\_attr**. There is no need to call the **hi\_mpi\_vi\_enable\_chn** API to enable the VI channel.

        2. If the user needs to obtain RAW images and also continue to send the images to VI for processing and conversion, then:
            1. When creating a pipe in **hi\_mpi\_vi\_create\_pipe**, the value of **hi\_vi\_pipe\_attr.depth** must be reasonably set. This value needs to reserve additional queue depth required for internal VI PIPE processing on top of the size of **hi\_vi\_dump\_attr.depth**, generally **hi\_vi\_dump\_attr.depth** + 3.
            2. Continue to call the **hi\_mpi\_vi\_set\_chn\_attr** and **hi\_mpi\_vi\_enable\_chn** APIs to enable the VI channel, and call the **hi\_mpi\_vi\_get\_chn\_frame** API to obtain and process the image result data after VI processing. After processing is complete, call the **hi\_mpi\_vi\_release\_chn\_frame** API to release the memory resources of the corresponding image.

    4. Call the **hi\_mpi\_vi\_set\_pipe\_frame\_dump\_attr** API to set the image queue depth reserved for image obtaining.
    5. Call the **hi\_mpi\_vi\_start\_pipe** API to start the pipe.

4. The user specifies the RAW image data, which is fed into and processed by the VI PIPE to obtain the YUV image. The flow is described as follows:

    ![](figures/user_specified_raw_image.png)

    In the user image re-injection scenario, the image data source is no longer an external camera device. However, because the current version does not support virtual pipes, images can only be fed through a physical pipe. Therefore, even if data is not input from the sensor, you still need to set the corresponding dev and call the **hi\_mpi\_vi\_set\_dev\_bind\_pipe** API to bind the dev and the pipe.

    1. Call the **hi\_mpi\_vi\_create\_pipe** API to create a pipe.
    2. Call the **hi\_mpi\_vi\_set\_pipe\_frame\_source** API to set the image data source of the pipe to **VI\_PIPE\_FRAME\_SOURCE\_USER**.
    3. Call the **hi\_mpi\_vi\_start\_pipe** API to start the pipe.
    4. Call the **hi\_mpi\_vi\_set\_chn\_attr** and **hi\_mpi\_vi\_enable\_chn** APIs to configure the attributes of the VI channel and enable the VI channel.
    5. Start sending the user-specified image data in a loop.
        1. Call **hi\_mpi\_vi\_pipe\_get\_buffer** to obtain idle image data. The maximum number of available memory blocks that can be obtained is determined by the **hi\_vi\_pipe\_attr.depth** attribute delivered by the **hi\_mpi\_vi\_create\_pipe** API.
        2. After the available memory resource is successfully obtained, write the image data to be fed into the returned memory address. The memory address is the **frame\_info.v\_frame.virt\_addr\[0\]** returned by the **hi\_mpi\_vi\_pipe\_get\_buffer** API. Then call the **hi\_mpi\_vi\_send\_pipe\_raw** API to send the RAW image data.
        3. After **hi\_mpi\_vi\_send\_pipe\_raw** successfully sends the data, call the **hi\_mpi\_vi\_pipe\_release\_buffer** API in a timely manner to release the memory resource.
        4. The figure shows the flow for sending bayer-format images. If you need to send YUV-format data, specify the pixel format **pixel\_format** as YUV when calling the **hi\_mpi\_vi\_create\_pipe** API to create a pipe, set **isp\_bypass** to **true**, and change the **hi\_mpi\_vi\_send\_pipe\_raw** API to **hi\_mpi\_vi\_send\_pipe\_yuv**. The YUV image formats supported for sending in the current version are: **HI\_PIXEL\_FORMAT\_YVU\_SEMIPLANAR\_422**, **HI\_PIXEL\_FORMAT\_YVU\_SEMIPLANAR\_420**, and **HI\_PIXEL\_FORMAT\_YUV\_400**.

<a id="section0926122591813"></a>

## Initializing and Running the ISP Module

![](figures/initializing_and_running_ISP.png)

1. Call the **hi\_mpi\_isp\_sensor\_reg\_callback** API to register the common sensor driver algorithm.
2. (Optional) Call the **hi\_mpi\_ae\_sensor\_reg\_callback** API and the **hi\_mpi\_awb\_sensor\_reg\_callback** API to register the built-in sensor driver AE and AWB algorithms.

    Here, you can register custom algorithms as required.

3. (Optional) Call the **hi\_mpi\_ae\_register** API and the **hi\_mpi\_awb\_register** API to initialize the built-in 2A algorithms.

    Here, you can register custom algorithms as required.

4. Call the **hi\_mpi\_isp\_mem\_init** API to initialize the internal ISP resources.
5. Call the **hi\_mpi\_isp\_set\_pub\_attr** API to initialize the algorithm module.
6. Call the **hi\_mpi\_isp\_init** API to initialize the ISP firmware.
7. Enable a separate thread and call the **hi\_mpi\_isp\_run** API to run the main scheduling process of the ISP algorithm.

<a id="section13127438161814"></a>

## Obtaining Processed Image Data

- **Obtaining YUV data**

    ![](figures/obtain_YUV_data.png)

    After VI image processing is complete, you can obtain the processed image on the corresponding VI channel and perform related processing. The typical API call process is as follows:

    1. (Optional) Use the system file handle + select/epoll wait mechanism to wait for the image processing completion event. You can obtain the system file handle of a specified channel through the **hi\_mpi\_vi\_get\_chn\_fd** API. After a frame of image data is obtained and processed in the background, the system select/epoll read wait request is woken up.
    2. Call the **hi\_mpi\_vi\_get\_chn\_frame** API to obtain the processed image data. At this point, the memory resource corresponding to the image data is automatically occupied by the user. After processing the image data, the user must call the **hi\_mpi\_vi\_release\_chn\_frame** API to release the memory resource of the corresponding image.
    3. If the user obtains image data through the **hi\_mpi\_vi\_get\_chn\_frame** API and wants to publish it to other processes, the user can obtain the **acltdtBuf** handle through the returned **hi\_video\_frame.user\_data\[0\]**, and then publish the object to other processes by combining the shared buffer management APIs (such as **acltdtCopyBufRef**) and the shared queue management APIs (such as **acltdtEnqueue**).

- **Obtaining RAW data**

    ![](figures/obtain_RAW_data.png)

    After VI image processing is complete, you can obtain the processed image on the corresponding VI pipe and perform related processing. The typical API call process is as follows:

    1. (Optional) Use the system file handle + select/epoll wait mechanism to wait for the image processing completion event. You can obtain the system file handle of a specified channel through the **hi\_mpi\_vi\_get\_pipe\_fd** API. After a frame of image data is obtained and processed in the background, the system select/epoll read wait request is woken up.
    2. Call the **hi\_mpi\_vi\_get\_pipe\_frame** API to obtain the processed image data. At this point, the memory resource corresponding to the image data is automatically occupied by the user. After processing the image data, the user must call the **hi\_mpi\_vi\_release\_pipe\_frame** API to release the memory resource of the corresponding image.
    3. If the user obtains image data through the **hi\_mpi\_vi\_get\_pipe\_frame** API and then wants to publish it to other processes, the user can obtain the **acltdtBuf** handle through the returned **hi\_video\_frame.user\_data\[0\]**, and then publish the object to other processes by combining the shared buffer management APIs (such as **acltdtCopyBufRef**) and the shared queue management APIs (such as **acltdtEnqueue**).

<a id="section053155901816"></a>

## Releasing ISP Module Resources

![](figures/release_ISP_resource.png)

1. Call the **hi\_mpi\_isp\_exit** API to deinitialize the ISP firmware.
2. Call the **hi\_mpi\_ae\_unregister** API and the **hi\_mpi\_awb\_unregister** API to deinitialize the 2A algorithm.
3. Call the **hi\_mpi\_ae\_sensor\_unreg\_callback** API and the **hi\_mpi\_awb\_sensor\_unreg\_callback** API to unregister the AE and AWB algorithms of the sensor driver.
4. Call the **hi\_mpi\_isp\_sensor\_unreg\_callback** API to unregister the general algorithm of the sensor driver.

<a id="section1909173011193"></a>

## Releasing VI Module Resources

![](figures/release_VI_resource.png)

1. Call the **hi\_mpi\_vi\_disable\_chn** API to disable the VI channel.
2. Call the **hi\_mpi\_vi\_stop\_pipe** and **hi\_mpi\_vi\_destroy\_pipe** APIs in sequence to stop and destroy the VI PIPE.
3. Call the **hi\_mpi\_vi\_disable\_dev** API to disable the VI device.

<a id="section440174412194"></a>

## Exiting MIPI/Sensor Hardware

![](figures/exiting_MIPI_SENSOR_hardware.png)

1. Use the **HI\_MIPI\_RESET\_SENSOR** command word to reset the sensor.
2. Use the **HI\_MIPI\_DISABLE\_SENSOR\_CLOCK** command word to disable the clock connected to the sensor.
3. Use the **HI\_MIPI\_RESET\_MIPI** command word to reset the MIPI interconnected with the sensor.
4. Use the **HI\_MIPI\_DISABLE\_MIPI\_CLOCK** command word to disable the MIPI.
