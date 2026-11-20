# Audio Obtaining & Audio Playback

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T02:34:37.746Z pushedAt=2026-10-21T03:33:03.955Z nl=2 -->

This section describes the API call process and precautions for audio obtaining and audio playback.

## Audio Obtaining

![](figures/obtain_audio.png)

1. Call the **hi\_mpi\_sys\_init** API to initialize the media common module.
2. Call the **hi\_mpi\_ai\_set\_pub\_attr** API to configure attributes.
3. Call the **hi\_mpi\_ai\_enable** API to enable the AI device, and then call the **hi\_mpi\_ai\_enable\_chn** API to enable the AI channel.
4. Call **hi\_mpi\_ai\_get\_frame** to obtain recording data for processing, and then call **hi\_mpi\_ai\_release\_frame** to release the audio frame. Repeat this process.
5. When AI audio obtaining ends, first call the **hi\_mpi\_ai\_disable\_chn** API to disable the channel, and then call the **hi\_mpi\_ai\_disable** API to disable the AI device.
6. Call the **hi\_mpi\_sys\_exit** API to release the initialization resources of the media common module.

## Audio Playback

![](figures/play_audio.png)

1. Call the **hi\_mpi\_sys\_init** API to initialize the media common module.
2. Call the **hi\_mpi\_ao\_set\_pub\_attr** API to configure attributes.
3. Call the **hi\_mpi\_ao\_enable** API to enable the AO device, and then call the **hi\_mpi\_ao\_enable\_chn** API to enable the AO channel.
4. Periodically obtain data and call the **hi\_mpi\_ao\_send\_frame** API to play audio.
5. When AO audio playback ends, first call the **hi\_mpi\_ao\_get\_chn\_delay** API to obtain the current audio delay of the AO channel. After the delay becomes 0, call the **hi\_mpi\_ao\_disable\_chn** API to disable the channel, and then call the **hi\_mpi\_ao\_disable** API to disable the AO device.
6. Call the **hi\_mpi\_sys\_exit** API to release the initialization resources of the media common module.
