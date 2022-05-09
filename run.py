"""
Application : Media Creation Tool
File name   : run.py
Authors     : Jacob Summerville
Description : This file converts an iso into bootable media using MacOS
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


def select_disk():
    """ Select disk to use for bootable media """
    result = subprocess.run(['df', '-h'], capture_output=True, text=True)

    if result.returncode != 0:
        print('Unable to detect media')
        sys.exit()

    disk_list = result.stdout.split('\n')
    parsed_disk_list = []

    # parse disks that can't be used out
        disk = disk.strip()
        if disk == disk_list[0] or '/dev/disk' in disk:
            parsed_disk_list.append(disk)

    # display possible disk options
    print('\nDisk selection for bootable media\n')
    print('  ', parsed_disk_list[0])
    for i in range(1, len(parsed_disk_list)):
        print(str(i) + ')', parsed_disk_list[i])

    # prompt use for disk selection and confirmation
    while True:
        selection = input('\nSelect which disk to use: ')
        try: 
            selection = int(selection)
        except:
            print('Please enter a number')
            continue

        max_select = len(parsed_disk_list) - 1
        if selection < 1 or selection > max_select:
            print('Please enter a number between 1 and', max_select)
            continue

        selected_disk = parsed_disk_list[selection].split()[0] 
        print('You selected', str(selection) + ':', selected_disk)
        
        confirm = input('\nIs this correct (y/n): ')

        if confirm.lower() == 'y':
            break

    print('')

    selected_disk = selected_disk.replace('/dev/disk', '')

    if 's' in selected_disk:
        selected_disk = selected_disk.split('s')[0]

    return selected_disk


def cli_command(opts):
    """ Run command line interface commands """
    result = subprocess.run(opts, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return result.returncode


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

    print('\n=====================')
    print(' Media Creation Tool')
    print('=====================\n')

    args = get_arguments()

    if not (args.file and os.path.isfile(args.file)):
        print('Please enter an iso file')
        sys.exit()

    if args.disk:
        disk = str(args.disk)
    else:
        disk = select_disk()

    iso_file = str(args.file)
    img_file = iso_file.replace('.iso', '.img')
    dmg_file = img_file + '.dmg'

    print('ISO:', iso_file)
    print('Disk:', disk, '\n')

    return

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
