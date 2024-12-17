# PSU Test Instructions

## Indicator LEDs abd Test Points

| LED | Color  | Description |
|-----|--------|-------------|
| D1  | Yellow | Barrel VDC OK |
| D3  | Amber  | 5V buck OK |
| D6  | Green  | +5V rail OK |
| D7  | Green  | +3V3 rail OK |
| D8  | Green  | +2V5 rail OK |
| D9  | Green  | +1V1 rail OK |

| TP  | Color  | Description |
|-----|--------|-------------|
| TP1 | Black  | GND |
| TP2 | (pad)  | Pre-fuse |
| TP3 | (pad)  | Post-fuse |
| TP4 | Yellow | VDC (~12V) |
| TP5 | Red    | 5V buck V_OUT |
| TP6 | Red    | +5V output (after mux, ~4.5V)|

## Testing Procedure

### 1. Make sure barrel jack center hole is +12V relative to outer shell.

### 2. First test 5V buck converter alone:

 - Plug in 12V barrel jack
 - D1 (yellow) should be ON indicating 12V input
 - D3 (amber) should be ON indicating 5V buck output
 - D6 (green) should be ON indicating ~4.5V output after mux
 - TP2 should be 12V
 - TP3 should be 12V
 - TP4 should be 12V (minus diode drop ~0.5V)
 - TP5 should be 5V
 - TP6 must be >= 4.5V
 - D7,D8,D9 should be OFF because DET not shorted to +5V simulating connector plug-in

### 3. Test USB VBUS input alone

 - Unplug 12V barrel jack
 - Apply artificial 5V to EXT VBUS input on J2
 - D1 (yellow) should be OFF indicating 12V input
 - D3 (amber) should be OFF indicating 5V buck output
 - D6 (green) should be ON indicating ~4.5V output after mux
 - TP2,TP3,TP4,TP5 should be all 0V
 - TP6 must be >= 4.5V
 - D7,D8,D9 should be OFF because DET not shorted to +5V simulating connector plug-in

### 4. Test USB VBUS **and** 12V barrel jack

 - Plug in 12V barrel jack
 - Apply artificial 5V to EXT VBUS input on J2
 - D1 (yellow) should be ON indicating 12V input
 - D3 (amber) should be ON indicating 5V buck output
 - D6 (green) should be ON indicating ~4.5V output after mux
 - TP2 should be 12V
 - TP3 should be 12V
 - TP4 should be 12V (minus diode drop ~0.5V)
 - TP5 should be 5V
 - TP6 should be >= 4.5V
 - D7,D8,D9 should be OFF because DET not shorted to +5V simulating connector plug-in

### 5. Measure voltage rails
 - Plug in 12V barrel jack only
 - Short DET to +5V on J2
 - D7,D8,D9 should now come ON
 - Measure +5V rail Vout on J2 with DMM (should be ~4.5V)
 - Measure +3V3 rail Vout on J2 with DMM (should be ~3.30V)
 - Measure +2V5 rail Vout on J2 with DMM (should be ~2.50V)
 - Measure +1V1 rail Vout on J2 with DMM (should be ~1.10V)

