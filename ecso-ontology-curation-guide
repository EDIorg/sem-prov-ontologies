# ECSO Ontology Curation Guide

## 1\. IDENTIFIER FORMAT & URI SYNTAX

### ECSO URI Structure

**Standard Format**: `http://purl.dataone.org/odo/ECSO_00000001`

Where:

- **Prefix**: `ECSO_`  
- **Local ID**: 8-digit zero-padded numeric string

**Examples**:

- `http://purl.dataone.org/odo/ECSO_00001122` (Freshwater Total Inorganic Carbon)  
- `http://purl.dataone.org/odo/ECSO_00002386` (Dissolved Oxygen Saturation)

### URI Assignment Rules

1. **New Terms**: Use the next available URI by incrementing the decimal portion of the most recently minted term  
2. **No Reuse**: Never reuse URIs for new terms, even if an old term is deprecated  
3. **Resolution**: URIs resolve through the DataONE persistent URL service  
4. **Avoid Non-Standard Formats**: Terms with URIs like `ECSO_#Leaf_Area_Index` are legacy errors—use standard 8-digit format only

---

## 2\. TERM ANNOTATION STANDARDS

### Required Annotation Properties

All terms in ECSO must include:

| Property | Namespace | Purpose |
| :---- | :---- | :---- |
| `rdfs:label` | [http://www.w3.org/2000/01/rdf-schema\#](http://www.w3.org/2000/01/rdf-schema#) | Preferred term name |
| `IAO:definition` | [http://purl.obolibrary.org/obo/](http://purl.obolibrary.org/obo/) (IAO\_0000115) | Clear definition of concept |
| `dc:creator` | [http://purl.org/dc/elements/1.1/](http://purl.org/dc/elements/1.1/) | ORCID of term creator |
| `dc:date` | [http://purl.org/dc/terms/](http://purl.org/dc/terms/) | ISO 8601 creation date |

### Optional Annotation Properties

| Property | Purpose |
| :---- | :---- |
| `skos:altLabel` / `obo:hasExactSynonym` | Exact synonyms or alternative names |
| `obo:hasNarrowSynonym` | Narrower terms with similar meaning |
| `obo:hasBroadSynonym` | Broader terms with similar meaning |
| `rdfs:seeAlso` | Related concepts |
| `owl:sameAs` | Equivalent concepts (must use URIs, NOT literals) |
| `dc:description` | Extended information beyond definition |
| `obo:hasDbXref` | Cross-references to external systems |
| `IAO:definition_source` | Source documentation for definition |

### Critical Error: Literal in owl:sameAs

**❌ WRONG**:

owl:sameAs "http://purl.dataone.org/odo/ECSO\_00001523"

**✅ CORRECT**:

owl:sameAs \<http://purl.dataone.org/odo/ECSO\_00001523\>

---

## 3\. SYNONYM & ABBREVIATION HANDLING

### Synonym Classification

1. **Exact Synonyms** (`hasExactSynonym`): Terms that refer to exactly the same concept  
2. **Broad Synonyms** (`hasBroadSynonym`): Terms that are more general  
3. **Narrow Synonyms** (`hasNarrowSynonym`): Terms that are more specific

### Abbreviation Best Practices

- **Be Specific**: Use abbreviations that clarify scope (e.g., "Freshwater POC" not just "POC")  
- **Document Source**: Record where synonyms originated  
- **Avoid Over-Generalization**: Don't use abbreviations that could apply to multiple domains  
- **Classify Carefully**: Use appropriate SKOS/OBO synonym properties

---

## 4\. TERM LIFECYCLE: CREATION & MODIFICATION

### Adding New Terms

1. **File an Issue**: Check GitHub issues to avoid duplication  
2. **Create Feature Branch**: Use naming `feature-{ISSUE_NUMBER}-{description}`  
   - Example: `feature-92-taxonomic-rank-clarification`  
3. **Add Term Metadata**: Include all required annotations  
4. **Link to Sources**: Provide definitions with `IAO:definition_source` when adapted from external ontologies  
5. **Submit Pull Request**: To `develop` branch with clear description

### Modifying Existing Terms

**For Minor Changes** (label fixes, adding synonyms): Create feature branch, submit PR to `develop`

**For Major Changes** (definition rewrites, structure): File issue first for community feedback before implementing

### Deprecating Terms

When a term is deprecated:

1. **Add Deprecation Mark**: `owl:deprecated true`  
2. **Indicate Replacement** (if applicable):  
     
   IAO:term\_replaced\_by \<http://purl.dataone.org/odo/ECSO\_00001234\>  
     
3. **Never Reuse URI**: The old URI remains permanently reserved  
4. **Document Reasoning**: Add comment explaining deprecation

---

## 5\. TERM HIERARCHY & CLASS ORGANIZATION

### High-Level Concept Categories

ECSO organizes concepts around:

- Biomass, Carbon (element & compounds)  
- Productivity, Growth, Primary Production  
- Soil & Water properties  
- Concentration & Flux measurements  
- Ecosystems & Aquatic systems  
- Temperature, Salinity, Dissolved constituents

### Hierarchy Best Practices

1. **Logical Placement**: Place new terms under appropriate parent classes  
2. **Single Hierarchy**: Prefer single, clear hierarchies; avoid polyhierarchy  
3. **Use Multiple Inheritance Sparingly**: Only when a term genuinely belongs to multiple categories  
4. **Defensible Placement**: Be able to explain parent/child relationships in pull requests

---

## 6\. DEVELOPMENT WORKFLOW & BRANCHING STRATEGY

### Branch Structure

| Branch | Purpose | Merge Requirements |
| :---- | :---- | :---- |
| **main** | Stable, released versions | 2 approvals required; via PR from `develop` |
| **develop** | Integration branch for features | Ready-to-deploy code only |
| **feature/**\* | Individual feature development | Frequent merges with `develop` |

### Feature Branch Naming

feature-{ISSUE\_NUMBER}-{description}

Examples: `feature-92-taxonomic-rank-definitions`, `feature-91-environmental-measurement-types`

### Contributor Workflow

1. **Fork** and **Clone** repository  
2. **Checkout develop**: `git checkout develop`  
3. **Create feature branch**: `git checkout -b feature-{ISSUE_NUMBER}-{description}`  
4. **Commit** with clear messages  
5. **Push** to your fork  
6. **Create Pull Request** to `develop` branch  
7. **Address review feedback**; merge once approved

### Pull Request Checklist

- [ ] Associated GitHub issue exists and is referenced  
- [ ] Base branch is `develop` (not `main`)  
- [ ] OWL files are valid; pass reasoner validation  
- [ ] New terms follow ECSO standards  
- [ ] Clear PR description with rationale  
- [ ] No merge conflicts

---

## 7\. TESTING & VALIDATION

### OWL File Validation

**Tools**: Pellet reasoner, Hermit reasoner

**Validation Steps**:

1. Open `.owl` file in Protégé  
2. Load ontology  
3. Run reasoner to check consistency  
4. Address inferred axioms or inconsistencies  
5. Export inferred axioms if needed for publication

### Release Pattern

For ontologies with inferred versions (MOSAiC, ARCRC):

- Edit only the `*_raw.owl` file  
- Run reasoner (Pellet recommended)  
- Export axioms to generate published version  
- Example: `MOSAiC_raw.owl` → (Pellet) → `MOSAiC.owl`

---

## 8\. ONTOLOGY FILE STRUCTURE & EDITING

### Main File: `ECSO8.owl`

- **Format**: OWL (Web Ontology Language)  
- **Serialization**: RDF/XML (default) or Turtle (preferred)  
- **Size**: \~2.3 MB (includes imports)  
- **Editing Tool**: Protégé recommended

### File Organization

1. **Consistent Formatting**: Follow existing style in `.owl` files  
2. **Group Related Terms**: Organize class hierarchies by topic  
3. **Include Comments**: Explain complex relationships or design decisions  
4. **Namespace Declarations**: Include proper namespace prefixes at file top

---

## 9\. QUALITY ASSURANCE CHECKLIST FOR CURATORS

### Before Committing Changes

- [ ] All terms have `rdfs:label` and `IAO:definition`  
- [ ] All creators have ORCID identifiers  
- [ ] All dates in ISO 8601 format  
- [ ] No `owl:sameAs` pointing to string literals (must be URIs)  
- [ ] Synonyms classified with appropriate SKOS/OBO properties  
- [ ] No duplicate terms or reused URIs  
- [ ] Deprecated terms marked with `owl:deprecated true`  
- [ ] Deprecated terms have `IAO:term_replaced_by` reference  
- [ ] Hierarchy placement is logically sound  
- [ ] OWL file is syntactically valid

### Before Submitting Pull Request

- [ ] Reasoner validation passes (no inconsistencies)  
- [ ] All new terms follow ECSO naming conventions  
- [ ] External ontology references use proper URIs  
- [ ] Feature branch is current with latest `develop`  
- [ ] Commit messages are clear and reference issue numbers  
- [ ] PR description explains changes and rationale

### Code Review Points

- [ ] Definition is clear and precise  
- [ ] Term placement in hierarchy is defensible  
- [ ] Synonyms are accurate and appropriately scoped  
- [ ] External references verified  
- [ ] Documentation is complete

