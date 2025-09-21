---
layout: default
title: How to make custom 4-channel BRSTMs (for MKWii specifically)
---
### How to make custom 4-channel BRSTMs (for MKWii specifically) ###

**Note**: this tutorial only applies to 4 channel BRSTMs (in MKWii, they are all lowercase named `.brstm` files). 
Some courses, such as Koopa Cape or Moonview Highway, are named `STRM_N_*.brstm` and they have extra audio channels for some sections of the track. These are more complicated to do and I haven't yet had time to mess with those.

**Prerequisites**:

- The music files you want to replace, in .wav format (you can convert them to WAV using `ffmpeg`: `ffmpeg -i in.mp3 out.wav`)
- A copy of [BrawlCrate](https://github.com/soopercool101/BrawlCrate)

**Steps**:

1) Open BrawlCrate and go into File > New > BRSTM Audio Stream.

2) Pick your .wav file. To avoid the song restarting, pick one that is at least the duration of an average race on that track.

3) If you want, trim the song. Keep the loop flag so the song will loop. Keep encoding as ADPCM.

4) Click "Okay": the song will now be rendered to a BRSTM stream.

5) Go to Edit > Export (or do CTRL+E) and save the file. Now you will have a .brstm file.

6) Rename the file accordingly: you can find all the file names you need [here](https://mariokartwii.com/showthread.php?tid=275).
For example, if you want to make a custom song for Mario Circuit, the file will need to be named `n_circuit32_n.brstm` (for the first 2 laps)

Reminder: MKWii uses a different file for the audio stream for the third lap of every course (it doesn't speed up the songs in real time), so you will need to create another .brstm file ending with `_f` (for example, Maple Treeway third lap is `n_maple_f.brstm`)

You can make a sped-up version that matches the speed-up seen in the game by using [Final Lap Stream Maker](https://wiki.tockdom.com/wiki/Final_Lap_Stream_Maker); you just need to drag&drop the non-sped-up BRSTM file (or select it with the file picker), let it do its job, and remember to name the file with a trailing `_f`.

7) Normally at this point you would need to patch `revo_kart.brsar`, because the file contains information about all the start, end and loop points for all audio files. But CTGP-R does this for you: there is an appropriately named setting in CTGP. Keep it enabled (it should be automatically enabled though).
I have never tried to edit `revo_kart.brsar` this way, so I have no idea on how to do it.

8) If you have CTGP-R or another mod that supports the My Stuff folder, put your new and renamed .brstm files in My Stuff. Else, you can try patching the ISO with `wit` ([Wiimms ISO Tools](https://wit.wiimm.de/)) or making a Riivolution mod. I have never used these tools before so I can't help you there.