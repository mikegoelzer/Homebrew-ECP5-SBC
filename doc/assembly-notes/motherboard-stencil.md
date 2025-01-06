# Solder Paste Stencil Notes

For Rev 1:

- Front stencil: aluminum 0.1mm, back stencil: doesn't matter
- "Solder paste relative clearance" settings on pads varies by component lead pitch:
	- For ≤ 0.5mm pitch components:  `-10%` in Kicad (approximately 35% volume reduction)
	- For 0.65mm pitch components:   `-7.5%` in Kicad (~28% reduction)
	- For ≥ 1.0mm  pitch components: `-5%` in Kicad (~19% reduction) or `0`

See [kicad-stencil-aperture-calcs.xlsx](./kicad-stencil-aperture-calcs.xlsx) for volume reduction empirical findings.
