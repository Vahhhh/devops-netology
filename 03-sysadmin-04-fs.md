#Ответы

1. Почитал, не всё понял... Точнее принцип то понял, что для ускорения используется понял, но это же усложняет весь процесс и ведёт к фрагментации.. 

2. Нет, не может, потому что по факту это один и тот же файл, и inode у него одинаковый. А судя по структуре данных системного вызова STAT (из презентации), идентифицировать файл мы можем по id устройства + inode. Т.к. в случае с hardlink'ом эти параметры совпадают, то и всё остальное также совпадает. К тому же если это контейнер метаданных файла, то получается тот самый inode и содержит те самые права доступа.. :)

3-13. done
```
sudo fdisk /dev/sdb
sudo sfdisk --dump /dev/sdb > sdb.dump ; sudo sfdisk /dev/sdc < sdb.dump (потом пересмотрел и понял что можно было как sudo sfdisk --dump /dev/sdb | sudo sfdisk /dev/sdc)
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
sudo fdisk /dev/sdb
sudo fdisk /dev/sdc (не стал по аналогии копировать таблицу, ибо подумал что раз рейд создан, структура/метаданные поменялись)
sudo mdadm --create --verbose /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
sudo pvcreate -v /dev/md0 /dev/md1
sudo vgcreate -v VG_1 /dev/md0 /dev/md1
sudo lvcreate -L 100m -n logical_vol_1 VG_1 /dev/md1
sudo mkfs.ext4 /dev/VG_1/logical_vol_1
sudo mount /dev/VG_1/logical_vol_1 /tmp/new/
```

14. 
```
vagrant@vagrant:~$ lsblk
NAME                     MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                        8:0    0   64G  0 disk
├─sda1                     8:1    0  512M  0 part  /boot/efi
├─sda2                     8:2    0    1K  0 part
└─sda5                     8:5    0 63.5G  0 part
  ├─vgvagrant-root       253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1     253:1    0  980M  0 lvm   [SWAP]
sdb                        8:16   0  2.5G  0 disk
├─sdb1                     8:17   0    2G  0 part
│ └─md0                    9:0    0    2G  0 raid1
└─sdb2                     8:18   0  511M  0 part
  └─md1                    9:1    0 1018M  0 raid0
    └─VG_1-logical_vol_1 253:2    0  100M  0 lvm   /tmp/new
sdc                        8:32   0  2.5G  0 disk
├─sdc1                     8:33   0    2G  0 part
│ └─md0                    9:0    0    2G  0 raid1
└─sdc2                     8:34   0  511M  0 part
  └─md1                    9:1    0 1018M  0 raid0
    └─VG_1-logical_vol_1 253:2    0  100M  0 lvm   /tmp/new

vagrant@vagrant:~$ lsblk --fs
NAME                     FSTYPE            LABEL     UUID                                   FSAVAIL FSUSE% MOUNTPOINT
sda
├─sda1                   vfat                        B948-9FE7                                 511M     0% /boot/efi
├─sda2
└─sda5                   LVM2_member                 TZbwMD-a0Qb-woZw-qWrn-gRm6-CYIy-kY6lY6
  ├─vgvagrant-root       ext4                        9ceb8696-d8c5-4f0d-803d-4652d6dc7a23     56.6G     3% /
  └─vgvagrant-swap_1     swap                        250fa0bc-9d2b-4dd7-948e-8f2aa022463b                  [SWAP]
sdb
├─sdb1                   linux_raid_member vagrant:0 5eec6240-7b0c-be4d-329b-1ea5c31718fa
│ └─md0                  LVM2_member                 zRGvvn-Xxld-D05s-ZA6s-FlL7-EgA8-TzYThV
└─sdb2                   linux_raid_member vagrant:1 88a749e8-4de6-a2d5-b25d-cbc80a3d42f4
  └─md1                  LVM2_member                 2yuTem-utef-jYFR-DzQ8-XypE-4NlQ-DqArUY
    └─VG_1-logical_vol_1 ext4                        6a17849f-0167-4ed8-a24b-9324845ad3d1     67.5M    20% /tmp/new
sdc
├─sdc1                   linux_raid_member vagrant:0 5eec6240-7b0c-be4d-329b-1ea5c31718fa
│ └─md0                  LVM2_member                 zRGvvn-Xxld-D05s-ZA6s-FlL7-EgA8-TzYThV
└─sdc2                   linux_raid_member vagrant:1 88a749e8-4de6-a2d5-b25d-cbc80a3d42f4
  └─md1                  LVM2_member                 2yuTem-utef-jYFR-DzQ8-XypE-4NlQ-DqArUY
    └─VG_1-logical_vol_1 ext4                        6a17849f-0167-4ed8-a24b-9324845ad3d1     67.5M    20% /tmp/new
```

15. 
```
vagrant@vagrant:~$ gzip -t /tmp/new/test.gz ; echo $?
0
```

16. 
```
sudo pvmove /dev/md1 /dev/md0

lsblk --fs
NAME                     FSTYPE            LABEL     UUID                                   FSAVAIL FSUSE% MOUNTPOINT
sda
├─sda1                   vfat                        B948-9FE7                                 511M     0% /boot/efi
├─sda2
└─sda5                   LVM2_member                 TZbwMD-a0Qb-woZw-qWrn-gRm6-CYIy-kY6lY6
  ├─vgvagrant-root       ext4                        9ceb8696-d8c5-4f0d-803d-4652d6dc7a23     56.6G     3% /
  └─vgvagrant-swap_1     swap                        250fa0bc-9d2b-4dd7-948e-8f2aa022463b                  [SWAP]
sdb
├─sdb1                   linux_raid_member vagrant:0 5eec6240-7b0c-be4d-329b-1ea5c31718fa
│ └─md0                  LVM2_member                 zRGvvn-Xxld-D05s-ZA6s-FlL7-EgA8-TzYThV
│   └─VG_1-logical_vol_1 ext4                        6a17849f-0167-4ed8-a24b-9324845ad3d1     67.5M    20% /tmp/new
└─sdb2                   linux_raid_member vagrant:1 88a749e8-4de6-a2d5-b25d-cbc80a3d42f4
  └─md1                  LVM2_member                 2yuTem-utef-jYFR-DzQ8-XypE-4NlQ-DqArUY
sdc
├─sdc1                   linux_raid_member vagrant:0 5eec6240-7b0c-be4d-329b-1ea5c31718fa
│ └─md0                  LVM2_member                 zRGvvn-Xxld-D05s-ZA6s-FlL7-EgA8-TzYThV
│   └─VG_1-logical_vol_1 ext4                        6a17849f-0167-4ed8-a24b-9324845ad3d1     67.5M    20% /tmp/new
└─sdc2                   linux_raid_member vagrant:1 88a749e8-4de6-a2d5-b25d-cbc80a3d42f4
  └─md1                  LVM2_member                 2yuTem-utef-jYFR-DzQ8-XypE-4NlQ-DqArUY
```

17. 
`sudo mdadm --fail /dev/md0 /dev/sdc1`

18.
```
cat /proc/mdstat
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10]
md1 : active raid0 sdc2[1] sdb2[0]
      1042432 blocks super 1.2 512k chunks

md0 : active raid1 sdc1[1](F) sdb1[0]
      2094080 blocks super 1.2 [2/1] [U_]

unused devices: <none>

[10667.304565] md/raid1:md0: Disk failure on sdc1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.
```               
               
19. 
```
vagrant@vagrant:~$ gzip -t /tmp/new/test.gz ; echo $?
0
```
