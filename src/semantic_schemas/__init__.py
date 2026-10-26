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

_schema_cache: "dict[tuple[str, str | None], Schema]" = {}


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
        self._schema: dict | None = None
        self._context: dict | None = None
        self._transform_src: str | None = None
        self._vocab_cache: dict[str, list] = {}

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _get_schema(self) -> dict:
        if self._schema is None:
            generated = self.dir / "specs" / "schema.oold.generated.json"
            if generated.exists():
                raw = json.loads(generated.read_text(encoding="utf-8"))
            else:
                raw = yaml.safe_load(
                    (self.dir / "specs" / "schema.oold.yaml").read_text(encoding="utf-8")
                )
            self._schema = raw
            self._context = raw.get("@context", {})
        return self._schema

    def _get_context(self) -> dict:
        if self._context is None:
            self._get_schema()
        return self._context

    def _get_transform_src(self) -> str:
        if self._transform_src is None:
            self._transform_src = (
                self.dir / "specs" / "transform.simplified.jsonata"
            ).read_text(encoding="utf-8")
        return self._transform_src

    # ------------------------------------------------------------------
    # Vocabulary resolution — label/id/IRI → plain IRI string
    # ------------------------------------------------------------------

    @staticmethod
    def _collect_vocab_fields(properties: dict, result: dict) -> None:
        """Recursively collect {field_name: vocab_url} from schema properties."""
        for field_name, field_def in properties.items():
            if not isinstance(field_def, dict):
                continue
            if "x-vocabulary" in field_def:
                result[field_name] = field_def["x-vocabulary"]
            items = field_def.get("items")
            if isinstance(items, dict):
                Schema._collect_vocab_fields(items.get("properties", {}), result)
            nested = field_def.get("properties")
            if isinstance(nested, dict):
                Schema._collect_vocab_fields(nested, result)

    def _resolve_to_iri(self, value: str, vocab_url: str) -> str:
        """Resolve a vocabulary value (label, id, or full IRI) to a plain IRI string.

        Lookup order:
        1. Full IRI (starts with http/https) → return as-is.
        2. Case-insensitive label match against vocabulary terms.
        3. Case-insensitive id match (short codes like "MIN", "K-PER-MIN").
        4. No match → return original value unchanged.
        """
        if value.startswith("http://") or value.startswith("https://"):
            return value

        if vocab_url not in self._vocab_cache:
            try:
                import requests as _req
                resp = _req.get(vocab_url, timeout=15)
                resp.raise_for_status()
                self._vocab_cache[vocab_url] = resp.json()
            except Exception:
                self._vocab_cache[vocab_url] = []

        terms = self._vocab_cache[vocab_url]
        if not terms:
            return value

        value_lower = value.lower()
        for term in terms:
            if term.get("label", "").lower() == value_lower:
                return term["iri"]
        for term in terms:
            if term.get("id", "").lower() == value_lower:
                return term["iri"]
        return value

    def _walk_vocab(self, node, vocab_fields: dict):
        """Walk an OO-LD node, resolving vocabulary field values to plain IRIs."""
        if isinstance(node, dict):
            return {
                key: (
                    self._resolve_to_iri(value, vocab_fields[key])
                    if key in vocab_fields and isinstance(value, str) and value
                    else self._walk_vocab(value, vocab_fields)
                )
                for key, value in node.items()
            }
        if isinstance(node, list):
            return [self._walk_vocab(item, vocab_fields) for item in node]
        return node

    def resolve_vocabulary(self, oold_doc: dict) -> dict:
        """Replace x-vocabulary field values (labels/ids) with plain IRI strings.

        Reads the schema's ``properties`` to find fields annotated with
        ``x-vocabulary``, fetches the vocabulary terms (cached per Schema
        instance), then walks the document replacing any label or short id
        with the corresponding full IRI.  Full IRIs are passed through unchanged.

        This step is required for standalone RDF generation: the JSON-LD
        ``@context`` maps vocabulary-backed fields with ``"@type": "@id"``,
        which means rdflib expects plain IRI strings — not human-readable
        labels or short codes.

        Args:
            oold_doc: OO-LD document (output of :meth:`transform`).

        Returns:
            New document with vocabulary field values replaced by full IRIs.
        """
        schema = self._get_schema()
        vocab_fields: dict[str, str] = {}
        self._collect_vocab_fields(schema.get("properties", {}), vocab_fields)
        if not vocab_fields:
            return oold_doc
        return self._walk_vocab(oold_doc, vocab_fields)

    @staticmethod
    def _expand_compact_iris(doc: dict, context: dict) -> dict:
        """Pre-expand compact IRI values in an OO-LD document before JSON-LD parsing.

        rdflib's JSON-LD parser correctly expands compact IRIs that appear as
        ``@id`` values inside ``@context`` entries (so predicate IRIs are correct).
        However, it does **not** expand compact IRIs that appear as data values,
        even when the prefix is defined in the context as a plain string.

        Example without this function::

            # schema @context defines:  "uo": "http://purl.obolibrary.org/obo/UO_"
            # schema data contains:     "unit": "uo:0000163"
            # rdflib produces:          (frac, IAO:0000039, URIRef("uo:0000163"))  ← wrong
            # expected:                 (frac, IAO:0000039, URIRef("http://…/UO_0000163"))

        This is a known rdflib limitation — using ``"@prefix": true`` (JSON-LD 1.1)
        or plain-string prefix entries both leave data-value compact IRIs unexpanded.

        This method walks the data document (not the ``@context``) and replaces
        any string value that starts with a plain-string context prefix with the
        fully-expanded IRI.  Full IRIs, numbers, booleans and ``None`` pass through
        unchanged.

        Args:
            doc:     OO-LD data document (the dict without the ``@context`` key).
            context: The ``@context`` dict loaded from the schema YAML/JSON.

        Returns:
            New document dict with compact IRI values replaced by full IRIs.
        """
        # Only plain-string entries contribute prefixes; object-form entries
        # (e.g. {"@id": "...", "@type": "@id"}) define named terms, not prefixes.
        # JSON-LD keywords (keys starting with "@") are skipped.
        prefix_map = {
            k + ":": v
            for k, v in context.items()
            if isinstance(v, str) and not k.startswith("@")
        }

        def _expand(val: str) -> str:
            """Expand val to a full IRI if it starts with a known prefix."""
            for prefix, base in prefix_map.items():
                if val.startswith(prefix):
                    return base + val[len(prefix):]
            return val

        def _walk(node):
            """Recursively expand all string leaves in a JSON-like structure."""
            if isinstance(node, dict):
                return {k: _walk(v) for k, v in node.items()}
            if isinstance(node, list):
                return [_walk(item) for item in node]
            if isinstance(node, str):
                return _expand(node)
            return node  # int, float, bool, None — pass through unchanged

        return _walk(doc)

    @staticmethod
    def _parse_oold(
        context: dict, oold_doc: dict, base: str | None = None
    ) -> rdflib.Graph:
        ctx = {**context, **({} if base is None else {"@base": base})}
        # Pre-expand compact IRI values (e.g. "uo:0000163") before handing the
        # document to rdflib.  rdflib expands compact IRIs inside @context entries
        # but leaves them unexpanded when they appear as data values, producing
        # URIRef("uo:0000163") instead of the correct full IRI.
        # See _expand_compact_iris for a full explanation and worked example.
        expanded_doc = Schema._expand_compact_iris(oold_doc, context)
        ds = rdflib.Dataset()
        ds.parse(
            data=json.dumps({"@context": ctx, **expanded_doc}),
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

    def to_graph(
        self,
        data: dict,
        base: str | None = None,
        resolve_vocabulary: bool = True,
    ) -> rdflib.Graph:
        """Transform *data* to OO-LD and parse into a flat rdflib.Graph.

        Parameters
        ----------
        data :
            Simplified input dict (as filled in by the user).
        base :
            Optional base IRI: see :meth:`parse` for details.
        resolve_vocabulary :
            When True (default), resolve ``x-vocabulary`` field values
            (human-readable labels, short ids like ``"MIN"``, or full IRIs)
            to full IRI strings before JSON-LD parsing.  This is required for
            schemas where the simplified transform accepts vocabulary labels
            instead of raw IRIs (e.g. ``"Degree Celsius (°C)"`` for
            ``parameter_unit``).  Disable only if the input already contains
            fully-expanded IRIs for all vocabulary-backed fields.
        """
        oold_doc = self.transform(data)
        if resolve_vocabulary:
            try:
                oold_doc = self.resolve_vocabulary(oold_doc)
            except Exception as exc:
                import warnings
                warnings.warn(
                    f"Vocabulary resolution failed, IRIs may be incorrect: {exc}",
                    stacklevel=2,
                )
        return self._parse_oold(self._get_context(), oold_doc, base=base)

    @classmethod
    def from_url(
        cls,
        schema_url: str,
        github_token: str | None = None,
    ) -> "Schema":
        """Create a Schema by fetching its spec files from a GitHub tree URL.

        Downloads ``specs/schema.oold.yaml`` and, if it exists,
        ``specs/transform.simplified.jsonata`` from the given GitHub tree URL.
        The returned Schema supports :meth:`transform`, :meth:`parse`, and
        :meth:`to_graph` exactly like a locally-loaded Schema.

        Parameters
        ----------
        schema_url :
            A GitHub ``/tree/`` URL pointing to the schema folder, e.g.
            ``https://github.com/org/repo/tree/tag/path/to/schema``.
        github_token :
            Optional GitHub personal-access token.  Falls back to the
            ``GITHUB_TOKEN`` environment variable when omitted.
        """
        import os
        import re

        import requests as _requests

        m = re.match(
            r"^https://github\.com/([^/]+/[^/]+)/tree/([^/]+)/(.+?)/?$",
            schema_url,
        )
        if not m:
            raise ValueError(
                f"Cannot parse GitHub tree URL: {schema_url!r}. "
                "Expected the form https://github.com/org/repo/tree/tag/path."
            )
        specs_base = (
            f"https://raw.githubusercontent.com/{m[1]}/{m[2]}/{m[3]}/specs/"
        )

        token = github_token or os.environ.get("GITHUB_TOKEN")
        cache_key = (schema_url, token)
        if cache_key in _schema_cache:
            return _schema_cache[cache_key]

        headers = {"Authorization": f"Bearer {token}"} if token else {}

        def _get(path: str) -> str | None:
            resp = _requests.get(specs_base + path, headers=headers, timeout=15)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.text

        oold_raw = _get("schema.oold.yaml")
        if oold_raw is None:
            raise RuntimeError(
                f"schema.oold.yaml not found at {specs_base}. "
                "Check that schema_url points to a valid schema folder."
            )

        instance = cls.__new__(cls)
        instance.dir = None
        instance._schema = yaml.safe_load(oold_raw)
        instance._context = instance._schema.get("@context", {})
        instance._transform_src = _get("transform.simplified.jsonata")
        instance._vocab_cache = {}
        _schema_cache[cache_key] = instance
        return instance

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
            extends a base schema (e.g. tensile-test extends characterization/generic).

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
