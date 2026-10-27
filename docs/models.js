// JavaScript port of models/*.py for the calculator page (docs/index.html).
// tests/test_calculator_parity.py runs this file under Node and requires the
// same answers as the Python models, so the page cannot drift from them.
(function (root) {
  "use strict";

  // ---- crew_water_loop.py ----
  const M_H2O = 0.018015, M_O2 = 0.031998;
  const WATER_PER_O2 = (2 * M_H2O) / M_O2;
  const LOOP_DEFAULTS = {
    potable: 2.5, hygiene: 0.4, flush: 0.3, o2: 0.82, urine: 1.2, condensate: 2.27,
    eta_urine: 0.85, eta_condensate: 1.0, eta_hygiene: 0.0, crew: 4, days: 180, reserve: 0.1,
  };

  function waterLoopBudget(inputs) {
    const i = Object.assign({}, LOOP_DEFAULTS, inputs);
    for (const k of ["potable", "hygiene", "flush", "o2", "urine", "condensate"]) {
      if (!(i[k] >= 0)) throw new Error("water rates must be >= 0");
    }
    for (const k of ["eta_urine", "eta_condensate", "eta_hygiene"]) {
      if (!(i[k] >= 0 && i[k] <= 1)) throw new Error("recovery fractions must be between 0 and 1");
    }
    if (!(i.crew > 0 && i.days > 0 && i.reserve >= 0)) throw new Error("crew and days must be > 0, reserve >= 0");
    const electrolysis = i.o2 * WATER_PER_O2;
    const demand = i.potable + i.hygiene + i.flush + electrolysis;
    if (!(demand > 0)) throw new Error("total demand must be > 0");
    const recovered = i.eta_urine * (i.urine + i.flush) + i.eta_condensate * i.condensate + i.eta_hygiene * i.hygiene;
    const makeup = Math.max(0, demand - recovered);
    const crewDays = i.crew * i.days * (1 + i.reserve);
    const mission = makeup * crewDays;
    const openLoop = demand * crewDays;
    return {
      demand, electrolysis, recovered, makeup,
      surplus: Math.max(0, recovered - demand),
      closure: Math.min(1, recovered / demand),
      mission, open_loop: openLoop, saved: openLoop - mission,
    };
  }

  // ---- lunar_settlement_water.py ----
  const DAYS_PER_YEAR = 365.25;

  function netLossTPerYear(population, useT, efficiency) {
    if (!(population > 0 && useT > 0)) throw new Error("population and use must be > 0");
    if (!(efficiency >= 0 && efficiency <= 1)) throw new Error("efficiency must be between 0 and 1");
    return population * useT * (1 - efficiency);
  }

  function yearsToExhaust(inventoryT, population, useT, efficiency) {
    if (!(inventoryT >= 0)) throw new Error("inventory must be >= 0");
    const loss = netLossTPerYear(population, useT, efficiency);
    return loss === 0 ? Infinity : inventoryT / loss;
  }

  function landersPerDay(population, useT, efficiency, landerT = 1000) {
    if (!(landerT > 0)) throw new Error("lander payload must be > 0");
    return netLossTPerYear(population, useT, efficiency) / landerT / DAYS_PER_YEAR;
  }

  // ---- water_delivery_gear_ratio.py ----
  const G0 = 9.80665;
  const DV_FROM_LEO = { GEO: 4330, "EML-1": 3770, LLO: 4040 };
  const DV_FROM_MOON_SURFACE = { LEO: 2740, GEO: 3920, "EML-1": 2520, LLO: 1870 };

  function propellantPerPayload(dv, isp, dryFrac) {
    if (!(dv >= 0 && isp > 0 && dryFrac >= 0)) throw new Error("dv >= 0, isp > 0 and dry_frac >= 0 required");
    const r = Math.exp(dv / (G0 * isp));
    const denom = 1 + dryFrac - dryFrac * r;
    return denom <= 0 ? Infinity : (r - 1) / denom;
  }

  function earthSourcedMassInLeo(dv, isp, dryFrac) {
    return 1 + propellantPerPayload(dv, isp, dryFrac) * (1 + dryFrac);
  }

  function lunarSourcedWaterMined(dv, isp, dryFrac) {
    return 1 + propellantPerPayload(dv, isp, dryFrac);
  }

  function gearTable(isp = 450, dryFrac = 0.1) {
    return Object.keys(DV_FROM_MOON_SURFACE).map((dest) => [
      dest,
      dest === "LEO" ? 1 : earthSourcedMassInLeo(DV_FROM_LEO[dest], isp, dryFrac),
      lunarSourcedWaterMined(DV_FROM_MOON_SURFACE[dest], isp, dryFrac),
    ]);
  }

  const api = {
    WATER_PER_O2, LOOP_DEFAULTS, waterLoopBudget,
    netLossTPerYear, yearsToExhaust, landersPerDay,
    G0, DV_FROM_LEO, DV_FROM_MOON_SURFACE, propellantPerPayload, earthSourcedMassInLeo, lunarSourcedWaterMined,
    gearTable,
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.SWL = api;
})(this);
