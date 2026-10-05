# Crew Water Loop

**Why this matters:** water is the largest crew consumable by mass. How much a station or vehicle has to receive depends less on how much the crew drinks than on how well the loop recycles urine and humidity, and on how much water is split to make oxygen.

Model: [`models/crew_water_loop.py`](../models/crew_water_loop.py), run with `python models/crew_water_loop.py`. The same model is proposed as an interactive calculator in [sidus-tools PR #212](https://github.com/massimodeluisa/sidus-tools/pull/212).

## Method

All rates are per crewmember-day.

```
demand    = potable + hygiene + flush + o2 * (2 M_H2O / M_O2)
recovered = eta_urine * (urine + flush) + eta_condensate * condensate + eta_hygiene * hygiene
makeup    = max(0, demand - recovered)
mission   = makeup * crew * days * (1 + reserve)
```

Splitting water for breathing oxygen (2 H2O -> 2 H2 + O2) uses about 1.126 kg of water per kg of O2. Set `o2 = 0` when oxygen is shipped as gas.

## Defaults

| Input | Value (kg per crew-day) | Source |
|---|---|---|
| Potable (drink 2.00 + food rehydration 0.50) | 2.5 | NASA BVAD Rev2, Table 4-20 |
| Hygiene | 0.4 | BVAD Rev2, Table 4-20, ISS column |
| Urinal flush | 0.3 | BVAD Rev2, Tables 4-20 and 4-21 |
| Urine | 1.2 | BVAD Rev2, Table 4-21 |
| Humidity condensate | 2.27 | BVAD Rev2, Table 4-21 |
| O2 made by electrolysis | 0.82 | ISS-order daily oxygen use |
| Urine recovery | 0.85 | ISS US-segment Urine Processor Assembly, BVAD Rev2 section 4.3.3 |
| Condensate recovery | 1.0 | Water Processor Assembly, near-complete |
| Hygiene recovery | 0 | ISS does not collect hygiene greywater |

For context, NASA reported 93 to 94% total ISS water recovery before the Brine Processor Assembly and 98% after (2023).

## Result (4 crew, 180 days, 10% reserve)

| Quantity | Value |
|---|---|
| Demand per crew-day | 4.123 kg (0.923 kg of it for O2) |
| Recovered per crew-day | 3.545 kg |
| Makeup per crew-day | 0.578 kg |
| Loop closure | 86.0% |
| Water to supply | 458 kg |
| Same mission with no recycling | 3,266 kg |
| Supply avoided by recycling | 2,808 kg |

## Limitations

Steady-state mass balance. No storage dynamics, Sabatier water return, brine or filter consumables, leaks or EVA water. A planning estimate, not a flight logistics plan.
