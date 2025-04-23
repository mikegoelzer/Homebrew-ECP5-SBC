# Hat

This is the top board that sits above the motherboard on standoffs and provides a touch screen plus a smaller OLED display for debugging the CPU's Verilog.

## OLED

The OLED is an 0.95" (96x64) SSD1331 display.  It is controlled via SPI entirely in Verilog.  I use it for very low-level debugging of the CPU itself, e.g., to display a register value or dump the contents of memory.

## Touch Screen

The touch screen is [this cool 2.8" 240x320 TFT LCD from Adafruit](https://www.adafruit.com/product/2090).  It is intended to be under software control rather than at the Verilog level.

## Power

Power is provided by the flat-flexible cable coming from the motherboard.  It is the same 5V supply as the motherboard itself.