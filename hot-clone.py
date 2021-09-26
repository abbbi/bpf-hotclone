import os
import uuid
import time
import glob
import logging
import subprocess
import signal, psutil
from concurrent.futures import ProcessPoolExecutor as Pool

src = "/dev/loop0"
tgt = "DATA"

device = os.stat(src).st_rdev
minor = os.minor(device)
major = os.major(device)
cur = os.path.dirname(os.path.abspath(__file__))

fh = open(src, "rb")

done = False


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(sig)


def callback(future):
    global done
    done = True
    if future.exception() is not None:
        print("MAIN PROCESS EX")
    else:
        print("MAIN PROCESS EX")


def trace_changes():
    with subprocess.Popen(
        ["{}/trace-changes".format(cur), str(major), str(minor)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    ) as tracer:
        for line in iter(tracer.stdout.readline, ""):
            if b"REPLAY" in line:
                time.sleep(0.1)
                print(line.decode().strip())
                rand = uuid.uuid4()
                (_, sector, size, action) = line.decode().split(":")
                fh.seek(int(sector) * 512, 0)
                with open("changeset/{}.{}".format(sector, rand), "wb") as targetfh:
                    targetfh.write(fh.read(int(size)))


def main():
    print("begin waiting")
    pool = Pool(max_workers=2)
    f = pool.submit(subprocess.run, "dd if={} of=DATA".format(src), shell=True)
    f.add_done_callback(callback)

    b = pool.submit(trace_changes)
    while True:
        if done is True:
            pool.shutdown(wait=False)
            kill_child_processes(os.getpid())
            break

    print("data copy finished")

    replayList = glob.glob("changeset/*")
    time.sleep(10)
    if replayList:
        print("replaying changes")
        replayList = glob.glob("changeset/*")
        replayList.sort(key=os.path.getmtime)
        tfh = open(tgt, "wb")
        tfh.seek(0)
        for repl in replayList:
            with open(repl, "rb") as rfh:
                _ = repl.split(".")[0]
                sector = _.split("/")[1]
                tfh.seek(int(sector) * 512, 0)
                tfh.write(rfh.read())
                tfh.seek(0)
            print(sector)
        tfh.close()

    print("done")


if __name__ == "__main__":
    main()
