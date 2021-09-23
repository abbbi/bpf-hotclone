hot clone a running device using BPF trace to get changed data
while copy. Requires bash, grep, dd and bpftrace.

Inspired by hot-clone:

 https://github.com/benjojo/hot-clone

Its all hardcoded, go figure ..

Testsetup:
```
 modprobe loop
 truncate -s 10G mydisk
 losetup /dev/loop0
```

Checkout major/minor number of created loopback device and change the `trace-changes`
script.
 
Now attempt to hot clone the device (it will copy the data to the local directory).
Requires root.

```
 # ./hot-clone
```
 
While copy is running, create a new filesystem on the device, or write data to it.. somehow.

```
 mkfs.xfs -f /dev/loop0
 ```

Changes to the device are tracked meanwhile using a bpftrace script.
After copy has finished, script replays changes to the device based
on the information from the bpftrace results.

Resulting volume contents may match (hopefully) :)

If you execute this on a running root volume, you may need to execute
from ramfs, or a network file system .. (not tested)


