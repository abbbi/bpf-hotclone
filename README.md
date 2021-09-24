hot clone a in use block device using BPF trace to get changed data
while copy. Requires bash, grep, dd and bpftrace. !POC!

Inspired by hot-clone:

 https://github.com/benjojo/hot-clone

Its all hardcoded, go figure ..

Testsetup:
```
 modprobe loop
 truncate -s 10G mydisk
 losetup /dev/loop0
```

Now attempt to hot clone the device (it will copy the data to the local directory).
Requires root.

```
 # ./hot-clone /dev/loop0 mydata
```
 
While copy is running, create a new filesystem on the original device, or write
data to it.. somehow.

```
 mkfs.xfs /dev/loop0 -f; mount /dev/loop0 /mnt; echo foo > /mnt/FILE; umount /mnt
```

Changes to the device are tracked meanwhile using a bpftrace script and stored
in a local folder (./changeset/)

After copy has finished, script replays changes to the target device based
on the information from changeset catched by the bpftrace results.

Resulting volume contents should have a consistent state (or in case of the
provided example, match byte by byte)

If you attempt to hot-copy a running root volume, you may want to execute
from ramfs, or a network file system .. (not tested)
