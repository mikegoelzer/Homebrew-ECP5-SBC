# Homebrew RISC-V Personal Computer

This is the hardware repo for a homebrew "personal computer" designed from scratch down to the logic gate level.  It's based on [my custom RISC-V CPU core](https://github.com/mikegoelzer/riscv) and has all the common peripherals you'd expect on a PC circa the early-2000s.

Be forewarned: this whole project was an educational exercise undertaken as a hobby, so everything is massively over-engineered to maximize the learnings. 🤷‍♀️

## CPU

The CPU is a custom RISC-V core -- pipelined, in-order, 5-stage.  It is written in Verilog and lives its own repo: [mikegoelzer/riscv](https://github.com/mikegoelzer/riscv).

## Hardware

This repo contains the Kicad files for the actual hardware of the computer.  There are several PCBs:

- [Compute Module](./cm/readme.md). This is the heart of the computer:  an FPGA that implements the RISC-V CPU and a DRAM that serves as the computer's main memory. It has two 100-pin Hirose DF13 snap-in connectors on the bottom, which mate with the motherboard.
- [Motherboard](./motherboard/readme.md). The motherboard breaks out the common periperal connectors -- HDMI, VGA, JTAG, and more -- which are driven by the Compute Module.  It also has an SD card to serve as the computer's "hard drive," a boot flash, and some diagnostic LEDs and switches.
- [Power Supply](./pd-booster-16amps/readme.md). Power initially comes into the motherboard via a USB-C cable.  Because I wanted to learn a bit about USB Power Deliver (USB-PD) as part of this project, I designed this plug-in board that negotiates higher voltages and currents and then buck-boost converts them to a stable 5V to power the motherboard.
- [Hat](./hat/readme.md).  This is top board that sits above the motherboard on standoffs and provides a touch screen plus a smaller OLED display for debugging your Verilog.





