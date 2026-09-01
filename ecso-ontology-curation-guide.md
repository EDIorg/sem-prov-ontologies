# ECSO Ontology Curation Guide

A comprehensive guide for curators and automated AI agents to edit, query, validate, and contribute to the Ecosystem Ontology (ECSO).

---

## 1. Identifier Format & URI Syntax

### ECSO URI Structure

**Standard Format**: `http://purl.dataone.org/odo/ECSO_00000001`

Where:
- **Prefix / Namespace**: `http://purl.dataone.org/odo/ECSO_` (or CURIE `ECSO:00000001`)
- **Local ID**: 8-digit zero-padded numeric string (e.g., `00001122`, `00010136`)

**Examples**:
- `http://purl.dataone.org/odo/ECSO_00001122` (`ECSO:00001122` - Freshwater Total Inorganic Carbon)
- `http://purl.dataone.org/odo/ECSO_00002386` (`ECSO:00002386` - Dissolved Oxygen Saturation)

### URI Assignment & Dynamic ID Discovery

1. **New Terms**: Dynamically discover the next available ID by identifying the highest existing numeric ID allocated for classes in `ecso/ECSO8.owl` and incrementing by 1 (e.g., `ECSO:00010137`).
2. **Helper Tool**: Agents and curators should run the dynamic ID discovery utility (e.g., `python3 scripts/get_next_ecso_id.py` or equivalent inline inspector) to mint sequential, collision-free IDs.
3. **No ID Reuse**: Never reuse URIs for new terms, even if an old term is deprecated.
4. **Resolution**: URIs resolve through the DataONE persistent URL service.
5. **Strict 8-Digit Format**: Avoid non-standard or legacy formats (such as string fragment URIs like `ECSO_#Leaf_Area_Index`). All newly minted terms must use standard 8-digit numeric formatting.

---

## 2. Term Annotation Standards

### Required Annotation Properties

All terms in ECSO must include:

| Property | CURIE / IRI | Purpose & Format |
| :--- | :--- | :--- |
| `rdfs:label` | `rdfs:label` | Lowercase primary term label (e.g., `freshwater total inorganic carbon`) |
| `IAO:definition` | `IAO:0000115` | OBO-compliant genus-differentia definition: `A <parent> which <differentia>` |
| `dc:creator` | `dc:creator` | Full ORCID URL of term creator (e.g., `https://orcid.org/0000-0002-4366-3088`) |
| `dc:date` | `dc:date` | ISO 8601 creation timestamp (e.g., `2026-09-01T12:00:00Z`) |

### Optional Annotation Properties

| Property | CURIE / IRI | Purpose |
| :--- | :--- | :--- |
| `oboInOwl:hasExactSynonym` | `oboInOwl:hasExactSynonym` | Exact synonyms or interchangeable alternative labels |
| `oboInOwl:hasNarrowSynonym` | `oboInOwl:hasNarrowSynonym` | Narrower terms with specialized meaning |
| `oboInOwl:hasBroadSynonym` | `oboInOwl:hasBroadSynonym` | Broader terms encompassing the concept |
| `oboInOwl:hasRelatedSynonym` | `oboInOwl:hasRelatedSynonym` | Linguistically related or associated terms |
| `rdfs:comment` | `rdfs:comment` | Contextual notes, domain nuances, non-universal attributes |
| `rdfs:seeAlso` | `rdfs:seeAlso` | Related external concepts or documentation |
| `oboInOwl:hasDbXref` | `oboInOwl:hasDbXref` | Cross-references to external vocabularies (SWEET, ENVO, CHEBI, etc.) |
| `IAO:definition_source` | `IAO:0000119` | Direct URL, PMID, DOI, or expert citation for verbatim/adapted definitions |
| `IAO:term_tracker_item` | `IAO:0000233` | Full GitHub issue URL tracking the curation request |
| `owl:deprecated` | `owl:deprecated` | Boolean `true` for obsolete concepts |
| `IAO:term_replaced_by` | `IAO:0000110` | URI of the replacement term when deprecated |

> [!IMPORTANT]
> **Avoid Literal in `owl:sameAs`**:
> - ❌ WRONG: `owl:sameAs "http://purl.dataone.org/odo/ECSO_00001523"`
> - ✅ CORRECT: `owl:sameAs <http://purl.dataone.org/odo/ECSO_00001523>`

---

## 3. Concept Definition Principles (OBO Genus-Differentia Pattern)

ECSO strictly follows the **OBO Foundry Aristotelian Genus-Differentia** pattern for all textual definitions (`IAO:0000115`):

### Definition Rules
- **Template**:
  - Entities, qualities, and measurements: `A <genus> which <differentia>.`
  - Processes: `A <genus> during which <differentia>.`
- **Genus**: Must match the exact primary label of the direct parent class (`rdfs:subClassOf`) in lowercase. Do not modify the genus with leading adjectives (e.g., use `A <parent> which is <adjective>...` instead of `An <adjective> <parent>...`).
- **Differentia**: Specifies universal, essential distinguishing characteristics. When multiple criteria exist, use modular numbering: `A <genus> which 1) <C1>, 2) <C2>, and 3) <C3>.`
- **Separation of Concerns**: Keep definitions minimal and universally true. Move non-universal details, sampling protocols, sensor models, and examples to `rdfs:comment`.
- **Citations**: Every definition must cite a verifiable reference URL or DOI (`IAO:0000119` or `oboInOwl:hasDbXref`).

### Examples
- ✅ **Good**: `A soil respiration rate which is determined by the metabolic activity of soil microorganisms.` (Parent: `soil respiration rate`)
- ❌ **Bad**: `An autotrophic soil respiration rate measured using dynamic gas chambers.` (Modified genus, embeds protocol into definition rather than `rdfs:comment`).

### Antipatterns to Avoid
- **Circularity / Tautology**: Defining a term using its own label without adding distinguishing semantic criteria.
- **Modified Genus**: Injecting adjectives into the genus subject position rather than the differentia clause.
- **Negative Definitions**: Stating what something is *not* rather than what it *is*.
- **Protocol Overreach**: Placing measurement techniques, sensor models, or sampling intervals in definitions instead of comments.
- **Parent Mismatch**: Stating a genus that does not match the asserted superclass in the hierarchy.

---

## 4. Querying & Semantic Search (OAK / SemSQL)

To search for existing concepts, check for duplicates, and inspect term hierarchies without error-prone raw text grepping, use the **Ontology Access Kit (`runoak`)**:

### Common OAK Query Commands
- **Term Lookup by ID**:
  ```bash
  runoak -i ecso/ECSO8.owl info ECSO:00001122
  ```
- **Fuzzy Search & Synonym Matching**:
  ```bash
  runoak -i ecso/ECSO8.owl search 'dissolved oxygen'
  ```
- **Hierarchical Ancestor Inspection**:
  ```bash
  runoak -i ecso/ECSO8.owl ancestors ECSO:00001122
  ```
- **Subclass / Descendant Inspection**:
  ```bash
  runoak -i ecso/ECSO8.owl descendants ECSO:00000010
  ```

### Duplicate Detection Policy
Before creating any term:
1. Search `ECSO8.owl` using `runoak search '<proposed label>'` and synonyms.
2. If the concept already exists as a primary label or exact synonym, **do not recreate or duplicate it**. Report the existing term ID and definition.

---

## 5. Curation & Editing Workflow (ROBOT Templates)

ECSO adopts the automated **ROBOT CSV Template** workflow for all term additions, updates, and relationship curation. Direct manual editing in Protégé is avoided in favor of deterministic, scriptable, and version-controlled ROBOT pipelines.

### Standard ROBOT CSV Template Structure

ROBOT template CSV files are authored in `ecso/modules/` (e.g., `ecso/modules/new_terms_template.csv`).

- **Row 1**: Human-readable column headers
- **Row 2**: ROBOT template instruction strings

| Column Header (Row 1) | ROBOT Template Definition (Row 2) | Expected Value / Format | Example |
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
| `term tracker item` | `A IAO:0000233` | GitHub Issue URL | `https://github.com/clnsmth/sem-prov-ontologies/issues/92` |
| `creation date` | `A dc:date` | ISO 8601 timestamp | `2026-09-01T12:00:00Z` |
| `created by` | `A dc:creator SPLIT=\|` | Full creator ORCID URL | `https://orcid.org/0000-0002-4366-3088` |

### Template Compilation & Merging Pipeline

1. **Convert Template CSV to Temporary OWL Module**:
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

2. **Merge Module into Primary ECSO Ontology**:
   ```bash
   robot merge \
     --input ecso/ECSO8.owl \
     --input ecso/modules/temp.owl \
     --collapse-import-closure false \
     convert --format rdfxml --output ecso/ECSO8.owl
   ```

---

## 6. Automated Testing & Validation Pipeline

All changes must pass automated syntactic and semantic validations before committing.

### Validation Steps

1. **Profile Validation**:
   Ensure OWL 2 DL compliance:
   ```bash
   robot validate-profile --input ecso/ECSO8.owl --profile DL -o ecso/build/profile_report.txt
   ```

2. **Reasoner Consistency Check**:
   Verify that no classes are unsatisfiable (`owl:Nothing`) and logical axioms are consistent using HermiT or ELK:
   ```bash
   robot reason --input ecso/ECSO8.owl --reasoner hermit --dump-inferred-axioms false
   ```

3. **Report Generation (QC Checks)**:
   Run ROBOT report to detect missing labels, duplicate definitions, or broken annotations:
   ```bash
   robot report --input ecso/ECSO8.owl --output ecso/build/robot_report.tsv
   ```

---

## 7. Git Workflow & Branching Strategy

All curation activities follow a structured Git feature branch model targeting the **`develop`** branch of `clnsmth/sem-prov-ontologies`.

### Branching Model

| Branch | Purpose | PR / Merge Target |
| :--- | :--- | :--- |
| **`develop`** | Active development & feature integration | Base branch for all feature PRs |
| **`main`** | Stable release versions | Merged from `develop` upon release |
| **`feature-{ISSUE_NUMBER}-{description}`** | Issue-specific curation branch | Base: `develop` → Target PR: `develop` |

### Step-by-Step Git Process

1. **Sync develop Branch**:
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature-92-soil-microbial-respiration develop
   ```

3. **Author Template & Apply ROBOT Pipeline**:
   - Write CSV template in `ecso/modules/`.
   - Run `robot template` and `robot merge`.
   - Run `robot reason` to validate consistency.

4. **Commit & Push**:
   ```bash
   git add ecso/ECSO8.owl ecso/modules/new_terms_template.csv
   git commit -m "Add soil microbial respiration terms via ROBOT template #92"
   git push origin feature-92-soil-microbial-respiration
   ```

5. **Open Pull Request**:
   Create PR targeting `develop` on `clnsmth/sem-prov-ontologies` using GitHub CLI:
   ```bash
   gh pr create --repo clnsmth/sem-prov-ontologies --base develop --head feature-92-soil-microbial-respiration --title "Add soil microbial respiration terms (#92)" --body "Resolves #92. Created terms via ROBOT template and verified reasoner consistency."
   ```

---

## 8. Commit Message Guidelines & Standards

To maintain clean, searchable, and professional version history across human and AI agent curation, all commits must adhere to standard formatting and structural conventions:

### Formatting Rules

1. **Subject Line**:
   - Write in the **imperative mood** (e.g., "Add...", "Fix...", "Update...", "Deprecate...", "Refactor..."). Avoid past tense ("Added") or present participle ("Adding").
   - Capitalize the first letter and do not place a trailing period.
   - Keep the subject line concise: **50–72 characters maximum**.
   - Reference the associated issue number (e.g., `(#92)` or `#92`).

2. **Message Body**:
   - Separate the subject from the body with **exactly one blank line**.
   - Explain the **what** and **why** of the change, including semantic rationale, parent class placement decisions, and external reference mappings.
   - **Wrap all body lines strictly at 72 characters** to ensure readability in terminal pagers and git logs.
   - Use modular bullet points for multi-term or multi-axiom updates.

3. **Agent Attribution / Signing**:
   - Curations performed by automated agents should sign off or attribute commits as `@edi-ontology-agent` (or designated agent signature).

### Commit Message Template & Examples

#### Standard Format
```text
<Imperative action summary> (#<issue-number>)

<Detailed explanation of semantic and ontological changes, rationale,
and background context. Wrapped strictly at 72 characters per line.>

- <Bullet point 1 detailing specific terms or axioms added/modified>
- <Bullet point 2 detailing validation, sources, or xrefs>
```

#### Example 1: New Term Addition via ROBOT Template
```text
Add soil microbial respiration terms (#92)

Add 'soil microbial respiration rate' (ECSO:00010137) and associated
respiration characteristics via ROBOT template merge:
- Define genus-differentia under soil respiration rate (ECSO:00000010).
- Link definition source to Wikipedia soil respiration reference.
- Add exact and narrow synonyms for heterotrophic respiration.
- Validate OWL 2 DL profile and verify HermiT reasoner consistency.
```

#### Example 2: Term Annotation or Synonym Update
```text
Add exact synonyms to dissolved organic carbon (#104)

Add exact synonyms 'DOC' and 'dissolved OC' to ECSO:00001205 to improve
search discoverability across ecological observation datasets.
```

#### Example 3: Deprecating Redundant Term
```text
Deprecate redundant leaf area index term (#115)

Mark ECSO:00000512 as deprecated (owl:deprecated true) in favor of
canonical ECSO:00002140 with IAO:term_replaced_by.
```

#### Example 4: Syntax or Validation Fix
```text
Fix owl:sameAs literal URI syntax in ECSO8.owl (#120)

Convert string literal to proper URI resource on ECSO:00001523 to
satisfy OWL 2 DL profile validation.
```

---

## 9. Term Hierarchy & Axiomatic Best Practices

### Core Measurement & Characteristic Organization
ECSO organizes environmental and ecosystem measurements around:
- **Measurements & Characteristics**: Carbon dynamics, elemental fluxes, biomass, soil respiration.
- **Physical & Chemical Properties**: Temperature, salinity, dissolved constituents, moisture content.
- **Ecosystem Entities**: Aquatic systems, terrestrial active layers, atmospheric boundaries.

### Axiom Construction in Templates
- Class expressions must be enclosed in parentheses: `('property' some 'target')`.
- Multiple axioms in a single CSV cell are pipe-delimited: `('part of' some 'soil active layer')|('has quality' some 'moist')`.
- Prefer single, clear parentage over unnecessary polyhierarchy unless multiple superclasses are conceptually required.

---

## 10. Quality Assurance Checklist for Curators & Agents

### Pre-Commit Checklist
- [ ] Next ID dynamically minted without collisions (8-digit standard `ECSO:XXXXXXXX`).
- [ ] Primary label is lowercase (unless containing proper nouns).
- [ ] Textual definition follows `A <parent> which <differentia>`.
- [ ] Definition reference URL/DOI is provided and validated as live.
- [ ] Creator ORCID is present in `dc:creator`.
- [ ] Creation timestamp in `dc:date` is valid ISO 8601.
- [ ] Issue tracker referenced via `IAO:0000233`.
- [ ] Synonyms correctly categorized (`hasExactSynonym`, `hasBroadSynonym`, etc.).
- [ ] No `owl:sameAs` pointing to raw string literals (URIs only).
- [ ] Commit message follows formatting standards (imperative mood, wrapped at 72 chars, explaining what and why).

### Pre-PR Checklist
- [ ] ROBOT template compiled and cleanly merged into `ecso/ECSO8.owl`.
- [ ] `robot reason` executed with zero unsatisfiable classes.
- [ ] Base branch is `develop` on `clnsmth/sem-prov-ontologies`.
- [ ] Associated GitHub issue referenced in commit and PR description.



