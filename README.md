hot clone a in use block device using BPF trace to get changed data
while copy.

Inspired by hot-clone:

 https://github.com/benjojo/hot-clone

Implemented in python.

Testsetup:
```
 modprobe loop
 truncate -s 2G mydisk
 losetup /dev/loop0 mydisk
 mkfs.xfs /dev/loop0
 mount /dev/loop0 /mnt
```

Now attempt to hot clone the device (it will copy the data to the local directory).
Requires root.

```
 # ./hot-clone clone --source /dev/loop0 --target BACKUP --changedir changes
 [..]
 Replay: sector [1611120640] from [changes/3146720.1992]
 done

```
 
While copy is running, create a new filesystem on the original device, or write
data to it if already mounted (dont forget to sync).

```
 # cp -r /etc/ /mnt/; sync
```

Changes to the device are tracked meanwhile using a bpftrace script and stored
in a local folder (changes)

After copy has finished, script replays changes to the target device based
on the information from changeset catched by the bpftrace results.

Resulting volume contents should have a consistent state (or in case of the
provided example, match byte by byte)

If you attempt to hot-copy a running root volume, you may want to execute
from ramfs, or a network file system .. (not tested)
