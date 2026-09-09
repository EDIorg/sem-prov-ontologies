# ECSO Ontology Project Guide for AI Agents

This guide provides instructions, architectural rules, and curation conventions for AI agents to edit, query, validate, and contribute to the Ecosystem Ontology (ECSO).

## 1. Project Layout
- The primary development ontology file is `ecso/ECSO8.owl`. All manual or automated ontology edits must be made directly in this file or via ROBOT templates compiled from `ecso/modules/`.
- Dynamic ID allocation is handled via `scripts/get_next_ecso_id.py`. ECSO uses an 8-digit zero-padded numeric identifier format (`ECSO:XXXXXXXX`). AI agents must dynamically discover and allocate the next sequential ID by running:
  ```bash
  python3 scripts/get_next_ecso_id.py
  ```
- ROBOT modules and CSV templates are located in `ecso/modules/`. This directory contains temporary CSV templates and compiled modules used by the ROBOT tool for automated term generation and batch updates.
- The local XML catalog is defined in `catalog-v001.xml` (or `ecso/catalog-v001.xml` if present).


## 2. Querying the Ontology
We use the Ontology Access Kit (OAK) CLI (`runoak`) to query `ecso/ECSO8.owl` directly instead of grepping raw OWL XML files.

- To look up a specific term by ID:
  ```bash
  runoak -i ecso/ECSO8.owl info ECSO:00001122
  ```
- To search for terms matching a label or description (handles fuzzy matching and synonyms):
  ```bash
  runoak -i ecso/ECSO8.owl search 'dissolved oxygen'
  ```
- To find transitive parent and ancestor classes of a term:
  ```bash
  runoak -i ecso/ECSO8.owl ancestors ECSO:00001122
  ```
- To find transitive descendant and child classes of a term:
  ```bash
  runoak -i ecso/ECSO8.owl descendants ECSO:00000010
  ```
- The `runoak` command is in your PATH and `oaklib` is pre-installed in the environment.
- Do not attempt to run standard grep or raw text searches over `ecso/ECSO8.owl` because OWL RDF/XML text search is slow and semantically inaccurate. Always use `runoak`.


## 3. Before Making Edits
Before starting any ontology edits, agents must perform semantic checks to maintain the logical integrity of ECSO.

- **Read the request and gather context**: Carefully read the instruction or issue. If a GitHub issue is mentioned, view its detailed thread and discussion using `gh issue view <issue-number>`. If a reference URL, PMID, or DOI is provided, fetch and read its abstract or content to ensure definitions are accurate.
- **Check for duplicates**: Never create a term without first confirming that it does not already exist in the ontology, either as a primary label or an exact synonym:
  ```bash
  runoak -i ecso/ECSO8.owl search 'your term name'
  ```
  - **Creating vs. Updating**: If asked to "add" or "create" a term that already exists (or is an exact synonym of an existing term), do not modify or duplicate it. Immediately halt and report that the concept already exists (citing the ID and definition). Only edit existing terms when explicitly asked to "modify" or "update" them.
- **Verify parent classes**: Always check proposed parent terms for logical consistency and scientific accuracy using `runoak -i ecso/ECSO8.owl ancestors ECSO:XXXXXXXX`.
- **Inspect subtree for existing terms**: When enriching existing terms lacking definitions, inspect both ancestors and descendants (`runoak ancestors` and `runoak descendants`) to ensure the definition holds true for all subclasses.


## 4. Concept Definition Principles (OBO Genus-Differentia Pattern)
All textual definitions (`IAO:0000115`) must strictly follow the **OBO Foundry Aristotelian Genus-Differentia** pattern:

- **Template**:
  - Entities, qualities, and measurements: `A <genus> which <differentia>.`
  - Processes: `A <genus> during which <differentia>.`
- **Genus**: Must match the exact primary label of the direct parent class (`rdfs:subClassOf`) in lowercase. Do not modify the genus with leading adjectives (e.g., use `A <parent> which is <adjective>...` instead of `An <adjective> <parent>...`).
- **Differentia**: Specifies universal, essential distinguishing characteristics. When multiple criteria exist, use modular numbering: `A <genus> which 1) <C1>, 2) <C2>, and 3) <C3>.`
- **Separation of Concerns**: Keep definitions minimal and universally true. Move non-universal details, sampling protocols, sensor models, and examples to `rdfs:comment`.
- **Citations**: Every definition must cite a verifiable reference URL or DOI (`IAO:0000119` or `oboInOwl:hasDbXref`).
- **Conservative Definition Policy for Existing Terms**:
  - When enriching terms lacking definitions, the definition must strictly honor and reflect existing structural and logical axioms (superclasses, restrictions, domain/range constraints, and child classes).
  - Do not modify, re-parent, or delete existing axioms when adding missing definitions or references unless explicitly requested and approved by maintainers.


## 5. Edits & Compilation Workflow (ROBOT-based)
In ECSO, editing is performed using the ROBOT template pipeline for CSV-based curation. We do not use Protégé. All template compilation, merging, and testing must be executed from the repository root.

### 1. Git Contributor Workflow
Always isolate changes in a dedicated feature branch based off `develop`:
- Sync develop branch:
  ```bash
  git checkout develop
  git pull origin develop
  ```
- Checkout a feature branch:
  ```bash
  git checkout -b feature-XYZ-description develop
  ```
- Prepare CSV Template:
  - Create or edit a CSV template file in `ecso/modules/`, such as `ecso/modules/new_terms_template.csv`.
  - Line endings must be LF and UTF-8 encoded.
- Compile Template into Temporary OWL Module:
  ```bash
  robot template \
    --template ecso/modules/new_terms_template.csv \
    -i ecso/ECSO8.owl \
    --prefix "ECSO:http://purl.dataone.org/odo/ECSO_" \
    --prefix "RO:http://purl.obolibrary.org/obo/RO_" \
    --prefix "IAO:http://purl.obolibrary.org/obo/IAO_" \
    --ontology-iri "http://purl.dataone.org/odo/ecso/modules/temp.owl" \
    convert --format ofn -o ecso/modules/temp.owl
  ```
- Merge Module into Primary ECSO Ontology:
  ```bash
  robot merge \
    --input ecso/ECSO8.owl \
    --input ecso/modules/temp.owl \
    --collapse-import-closure false \
    convert --format rdfxml --output ecso/ECSO8.owl
  ```
- Run Local Validations:
  ```bash
  robot validate-profile --input ecso/ECSO8.owl --profile DL
  robot reason --input ecso/ECSO8.owl --reasoner hermit --dump-inferred-axioms false
  ```
- Commit & Push:
  ```bash
  git add ecso/ECSO8.owl ecso/modules/new_terms_template.csv
  git commit -m "Add soil respiration terms via ROBOT template #XYZ"
  git push -u origin feature-XYZ-description
  ```
- Submit Pull Request:
  ```bash
  gh pr create --repo EDIorg/sem-prov-ontologies --base develop --head feature-XYZ-description --title "Add soil respiration terms (#XYZ)" --body "Resolves #XYZ. Validated reasoner consistency."
  ```

### 2. Standard ROBOT CSV Template Reference
Row 1 contains column headers; Row 2 contains ROBOT template definitions:

| Column Header (Row 1) | ROBOT Template Definition (Row 2) | Expected Format | Example |
| :--- | :--- | :--- | :--- |
| `Ontology ID` | `ID` | CURIE ID | `ECSO:00010137` |
| `label` | `A rdfs:label` | Lowercase term label | `soil microbial respiration rate` |
| `parent class` | `SC %` | Parent CURIE or label | `ECSO:00000010` |
| `definition` | `A IAO:0000115` | OBO Genus-Differentia definition | `A soil respiration rate which measures...` |
| `definition cross reference` | `AI oboInOwl:hasDbXref SPLIT=\|` | Pipe-separated reference URLs/DOIs | `https://en.wikipedia.org/wiki/Soil_respiration` |
| `comment` | `A rdfs:comment` | Non-universal context | `Commonly measured using dynamic closed chambers.` |
| `exact synonym` | `AL oboInOwl:hasExactSynonym@en SPLIT=\|` | Exact synonym labels | `soil microbial respiration` |
| `broad synonym` | `AL oboInOwl:hasBroadSynonym@en SPLIT=\|` | Broader synonym labels | `soil respiration` |
| `narrow synonym` | `AL oboInOwl:hasNarrowSynonym@en SPLIT=\|` | Narrower synonym labels | `heterotrophic soil respiration rate` |
| `related synonym` | `AL oboInOwl:hasRelatedSynonym@en SPLIT=\|` | Loose/related synonyms | `belowground carbon flux` |
| `cross reference` | `AI oboInOwl:hasDbXref SPLIT=\|` | External vocabulary CURIEs/URIs | `ENVO:01001234\|SWEET:SoilRespiration` |
| `subclass axiom` | `SC %` | OWL class expressions | `('has part' some 'carbon dioxide')` |
| `term tracker item` | `A IAO:0000233` | GitHub Issue URL | `https://github.com/EDIorg/sem-prov-ontologies/issues/92` |
| `creation date` | `A dc:date` | ISO 8601 timestamp | `2026-09-01T12:00:00Z` |
| `created by` | `A dc:creator SPLIT=\|` | Full creator ORCID URL | `https://orcid.org/0000-0002-4366-3088` |


## 6. Commit Message Guidelines
All commit messages authored by agents must follow these conventions:
1. **Subject Line**:
   - Written in the **imperative mood** (e.g. "Add...", "Update...", "Deprecate...").
   - Capitalized, no trailing period, **50–72 characters maximum**.
   - Reference the issue number (e.g., `(#XYZ)` or `#XYZ`).
2. **Message Body**:
   - Separated from subject by exactly one blank line.
   - Explain **what** and **why** of the changes.
   - **Wrapped strictly at 72 characters per line**.
   - Use concise bullet points for specific term/axiom modifications.
3. **Attribution**: Sign commits as `@edi-ontology-agent`.


## 7. GitHub Contribution & PR Rules
- **Strict Git & PR Rule (Ephemeral Runner)**: Since you run in a single-turn, ephemeral GitHub Actions runner, any local file modifications left on disk will be lost when the run ends. If you make ANY modifications to repository files, you MUST commit, push your branch, and open a Pull Request targeting `develop` on `EDIorg/sem-prov-ontologies` before terminating execution.
- **Repository Targeting**: Pull Requests must target **`EDIorg/sem-prov-ontologies`** base branch **`develop`** (never push directly to `develop` or `main`).
- **Signature**: Always sign GitHub comments and reviews as `@edi-ontology-agent`.


## 8. Workflow: EDI to ECSO Term Request Mapping
When a curator requests mapping an issue containing an "EDI Annotation Studio New Term Request" (indicated by headings like `### Suggested Term Name`, `### Description`, and `### ORCID URL`), follow the mapping and inference guidelines in `.agents/skills/edi-to-ecso-mapping.md`.
- Triggered on mentions matching "map this", "convert to ECSO request", or "format for ECSO".
- Run OAK duplicate check on `ecso/ECSO8.owl`. If found, report existing ID/definition and halt.
- If not found, formulate an OBO genus-differentia definition, find candidate parent classes, verify live reference URLs, and post a copy-pasteable ECSO New Term Request block.


## 9. Specialized Multi-Agent Profiles
The curation harness utilizes 7 specialized subagent profiles defined under `.agents/agents/`:

1. **`task-coordinator.md`**: Master planning and orchestration agent. Analyzes requests, checks duplicates, discovers next IDs via `scripts/get_next_ecso_id.py`, sequences subagents, and oversees final ROBOT merge and validation.
2. **`deep-research-specialist.md`**: Researches literature, glossaries, and web references to draft scientifically grounded definitions adhering strictly to the genus-differentia pattern and verifying live URL resolution.
3. **`design-pattern-advisor.md`**: Advises on structural patterns for measurement types, characteristics, and physical/chemical properties in ECSO.
4. **`identifier-validator.md`**: Guards against malformed or hallucinated identifiers. Validates 8-digit `ECSO:XXXXXXXX` IDs, cross-references (CHEBI, ENVO, SWEET, PATO), and live reference URLs.
5. **`metadata-checker.md`**: Validates mandatory annotations (`rdfs:label`, `IAO:0000115`, `dc:creator` ORCID, `dc:date`, `IAO:0000233`) and enforces the conservative definition policy for existing terms.
6. **`ontology-reasoner.md`**: Logical consistency gatekeeper. Runs `robot reason --input ecso/ECSO8.owl --reasoner hermit` and `robot explain` to diagnose unsatisfiable classes or logical conflicts.
7. **`ontology-term-lookup.md`**: Queries `ecso/ECSO8.owl` via `runoak` for semantic search, candidate parents, and duplicate checks.
