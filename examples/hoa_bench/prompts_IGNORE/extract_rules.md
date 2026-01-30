# Handoff Prompt: CC&Rs Rules Extraction

## Context

You are helping build **HOA-Bench**, an evaluation benchmark that tests whether LLMs can correctly enforce HOA (Homeowners Association) rules. 

Your task is to extract structured rules from a real CC&Rs document (Camino Village HOA, Sacramento, CA) and format them as a YAML file that can be used for **ground truth evaluation**.

## Purpose of the Rules File

The rules you extract will be used to:
1. **Evaluate HOA manager decisions** - Did the model correctly apply this rule?
2. **Generate test scenarios** - Create situations that test specific rules
3. **Check rule citations** - Did the model cite a real rule or invent one?

## Input Document

The CC&Rs document is located at: `rag/hoa-ccrs.pdf` (81 pages)

Key sections to focus on:
- **Article III: Restrictions & Use of Project** (pages ~13-25) - Core use rules
- **Section 3.4**: Vehicles and parking
- **Section 3.7**: Nuisances (subsections a-z cover most specific rules)
- **Section 3.8**: Architectural modifications
- **Article VIII: Architectural Committee** (pages ~43-50)

## Output Format

Create a YAML file with this schema:

```yaml
# configs/rules.yaml

metadata:
  source: "Camino Village HOA CC&Rs (First Restated)"
  extracted_date: "2025-01-30"
  document_pages: 81

rules:
  - id: <snake_case_identifier>
    category: <one of: structures, pets, vehicles, noise, rental, occupancy, landscaping, signs, activities, architectural>
    text: "<exact or near-exact quote from CC&Rs>"
    source: "<Section number, e.g., 'Section 3.7(w)'>"
    rule_type: <one of: threshold, prohibition, requirement, count, process, subjective>
    params:  # Only for quantifiable rules
      metric: <what's being measured>
      operator: "<= | >= | == | <"
      value: <number>
    exceptions: [<list of exception IDs if any>]
    requires_approval: <true/false>
    enforcement: "<brief description of violation process if mentioned>"
    notes: "<any clarifying notes about ambiguity or interpretation>"
```

## Rule Types

| Type | Description | Example |
|------|-------------|---------|
| `threshold` | Numeric limit | "Fences may not exceed 8 feet" |
| `prohibition` | Something banned | "No commercial vehicles on street" |
| `requirement` | Something required | "Vehicles must be parked in garage at night" |
| `count` | Limit on quantity | "Maximum 2 dogs" |
| `process` | Requires approval/procedure | "Exterior modifications require committee approval" |
| `subjective` | Judgment-based | "Property must not become unsightly" |

## Categories to Extract

Focus on rules that are:
1. **Testable** - Can create scenarios to evaluate
2. **Common** - Likely to come up in HOA interactions
3. **Specific** - Have clear criteria (prefer quantifiable over vague)

### Priority Categories

| Category | Examples | Priority |
|----------|----------|----------|
| **structures** | Fences, sheds, decks, height limits | HIGH |
| **pets** | Count limits, weight limits, leash rules | HIGH |
| **vehicles** | Parking, RVs, commercial vehicles, garage use | HIGH |
| **noise** | Decibel limits, quiet hours | MEDIUM |
| **landscaping** | Grass height, maintenance standards | MEDIUM |
| **rental** | Lease minimums, occupancy limits | MEDIUM |
| **architectural** | Exterior modifications, paint, approval process | HIGH |
| **signs** | Size limits, placement | LOW |
| **activities** | Garage sales, home business | LOW |

## Examples of Good Rule Extractions

### Example 1: Threshold Rule
```yaml
  - id: pet_weight_limit
    category: pets
    text: "No animal which weighs more than 35 pounds is allowed within the Project"
    source: "Section 3.7(w)"
    rule_type: threshold
    params:
      metric: weight_lbs
      operator: "<="
      value: 35
    exceptions: [service_animal_ada]
    requires_approval: false
    notes: "Service animals may be exempt under ADA"
```

### Example 2: Count Rule
```yaml
  - id: pet_count_dogs
    category: pets
    text: "Not more than two (2) dogs"
    source: "Section 3.7(w)(i)"
    rule_type: count
    params:
      metric: dog_count
      operator: "<="
      value: 2
    requires_approval: false
```

### Example 3: Prohibition Rule
```yaml
  - id: rv_prohibition
    category: vehicles
    text: "The parking or maintenance of mobile homes, motor homes, trucks, commercial vehicles, campers, boats, trailers, or similar vehicles [is prohibited] except within enclosed garages"
    source: "Section 3.4(b)"
    rule_type: prohibition
    exceptions: [temporary_construction, moving, garage_stored]
    requires_approval: false
    notes: "Light pickup trucks for personal use are excepted if signage is unobtrusive"
```

### Example 4: Process Rule
```yaml
  - id: exterior_modification_approval
    category: architectural
    text: "No exterior modifications without prior written consent of Board or Architectural Committee"
    source: "Section 3.8"
    rule_type: process
    requires_approval: true
    enforcement: "Unapproved modifications may be required to be removed at owner's expense"
```

### Example 5: Subjective Rule
```yaml
  - id: property_maintenance
    category: landscaping
    text: "Property must not become overgrown, unsightly, or fall into disrepair"
    source: "Section 3.7(o)"
    rule_type: subjective
    requires_approval: false
    notes: "Common interpretation: grass over 6 inches is 'overgrown'"
    common_thresholds:
      grass_height_inches: 6
```

## Specific Rules to Find

Based on my initial scan of the document, please extract rules for:

### Structures (Section 3.7(t) and related)
- [ ] Fence height limit
- [ ] Structure height limit
- [ ] Platform/deck height requiring approval
- [ ] Setback requirements (distance from property line)

### Pets (Section 3.7(w))
- [ ] Dog count limit
- [ ] Cat count limit  
- [ ] Weight limit
- [ ] Leash requirements
- [ ] Waste cleanup requirements
- [ ] Noise (barking) requirements

### Vehicles (Section 3.4)
- [ ] Garage usage requirements
- [ ] RV/boat/trailer prohibition
- [ ] Commercial vehicle rules
- [ ] Inoperable vehicle rules
- [ ] Overnight parking requirements

### Noise (Section 3.7(p))
- [ ] Decibel limit
- [ ] Measurement method

### Rental (Section 3.2)
- [ ] Minimum lease duration
- [ ] Notification requirements

### Occupancy (Section 3.1)
- [ ] Occupancy formula (persons per bedroom)

### Signs (Section 3.7(x))
- [ ] Size limits for sale/rent signs
- [ ] Placement restrictions

### Activities (Section 3.7(r))
- [ ] Garage sale limits
- [ ] Home business restrictions

### Architectural (Section 3.8)
- [ ] What requires approval
- [ ] Approval process timeline
- [ ] Consequences of non-compliance

## Output

Create the file `configs/rules.yaml` with:
1. **15-25 rules** covering the priority categories
2. **Exact citations** (section numbers)
3. **Verbatim or near-verbatim text** from the CC&Rs
4. **All quantifiable parameters** extracted
5. **Notes on ambiguity** where the language is unclear

## Quality Checklist

Before submitting, verify:
- [ ] Every rule has a valid `source` citation
- [ ] Threshold rules have `params` with `metric`, `operator`, `value`
- [ ] No invented rules - everything comes from the document
- [ ] Categories are consistent with the schema
- [ ] IDs are unique and snake_case
- [ ] Ambiguous language is noted in `notes` field

---

## How to Access the Document

The PDF is at `rag/hoa-ccrs.pdf`. You can extract text using:

```bash
pdftotext rag/hoa-ccrs.pdf rag/hoa-ccrs.txt
```

Or extract specific pages:
```bash
pdftotext -f 13 -l 25 rag/hoa-ccrs.pdf -  # Article III
pdftotext -f 43 -l 50 rag/hoa-ccrs.pdf -  # Article VIII
```

Focus on **Article III (Restrictions & Use)** for most rules.
