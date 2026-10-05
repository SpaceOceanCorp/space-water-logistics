# Space Water Logistics

Open models for delivering water in space, from [Space Ocean Corp](https://spaceoceancorp.com).

Water is the heaviest crew consumable and a ready source of propellant. These models size how much water a mission needs, how much recycling saves, and when water from the Moon beats water launched from Earth. Every input comes from a public source, and every model is a screening tool, not a flight plan.

## Models

| Model | Question it answers | Run |
|---|---|---|
| [Water delivery gear ratio](docs/water_delivery_gear_ratio.md) | How much mass must be launched (Earth source) or mined (lunar source) per kg of water delivered to LEO, GEO, EML-1 or low lunar orbit? | `python models/water_delivery_gear_ratio.py` |

Result at Isp 450 s and 10% stage dry mass: beyond LEO, lunar water needs 1.56 to 2.67 kg mined per kg delivered. Earth water needs 2.72 to 3.20 kg already in LEO, before counting the launch from the ground.

## Contributions to other open-source projects

| Project | Contribution | Status |
|---|---|---|
| [sidus-tools](https://github.com/massimodeluisa/sidus-tools) | Crew water loop & resupply tool: daily water demand, recycling, loop closure and resupply mass, with NASA BVAD Rev2 defaults | Proposed |
| [space-logistics-optimization](https://github.com/masaisaji/space-logistics-optimization) | Optional water recovery rate for lunar surface consumption | Proposed |

## Sources

- NASA, *Life Support Baseline Values and Assumptions Document*, NASA/TP-2015-218570 Rev2 (2022), Tables 4-20 and 4-21
- NASA, *NASA Achieves Water Recovery Milestone on International Space Station* (2023): 93 to 94% total recovery before the Brine Processor Assembly, 98% after
- Wikipedia, *Delta-v budget*, table "Earth-Moon space, high thrust"

## Tests

```
python -m unittest discover -s tests
```

Python 3.10 or later, standard library only.

## License

Apache-2.0. See [LICENSE](LICENSE).
