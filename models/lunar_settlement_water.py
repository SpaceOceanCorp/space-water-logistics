"""
Lunar settlement water: how long local ice lasts, and how much must be imported.

Purpose
    Reproduces the water depletion and import arithmetic of Elvis & McDowell
    (2026), "No cities on the Moon: a billion tons of water is not enough for
    sustainability", Frontiers in Space Technologies 7:1894104,
    doi:10.3389/frspt.2026.1894104 (CC BY), so the numbers can be rerun with
    other populations, usage rates, recycling efficiencies and ice inventories.

Model
    A population N uses m tons of water per person per year and recycles a
    fraction e of it. The net loss is N * m * (1 - e) tons per year.
    - Local inventory M lasts  T = M / (N * m * (1 - e))  years.
    - Keeping the settlement supplied indefinitely without drawing down local
      ice needs an import of  N * m * (1 - e)  tons per year.

Defaults (from the paper)
    - Inventory M: 1 billion tons, which the paper calls a generous baseline.
    - Use m: 500 tons per person per year. The paper's Table 2 gives drinking
      and hygiene 125, breathing 2 and growing food 500 t/person/yr; it then
      assumes improved cultivation halves food water, giving about 500 in total.
    - Lander payload: 1,000 tons, the paper's import example.

Units
    tons (metric) of water, years, people.

Limitations
    Linear depletion at constant population and usage, no rocket propellant
    drawn from the same ice (the paper lists 1,200 t per Starship-class
    second stage), and no recovery of water lost to space or regolith.
"""

from __future__ import annotations

DAYS_PER_YEAR = 365.25


def net_loss_t_per_year(population: float, use_t: float, efficiency: float) -> float:
    """Water lost per year (tons) after recycling."""
    if population <= 0 or use_t <= 0:
        raise ValueError("population and use must be > 0")
    if not 0 <= efficiency <= 1:
        raise ValueError("efficiency must be between 0 and 1")
    return population * use_t * (1 - efficiency)


def years_to_exhaust(inventory_t: float, population: float, use_t: float, efficiency: float) -> float:
    """T = M / (N m (1 - e)); infinite when recycling is perfect."""
    if inventory_t < 0:
        raise ValueError("inventory must be >= 0")
    loss = net_loss_t_per_year(population, use_t, efficiency)
    return float("inf") if loss == 0 else inventory_t / loss


def landers_per_day(population: float, use_t: float, efficiency: float, lander_t: float = 1000.0) -> float:
    """Landers per Earth day needed to import the annual net loss."""
    if lander_t <= 0:
        raise ValueError("lander payload must be > 0")
    return net_loss_t_per_year(population, use_t, efficiency) / lander_t / DAYS_PER_YEAR


if __name__ == "__main__":
    M, m = 1e9, 500.0
    print("Years to exhaust 1 billion tons at 500 t/person/yr (Elvis & McDowell 2026, Table 3)\n")
    print(f"{'recycling':>10}{'100,000 people':>18}{'1,000,000 people':>20}")
    for e in (0.0, 0.94, 0.98, 0.99, 0.999):
        print(f"{e:>10.1%}{years_to_exhaust(M, 1e5, m, e):>18,.0f}{years_to_exhaust(M, 1e6, m, e):>20,.0f}")
    imp = net_loss_t_per_year(1e6, m, 0.98)
    print(
        f"\n1M people at ISS-best 98% recycling: import {imp / 1e6:.0f} million t/yr"
        f" = {landers_per_day(1e6, m, 0.98):.1f} landers/day at 1,000 t each"
    )
