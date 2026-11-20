# NVR Scenario Voice Intercom

<!-- md-trans-meta sourceCommit=fc161aa801bc6bad9265578932803f7e008ac561 translatedAt=2026-10-16T03:23:22.463Z pushedAt=2026-10-22T06:53:45.378Z nl=2 -->

This section describes the typical processes, key APIs, and precautions for NVR audio service processing.

Network Video Recorder (NVR) is the storage and forwarding component of a network video system. Working together with network cameras, an NVR records, stores, and forwards audio and video. In addition, an NVR provides a local human-machine interaction interface, video decoding, video display, and voice intercom functions.

## NVR Audio Scenario Description

**This section describes the API call process of the NVR audio service (voice intercom function).** The voice intercom function includes initialization and deinitialization of the media data processing system, [receiving voice from an IP camera and playing the audio](#section3741201132710), and [recording audio and sending voice to an IP camera](#section86391611152718). The involved modules include the common module, audio input module (AI), audio encoding module (AENC), audio output module (AO), and audio decoding module (ADEC).

![](figures/NVR_audio.png)

<a id="section3741201132710"></a>

## Receiving Audio from an IP Camera and Playing It

**Figure 1** **Receiving audio from an IP camera and playing it**  
![](figures/receiving_audios_from_IPCamera.png "Receiving audio from an IP camera and playing it")

The API call process is described as follows:

1. Call the **hi\_mpi\_adec\_create\_chn** API to **create an audio decoding channel**.
2. **Enable the AO audio output device and channel**:
    1. Call the **hi\_mpi\_ao\_set\_pub\_attr** API to set the AO device attributes.
    2. Call the **hi\_mpi\_ao\_enable** API to start the AO device.
    3. Call the **hi\_mpi\_ao\_enable\_chn** API to start the AO channel.
    4. Call the **hi\_mpi\_ao\_enable\_resample** API to enable the AO resampling function.

        Because the AO sampling rate is fixed at 48 kHz, while the G.711a and G.711u protocols support only an 8 kHz sampling rate, the resampling function must be enabled. In contrast, 48 kHz falls within the sampling rate range supported by the AAC protocol, so no resampling is required for AO when the AAC protocol is used.

3. Call the **hi\_mpi\_sys\_bind** API to **bind ADEC and AO**.

    | ADEC Device ID | ADEC Channel Number | AO Device ID | AO Channel Number |
| --- | --- | --- | --- |
| 0 | 0 | 2 | 0 |
| 0 | 1 | 3 | 0 |

4. Call the **hi\_mpi\_adec\_send\_stream** API in a loop to send each frame of audio data to be decoded to the decoder for **decoding**.

    The decoded audio data is automatically sent to the corresponding AO device for audio playback based on the binding relationship in step 3.

5. After audio playback is complete, in the exit process, first call the **hi\_mpi\_sys\_unbind** API to **unbind ADEC and AO**, then call the **hi\_mpi\_ao\_disable\_resample** API to disable the AO resampling function, call the **hi\_mpi\_ao\_disable\_chn** API to disable the AO channel, call the **hi\_mpi\_ao\_disable** API to disable the AO device, and finally call the **hi\_mpi\_adec\_destroy\_chn** API to destroy the ADEC channel.

<a id="section86391611152718"></a>

## Recording Audio and Sending Audio to the IP Camera

**Figure 2** **Recording audio and sending audio to the IP Camera**  
![](figures/recording_audios_and_sending_audios_to_IPCamera.png "Recording audio and sending audio to the IP Camera")

The API call process is described as follows:

1. **Enable the AI audio input device and channel**:
    1. Call the **hi\_mpi\_ai\_set\_pub\_attr** API to set the AI device attributes.
    2. Call the **hi\_mpi\_ai\_enable** API to start the AI device.
    3. Call the **hi\_mpi\_ai\_set\_chn\_attr** API to set the AI channel attributes.
    4. Call the **hi\_mpi\_ai\_enable\_chn** API to start the AI channel.
    5. Call the **hi\_mpi\_ai\_enable\_resample** API to enable the AI resampling function.

        Because the AI sampling rate is fixed at 48 kHz, while the G.711a and G.711u protocols support only an 8 kHz sampling rate, the resampling function must be enabled. In contrast, 48 kHz falls within the sampling rate range supported by the AAC protocol, so resampling is not required for AI when the AAC protocol is used.

2. Call the **hi\_mpi\_aenc\_create\_chn** API to **create an audio encoding channel**.
3. Call the **hi\_mpi\_sys\_bind** API to **bind AI and AENC**.

    | AI Device ID | AI Channel Number | AENC Device ID | AENC Channel Number |
| --- | --- | --- | --- |
| 2 | 0 | 0 | 0 |

4. Call **hi\_mpi\_aenc\_get\_stream** in a loop to obtain encoded data. After the encoded data is used, call the **hi\_mpi\_aenc\_release\_stream** API in a timely manner to **release the encoded data**.

    The audio data obtained through the AI device is automatically sent to the corresponding AENC channel for encoding based on the binding relationship in step 3, and is used to send voice to the IP camera.

5. After the voice is sent, in the exit process, first call the **hi\_mpi\_sys\_unbind** API to **unbind AI and AENC**, then call the **hi\_mpi\_aenc\_destroy\_chn** API to destroy the AENC channel, and finally call the **hi\_mpi\_ai\_disable\_resample** API to disable the AI resampling function, the **hi\_mpi\_ai\_disable\_chn** API to disable the AI channel, and the **hi\_mpi\_ai\_disable** API to disable the AI device in sequence.
