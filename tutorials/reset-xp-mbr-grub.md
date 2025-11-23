---
layout: default
title: How to reinstall Windows XP's MBR after removing GRUB
---
### How to reinstall Windows XP's MBR after removing GRUB ###

Installing GRUB always overwrites your Master Boot Record; so what if you don't want to dualboot anymore, freeing up some space on your dual booting XP machine?

1) Start `diskmgmt.msc` as an administrator.

2) Delete all partitions related to Linux - they are usually of an unrecognized file system. If you try to delete them and Windows tells you that they were made by another operating system, you are deleting the right partitions. 

Don't delete anything else, especially OEM recovery partitions (they are usually FAT16 or FAT32).

3) You should now have a bricked GRUB install that boots to a rescue prompt. That's good, actually.

4) Grab any XP install media and start it. At the prompt, press R to enter the recovery console.

5) Select the Windows installation you want to repair; then run `fixmbr` and `fixboot`. Restart the computer.

6) If you have an OEM recovery partition, the computer should boot into it and allow you to start the recovery. 

Note: the system can bootloop into the recovery partition if the OEM made some really crappy recovery software; in that case, you may need to mark the Windows partition as active. I think you can do that with `fdisk`.

7) You should now have an unbricked Windows XP install.

8) (optional) Open `diskmgmt.msc` again and either expand the Windows partition to take the now free space, or create a new partition from the now free space.
