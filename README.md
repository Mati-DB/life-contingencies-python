# Actuarial Life Insurance Engine

A Python project for implementing and exploring actuarial calculations for life insurance.

The project is being developed incrementally as both a learning project and a portfolio project, with an emphasis on clear actuarial reasoning, readable Python code, and reusable components.

## Project status

The project is currently in its initial development stage.

Version 1 will focus on annual discrete actuarial calculations, including:

- survival and death probabilities;
- financial discounting;
- commutation functions;
- pure endowments;
- life annuities;
- life insurance benefits;
- basic endowment-type products;
- net single premiums.

Fractional-year calculations, more complex benefit patterns, reserves, gross premiums, surrender values, and other advanced features are planned for later stages.

## Initial actuarial basis

The initial development and validation basis will use:

- 1980 CSO male and female mortality tables;
- a 4% annual effective interest rate.

These assumptions are intended as initial defaults only. Mortality tables and interest rates will be configurable rather than embedded in the calculation logic.

## Design principles

The project follows a few simple principles:

- build actuarial functionality incrementally;
- keep actuarial assumptions separate from calculation logic;
- use standard English actuarial terminology;
- avoid unnecessary abstractions until they provide a clear benefit;
- prefer reusable elementary actuarial components over duplicated product-specific calculations.

## Development roadmap

The first stage focuses on annual discrete calculations.

Future iterations are expected to introduce fractional-year calculations, variable benefits and premiums, reserves, pricing components, and additional life insurance products.

The scope will evolve gradually as the actuarial engine becomes more complete.

## Mortality data

The initial mortality tables are based on male and female 1980 CSO tables provided as university course material.

These files have not been independently verified against an official Society of Actuaries dataset and should not be assumed to reproduce an SOA-published version exactly.