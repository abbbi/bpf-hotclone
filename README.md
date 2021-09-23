hot clone a running device using BPF trace to get changed data
while copy. Requires bash and bpftrace installed.

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
While copy is running, create a new filesystem on the device:

```
 mkfs.xfs -f /dev/loop0
 ```

Changes to the device are tracked meanwhile using a bpftrace script.
After copy has finished, script replays changes to the device based
on the information from the bpftrace script.

Resulting volumes should match then :)

If you execute this on a running root volume, you may need to execute
from ramfs .. (not tested)


