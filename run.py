"""
Application : Media Creation Tool
File name   : run.py
Authors     : Jacob Summerville
Description : This file converts an iso into bootable media
"""

import argparse
import os
import subprocess
import sys

def get_arguments():
    """ Get command line arguments """
    parser = argparse.ArgumentParser(description='Makes bootable media')

    parser.add_argument('-f', '--file', help='iso file')
    parser.add_argument('-d', '--disk', help='disk number')

    return parser.parse_args()


def cli_command(opts):
    """ Run command line interface commands """
    output = subprocess.run(opts, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return output.returncode


def convert_ISO (iso_file, img_file, dmg_file):
    """ Convert the ISO file provided into an image to use """
    print('Converting the iso to an image...')
    status = cli_command(['hdiutil', 'convert', '-format', 'UDRW', '-o', img_file, iso_file])
    if status !=0:
        print('Error converting file:', img_file)
        sys.exit()

    status = cli_command(['mv', dmg_file, img_file])
    if status !=0:
        print('Error renaming file:', img_file)
        sys.exit()


def unmount_disk (disk):
    """ Unmount the specified disk """
    print('Unmounting Disk...')
    status = cli_command(['diskutil', 'unmountDisk', '/dev/disk' + disk])
    if status !=0:
        print('Error unmounting disk' + disk)
        sys.exit()


def eject_disk (disk_number):
    """ Eject the specified disk """
    print('\nEjecting Disk...')
    status = cli_command(['diskutil', 'unmountDisk', '/dev/disk' + disk_number])
    if status !=0:
        print('Error ejecting disk' + disk)
        sys.exit()


def create_installer (file, disk):
    """ Create the bootable media on the specified disk using the created image """
    print('\nCreating bootable drive - This may take a few minutes')
    status = cli_command(['sudo', 'dd', 'if=' + file, 'of=/dev/rdisk' + disk, 'bs=1m'])
    if status !=0:
        print('Error creating the bootable drive')
        sys.exit()

    print('\nBootable drive created')


def main ():
    """ Main function for the media creation tool """ 
    args = get_arguments()

    if not (args.file and os.path.isfile(args.file)):
        print('Please enter an iso file')
        sys.exit()

    if not args.disk:
        print('Please enter the disk number of the flash drive')
        sys.exit()

    print('\n=====================')
    print(' Media Creation Tool')
    print('=====================\n')

    iso_file = str(args.file)
    img_file = iso_file.replace('.iso', '.img')
    dmg_file = img_file + '.dmg'
    disk = str(args.disk)

    print('ISO:', iso_file)
    print('Disk:', disk, '\n')

    if os.path.isfile(img_file):
        os.remove(img_file)

    if os.path.isfile(dmg_file):
        os.remove(dmg_file)

    convert_ISO(iso_file, img_file, dmg_file)
    unmount_disk(disk)
    create_installer(img_file, disk)
    eject_disk(disk)

    print('\n\nYou may now unplug the bootable media\n')

if __name__ == '__main__':
    main()
