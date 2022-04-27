## Debugging

If you are asked to send debug info or want to fix bugs, follow the guide
displayed when [opening a new bug report](https://github.com/atar-axis/xpadneo/issues/new?template=bug_report.md).
This has all the hints to get you started with debugging. You may also want
to increase the kernel debug level if your distribution sets it very low.
Otherwise, the driver reports most incidents, quirks, and fixes to `dmesg`.


### Environment

Useful information can now be aquired with the commands:

  * `dmesg`: I advise you to run `dmesg -wdH` in a terminal while you connect your controller from a second terminal
    to get hardware information in realtime.
  * `modinfo hid_xpadneo`: get information on xpadneo as a kernel module.
  * When your gamepad is connected, get the HID report descriptor:

```bash
xxd -c20 -g1 /sys/module/hid_xpadneo/drivers/hid:xpadneo/0005:045E:*/report_descriptor | tee >(cksum)
```


### Generated Events

If you are asked to supply the events generated by xpadneo, please run the following command:
```
perl -0777 -l -ne 'print "/dev/input/$1\n" if /Name="Xbox Wireless Controller".*Handlers.*(event[0-9]+)/s' /proc/bus/input/devices | xargs evtest
```

Do whatever you think does not behave correctly (e.g. move the sticks from left to right if you think the range
is wrong) and upload the output.


### HID device descriptor (including checksum)

If we ask you to supply the device descriptor, please post the output of the following command:
```bash
xxd -c20 -g1 /sys/module/hid_xpadneo/drivers/hid:xpadneo/0005:045E:*/report_descriptor | tee >(cksum)
```


### Bluetooth Connection

Some debugging needs a deeper low level look. You can do this by running `btmon`:
```bash
sudo btmon | tee xpadneo-btmon.txt
```

Then reproduce the problem you are observing.

We probably also need some information about the dongle:

  * Run `lsusb` and pick the device number of your dongle.
  * Run `lsusb -v -s## | tee xpadneo-lsusb.txt` where `##` is the device number picked in the previous step.