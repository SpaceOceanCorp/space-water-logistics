# Space Water Logistics

Open models for delivering water in space, from [Space Ocean Corp](https://spaceoceancorp.com).

Listed in [Awesome Space](https://github.com/orbitalindex/awesome-space#mission-design) under Mission Design.

Water is the heaviest crew consumable and a ready source of propellant. These models size how much water a mission needs, how much recycling saves, and when water from the Moon beats water launched from Earth. Every input comes from a public source, and every model is a screening tool, not a flight plan.

## Models

| Model | Question it answers | Run |
|---|---|---|
| [Crew water loop](docs/crew_water_loop.md) | How much water does a crew draw each day, how much does recycling return, and how much must be shipped for a mission? | `python models/crew_water_loop.py` |
| [Lunar settlement water](docs/lunar_settlement_water.md) | How long does local lunar ice last for a settlement, and how much water must be imported to keep it supplied? | `python models/lunar_settlement_water.py` |
| [Water delivery gear ratio](docs/water_delivery_gear_ratio.md) | How much mass must be launched (Earth source) or mined (lunar source) per kg of water delivered to LEO, GEO, EML-1 or low lunar orbit? | `python models/water_delivery_gear_ratio.py` |

Headline results:

- **Crew water loop:** 4 crew for 180 days with ISS-class recycling need 458 kg of water shipped, against 3,266 kg with no recycling.
- **Lunar settlement water:** a city of 1 million recycling at the ISS's best 98% loses 10 million tons of water a year, about 27 landers of 1,000 t per day (Elvis & McDowell 2026).
- **Water delivery gear ratio:** beyond LEO, lunar water needs 1.56 to 2.67 kg mined per kg delivered, while Earth water needs 2.72 to 3.20 kg already in LEO, before counting the launch from the ground.

## Contributions to other open-source projects

| Project | Contribution | Status |
|---|---|---|
| [sidus-tools](https://github.com/massimodeluisa/sidus-tools) | Crew water loop & resupply tool: daily water demand, recycling, loop closure and resupply mass, with NASA BVAD Rev2 defaults | [PR #212](https://github.com/massimodeluisa/sidus-tools/pull/212) (open) |
| [space-logistics-optimization](https://github.com/masaisaji/space-logistics-optimization) | Optional water recovery rate for lunar surface consumption | [PR #1](https://github.com/masaisaji/space-logistics-optimization/pull/1) (open) |
| [Awesome Space](https://github.com/orbitalindex/awesome-space) | Listing for this repository under Mission Design | [PR #127](https://github.com/orbitalindex/awesome-space/pull/127) (merged) |

## Sources

- NASA, *Life Support Baseline Values and Assumptions Document*, NASA/TP-2015-218570 Rev2 (2022), Tables 4-20 and 4-21
- NASA, *NASA Achieves Water Recovery Milestone on International Space Station* (2023): 93 to 94% total recovery before the Brine Processor Assembly, 98% after
- M. Elvis and J. C. McDowell, *No cities on the Moon: a billion tons of water is not enough for sustainability*, Frontiers in Space Technologies 7:1894104 (2026), doi:10.3389/frspt.2026.1894104 (CC BY)
- Wikipedia, *Delta-v budget*, table "Earth-Moon space, high thrust"

## Tests

```
python -m unittest discover -s tests
```

Python 3.10 or later, standard library only.

## License

Apache-2.0. See [LICENSE](LICENSE).
