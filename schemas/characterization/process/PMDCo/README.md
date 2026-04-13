# Characterization Process (PMDCo)

A **fixed-structure template** for documenting a characterization experiment.
The template pre-decides what to record: three slots are always present, always
named the same way, always required. You fill in the values — no structural
decisions needed.

| Slot | What to fill in | Ontology property |
|---|---|---|
| `operator_iri` | IRI of the expert / technician who ran the experiment | `prov:wasAssociatedWith` |
| `device_iri` | IRI of the measurement device used | `schema:instrument` |
| `specimen_iri` | IRI of the specimen being characterised | `obi:has_specified_input` |

The template works equally well whether you are filling it in before an
experiment, during it, or retrospectively from paper records. Its value is
always the same: the structure is given, so you only decide the values.

The optional `step_reference` field links this record to a detailed result node
elsewhere in the graph (e.g. a `tto:TensileTest` from
[`characterization/step/tensile-test/TTO/`](../step/tensile-test/TTO/README.md)).

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/1_characterization_process_workflow.ipynb
```

### What you need before filling in this template

Each of the three required slots takes an IRI — a stable identifier for a node
already registered in your knowledge graph. If you haven't registered these yet,
use the linked schemas first:

- **Specimen** → [`specimen/PMDCo/`](../../specimen/PMDCo/README.md)
- **Measurement device** → [`measurement-device/PMDCo/`](../../measurement-device/PMDCo/README.md)
- **Expert / operator** → [`expertise/`](../../expertise/README.md)

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "process_name": "Tensile test 316L batch 1 — QA run",
  "operator_iri": "https://example.org/people/jane-doe",
  "device_iri":   "https://example.org/devices/zwick-z250-1",
  "specimen_iri": "https://example.org/specimens/316L-tensile-bar-1",
  "date": "2024-11-15T09:30:00",
  "step_reference": "https://example.org/characterization/tensile-test-316L-batch-1",
  "conditions": [
    { "name": "Test Standard", "unit": "ISO 6892-1" },
    { "name": "Strain Rate",   "value": 0.00025, "unit": "1/s" },
    { "name": "Temperature",   "value": 23,      "unit": "°C" }
  ]
}
```

| Field | Required | Description |
|---|---|---|
| `process_name` | yes | Human-readable name for this experiment |
| `operator_iri` | **yes** | IRI of the person who conducted the experiment |
| `device_iri` | **yes** | IRI of the measurement device used |
| `specimen_iri` | **yes** | IRI of the specimen being characterised |
| `date` | no | Experiment date/time in ISO 8601 format |
| `step_reference` | no | IRI of the detailed result node in the knowledge graph |
| `conditions` | no | Quantitative test parameters (name, value, unit) |
| `preceded_by` | no | IRIs of preceding characterization processes |
| `process_id` | no | Custom IRI slug; auto-derived from `process_name` if omitted |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/1_characterization_process_workflow.ipynb` | Step-by-step notebook |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition (expert reference) |
| `specs/shape.ttl` | SHACL validation rules |
| `CHANGELOG.md` | Version history |

---

## Typical usage sequence

```text
1. Register specimen      →  specimen/PMDCo/                   →  note the IRI
2. Register device        →  measurement-device/PMDCo/         →  note the IRI
3. Register operator      →  expertise/                        →  note the IRI
4. Fill in this template  →  characterization/process/PMDCo/   (this schema)
5. Record detailed result →  characterization/step/tensile-test/TTO/
6. Link the result back   →  add step_reference IRI to this record
```

Steps 1–3 can be done in any order and reused across experiments: once a device
is registered, every experiment that uses it just references the same IRI.

---

## How it differs from the step schemas

The `characterization/step/` schemas (e.g. `step/base/PMDCo/`, `step/tensile-test/TTO/`)
record **what was measured**: result values, test conditions, measured properties.
They leave operator, device, and specimen optional.

This template records **who, with what, on what**. The three provenance slots
are required — the schema will not validate without them. The detailed measurement
results go in a `step/` record; `step_reference` links the two together.

Use this template when you want every experiment record to be traceable. Use the
`step/` schemas when you only need the measurement data.

---

## For the curious: how this maps to the ontology

```text
Assay  (obi:OBI_0000070)
  rdfs:label               ──── process name
  rdfs:comment             ──── description  (optional)
  prov:wasAssociatedWith ──────► Expert IRI (foaf:Person)   [required]
  schema:instrument ───────────► Device IRI (obi:Device)    [required]
  has_specified_input ─────────► Specimen IRI               [required]
  dcterms:references ──────────► Step result IRI            [optional]
  dcterms:date             ──── experiment date/time        (optional)
  has_process_condition ───────► ProcessCondition (PMD_0000013)  [0..N]
```

`prov:wasAssociatedWith` (W3C PROV-O) is the canonical provenance property for
linking an activity to a responsible agent. `schema:instrument` (schema.org)
precisely captures "the object that helped the agent perform the action".

---

## Further reading

- [Measurement Device (PMDCo)](../../measurement-device/PMDCo/README.md): the device schema
- [Tensile Test (TTO)](../step/tensile-test/TTO/README.md): detailed result schema
- [Specimen (PMDCo)](../../specimen/PMDCo/README.md): specimen schema
- [Expertise](../../expertise/README.md): expert/operator schema
- [OO-LD primer](../../docs/2_oold-primer.md): how the schema format works
- [PMDCo core ontology](https://github.com/materialdigital/core-ontology)
- [PROV-O: wasAssociatedWith](https://www.w3.org/TR/prov-o/#wasAssociatedWith)
