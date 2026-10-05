# Lunar Settlement Water

**Why this matters:** Elvis and McDowell (2026) argue that on the Moon, power is a weak constraint and water is the hard limit. Even a generous billion tons of polar ice lasts only about a century for a city of a million people recycling at the ISS's best rate. Past a population of about 100,000, a settlement either recycles far better than the ISS or imports water. This model reproduces their arithmetic so it can be rerun with other assumptions.

Model: [`models/lunar_settlement_water.py`](../models/lunar_settlement_water.py), run with `python models/lunar_settlement_water.py`.

Source: M. Elvis and J. C. McDowell, "No cities on the Moon: a billion tons of water is not enough for sustainability", *Frontiers in Space Technologies* 7:1894104 (2026), [doi:10.3389/frspt.2026.1894104](https://doi.org/10.3389/frspt.2026.1894104), open access under CC BY.

## Method

A population `N` uses `m` tons of water per person per year and recycles a fraction `e`:

```
net loss per year      = N * m * (1 - e)
years until ice is gone = M / (N * m * (1 - e))
import to stay supplied = N * m * (1 - e)  tons per year
```

## Inputs from the paper

| Input | Value | Note |
|---|---|---|
| Local ice inventory `M` | 1 billion tons | The paper calls this a generous baseline |
| Water use `m` | 500 t per person per year | Table 2: drinking and hygiene 125, breathing 2, growing food 500. The paper assumes improved cultivation halves food water, about 500 in total |
| Lander payload | 1,000 t | The paper's import example |

## Result: years until 1 billion tons is used up

| Recycling | 100,000 people | 1,000,000 people |
|---|---|---|
| 0% | 20 | 2 |
| 94% | 333 | 33 |
| 98% (ISS best) | 1,000 | 100 |
| 99% | 2,000 | 200 |
| 99.9% | 20,000 | 2,000 |

The paper's Table 3 prints 330 for 94% at 100,000 people; the formula gives 333.

## Import demand

A city of 1 million people recycling 98% loses **10 million tons of water a year**. Replacing that by import takes **about 27 landers per Earth day** at 1,000 t each, which the paper calls substantial but not inconceivable.

## Limitations

Linear depletion at constant population and usage. Rocket propellant made from the same ice (the paper lists 1,200 t per Starship-class second stage) is not drawn down here, so real depletion would be faster. No recovery of water lost to space or regolith.
