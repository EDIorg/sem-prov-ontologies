# ENVO Ontology Project Guide for AI Agents

This guide provides instructions and conventions for AI agents to edit, query, and contribute to the Environment Ontology (ENVO).

## 1. Project Layout
- The primary development file is `src/envo/envo-edit.owl`. All manual or automated ontology edits must be made directly in this file or via ROBOT templates in the modules directory. Never edit release or compiled files directly, such as `envo.owl`, `envo.obo`, or `envo.json` in either the repository root or the `src/envo/` directory. These are derived files generated during the release build.
- Assigned ID ranges are stored in `src/envo/envo-idranges.owl`. This file stores the designated numeric ID ranges assigned to active curators and editors to prevent ID collisions. AI agents must strictly use IDs allocated within their permitted range.
  - **AI Agent Permitted ID Range**: `ENVO:03622000` to `ENVO:03622999` (ID range 31 allocated to `edi-ontology-agent`).
- ROBOT and pattern modules are located in `src/envo/modules/`. This directory contains CSV templates and modules used by the ROBOT tool for automated term generation and bulk imports.
- The local XML catalog is defined in `src/envo/catalog-v001.xml`. This file defines local URIs and mappings for resolving imported ontologies without requiring active internet connectivity.


## 2. Querying the Ontology
We use the Ontology Access Kit (OAK) CLI (`runoak`) to query our local, dynamically generated SemSQL SQLite database instead of grepping raw files.

- The compiled local SQLite database is located at `src/envo/envo.db`. If this file is missing in your local workspace, generate it on the fly by running `cd src/envo && ./run.sh semsql make envo.db`.
- To look up a specific term by ID, run: `runoak -i sqlite:src/envo/envo.db info ENVO:00000114`
- To search for terms matching a label or description, which handles fuzzy matching and synonyms, run: `runoak -i sqlite:src/envo/envo.db search 'marine environment'`
- To find transitive parent and ancestor classes of a term, run: `runoak -i sqlite:src/envo/envo.db ancestors ENVO:00000114`
- The `runoak` command is in your PATH, and `oaklib` is pre-installed in your environment.
- Do not attempt to run standard grep or raw text searches over files in `src/envo/` because they are structured in OWL XML, and text-based grep is slow and highly inaccurate. Always use `runoak` against the SQLite DB.
- Only use the methods above for searching the ontology.


## 3. Before Making Edits
Before starting any ontology edits, agents must perform a series of semantic checks and research steps to maintain the high logical integrity of ENVO.

- Read the request and gather context. Carefully read the instruction or issue. If a GitHub issue is mentioned, view its detailed thread and discussion by running `gh issue view <issue-number>`. If a literature reference like a PMID, DOI, or URL is provided, always fetch and read its abstract or full text to ensure definitions are accurate and scientific.
- Check for duplicates. Never create a term without first confirming that it does not already exist in the ontology, either as a primary label or an exact synonym. Use the local `runoak` search to scan the SemSQL database by running `runoak -i sqlite:src/envo/envo.db search 'your term name'`.
  - **Creating vs. Updating**: If asked to "add" or "create" a term that already exists (or is an exact synonym of an existing term), do not modify or update it. Immediately halt and report that the concept already exists (citing the ID and definition). Only edit existing terms when explicitly asked to "modify" or "update" them.
- Verify parent classes. Always check the proposed parent terms for logical consistency and scientific accuracy. Run the ancestors command on candidate parent terms to inspect their position in the upper level hierarchy by running `runoak -i sqlite:src/envo/envo.db ancestors ENVO:NNNNNNNN`.
- Match existing design patterns. Check `src/envo/patterns/` for any existing Dead Simple OWL Design Patterns (DOSDP) YAML templates that might apply to your term, such as `biome.yaml`, `ecosystem.yaml`, or `atmospheric_material_subtype.yaml`. If a relevant pattern is found, any new classes or assertions must strictly follow the schema and logical definitions specified in that pattern.


## 4. Editors Guide
- Design patterns are located in `src/envo/patterns/`.


## 5. Edits & Compilation
In ENVO, editing is strictly performed using the ROBOT template pipeline for CSV-based curation. We do not use Protégé. All template compilation, merging, and testing must be executed from `/src/envo/`.

### 1. Git Curation Workflow (ROBOT-based)
Always isolate your changes in a dedicated git branch matching the issue number.
- Synchronize upstream. Fetch and sync your local master branch with the official upstream master:
  ```bash
  git checkout master
  git pull https://github.com/EnvironmentOntology/envo.git master
  git push origin master
  ```
- Checkout a branch. Always create topic branches from your clean master branch to keep agent files separate. Run:
  ```bash
  git checkout -b issue-xyz master
  ```
- Prepare the CSV Template.
  - Create or edit a CSV template file in `src/envo/modules/`, such as `temporary_robot_template.csv`.
  - Line endings must be LF (not CRLF) and special characters must be properly UTF-8 encoded.
- Compile the Template. Convert the CSV template into a temporary OWL module by running:
  ```bash
  robot template --template modules/temporary_robot_template.csv -i envo-edit.owl --prefix "RO:http://purl.obolibrary.org/obo/RO_" --prefix "ENVO:http://purl.obolibrary.org/obo/ENVO_"  --ontology-iri "http://purl.obolibrary.org/envo/modules/temporary_robot_template.owl" convert --format ofn -o modules/temporary_robot_template.owl
  ```
- Merge into the Edit File. Merge the OWL template back into the primary development file `envo-edit.owl` by running:
  ```bash
  robot merge --input envo-edit.owl --input modules/temporary_robot_template.owl --collapse-import-closure false convert --format ofn --output envo-edit.owl
  ```
- Compile & Run Local Tests. Run the validation and build tasks inside `/src/envo/` to invoke the reasoner and check for logical inconsistencies. Any unsatisfiable classes reasoning under `owl:Nothing` will fail the test. Run:
  ```bash
  make test
  ```
- Commit & Push. Commit the updated `envo-edit.owl` along with the source CSV template, and push to create a PR:
  ```bash
  git add src/envo/envo-edit.owl src/envo/modules/temporary_robot_template.csv
  git commit -m "Run robot merge to add template terms #xyz"
  git push origin issue-xyz
  ```

### 2. Defining Relationship Axioms in ROBOT Templates
To add logical links between classes in ROBOT templates, use the subclass axiom column.
- Class expressions containing multiple terms must be wrapped in parentheses. The expected format is `('property' some 'value')`.
- When describing the main constituent of an environmental material, use the 'composed primarily of' (`RO_0002473`) relation to map to other material entities or ChEBI chemical entities. For example, use `('composed primarily of' some 'water ice')` or `('composed primarily of' some 'water')` where water is `CHEBI_15377`.

### 3. Compilation & Local Testing Commands
Execute these verification targets inside the `src/envo/` directory.
- To run standard syntax, profile, and reasoner tests, run: `cd src/envo && make test`
- To run full CI checks locally, run: `cd src/envo && make continuous_integration_test`

### 4. Standard ROBOT CSV Template Reference
When creating or editing a ROBOT template, use the following structure. Row 1 contains the headers, and Row 2 contains the ROBOT template definitions:

| Column Header (Row 1) | ROBOT Template Definition (Row 2) | Purpose & Expected Format |
| :--- | :--- | :--- |
| Ontology ID | ID | The 8-digit CURIE ID of the term, such as ENVO:01001234. |
| label | A rdfs:label | The lowercase primary label, such as seawater. |
| parent class | SC % | Label or ID of the parent class, such as environmental material. |
| definition | A IAO:0000115 | Textual genus-differentia definition, such as A B which Cs. |
| definition cross reference | AI oboInOwl:hasDbXref SPLIT=\| | Pipe-separated reference URLs/ORCIDs for the definition (no spaces). |
| comment | A rdfs:comment | Non-universal but useful supporting context. |
| comment cross reference | AI oboInOwl:hasDbXref SPLIT=\| | Pipe-separated reference URLs/ORCIDs for the comment. |
| editors note | A IAO:0000116 | Developer notes, engineering decisions, or TODOs. |
| exact synonym | AL oboInOwl:hasExactSynonym@en SPLIT=\| | Interchangeable term labels, such as seawater\|sea water. |
| broad synonym | AL oboInOwl:hasBroadSynonym@en SPLIT=\| | Broader synonym terms, such as acid rain. |
| narrow synonym | AL oboInOwl:hasNarrowSynonym@en SPLIT=\| | Narrower synonym terms, such as highway. |
| related synonym | AL oboInOwl:hasRelatedSynonym@en SPLIT=\| | Linguistically loose or related synonyms, such as sea floor. |
| in subset | AL oboInOwl:inSubset SPLIT=\| | Target ENVO subsets/slims, such as envoPolar\|envoPlastics. |
| cross reference | AI oboInOwl:hasDbXref SPLIT=\| | Cross-references to SWEET or other vocabularies. |
| subclass axiom | SC % | Computable logical relationships, such as ('part of' some 'coast'). |
| creation date | A dc:date | ISO 8601 creation timestamp, such as 2026-07-17T13:56:27Z. |
| created by | A dc:creator SPLIT=\| | Creator's full ORCID URL(s), such as https://orcid.org/0000-0002-4366-3088. |


## 6. Ontology Format Guidelines
To maintain quality and logical consistency across all curated concepts, ENVO enforces strict structural and stylistic rules for term creation.

- Term ID Format. ENVO IDs use exactly 8 digits, unlike the 7-digit IDs common in other OBO ontologies. In ROBOT CSV templates and OAK queries, use the colon format, such as `ENVO:01001234` or `ENVO:03000102`. This is required in ROBOT template ID and parent columns and for running `runoak` commands. In raw OWL files like `envo-edit.owl` and `envo-idranges.owl`, the colon is replaced by an underscore, such as `ENVO_01001234`, as part of full PURL IRIs like `http://purl.obolibrary.org/obo/ENVO_01001234`. Assign IDs for new term requests strictly within your assigned range in `src/envo/envo-idranges.owl` to avoid ID collisions. Never guess IDs, and use `runoak` to verify.
- Class Labels. Class labels are lowercase, such as `marsh`, `water ice`, or `seawater`. Proper nouns and standard groupings can be capitalized, such as `Taylor column` or `WMO blizzard`.
- Textual Definitions. All definitions must follow OBO Foundry principles, using either the format `A B which Cs` like "A chair which is red" or `A B during which C` like "A mass wasting process during which slab snow rapidly moves...". The parent term B must match the exact label of the direct parent class. Do not modify B with adjectives in the genus part, using "A B which is green..." instead of "A green B...". If there are multiple differentiating attributes, use a clean modular numbered list in the format `A B which 1) C1s, 2) C2s, and 3) C3s`. Keep differentiae minimal and universally true of all subclasses of the term. If there are useful properties or attributes that are not universally true of all subclasses, do not put them in the definition. Instead, document them in the `rdfs:comment` field (the `comment` column in templates) to keep definitions clean and minimal.
- Synonyms. ENVO uses four distinct synonym types to handle terminology variations. Synonym values are literal strings. The `has_exact_synonym` relation in the `exact synonym` column represents interchangeable class names, such as seawater and sea water. The `has_broad_synonym` relation in the `broad synonym` column represents synonyms broader than the primary label, such as acid rain for the process acid rainfall. The `has_narrow_synonym` relation in the `narrow synonym` column represents synonyms more specific than the primary label, such as highway for road. The `has_related_synonym` relation in the `related synonym` column represents linguistically loose or related synonyms that are not strictly equivalent, such as sea floor for ocean floor.
- Subsets and Slims. Subsets are slimmed-down selections of ENVO built for specific user communities or projects, such as `envoPolar` or `envoPlastics`. Annotate a term's subset membership using the `in subset` template column, separating multiple subsets by a pipe with no spaces.
- Definition Citations. Every definition must cite a reference, which can be a scholarly URL, PMID, DOI, or expert ORCID. For verbatim definitions, map to the definition source (`IAO_0000119`) property. For paraphrased or adapted definitions, map to the database cross reference (`oboInOwl:hasDbXref`) property.


## 7. Publications & Citations
All term definitions and significant comments in ENVO must be substantiated with reliable literature or expert citations.

- Finding References. Always search literature databases or the web to locate the correct PMIDs, DOIs, or persistent glossary URLs. Do not guess citations.
- Reference Formats. URLs and IRIs are strongly preferred for web glossaries and open databases. PMIDs and DOIs are preferred for scholarly publications. ORCIDs are used to credit expert individual knowledge. Literal strings, such as book ISBNs, can be used if no persistent URI exists.
- Specifying Citations in ROBOT Templates. Map verbatim text to the `definition source` (`IAO_0000119`) property. Map paraphrased or adapted text to the `database_cross_reference` (`oboInOwl:hasDbXref`) property.
- Multiple References. Combine multiple citations in a single ROBOT template cell using the pipe delimiter without spaces, as in: `https://www.ec.gc.ca/meteo-weather/|http://glossary.ametsoc.org/wiki/Main_Page`


## 8. GitHub Contribution Process
- Most requests from users follow one of two patterns. Either you are not confident how to proceed, in which case you should end by asking a clarifying question via `gh`, or you are confident how to proceed, in which case you should make changes, commit on a branch, and open a PR for the user to review.
- **Strict Git & PR Rule (Ephemeral Runner)**: Since you run in a single-turn, ephemeral GitHub Actions runner, any local file modifications left on disk will be lost forever when the run ends. If you make ANY modifications to repository files (even minor or intermediate ones), you MUST commit, push your branch, and open a Pull Request (or Draft PR) targeting the master branch before terminating your execution. Always reference the PR in your GitHub issue comments.
- Check existing terms before adding new ones.
- For new terms, provide a name, definition, place in the hierarchy, and references.
- Include PMIDs, DOIs, or URLs for all assertions.
- Follow naming conventions from parent terms.
- Always commit in a branch, such as issue-NNN. To prevent agent harness or configuration files from leaking into the upstream official ENVO repository, always base your branch directly on your clean master branch. Run:
  ```bash
  git checkout master
  git pull https://github.com/EnvironmentOntology/envo.git master
  git push origin master
  git checkout -b issue-xyz master
  ```
- If there is an existing PR which you started, checkout that branch and continue, rather than starting a new PR, unless you explicitly want to abandon the original PR because it was on completely the wrong tracks.
- Always make clear detailed commit messages, saying what you did and why.
- Always sign your commits as `@edi-ontology-agent`.
- Create PRs using `gh pr create`. When creating a Pull Request, you **MUST** target the fork repository `EDIorg/envo` (e.g., `gh pr create --repo EDIorg/envo`) and **NEVER** target the official upstream `EnvironmentOntology/envo` repository, to avoid notifying upstream maintainers.
- File PRs with clear descriptions, and sign your PR.


## 9. Handling GitHub Issues and Requests
- Use the `gh` tool to read and write issues and PRs.
  - **Repository Targeting**: When running in GitHub Actions, the local repository's default configuration is automatically set using `gh repo set-default` to target the active fork repository. Ensure all your manual or automated issue and PR operations align with this dynamically configured target for maximum portability.
- Sign all commits and PRs as `@edi-ontology-agent`.


## 10. Troubleshooting
- ROBOT Template Compilation Errors. If the CSV template fails to compile, append the `-vvv` verbose flag to the `robot template` command to view the full Java stack trace and pinpoint the exact row or cell formatting error by running:
  ```bash
  robot template -vvv --template modules/temporary_robot_template.csv -i envo-edit.owl ...
  ```
- Reasoner or Profile Validation Failures. If `make test` fails, check the console output to identify unsatisfiable classes or syntax profile violations. To trace low-level parsing issues in the main OWL file, you can run:
  ```bash
  robot convert -vvv -i envo-edit.owl -f ofn -o /dev/null
  ```


## 11. Other Metadata & Annotations
- Issue Tracking. Link back to the GitHub issue using the `term_tracker_item` annotation property with the full issue URL.
- Definitions. Every new class must have exactly one definition, with at least one definition xref pointing to a PMID, DOI, or scholarly URL.
- Creator Annotation. Value must be the full ORCID URL of the curator/editor, such as `https://orcid.org/0000-0002-4366-3088`. In ROBOT templates, map this to the `created by` column.
- Contributor Annotation. Credit additional individuals or organizations using ORCID URLs.
- Creation Date. Track term creation timestamps using the ISO 8601 format, such as `2026-07-17T13:56:27Z`. In ROBOT templates, map this to the `creation date` column.


## 12. Relationships & Axioms
- Parent Class. Every term must have at least one parent, specified in the `parent class` column of ROBOT templates or as an asserted subclass.
- Core Relationships. The `'composed primarily of'` (`RO_0002473`) relation is used to describe the main constituent of an environmental material. Map to other materials or ChEBI chemical entities, such as the `pedosphere` composed primarily of some `soil`, or liquid water composed primarily of some `water` (`CHEBI:15377`).
- The `'part of'` (`BFO_0000050`) relation is used when a term is a physical or structural part of another, such as a `shore` is part of a `coast`.
- The `'has part'` (`BFO_0000051`) relation is the inverse of `'part of'`.
- The `'occurs in'` (`BFO_0000066`) relation is used to link a process to the environmental system or material where it takes place, such as a process occurring in some ecosystem.
- The `'formed as result of'` (`RO_0002354`) relation links a material entity to the process that created it.
- Other common properties include `adjacent to` (`RO_0002151`), `has quality` (`RO_0000086`), `overlaps` (`RO_0002131`), `input of` (`RO_0002233`), `output of` (`RO_0002234`), `located in` (`RO_0001025`), `location of` (`RO_0001015`), and `determined by` (`RO_0002507`).


## 13. Logical Definitions
- Logical definitions must follow the genus-differentia form, and the text definition should closely mirror the logical assertions like subclass axioms and restrictions.
- Subclass Axioms in ROBOT Templates. Specify subclass restrictions in the `subclass axiom` column of the CSV. Always wrap expressions containing multiple terms in parentheses, in the format `('property' some 'value')`. Use the pipe delimiter without spaces to list multiple axioms in a single template cell.
- Example. Under this schema, the label is `grain of snow`, the parent class is `ice mass`, and the textual definition is "An ice mass which is 1) on the order of 1 millimeter or less, 2) has a white and opaque appearance, and 3) is formed as a result of water droplets freezing during precipitation." The subclass axioms cell contains: `('has quality' some (opaque and white))|('formed as result of' some 'freezing of water into water ice')|('participates in' some 'precipitation process')`


## 14. Workflow: EDI to ENVO Term Request Mapping
When a curator requests mapping an issue containing an "EDI Annotation Studio New Term Request" (indicated by the presence of headings like `### Suggested Term Name`, `### Description`, and `### ORCID URL`), follow the mapping, duplicate checks, and missing-field inference guidelines defined in `.agents/skills/edi-to-envo-mapping.md`.
- Trigger the mapping workflow dynamically for any mention with intent matching variations of "map this" or "convert to ENVO request".
- Always use existing OAK search strategies (`runoak search`) as documented in `## 2. Querying the Ontology` and `.agents/agents/ontology-term-lookup.md` to verify if the suggested term or synonyms already exist locally.
- If the term already exists, report back immediately and halt.
- If the term does not exist:
  - Extract the EDI fields and proactively identify/fill any missing required information (such as missing descriptions or references) by web search or inference.
    - **CRITICAL**: Do NOT perform complex academic/literature database searches (such as PubMed/DOI lookups) to fetch a peer-reviewed publication. Instead, use a direct URL to a specific Wikipedia page or glossary page representing the source of the definition. General search engine query URLs (such as Google search results) are NOT valid.
    - **VERIFICATION**: Verify that all fetched/used reference URLs or DOIs actually resolve to active, live webpages before outputting them. Do not include broken or dead links.
    - **CRITICAL COUPLING**: The textual definition and the 'Definition Source / Reference' field MUST be tightly coupled. The textual definition MUST be derived directly and exclusively from the specific webpage whose URL is used in the reference citation field. Never mix multiple sources or mismatch the definition and its source URL.
  - Formulate OBO-compliant genus-differentia definitions starting with a lowercase parent term.
  - Output the mapped request exactly as a copy-pasteable ENVO New Term Request markdown block for the upstream tracker, rather than a table.
    - **CRITICAL**: NEVER output the local repository issue thread URL in the 'Term Tracker Item' field. You must ALWAYS output exactly the literal boilerplate string: `[To be filled in with the ENVO issue URL]`.


## 15. Specialized Multi-Agent Profiles
To maintain high logical quality and delegate specific curation tasks, our AI ontology agent system utilizes 7 distinct, specialized subagent profiles defined under `.agents/agents/`. When handling issue requests, the agent harness references these custom system prompts and instructions:

1. **`task-coordinator.md`**: The master planning and orchestration agent. Used at the start of any task to analyze requests, distinguish creation vs. modification, plan subagent execution sequences, and verify that final merge validations are scheduled.
2. **`deep-research-specialist.md`**: Specialized in literature review. When external references (PMIDs, DOIs, URLs) are provided, this profile fetches and parses the reference abstracts or full text using `aurelian` or web searches to draft accurate, scientifically grounded definitions.
3. **`design-pattern-advisor.md`**: Responsible for Dead Simple OWL Design Pattern (DOSDP) template compliance. Inspects templates in `src/envo/patterns/` (such as `biome.yaml`, `ecosystem.yaml`, or `atmospheric_material_subtype.yaml`) and ensures any new assertions adhere strictly to pattern schemas.
4. **`identifier-validator.md`**: Guards the ontology against hallucinated or malformed identifiers. Formally verifies PMID format and existence, checks database cross-references (CHEBI, NCBITaxon, FoodOn, Wikidata) using Bioregistry lookups, and flags inconsistent or inactive external references.
5. **`metadata-checker.md`**: Performs strict metadata validation on new or modified terms. Confirms the presence of mandatory annotations, such as `created by` (full curator ORCID URL), `creation date` (ISO 8601 timestamp), correct label casing, and `term_tracker_item` links.
6. **`ontology-reasoner.md`**: The logical consistency gatekeeper. Executes standard reasoning tests via `make test`, diagnoses unsatisfiable classes and conflicting axioms using `robot explain`, and suggests logical restructuring or axiom edits to resolve conflicts.
7. **`ontology-term-lookup.md`**: Handles semantic lookup, synonyms, and class searches. Queries the compiled SemSQL SQLite database (`src/envo/envo.db`) using the OAK CLI (`runoak`) to detect duplicates and Candidate parent classes.

