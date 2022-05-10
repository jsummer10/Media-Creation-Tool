# Bootable Media Creation Tool

This program uses a downloaded iso file to create bootable media. Note: this software is intended to only be used on MacOS. 

## How-To

Prior to running, format the intended device using disk utility. Next, run the run.py python file with the iso file via terminal using the following command

```
python run.py -f /path/to/iso/file.iso
```

There is also an optional argument that can be used for the intended disk number. If this is not passed in, the disk selection utility will be run. The disk number can be found using disk utility. Only the number at the end should be entered.

```
python run.py -f /path/to/iso/file.iso -d [your disk number here (e.g. 4)]
```
