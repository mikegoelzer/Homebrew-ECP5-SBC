# Compute Module

The Compute Module (CM) is the heart of the computer.  It has the two things that every computer needs:  a processor and memory.  

### Features

- ECP5U 85K FPGA
- 1.1V, 2.5V and 3.3V buck regulators for the FPGA's voltage rails
- Supply sequencer to bring voltage rails up and down "correctly" (see below)
- 16MB DRAM
- 25MHz oscillator
- Bitstream SPI flash chip
- 100-pin Hirose DF13 snap-in connectors on the bottom

### Power

The Compute Module is powered by a 5V input.  The 1.1V and 2.5V and 3.3V rails are produced by three TI buck regulators.

The ECP5 should not require a rail sequencer, but I included one (based on a design borrowed from Trellis Board) because I've seen other ECP5 boards get into weird states that seem like they may be caused by rail ramp rate problems.  Thus, the rail sequencing complies strictly with the ECP5's datasheet, at a cost of two extra chips.

### Electrical and Mechanical Connections

The basic idea with the CM is that you use it by snapping it into some larger board -- in my case, the [the motherboard](../motherboard/readme.md) in this repo.  This is the purpose of the two 100-pin Hirose DF13 male connectors on the bottom of the CM.  Everything, even power andJTAG, is brought out solely through these connectors.

The connectors and overall size and shape were inspired by the Raspberry Pi Compute Module 3 (CM3).  I wasn't able to maintain the same pinout as the Pi CM3 because I needed to bring out more IOs and wanted to run off a 5V input.

### Clock Speed

The FPGA includes several PLLs, so the 25 MHz oscillator in this circuit enables the CPU to run at 100 MHz.  

While the CPU itself would probably run fine at higher clock speeds, the DRAM is rated for a maximum speed of 133 MHz.  The memory controller is simplified considerably when you can get results back from DRAM in one clock cycle, so I just run everything in a single 100 MHz clock domain.
