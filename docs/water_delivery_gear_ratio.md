# Water Delivery Gear Ratio (Earth vs Moon)

**Why this matters:** water is both a crew consumable and a propellant. Whether off-Earth water pays off depends on one number per destination: how much mass has to be moved or mined to deliver 1 kg of water there. This note puts that number on a table using public delta-v values.

Model: [`models/water_delivery_gear_ratio.py`](../models/water_delivery_gear_ratio.py) (standard library only, runs with `python models/water_delivery_gear_ratio.py`).

## Method

One expendable chemical stage per leg, with stage dry mass a fixed fraction `s` of its propellant:

```
R   = exp(dv / (g0 * Isp))
p/P = (R - 1) / (1 + s - s R)        propellant per kg of water delivered
```

- **Earth-sourced:** mass that must already be in LEO per kg delivered = `1 + p(1 + s)`. The Earth-to-LEO ascent (9.3 to 10 km/s) is common to every row and is not included, so these figures understate the true Earth cost.
- **Lunar-sourced:** lunar water mined per kg delivered = `1 + p`, because the H2/O2 propellant is electrolyzed from the same water. Stage hardware is not water and is not counted.

Delta-v values come from Wikipedia, *Delta-v budget*, table "Earth-Moon space, high thrust" (LEO-Ken, returns to LEO assume aerobraking).

## Result (Isp 450 s, s = 0.10)

| Destination | dv from LEO (km/s) | dv from Moon surface (km/s) | Earth: kg in LEO per kg delivered | Moon: kg of water mined per kg delivered |
|---|---|---|---|---|
| LEO | 0 | 2.74 | 1.00 | 1.94 |
| GEO | 4.33 | 3.92 | 3.20 | 2.67 |
| EML-1 | 3.77 | 2.52 | 2.72 | 1.83 |
| LLO | 4.04 | 1.87 | 2.94 | 1.56 |

## Reading it

- Beyond LEO, lunar water needs less moved mass per delivered kilogram than Earth water at every destination in the table, before counting the Earth-to-LEO launch that every Earth-sourced kilogram has already paid for.
- The two columns are in different currencies: a kilogram in LEO is a launched kilogram, while a kilogram mined on the Moon is regolith processing plus power. The crossover therefore depends on the cost of mining and electrolysis relative to launch, which this model leaves open.
- EML-1 is the natural depot point: it is cheap to reach from the lunar surface (2.52 km/s) and cheap to leave toward LEO with aerobraking (0.77 km/s).

## Limitations

Screening model only. No boil-off, transfer losses, reusable tankers, mining plant mass, or cost. A reusable lunar tanker would improve the lunar column. Excess oxygen from running fuel-rich of stoichiometric is ignored. Override `DV_FROM_LEO`, `DV_FROM_MOON_SURFACE`, `isp` and `dry_frac` for a specific architecture.
