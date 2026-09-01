# Project Decisions

This document records the main technical and actuarial design decisions adopted during the development of the project.

The goal is to keep the reasoning behind important choices explicit and to avoid changing them implicitly as the project evolves.

## 1. Incremental architecture

The project will evolve incrementally from simple actuarial calculations toward reusable components.

Classes, design patterns, additional abstraction layers, or complex infrastructure will only be introduced when a concrete requirement justifies them.

The project should remain simple and readable while its scope is still limited.

## 2. Project language

Source code, public APIs, module names, documentation, and repository content will be written in English.

Actuarial terminology will follow standard English-language actuarial usage whenever possible rather than literal translations from Spanish.

## 3. Mortality data

Published or observed mortality tables will be stored as external data files, primarily in CSV format.

Python will be responsible for loading, validating, and transforming mortality data.

Mortality tables generated from mortality laws or models may instead be created programmatically.

### Canonical mortality input

Internal actuarial calculations will operate on a normalized mortality table with a defined structure. Source-specific parsing and normalization will be handled before actuarial calculations rather than embedded in them.

### Incremental tabular representation

Mortality, life, and commutation tables will initially be represented as successive enriched tables. Some duplication of derived columns is accepted in favor of clarity and inspectability.

## 4. Mortality and interest assumptions

The initial mortality basis will use the 1980 CSO male and female mortality tables.

An annual effective interest rate of 4% will be used as the initial reference assumption.

Both mortality and interest assumptions must remain configurable and must not be hardcoded into the actuarial calculation logic.

## 5. Commutation functions

Discrete actuarial calculations will be based primarily on commutation functions.

Commutation values will be calculated programmatically from the mortality basis and interest assumption rather than stored as fixed input data.

Only the commutation functions required by the implemented calculations will be introduced.

## 6. Product composition

When an actuarial product can naturally be represented as a combination of simpler actuarial benefits, the implementation should prefer composing those existing components rather than introducing independent duplicated calculation logic.

### Composable actuarial API

The package will prioritize reusable actuarial benefits, premium patterns, and valuation functions that users can combine to model products.

Standard products may be provided as convenience functions when they represent common and well-defined compositions, but the package will not attempt to encode every possible insurance plan as a separate implementation.

### Premium patterns

Premium calculations will be modeled independently from insurance benefits.

The package will support single, level, limited-payment, and variable premium patterns, including arithmetic and geometric progressions, so that the same actuarial benefit can be financed under different premium structures.

## 7. Version 1 calculation basis

Version 1 will focus on annual discrete actuarial calculations.

Fractional-year calculations and assumptions will be introduced in a later version, initially planned for Version 1.1.

## 8. Licensing

The project will be released under the MIT License, allowing reuse, modification, distribution, and commercial use, provided that the copyright and license notices are preserved.

**Rationale:** A permissive license is consistent with the project's portfolio and open-source goals while preserving the author's copyrigh