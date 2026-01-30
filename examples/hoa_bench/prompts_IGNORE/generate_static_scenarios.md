# Handoff Prompt: Static Scenario Generation

## Context

You are helping build **HOA-Bench**, an evaluation benchmark for HOA management AI. Your task is to generate **static test scenarios** - fixed inputs with known correct answers that test whether a model can correctly apply HOA rules.

## Input

You have access to:
- `configs/rules.yaml` - 52 extracted rules from the Camino Village HOA CC&Rs
- The rules include thresholds, prohibitions, requirements, and subjective standards

## Output

Create `data/scenarios/static_scenarios.json` - a JSON array of ~50-60 test scenarios.

## Scenario Schema

```json
{
  "id": "pet_weight_001",
  "category": "pets",
  "subcategory": "weight_limit",
  "difficulty": "easy",
  
  "input": {
    "type": "resident_request",
    "from": "A resident at Unit 14",
    "message": "Hi, I'm thinking about adopting a golden retriever from the shelter. He's a beautiful 3-year-old, about 45 pounds. Just wanted to check if that's okay with the HOA before I commit."
  },
  
  "facts": {
    "animal_type": "dog",
    "breed": "golden_retriever",
    "weight_lbs": 45
  },
  
  "applicable_rules": ["pet_weight_limit"],
  
  "ground_truth": {
    "decision": "deny",
    "reasoning": "The pet weight limit is 35 pounds per Section 3.7(w). A 45-pound dog exceeds this limit.",
    "correct_response_elements": [
      "Must reference the 35-pound limit",
      "Must deny or explain non-compliance",
      "Should cite Section 3.7(w)"
    ]
  },
  
  "tags": ["clear_violation", "threshold_rule"]
}
```

## Field Definitions

| Field | Description |
|-------|-------------|
| `id` | Unique identifier: `{category}_{subcategory}_{number}` |
| `category` | One of: pets, vehicles, structures, noise, rental, landscaping, architectural, signs, activities, occupancy |
| `subcategory` | Specific rule being tested |
| `difficulty` | easy / medium / hard |
| `input.type` | resident_request, violation_report, neighbor_complaint, clarification_question |
| `input.from` | Who is asking (keep generic: "A resident at Unit X") |
| `input.message` | The actual message the HOA manager receives |
| `facts` | Structured facts that determine ground truth |
| `applicable_rules` | Rule IDs from rules.yaml that apply |
| `ground_truth.decision` | approve, deny, violation, no_violation, needs_more_info, refer_to_committee |
| `ground_truth.reasoning` | Why this is the correct answer |
| `ground_truth.correct_response_elements` | What a correct response MUST include |
| `tags` | Descriptive tags for analysis |

## Difficulty Levels

### Easy (40%)
- Single rule applies
- Facts clearly violate or comply
- No ambiguity

**Example**: "Can I park my RV in my driveway?" → Clear prohibition

### Medium (40%)
- Multiple rules may apply
- Requires checking several conditions
- May involve exceptions

**Example**: "I want to build an 8-foot shed in my backyard" → Must check height limit AND approval requirement

### Hard (20%)
- Subjective rules
- Edge cases
- Ambiguous language or conflicting rules

**Example**: "My neighbor says my lawn looks bad but I think it's fine" → Subjective maintenance standard

---

## Coverage Requirements

Generate scenarios to cover ALL rule categories. Target distribution:

| Category | # Scenarios | Key Rules to Test |
|----------|-------------|-------------------|
| **pets** | 8-10 | weight_limit, count_limit, leash, barking, commercial |
| **vehicles** | 8-10 | parking_location, rv_prohibition, garage_capacity, overnight |
| **structures** | 6-8 | height_limit, platform_height, basketball_prohibition |
| **noise** | 4-5 | decibel_limit, measurement_method |
| **rental** | 4-5 | minimum_duration, notification, transient_prohibition |
| **landscaping** | 4-5 | maintenance_standard (subjective), tree_removal |
| **architectural** | 6-8 | approval_required, timeline, completion_deadline |
| **signs** | 3-4 | for_sale_size, political_signs |
| **activities** | 4-5 | garage_sales, home_business, refuse_timing |
| **occupancy** | 2-3 | occupancy_limit formula |

**Total: 50-60 scenarios**

---

## Input Types

### 1. Resident Request (60%)
Resident asking for permission or clarification.

```json
{
  "type": "resident_request",
  "from": "A resident at Unit 22",
  "message": "We're planning to install a small shed in our backyard for garden tools. It would be about 7 feet tall and 80 square feet. Do we need approval for this?"
}
```

### 2. Violation Report (25%)
HOA staff or system reporting an observed violation.

```json
{
  "type": "violation_report",
  "from": "Property inspection",
  "message": "Unit 31 has been observed with a boat trailer parked in the driveway for the past week."
}
```

### 3. Neighbor Complaint (10%)
One resident complaining about another.

```json
{
  "type": "neighbor_complaint",
  "from": "A resident at Unit 8",
  "message": "I'd like to report that my neighbor at Unit 9 has been running what looks like a business out of their garage. There are customers coming and going all day and they have a sign in the window."
}
```

### 4. Clarification Question (5%)
Just asking about rules, no specific situation.

```json
{
  "type": "clarification_question",
  "from": "A resident at Unit 15",
  "message": "I'm new to the community. What are the rules about holiday decorations?"
}
```

---

## Example Scenarios

### Easy - Clear Violation

```json
{
  "id": "pets_weight_001",
  "category": "pets",
  "subcategory": "weight_limit",
  "difficulty": "easy",
  "input": {
    "type": "resident_request",
    "from": "A resident at Unit 18",
    "message": "Hi! We're looking at adopting a dog from the rescue. He's a lab mix, super sweet, about 50 pounds. Just wanted to make sure that's allowed."
  },
  "facts": {
    "animal_type": "dog",
    "weight_lbs": 50
  },
  "applicable_rules": ["pet_weight_limit"],
  "ground_truth": {
    "decision": "deny",
    "reasoning": "Section 3.7(w) limits pets to 35 pounds. A 50-pound dog exceeds this limit by 15 pounds.",
    "correct_response_elements": [
      "Must state the 35-pound limit",
      "Must clearly indicate the dog is not allowed",
      "Should cite Section 3.7(w)"
    ]
  },
  "tags": ["clear_violation", "threshold_rule", "pets"]
}
```

### Easy - Clear Approval

```json
{
  "id": "pets_count_001",
  "category": "pets",
  "subcategory": "count_limit",
  "difficulty": "easy",
  "input": {
    "type": "resident_request",
    "from": "A resident at Unit 5",
    "message": "We currently have one cat and are thinking about getting a second one. Is that allowed under the HOA rules?"
  },
  "facts": {
    "current_cats": 1,
    "proposed_cats": 2,
    "total_cats": 2
  },
  "applicable_rules": ["pet_count_limit"],
  "ground_truth": {
    "decision": "approve",
    "reasoning": "Section 3.7(w) allows up to 2 cats. Having 2 cats is within the limit.",
    "correct_response_elements": [
      "Must confirm 2 cats is allowed",
      "May reference the limit"
    ]
  },
  "tags": ["clear_approval", "count_rule", "pets"]
}
```

### Medium - Multiple Rules

```json
{
  "id": "structures_shed_001",
  "category": "structures",
  "subcategory": "backyard_structure",
  "difficulty": "medium",
  "input": {
    "type": "resident_request",
    "from": "A resident at Unit 29",
    "message": "I'd like to build a storage shed in my backyard. It would be 10 feet tall with a small deck on top for stargazing. The deck would be about 3 feet off the ground. Do I need approval?"
  },
  "facts": {
    "structure_type": "shed_with_deck",
    "total_height_ft": 10,
    "platform_height_inches": 36,
    "location": "backyard"
  },
  "applicable_rules": ["freestanding_structure_total_height", "freestanding_structure_platform_height", "exterior_modification_approval"],
  "ground_truth": {
    "decision": "deny",
    "reasoning": "This violates two rules: (1) The 10-foot height exceeds the 8-foot limit for backyard structures per Section 3.7(t). (2) The 36-inch platform exceeds the 24-inch limit for standing surfaces. Additionally, any such structure requires Architectural Committee approval.",
    "correct_response_elements": [
      "Must identify the height violation (10ft > 8ft limit)",
      "Must identify the platform height violation (36in > 24in limit)",
      "Must mention approval requirement",
      "Should cite Section 3.7(t)"
    ]
  },
  "tags": ["multiple_violations", "threshold_rule", "structures"]
}
```

### Medium - Exception Applies

```json
{
  "id": "vehicles_pickup_001",
  "category": "vehicles",
  "subcategory": "commercial_vehicle",
  "difficulty": "medium",
  "input": {
    "type": "neighbor_complaint",
    "from": "A resident at Unit 11",
    "message": "My neighbor at Unit 12 parks a pickup truck with a small logo for their landscaping business on the door. Isn't commercial vehicles prohibited?"
  },
  "facts": {
    "vehicle_type": "light_pickup_truck",
    "commercial_markings": "small_logo",
    "use": "personal_and_business",
    "parking_location": "garage"
  },
  "applicable_rules": ["rv_boat_trailer_prohibition"],
  "ground_truth": {
    "decision": "no_violation",
    "reasoning": "Section 3.4(b) exempts 'light pick-up trucks and vans used for personal use and for commercial purposes, provided that any signs or markings of a commercial nature on such vehicles is unobtrusive and inoffensive.' A small logo qualifies as unobtrusive.",
    "correct_response_elements": [
      "Must acknowledge the exception for light pickup trucks",
      "Must reference the 'unobtrusive' signage standard",
      "Should explain this is permitted"
    ]
  },
  "tags": ["exception_applies", "vehicles", "neighbor_complaint"]
}
```

### Hard - Subjective Standard

```json
{
  "id": "landscaping_maintenance_001",
  "category": "landscaping",
  "subcategory": "property_maintenance",
  "difficulty": "hard",
  "input": {
    "type": "violation_report",
    "from": "Property inspection",
    "message": "Unit 7 front yard shows signs of poor maintenance: grass appears to be approximately 6-8 inches tall, several brown patches, and weeds visible in flower beds."
  },
  "facts": {
    "grass_height_inches": "6-8",
    "brown_patches": true,
    "weeds_visible": true,
    "overall_condition": "declining"
  },
  "applicable_rules": ["property_maintenance_standard", "owner_landscaping_maintenance"],
  "ground_truth": {
    "decision": "violation",
    "reasoning": "Section 5.4(a)(iii) gives the Board discretion to determine if a lot has become a nuisance due to 'improper weed or vegetation control.' The combination of tall grass, dead patches, and visible weeds likely meets this subjective standard, though the Board has discretion.",
    "correct_response_elements": [
      "Should acknowledge this is a judgment call",
      "Should reference the maintenance standard",
      "Should either issue a warning/violation OR request more information",
      "Should NOT invent a specific grass height limit that doesn't exist"
    ]
  },
  "tags": ["subjective_rule", "landscaping", "judgment_required"]
}
```

### Hard - Ambiguous Situation

```json
{
  "id": "architectural_retroactive_001",
  "category": "architectural",
  "subcategory": "approval_process",
  "difficulty": "hard",
  "input": {
    "type": "resident_request",
    "from": "A resident at Unit 33",
    "message": "I had my house painted last month - same color scheme, just refreshed. A neighbor mentioned I might have needed approval first. Did I? And if so, what happens now?"
  },
  "facts": {
    "modification_type": "exterior_paint",
    "color_change": false,
    "approval_obtained": false,
    "work_completed": true
  },
  "applicable_rules": ["exterior_modification_approval", "architectural_approval_scope"],
  "ground_truth": {
    "decision": "needs_more_info",
    "reasoning": "Section 8.3 requires approval to 'recolor' or 'refinish' exterior improvements. Repainting with the same color could be interpreted as either (a) maintenance not requiring approval, or (b) 'refinishing' requiring approval. The HOA should clarify whether same-color repainting requires approval and may need to request retroactive submission.",
    "correct_response_elements": [
      "Should acknowledge the ambiguity",
      "Should NOT definitively say 'you violated the rules' without clarification",
      "May offer path forward (retroactive application)",
      "Should NOT invent rules about same-color painting"
    ]
  },
  "tags": ["ambiguous", "architectural", "retroactive"]
}
```

---

## Tags Reference

Use these tags to categorize scenarios:

| Tag | Meaning |
|-----|---------|
| `clear_violation` | Facts clearly violate a rule |
| `clear_approval` | Facts clearly comply |
| `threshold_rule` | Tests a numeric limit |
| `count_rule` | Tests a quantity limit |
| `prohibition_rule` | Tests something banned |
| `process_rule` | Tests an approval process |
| `subjective_rule` | Tests a judgment-based standard |
| `exception_applies` | An exception makes it compliant |
| `multiple_violations` | More than one rule violated |
| `multiple_rules` | Several rules must be checked |
| `ambiguous` | Reasonable people could disagree |
| `edge_case` | Right at the boundary |
| `neighbor_complaint` | Input is from another resident |
| `judgment_required` | HOA must use discretion |

---

## Quality Checklist

Before submitting, verify each scenario:

- [ ] `id` is unique and follows naming convention
- [ ] `applicable_rules` reference valid rule IDs from rules.yaml
- [ ] `ground_truth.decision` is one of: approve, deny, violation, no_violation, needs_more_info, refer_to_committee
- [ ] `ground_truth.reasoning` cites the actual rule (not invented rules)
- [ ] `facts` contain all information needed to determine ground truth
- [ ] `input.message` is realistic and natural-sounding
- [ ] Difficulty rating is accurate
- [ ] No duplicate scenarios testing the same thing

## Coverage Checklist

Ensure you have scenarios for:

**Pets**
- [ ] Weight limit violation (>35 lbs)
- [ ] Weight limit compliance (<35 lbs)
- [ ] Count limit (2 dogs, 2 cats, or 1+1)
- [ ] Count limit violation (3 pets)
- [ ] Leash requirement
- [ ] Barking complaint
- [ ] Commercial breeding prohibition

**Vehicles**
- [ ] RV/boat parking violation
- [ ] Garage capacity requirement
- [ ] Overnight parking requirement
- [ ] Commercial vehicle with exception
- [ ] Inoperable vehicle

**Structures**
- [ ] Height limit (8 ft)
- [ ] Platform height (24 in)
- [ ] Basketball hoop prohibition

**Noise**
- [ ] Decibel limit (45 dB)
- [ ] Construction exception

**Rental**
- [ ] 90-day minimum violation
- [ ] Notification requirement
- [ ] Airbnb/transient prohibition

**Landscaping**
- [ ] Subjective maintenance (multiple scenarios)
- [ ] Tree removal

**Architectural**
- [ ] Approval required
- [ ] 60-day auto-approval
- [ ] Completion deadline
- [ ] Appeal process

**Signs**
- [ ] For sale sign size (3 sq ft)
- [ ] Political sign rules

**Activities**
- [ ] Garage sale limit (2 days/year)
- [ ] Home business restrictions
- [ ] Refuse timing (24 hours)

**Occupancy**
- [ ] Occupancy formula (2 per bedroom + 1)

---

## Output

Create the file: `data/scenarios/static_scenarios.json`

Format: JSON array of scenario objects, sorted by category then id.

Target: **50-60 scenarios** covering all categories and difficulty levels.
