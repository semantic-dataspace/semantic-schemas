# Changelog: MD Simulation (LAMMPS, PMDCo)

All notable changes to this schema are documented here.
Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: breaking changes (renamed fields, removed properties, incompatible graph structure)
- **MINOR**: backwards-compatible additions (new optional fields)
- **PATCH**: corrections that do not affect the graph structure (typos, description fixes)

---

## [0.1.0] - 2026-07-21

### Added

- Initial release of the MD simulation schema using LAMMPS.
- Extends `process-step/PMDCo` via `allOf + $ref`; inherits shared fields
  (`label`, `date`, `has_specified_input`, `has_specified_output`,
  `preceded_by`, `operator`, `instrument`) from the base.
- Ontology pattern: OBI ComputerSimulation (`obi:OBI_0000471`) + PROV-O Activity.
- Schema-specific fields: `purpose`, `project`, `material_system`,
  `lammps_version`, `force_field`, `atom_count`, `temperature_K`,
  `timesteps`, `keywords`.
- Custom predicates: `fairsim:forceField`, `fairsim:atomCount`,
  `fairsim:temperature`, `fairsim:timesteps` for MD-specific quantities.
- `operator` typed as single IRI (`prov:wasAssociatedWith`, `format: uri`) to
  match the base schema.
- `date` maps to `dcterms:created` (`xsd:date`), overriding the base schema's
  `dcterms:date` (`xsd:dateTime`) to record the run date (not a datetime).
