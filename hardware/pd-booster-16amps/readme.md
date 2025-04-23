# PD Booster (16 amps)

This is a USB-PD power supply that can deliver up to 16 amps at 5V.  It consists of two PCBs, which plug into each other:  a USB-PD controller and a buck-boost converter.

## Theory of Operation

USB-PD is mainly for battery charging, and the idea is that you have a USB-C cable coming into your device from a charger.  The charger initially supplies the standard 5V/2.5A, but you can negotiate over the CC lines side-channel to request both higher current and higher voltages (up to 20V).

Since you don't know in advance what voltage you will get, you need some additional circuitry to step down the voltage whatever you actually want to run at.  In my case, that's 5V.  The buck-boost converter is that additional circuitry:  it will maintain 5V output over the entire range of input voltages from 5V to as high as 20V.

## USB-PD Controller

The first PCB is the USB-PD controller, which is based on [TI TPS25730](https://www.ti.com/lit/ds/symlink/tps25730.pdf?ts=1707773923998&ref_url=https%253A%252F%252Fwww.mouser.at%252F).  It is resistor-strapped to request the highest voltage and current it can get (which would be 20V/5A), but will accept voltages as low as 5V.

## Buck-Boost Converter

The second PCB is the buck-boost converter.  It accepts whatever voltage the USB-PD controller was able to negotiate and regulates it to 5V.


