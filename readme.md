# Homebrew RISC-V Computer

This is the hardware repo for a homebrew "personal computer" designed from scratch down to the logic gate level.

The computer is based on [my custom RISC-V CPU core](https://github.com/mikegoelzer/riscv) (pipelined, in-order, 5-stage) and has all the common peripherals you'd expect on a PC circa the early-2000s like USB, HDMI, keyboard and mouse, etc.

This repo is focused specifically on the PCBs necessary to build the complete computer.

## Hardware

In this repo, you'll find all the Kicad files and bills of materials needed to construct the entire computer.  There are several PCBs:

- [Compute Module](./hardware/cm/readme.md). This is the heart of the computer:  an FPGA that implements the RISC-V CPU and some SDRAM that serves as the computer's main memory. It has two 100-pin Hirose DF13 snap-in connectors on the bottom, which mate with the motherboard.
- [Motherboard](./hardware/motherboard/readme.md). The Compute Module snaps into this motherboard, which breaks out the common PC periperal interfaces, like HDMI, VGA, JTAG, and more.  It also has an SD card to serve as the computer's "hard drive," a boot flash, and some diagnostic LEDs and switches.
- [Power Supply](./hardware/pd-booster-16amps/readme.md). Power initially comes into the motherboard via a USB-C cable.  Because I wanted to learn a bit about USB Power Deliver (USB-PD) as part of this project, I designed this plug-in board that negotiates higher voltages and currents and then buck-boost converts them to a stable 5V to power the motherboard.
- [Hat](./hardware/hat/readme.md).  This is a top board that sits above the motherboard on standoffs and provides a touch screen plus a smaller OLED display for debugging your Verilog.  The name is, of course, inspired by the Pi HAT, though it bears no electrical or mechanical resemblance.

## About this project

This project was a personal hobby exercise that I pursued on and off over a couple of years.  Everything is massively over-engineered because I was trying to maximize my learnings. 🤷‍♀️

## Acknowledgements

This hardware was heavily inspired by the [ULX3S](https://radiona.org/ulx3s/), which I consider the best low-cost Lattice ECP5 FPGA board ever created.

I also borrowed ideas from several other open-source ECP5 designs:

- [Lattice ECP5 Eval Board](https://www.latticesemi.com/products/developmentboardsandkits/ecp5evaluationboard)
- [Trellis Board](https://github.com/gatecat/TrellisBoard).  Not sure if this was ever sold to the public, but this guy's design is utterly brilliant.
- [Orange Crab](https://github.com/orangecrab-fpga/orangecrab-hardware)

## License

This material is licensed under `CERN-OHL-S v2` (or later), a strong "copyleft" license. If you require more permissive terms or patent protection, please contact the author. A copy of the license can be found in the [LICENSES](./LICENSES) directory.

Copyright © 2025 Mike Goelzer <mike@goelzer.org>