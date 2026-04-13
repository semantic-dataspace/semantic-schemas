# Measurement Device (PMDCo/OBI)

Records a **physical measurement or characterization instrument**: its name,
manufacturer, model, serial number, and last calibration date, following the
[OBI](http://purl.obolibrary.org/obo/obi.owl) /
[Platform MaterialDigital Core Ontology (PMDCo)](https://w3id.org/pmd/co/) conventions.

Once registered, the device receives a stable IRI in the knowledge graph.
That IRI is referenced in experiment records (e.g.
[`characterization/process/PMDCo/`](../../characterization/process/PMDCo/README.md))
to permanently link measurements to the instrument that produced them.

---

## Quick start

**The fastest way in:** open the notebook.

```bash
pip install jupyterlab
jupyter lab docs/1_device_workflow.ipynb
```

### Input fields

Copy [`docs/example.input.json`](docs/example.input.json) and fill in your values:

```json
{
  "device_name":      "Zwick Z250 Universal Testing Machine #1",
  "manufacturer":     "Zwick Roell",
  "model":            "Z250",
  "serial_number":    "ZR-12345",
  "calibration_date": "2024-03-01"
}
```

| Field | Required | Description |
|---|---|---|
| `device_name` | yes | Name that uniquely identifies this unit in the lab |
| `manufacturer` | no | Manufacturer name (e.g. `"Zwick Roell"`, `"Zeiss"`) |
| `model` | no | Model name or number as given by the manufacturer |
| `serial_number` | no | Manufacturer serial number for this individual unit |
| `calibration_date` | no | Last calibration date in ISO 8601 format (`YYYY-MM-DD`) |
| `description` | no | Free-text description of the device or its capabilities |
| `device_id` | no | Custom IRI slug; auto-derived from `device_name` if omitted |

---

## Files in this folder

| File | Purpose |
|---|---|
| `docs/example.input.json` | Ready-to-edit example (start here) |
| `docs/1_device_workflow.ipynb` | Step-by-step notebook |
| `specs/schema.simplified.json` | Input field reference |
| `specs/transform.simplified.jsonata` | Converts your input to the structured format |
| `specs/schema.oold.yaml` | Full schema definition (expert reference) |
| `specs/shape.ttl` | SHACL validation rules |
| `CHANGELOG.md` | Version history |

---

## For the curious: how this maps to the ontology

```text
Device  (obi:OBI_0000968)
  rdfs:label          ──── device name
  rdfs:comment        ──── description  (optional)
  schema:manufacturer ──── manufacturer name  (optional)
  schema:model        ──── model identifier  (optional)
  schema:serialNumber ──── serial number  (optional)
  dcterms:date        ──── last calibration date (xsd:date)  (optional)
```

The root class `obi:OBI_0000968` is the OBI canonical class for physical
instruments. Descriptive metadata uses [schema.org](https://schema.org)
terms (`manufacturer`, `model`, `serialNumber`) which are stable, widely
recognised, and unambiguous in engineering contexts.

---

## Further reading

- [Characterization Process (PMDCo)](../../characterization/process/PMDCo/README.md): references this device IRI
- [Expertise schema](../../expertise/README.md): links a person to the devices they operate
- [OO-LD primer](../../docs/2_oold-primer.md): how the schema format works
- [OBI Device class](http://purl.obolibrary.org/obo/OBI_0000968)
- [PMDCo core ontology](https://github.com/materialdigital/core-ontology)
