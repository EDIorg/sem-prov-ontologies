# Skill: Mapping EDI Annotation Studio Term Requests to ECSO Schema

This skill defines the workflow and mapping rules for converting a "New term request received by the EDI annotation studio" into a standard "ECSO new term request" format.

## Triggering Condition
This workflow is triggered when a human curator mentions `@edi-ontology-agent` on a GitHub issue containing an EDI-formatted term request, asking using any natural variation of:
`@edi-ontology-agent please map this to ECSO new term request` or `@edi-ontology-agent please map this`.

The agent should recognize semantic variations such as:
- "map this"
- "convert to ECSO request"
- "translate this to ECSO schema"
- "format for ECSO"

## Input Format (EDI Annotation Studio Request)
The issue body typically contains the following markdown structure:
```markdown
# Proposed Ontology Term

### Suggested Term Name
[Suggested Term Name]

### Description
[Textual Description]

### Reference / Source
[Reference URL, PMID, or DOI]

### GitHub Username
@[Username]

### ORCID URL
[ORCID URL]

### Attribution Consent
[Attribution Consent Statement]
```

## Mapping & Validation Workflow

### Step 1: Extract Fields and Fill Blanks
Carefully parse and extract fields from the issue body:
- `SUGGESTED_NAME`: Extract from `### Suggested Term Name`
- `DESCRIPTION`: Extract from `### Description`
- `REFERENCE`: Extract from `### Reference / Source`
- `CREATOR_ORCID`: Extract from `### ORCID URL`
- `CREATOR_GITHUB`: Extract from `### GitHub Username`

**Handling Missing Information**:
If any required information is missing, the agent MUST do its best to fill in the blanks proactively:
1. **Missing Name**: Halt and request clarification.
2. **Missing Description**: Attempt to query Wikipedia or search authoritative glossaries using the term name to draft a plausible definition.
3. **Missing Reference**: Do NOT perform complex academic/literature database searches. Output a direct URL to a specific Wikipedia page or specific glossary page where the definition exists.
   - **NO SEARCH ENGINES**: General search engine query links (such as Google search results) are NOT valid citations.
   - **URL VERIFICATION CHECK**: You MUST verify that any reference URL or DOI you fetch actually resolves to an active, live webpage (does not return a 404 or unresolvable domain).
4. **Missing ORCID**: Look up the GitHub user's public profile or use a placeholder, clearly flagging that the ORCID must be updated by the curator.
5. **Always flag any filled-in blanks** at the end of the post so curators are aware of what was inferred.

> [!IMPORTANT]
> **Strict Formatting Overrides**:
> - **NEVER output the local GitHub issue thread URL** in the 'Term Tracker Item' field. You must ALWAYS output exactly the literal string: `[To be filled in with the ECSO issue URL]` on this line.
> - **Strict Source Coupling**: The textual definition and the cited reference URL MUST be tightly coupled and derived directly from that specific webpage.

### Step 2: Check for Existing Terms (Duplicate Check)
Run OAK search against `ecso/ECSO8.owl`:
```bash
runoak -i ecso/ECSO8.owl search "<SUGGESTED_NAME>"
```

- **IF EXACT MATCH IS FOUND**:
  Stop and report back immediately by posting a comment to the issue thread:
  ```markdown
  🤖 **Concept Already Exists**
  
  The term **<SUGGESTED_NAME>** already exists in the Ecosystem Ontology (ECSO).
  - **Ontology ID**: `ECSO:XXXXXXXX`
  - **Label**: `[Matched Term Label]`
  - **Definition**: `[Matched Term Definition]`
  
  No further mapping was performed.
  ```

### Step 3: Suggest Parent Classes
If the term does NOT exist, search ECSO for potential parent terms:
```bash
runoak -i ecso/ECSO8.owl search "<keyword from SUGGESTED_NAME or DESCRIPTION>"
```
Identify 1-3 candidate parent classes and their IDs.

### Step 4: Formulate the OBO-Compliant Definition
Formulate a definition in the standard OBO genus-differentia format:
- **Format**: `A [Suggested Parent Class in lowercase] which [differentia based on Description].`
- Ensure the parent class is an actual, lowercase ECSO class label.
- Start with the indefinite article (`A` or `An`).

### Step 5: Post copy-pasteable ECSO New Term Request
Post a markdown comment containing the final ECSO issue template format:

```markdown
🤖 **Mapped ECSO New Term Request**

I have successfully mapped the EDI annotation studio term request to the standard ECSO new term request schema!

You can copy and paste the markdown block below directly into a new issue on the ECSO ontology repository:

```markdown
# New Term Request: <SUGGESTED_NAME in lowercase>

- **Preferred Term Label**: <SUGGESTED_NAME in lowercase>
- **Textual Definition**: A [Suggested Parent Class] which [differentia based on Description].
- **Parent Class (Position in Hierarchy)**: [Suggested Parent Class] ([ECSO ID])
- **Definition Source / Reference**: <REFERENCE>
- **Exact Synonym(s)**: [Optional - list exact synonyms if any]
- **Created By**: <CREATOR_ORCID>
- **Creation Date**: <CURRENT_ISO_8601_TIMESTAMP>
- **Term Tracker Item**: [To be filled in with the ECSO issue URL]
```

---
*Note on filled-in/inferred information:*
- [List any fields that were missing and filled/inferred by the agent, or 'None' if all were present in the source]
```
