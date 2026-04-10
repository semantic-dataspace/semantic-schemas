"""
Utility library for semantic-schemas notebooks.

Provides the Schema class, which wraps the three core operations
(transform, parse to RDF graph, SHACL validate) so that notebooks
can focus on domain content rather than plumbing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

import rdflib
import yaml


__all__ = ["Schema"]


class Schema:
    """
    Wraps a single schema directory and exposes three operations:

    - transform(data)      Run the JSONata transform; return the OO-LD document.
    - to_graph(data)       Transform + parse into a flat rdflib.Graph.
    - validate(data, ...)  Build the graph and run SHACL validation.

    Parameters
    ----------
    schema_dir : path-like
        Root of the schema directory, i.e. the folder that contains
        ``specs/schema.oold.yaml``, ``specs/shape.ttl``, and
        ``specs/transform.simplified.jsonata``.
    """

    def __init__(self, schema_dir: Union[Path, str]) -> None:
        self.dir = Path(schema_dir)
        self._context: dict | None = None
        self._transform_src: str | None = None

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_context(self) -> dict:
        if self._context is None:
            raw = yaml.safe_load(
                (self.dir / "specs" / "schema.oold.yaml").read_text(encoding="utf-8")
            )
            self._context = raw["@context"]
        return self._context

    def _get_transform_src(self) -> str:
        if self._transform_src is None:
            self._transform_src = (
                self.dir / "specs" / "transform.simplified.jsonata"
            ).read_text(encoding="utf-8")
        return self._transform_src

    @staticmethod
    def _parse_oold(
        context: dict, oold_doc: dict, base: str | None = None
    ) -> rdflib.Graph:
        ctx = {**context, **({} if base is None else {"@base": base})}
        ds = rdflib.Dataset()
        ds.parse(
            data=json.dumps({"@context": ctx, **oold_doc}),
            format="json-ld",
        )
        g = rdflib.Graph()
        for s, p, o, _ in ds.quads():
            g.add((s, p, o))
        # Propagate all namespace bindings the JSON-LD parser derived from
        # the @context.  Schemas declare their own prefixes there, so no
        # hard-coding is needed here.
        for prefix, ns in ds.namespaces():
            g.bind(prefix, ns)
        return g

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self, oold_doc: dict, base: str | None = None) -> rdflib.Graph:
        """Parse an already-transformed OO-LD document into a flat rdflib.Graph.

        Use this when you have assembled the OO-LD document manually (e.g. by
        merging outputs from multiple schemas) and only need the parsing step.

        Parameters
        ----------
        oold_doc :
            The OO-LD document (already transformed from simplified input).
        base :
            Optional base IRI used to resolve relative node identifiers.
            When omitted the schema's own ``@base`` (if any) applies; schemas
            without a built-in ``@base`` fall back to the current working
            directory.  Pass your own IRI (e.g. ``"https://example.org/"``) to
            produce portable, globally-unique node IRIs.
        """
        return self._parse_oold(self._get_context(), oold_doc, base=base)

    def transform(self, data: dict) -> dict:
        """Run the JSONata transform and return the OO-LD document."""
        from jsonata.jsonata import Jsonata

        return Jsonata(self._get_transform_src()).evaluate(data)

    def to_graph(self, data: dict, base: str | None = None) -> rdflib.Graph:
        """Transform *data* to OO-LD and parse into a flat rdflib.Graph.

        Parameters
        ----------
        data :
            Simplified input dict (as filled in by the user).
        base :
            Optional base IRI — see :meth:`parse` for details.
        """
        oold_doc = self.transform(data)
        return self._parse_oold(self._get_context(), oold_doc, base=base)

    def validate(
        self,
        data: Union[dict, rdflib.Graph],
        also: list[Union["Schema", Path]] | None = None,
    ) -> tuple[bool, list[str]]:
        """
        Validate *data* against this schema's SHACL shape.

        Parameters
        ----------
        data :
            Either a plain Python dict (transformed to a graph first) or an
            already-built rdflib.Graph.
        also :
            Additional Schema objects or Path objects whose shape files are
            loaded alongside this schema's own shape.  Use this when a schema
            extends a base schema (e.g. tensile-test extends characterization/step).

        Returns
        -------
        conforms : bool
        violations : list[str]
            Human-readable violation messages (empty when conforms is True).
        """
        import pyshacl

        graph = data if isinstance(data, rdflib.Graph) else self.to_graph(data)

        shapes = rdflib.Graph()
        shapes.parse(str(self.dir / "specs" / "shape.ttl"))
        for extra in also or []:
            if isinstance(extra, Schema):
                shapes.parse(str(extra.dir / "specs" / "shape.ttl"))
            else:
                shapes.parse(str(extra))

        conforms, report, _ = pyshacl.validate(
            graph, shacl_graph=shapes, inference="rdfs"
        )

        violations: list[str] = []
        if not conforms:
            SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
            for res in report.subjects(rdflib.RDF.type, SH.ValidationResult):
                msg  = report.value(res, SH.resultMessage)
                path = report.value(res, SH.resultPath)
                prop = (
                    str(path).rsplit("/", 1)[-1].rsplit("#", 1)[-1]
                    if path else None
                )
                violations.append(
                    str(msg) + (f"  [{prop}]" if prop else "")
                )

        return conforms, violations
