"""
Crew water loop: daily water demand, recycling, and resupply mass for a mission.

Purpose
    How much water a crewed vehicle or station draws each day, how much its
    recycling hardware returns, and how much has to be shipped for a mission
    compared with no recycling at all.

Model (all rates per crewmember-day)
    demand    = potable + hygiene + flush + o2 * (2 M_H2O / M_O2)
    recovered = eta_urine * (urine + flush)
              + eta_condensate * condensate
              + eta_hygiene * hygiene
    makeup    = max(0, demand - recovered)
    mission   = makeup * crew * days * (1 + reserve)

    The electrolysis term is the water split to make breathing oxygen
    (2 H2O -> 2 H2 + O2, about 1.126 kg of water per kg of O2). Set o2 to 0
    when oxygen is shipped as gas.

Defaults (public sources)
    - NASA/TP-2015-218570 Rev2, Life Support Baseline Values and Assumptions
      Document (Feb 2022), Tables 4-20 and 4-21, ISS column: drinking 2.00 +
      food rehydration 0.50, hygiene 0.4, urinal flush 0.3, urine 1.20,
      humidity condensate 2.27 kg per crewmember-day.
    - Urine recovery 0.85: ISS US-segment Urine Processor Assembly, BVAD Rev2
      section 4.3.3. NASA reported 93 to 94% total ISS water recovery before
      the Brine Processor Assembly and 98% after (2023).
    - O2 0.82 kg per crewmember-day: ISS-order daily oxygen use.

Units
    kg per crewmember-day for rates, days for duration, kg for mission totals.

Limitations
    Steady-state mass balance only. No storage dynamics, Sabatier water
    return, brine or filter consumables, leaks, or EVA water. A planning
    estimate, not a flight logistics plan.
"""

from __future__ import annotations

from dataclasses import dataclass

M_H2O = 0.018015  # kg/mol
M_O2 = 0.031998  # kg/mol
WATER_PER_O2 = 2 * M_H2O / M_O2  # kg water electrolyzed per kg O2


@dataclass(frozen=True)
class WaterLoopInputs:
    potable: float = 2.5  # drink + food rehydration, BVAD Rev2 Table 4-20
    hygiene: float = 0.4  # personal hygiene, BVAD Rev2 Table 4-20 (ISS)
    flush: float = 0.3  # urinal flush, BVAD Rev2 Tables 4-20/4-21 (ISS)
    o2: float = 0.82  # O2 made by electrolysis; 0 if shipped as gas
    urine: float = 1.2  # BVAD Rev2 Table 4-21 (ISS)
    condensate: float = 2.27  # crew latent humidity condensate, Table 4-21
    eta_urine: float = 0.85  # ISS UPA, BVAD Rev2 section 4.3.3
    eta_condensate: float = 1.0
    eta_hygiene: float = 0.0  # ISS does not collect hygiene greywater
    crew: int = 4
    days: float = 180.0
    reserve: float = 0.1  # extra fraction shipped as contingency

    def __post_init__(self) -> None:
        rates = (self.potable, self.hygiene, self.flush, self.o2, self.urine, self.condensate)
        if any(r < 0 for r in rates):
            raise ValueError("water rates must be >= 0")
        for eta in (self.eta_urine, self.eta_condensate, self.eta_hygiene):
            if not 0 <= eta <= 1:
                raise ValueError("recovery fractions must be between 0 and 1")
        if self.crew <= 0 or self.days <= 0 or self.reserve < 0:
            raise ValueError("crew and days must be > 0, reserve >= 0")


@dataclass(frozen=True)
class WaterLoopBudget:
    demand: float  # kg per crewmember-day
    electrolysis: float  # kg per crewmember-day
    recovered: float  # kg per crewmember-day
    makeup: float  # kg per crewmember-day that must be supplied
    surplus: float  # kg per crewmember-day recovered beyond demand
    closure: float  # share of demand met by recycling, 0 to 1
    mission: float  # kg to supply for the mission, incl. reserve
    open_loop: float  # kg the same mission needs with no recycling
    saved: float  # kg of supply avoided by recycling


def water_loop_budget(i: WaterLoopInputs) -> WaterLoopBudget:
    electrolysis = i.o2 * WATER_PER_O2
    demand = i.potable + i.hygiene + i.flush + electrolysis
    if demand <= 0:
        raise ValueError("total demand must be > 0")
    recovered = (
        i.eta_urine * (i.urine + i.flush)
        + i.eta_condensate * i.condensate
        + i.eta_hygiene * i.hygiene
    )
    makeup = max(0.0, demand - recovered)
    crew_days = i.crew * i.days * (1 + i.reserve)
    mission = makeup * crew_days
    open_loop = demand * crew_days
    return WaterLoopBudget(
        demand=demand,
        electrolysis=electrolysis,
        recovered=recovered,
        makeup=makeup,
        surplus=max(0.0, recovered - demand),
        closure=min(1.0, recovered / demand),
        mission=mission,
        open_loop=open_loop,
        saved=open_loop - mission,
    )


if __name__ == "__main__":
    i = WaterLoopInputs()
    b = water_loop_budget(i)
    print(f"{i.crew} crew, {i.days:.0f} days, {i.reserve:.0%} reserve, ISS-class defaults\n")
    print(f"demand per crew-day       {b.demand:8.3f} kg  (incl. {b.electrolysis:.3f} kg for O2)")
    print(f"recovered per crew-day    {b.recovered:8.3f} kg")
    print(f"makeup per crew-day       {b.makeup:8.3f} kg")
    print(f"loop closure              {b.closure:8.1%}")
    print(f"water to supply           {b.mission:8.1f} kg")
    print(f"with no recycling         {b.open_loop:8.1f} kg")
    print(f"supply avoided            {b.saved:8.1f} kg")
