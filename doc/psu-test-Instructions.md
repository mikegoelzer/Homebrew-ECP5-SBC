# PSU Test Instructions

## Warnings

**IMPORTANT:**  `J2` and `J3` should **never** both be gang shunted simultaneously.

Here is the logic of `J2` and `J3`:
| J2 Shunted | J3 Shunted | Circuit State |
|------------|------------|---------------|
| No         | No         | Circuit is off. Barrel jack not connected to anything. |
| Yes        | No         | Fuse circuit is the only power path. |
| No         | Yes        | Fuse circuit bypassed and barrel jack directly feeds the buck. |

## Indicator LEDs abd Test Points

| LED | Color  | Description |
|-----|--------|-------------|
| D1  | Yellow | Barrel powering eFuse; check TP3 if no D2 |
| D2  | Yellow | VDC supplied via eFuse path |
| D3  | Green  | VDC on (either path) |
| D4  | Amber  | 5V output OK |

| TP  | Description |
|-----|-------------|
| TP1 | GND |
| TP2 | eFuse V_ISENSE (1mV/mA) |
| TP3 | eFuse FAULT output; see datasheet to interpret voltage levels |
| TP4 | 5V buck V_OUT |

## Testing Procedure

### 1. Make sure barrel jack is +12V relative to outside.

### 2. First test buck converter alone:

 - Unplug barrel jack.
 - Install **only** J3 bypass gang shunt.
 - Plug in 12V barrel jack.
 - D1 (yellow) and D2 (also yellow) will be OFF.
 - D3 (green) will be ON.

### 3. Measure 5V at output.

### 4. Measure 3.3V at output.

### 5. Measure 12V at input.
