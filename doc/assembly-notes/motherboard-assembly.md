# Motherboard Assembly Notes

## Important Notes

- All fine-pitch components on are front side
- LED polarity mark goes toward silkscreen cathode mark (thick line)
	- Also: silkscreen arrow always points toward polarity (cathode) mark
- Power LEDs:
	- (amber) = VBUS\_IN (5V)
	- (white) = +5V rail good
	- (green) = +3.3V rail good
- When placing J3, make sure pins on bottom line up with pads!  Connector can only go one way.
- **IMPORTANT**:  need to cut VBUS trace into TVS. See image at [https://github.com/mikegoelzer/Homebrew-ECP5-SBC/issues/6](github.com/mikegoelzer/Homebrew-ECP5-SBC/issues/6)

## Assembly Instructions

1.  Assemble front side and bake

2.  Assemble back side and bake

3.  Plug the `pd-booster-null` board into 2x4 connector to pull `CC1`/`CC2` down with 5.1k to ground

4.  To test USB-PD:

	- First, cut the trace near `D1` silk screen as described above
	- Replace `pd-booster-null` with `pd-booster-16amps`
	- Plug in USB-C cable to charger that supports USB-PD
	- Check power LEDs