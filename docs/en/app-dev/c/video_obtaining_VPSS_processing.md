# Video Data Obtaining + VPSS Video Processing

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:35:36.604Z pushedAt=2026-10-22T08:09:04.751Z nl=2 -->

VPSS must be used together with the VI module. This section describes the API call process and precautions.

**Figure 1**  VPSS call process  
![](figures/VPSS_API_call_process.png "VPSS call process")

The API call process is described as follows:

1. **Perform initialization**:
    1. Call **hi\_mpi\_sys\_init** to complete media system initialization.
    2. Call **hi\_mpi\_rgn\_create** to create a region.
    3. The VPSS module can only act as the bound party, passively receiving and processing video stream data. Therefore, call **hi\_mpi\_sys\_bind** to bind the planned VI channel to the VPSS group.
    4. Call **hi\_mpi\_vpss\_create\_grp** to create a VPSS group, which serves as the bound party of **hi\_mpi\_sys\_bind**.
    5. Enable VPSS functions as required:
        - If group cropping is required, call the **hi\_mpi\_vpss\_set\_grp\_crop** API to set the cropping-related configuration.
        - If 3DNR needs to be enabled, in addition to turning on the NR switch and configuring the NR attributes when calling the **hi\_mpi\_vpss\_create\_grp** API, you can also set advanced NR parameters through the **hi\_mpi\_vpss\_set\_grp\_param** API.
        - If fisheye correction needs to be enabled and the Lens Map Function \(LMF\) parameter function is enabled through the **hi\_fisheye\_attr** attribute in the **hi\_mpi\_vi\_set\_chn\_fisheye** API, you must call the **hi\_mpi\_vpss\_set\_grp\_fisheye\_cfg** API to set the LMF parameters.

    6. Call the **hi\_mpi\_vpss\_start\_grp** API to enable the VPSS group.
    7. Call the **hi\_mpi\_vpss\_set\_chn\_attr** API to set the channel attributes. The channel output resolution can differ from the input source resolution. When they differ, scaling is automatically enabled. Different channels have different scaling capabilities.
    8. If fisheye distortion correction needs to be enabled, you also need to call the **hi\_mpi\_vi\_set\_chn\_fisheye** API to set the fisheye correction parameters.
    9. Call the **hi\_mpi\_vpss\_enable\_chn** API to start the VPSS channel.
    10. Call the **hi\_mpi\_rgn\_attach\_to\_chn** API to overlay the region onto the VPSS channel.

2. **Collect and process data**:
    1. Use the MIPI Rx ioctl command to initialize the MIPI/sensor hardware interconnection information. For the API call process, see [Initializing MIPI/Sensor Hardware Interconnection Information](video_obtaining.md#section5234939161715).
    2. Use the Video Input (VI) functional API to initialize the VI module. For the API call process, see [Initializing the VI Module](video_obtaining.md#section140011491810).
    3. Use the Image Signal Processing (ISP) system control API to initialize and run the ISP module. For the API call process, see [Initializing and Running the ISP Module](video_obtaining.md#section0926122591813).
    4. Based on the binding policy configured by the **hi\_mpi\_sys\_bind** API, the system automatically passes the image processed by VI to VPSS.
    5. Based on the parameters configured for VPSS, the system automatically performs cropping, 3DNR, fisheye correction, and scaling.
    6. Update the region information as required:
        - Set the region channel display attributes:
            1. Call the **hi\_mpi\_rgn\_get\_display\_attr** API to obtain the current channel display attributes of the region.
            2. Call the **hi\_mpi\_rgn\_set\_display\_attr** API to set the channel display attributes of the region.

        - Set the region display canvas information:
            1. Call the **hi\_mpi\_rgn\_get\_canvas\_info** API to obtain the current display canvas information of the region.
            2. Call the **hi\_mpi\_rgn\_update\_canvas** API to update the display canvas information.

3. **Obtain the processing result data**:

    At this point, you can call the **hi\_mpi\_vpss\_get\_chn\_fd** API to obtain the handle of the specified VPSS channel, and use the select/epoll API to wait for the VPSS processing result. After VPSS completes processing, it automatically wakes up the select/epoll wait. You can then call the **hi\_mpi\_vpss\_get\_chn\_frame** API to obtain the image data processed by VPSS for subsequent processing, and finally call **hi\_mpi\_vpss\_release\_chn\_frame** to release one frame of channel image.

4. **Release the VI and VPSS initialization resources**.
    1. Use the ISP functional API to release the ISP module resources. For the API call process, see [Releasing ISP Module Resources](video_obtaining.md#section053155901816).
    2. Use the VI functional API to release the VI module resources. For the API call process, see [Releasing VI Module Resources](video_obtaining.md#section1909173011193).
    3. Use the MIPI Rx ioctl command to exit the MIPI/sensor hardware. For the API call process, see [Exiting the MIPI/Sensor Hardware](video_obtaining.md#section440174412194).
    4. Call the **hi\_mpi\_rgn\_detach\_from\_chn** API to delete the specified region from the channel.
    5. Call the **hi\_mpi\_vpss\_disable\_chn** API to disable the VPSS channel.
    6. Call the **hi\_mpi\_vpss\_stop\_grp** API to stop the VPSS group.
    7. Call the **hi\_mpi\_vpss\_destroy\_grp** API to destroy the VPSS group.
    8. Call the **hi\_mpi\_sys\_unbind** API to unbind VI and VPSS.
    9. Call the **hi\_mpi\_rgn\_destroy** API to destroy the region.
    10. Finally, call the **hi\_mpi\_sys\_exit** API to exit the media system.
