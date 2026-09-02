# ECSO AI Agent Manual Verification Testing Matrix

This guide provides a comprehensive test suite of copy-pasteable GitHub issues to manually verify that `@clnsmth-ontology-agent` executes all target curation behaviors correctly in `clnsmth/sem-prov-ontologies`.

---

## Overview & Execution Instructions

1. **Prerequisites**: Ensure the GitHub Actions workflow `AI Agent GitHub Mentions` is active on the repository and your username is in `.github/ai-controllers.json`.
2. **Issue Creation**: Open a new issue in `clnsmth/sem-prov-ontologies` using the copy-pasteable **Issue Title** and **Issue Body** from each test case below.
3. **Execution**: The workflow will trigger automatically upon issue creation or assignment, post an `eyes` reaction, and post a progress comment with a link to the GitHub Actions run.
4. **Verification**: Inspect the resulting automated comment, PR creation, commit message format, and reasoner validation checks.

---

## Test Case 1: New Term Request (Creation Workflow)

**Target Behavior**: Agent detects term is novel, mints next available 8-digit ID (`ECSO:00010137`), generates a ROBOT template in `ecso/modules/`, merges into `ecso/ECSO8.owl`, validates reasoner consistency, and opens a PR targeting `develop`.

### Issue Title
```text
New term request: sap flux density
```

### Issue Body
```markdown
@clnsmth-ontology-agent please create a new term for `sap flux density`.

- **Preferred Term Label**: sap flux density
- **Parent Class**: mass flux rate (ECSO:00000010)
- **Textual Definition**: A mass flux rate which measures the volume or mass of sap passing through a given cross-sectional area of xylem tissue per unit time.
- **Definition Reference**: https://en.wikipedia.org/wiki/Sap_flow
- **Exact Synonym(s)**: sap flow velocity|sap velocity
- **Subclass Axiom**: ('has part' some 'water')
- **Created By**: https://orcid.org/0000-0002-5896-7295
```

### Expected Agent Deliverables
- [ ] OAK duplicate search confirms concept does not exist.
- [ ] Runs `python3 scripts/get_next_ecso_id.py` and assigns `ECSO:00010137`.
- [ ] Creates ROBOT template in `ecso/modules/`.
- [ ] Compiles and merges into `ecso/ECSO8.owl`.
- [ ] Validates syntax and reasoner (`robot validate-profile --profile DL` and `robot reason --reasoner hermit`).
- [ ] Opens Pull Request targeting base `develop` with branch `clnsmth-ontology-agent-issue-<NUM>-run<RUN>`.
- [ ] Signs commit and PR as `@clnsmth-ontology-agent`.

---

## Test Case 2: Enrich Existing Term Lacking Definition (Conservative Policy)

**Target Behavior**: Agent recognizes existing term `ECSO:00001122`, inspects ancestors/descendants to formulate an OBO genus-differentia definition, preserves existing axioms, merges changes, and opens a PR targeting `develop`.

### Issue Title
```text
Add textual definition and reference to ECSO:00001122
```

### Issue Body
```markdown
@clnsmth-ontology-agent please add a textual definition and reference to ECSO:00001122 (`dissolved oxygen`).

- **Target Term**: ECSO:00001122
- **Definition Source / Reference**: https://en.wikipedia.org/wiki/Oxygen
- **Curator ORCID**: https://orcid.org/0000-0002-5896-7295

Please ensure the definition follows the OBO genus-differentia format and honors existing ontological commitments without modifying superclasses.
```

### Expected Agent Deliverables
- [ ] Queries `runoak -i ecso/ECSO8.owl info ECSO:00001122` and inspects existing superclasses.
- [ ] Adds `IAO:0000115` textual definition starting with lowercase parent genus (`A dissolved gas concentration which...`).
- [ ] Adds `IAO:0000119` or `oboInOwl:hasDbXref` pointing to `https://en.wikipedia.org/wiki/Oxygen`.
- [ ] Preserves all existing `rdfs:subClassOf` and restriction axioms.
- [ ] Passes HermiT reasoner check and opens PR targeting `develop`.

---

## Test Case 3: Term Modification & Synonym Addition

**Target Behavior**: Agent recognizes explicit modification request, adds exact synonyms and cross-references, validates metadata, and opens a PR targeting `develop`.

### Issue Title
```text
Add exact synonyms and xrefs to ECSO:00001205
```

### Issue Body
```markdown
@clnsmth-ontology-agent please update ECSO:00001205 (`dissolved organic carbon concentration`) with additional exact synonyms and cross-references.

- **Target Term**: ECSO:00001205
- **Exact Synonym(s)**: DOC concentration|dissolved organic carbon
- **Cross Reference**: CHEBI:15377
- **Curator ORCID**: https://orcid.org/0000-0002-5896-7295
```

### Expected Agent Deliverables
- [ ] Updates annotations for `ECSO:00001205` in `ecso/ECSO8.owl`.
- [ ] Validates synonym annotation tags (`oboInOwl:hasExactSynonym`).
- [ ] Merges, tests reasoner, and opens PR targeting `develop`.

---

## Test Case 4: Duplicate Detection Guard (Halt Behavior)

**Target Behavior**: Agent searches `ecso/ECSO8.owl` for `dissolved oxygen saturation`, discovers existing term `ECSO:00002386`, halts immediately without modifying any files, and posts a comment explaining that the term already exists.

### Issue Title
```text
New term request: dissolved oxygen saturation
```

### Issue Body
```markdown
@clnsmth-ontology-agent please create a new term for `dissolved oxygen saturation`.

- **Preferred Term Label**: dissolved oxygen saturation
- **Parent Class**: oxygen concentration
- **Textual Definition**: A relative measure of the amount of oxygen dissolved in water.
- **Reference**: https://en.wikipedia.org/wiki/Oxygen_saturation
- **Created By**: https://orcid.org/0000-0002-5896-7295
```

### Expected Agent Deliverables
- [ ] Runs `runoak -i ecso/ECSO8.owl search 'dissolved oxygen saturation'`.
- [ ] Detects exact match `ECSO:00002386` (`Dissolved Oxygen Saturation`).
- [ ] **Halts immediately** without generating templates or modifying `ecso/ECSO8.owl`.
- [ ] Does **NOT** open a Pull Request.
- [ ] Posts a comment citing `ECSO:00002386` and its existing definition.

---

## Test Case 5: EDI Annotation Studio Term Request Mapping

**Target Behavior**: Agent parses raw markdown from the EDI Annotation Studio, checks for duplicates, infers missing fields and parent classes, formulates an OBO genus-differentia definition, and posts a copy-pasteable ECSO New Term Request block to the issue thread.

### Issue Title
```text
New term request received by the EDI annotation studio: canopy leaf nitrogen content
```

### Issue Body
```markdown
@clnsmth-ontology-agent please map this to ECSO new term request

# Proposed Ontology Term

### Suggested Term Name
canopy leaf nitrogen content

### Description
The mass of nitrogen per unit leaf dry mass or ground area in a forest canopy.

### Reference / Source
https://en.wikipedia.org/wiki/Leaf_nitrogen

### GitHub Username
@clnsmth

### ORCID URL
https://orcid.org/0000-0002-5896-7295

### Attribution Consent
Yes, I consent to attribution under CC-BY.
```

### Expected Agent Deliverables
- [ ] Parses EDI fields (`SUGGESTED_NAME`, `DESCRIPTION`, `REFERENCE`, `CREATOR_ORCID`).
- [ ] Runs OAK duplicate search on `ecso/ECSO8.owl`.
- [ ] Identifies candidate parent class (e.g. `nitrogen content` or `chemical characteristic`).
- [ ] Formulates genus-differentia definition starting with lowercase parent class.
- [ ] Verifies live URL resolution.
- [ ] Posts formatted response containing copy-pasteable `# New Term Request: canopy leaf nitrogen content` block.
- [ ] Does **NOT** open a PR (mapping is an issue-level translation step).

---

## Summary Checklist for Human Verification

| Test Case | PR Created? | Files Modified | Target Branch | Expected Status |
| :--- | :--- | :--- | :--- | :--- |
| **Test 1 (New Term)** | Yes | `ecso/ECSO8.owl`, `ecso/modules/*.csv` | `develop` | Reasoner pass, ID sequential |
| **Test 2 (Enrichment)** | Yes | `ecso/ECSO8.owl`, `ecso/modules/*.csv` | `develop` | Reasoner pass, superclasses preserved |
| **Test 3 (Modification)** | Yes | `ecso/ECSO8.owl` | `develop` | Synonyms/xrefs added |
| **Test 4 (Duplicate Guard)** | **No** | *None* | *N/A* | Halts with explanatory comment |
| **Test 5 (EDI Mapping)** | **No** | *None* | *N/A* | Posts copy-pasteable issue block |
