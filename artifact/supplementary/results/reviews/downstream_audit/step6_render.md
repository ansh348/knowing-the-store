# Step 6 -- render check: three complete prompts as the answerer received them

System message (`SYSTEM_ANSWER`, D.4; identical under every policy):
````
You answer a question about a user from a view of the user's memory store. The view lists entries; each entry carries the lifecycle metadata the store records for it. An entry marked active is what the store currently holds as true. An entry marked superseded has been replaced by a later entry; one marked retracted was withdrawn by the user; one marked expired describes an arrangement whose date has passed. Superseded, retracted and expired entries do not state the user's current situation and must not be given as the answer.

Answer in at most two sentences, from the view alone. If no entry in the view answers the question as it stands, say that the store does not currently contain the answer. Do not guess and do not use knowledge from outside the view.

Return JSON only: {"answer": "<your answer>"}
````

Amendment 3 system message (`SYSTEM_ANSWER_A3`; the paragraph before `Return JSON only` is the addition):
````
You answer a question about a user from a view of the user's memory store. The view lists entries; each entry carries the lifecycle metadata the store records for it. An entry marked active is what the store currently holds as true. An entry marked superseded has been replaced by a later entry; one marked retracted was withdrawn by the user; one marked expired describes an arrangement whose date has passed. Superseded, retracted and expired entries do not state the user's current situation and must not be given as the answer.

Answer in at most two sentences, from the view alone. If no entry in the view answers the question as it stands, say that the store does not currently contain the answer. Do not guess and do not use knowledge from outside the view.

Treat every entry tagged superseded, retracted or expired as not to be used: do not draw on it for the answer and do not report it as the user's current situation. If the only entries that bear on the question carry one of those tags, say that the store does not currently contain the answer.

Return JSON only: {"answer": "<your answer>"}
````


## PN supersession, three distinct views: `frbank:aisha:aisha_q02:FULL` (state sup)

### policy ALWAYS -- 5 lines, view sha 125f55970fce7419, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: gym_change | age: 175 days | text: User switched to a new gym that is sisters-only in Rusholme.
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: gym_type | age: 175 days | text: User goes to a small, women-only gym in Rusholme with a welcoming, community vibe.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User has recently changed gyms.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User goes to the gym 3 or 4 times a week, usually after work
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User does a mix of cardio and some weights at the gym
```

Question: Which gym does Aisha go to?
````

- recorded answer [mini-D4]: (no call: abstained or record not reached under this policy)
- recorded answer [h45-D4]: (no call: abstained or record not reached under this policy)
- recorded answer [mini-A3]: (no call: abstained or record not reached under this policy)
- recorded answer [h45-A3]: (no call: abstained or record not reached under this policy)

### policy MODEL -- 12 lines, view sha 562acdee794a9018, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: gym_change | age: 175 days | text: User switched to a new gym that is sisters-only in Rusholme.
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: gym_type | age: 175 days | text: User goes to a small, women-only gym in Rusholme with a welcoming, community vibe.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User has recently changed gyms.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User goes to the gym 3 or 4 times a week, usually after work
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User does a mix of cardio and some weights at the gym
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 475 days | text: User lives in Ancoats in a new build flat with Zara.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 110 days | text: User currently lives in Manchester, sharing a nice 2-bedroom flat in Ancoats.
[8] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 484 days | text: User goes to PureGym near Piccadilly, which is a 24-hour gym about a 10-minute walk from their office.
[9] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 484 days | text: User goes to PureGym near Piccadilly, which is a 24-hour gym about 10 minutes from their office.
[10] lifecycle: superseded | category: OBLIGATIONS | attribute: job_title | age: 560 days | text: User works in audit at PwC in Manchester at a junior level
[11] lifecycle: superseded | category: OBLIGATIONS | attribute: job_title | age: 560 days | text: User works in audit at PwC in Manchester at a junior level
[12] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 475 days | text: User lives in a flat in Ancoats with a flatmate named Zara
```

Question: Which gym does Aisha go to?
````

- recorded answer [mini-D4]: Aisha goes to a small, women-only gym in Rusholme with a welcoming, community vibe.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}
- recorded answer [h45-D4]: The user goes to a small, women-only gym in Rusholme with a welcoming, community vibe. This is a sisters-only gym that the user switched to recently.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}
- recorded answer [mini-A3]: Aisha goes to a small, women-only gym in Rusholme with a welcoming, community vibe.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}
- recorded answer [h45-A3]: The user goes to a small, women-only gym in Rusholme that has a welcoming, community vibe. This is a sisters-only gym that the user switched to recently.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}

### policy ORACLE -- 7 lines, view sha f1844b4e34eaedf1, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: gym_change | age: 175 days | text: User switched to a new gym that is sisters-only in Rusholme.
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: gym_type | age: 175 days | text: User goes to a small, women-only gym in Rusholme with a welcoming, community vibe.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User has recently changed gyms.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User goes to the gym 3 or 4 times a week, usually after work
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User does a mix of cardio and some weights at the gym
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 484 days | text: User goes to PureGym near Piccadilly, which is a 24-hour gym about a 10-minute walk from their office.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 484 days | text: User goes to PureGym near Piccadilly, which is a 24-hour gym about 10 minutes from their office.
```

Question: Which gym does Aisha go to?
````

- recorded answer [mini-D4]: Aisha goes to a small, women-only gym in Rusholme with a welcoming, community vibe.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}
- recorded answer [h45-D4]: The user goes to a small, women-only gym in Rusholme with a welcoming, community vibe. This is a sisters-only gym that the user switched to recently.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}
- recorded answer [mini-A3]: Aisha goes to a small, women-only gym in Rusholme with a welcoming, community vibe.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}
- recorded answer [h45-A3]: The user goes to a small, women-only gym in Rusholme. This is a sisters-only gym with a welcoming, community vibe that the user switched to recently.  ← {'stale_use_tau_gold': False, 'stale_use': False, 'stale_cov': 0.2}

## PN untagged reached record (retraction/expiry printed active): `frbank:bruna:bruna_q06:FULL` (state ret)

### policy ALWAYS -- 5 lines, view sha ec2b9f9d36cb55c2, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
```

Question: Is Bruna planning to get any new certifications?
````

- recorded answer [mini-D4]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [h45-D4]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025. Additionally, she is considering the credential recognition process for her physical therapy qualifications in Portugal.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [mini-A3]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [h45-A3]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}

### policy MODEL -- 5 lines, view sha ec2b9f9d36cb55c2, abstain True

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
```

Question: Is Bruna planning to get any new certifications?
````

- recorded answer [mini-D4]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [h45-D4]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025. Additionally, she is considering the credential recognition process for her physical therapy qualifications in Portugal.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [mini-A3]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [h45-A3]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}

### policy ORACLE -- 5 lines, view sha ec2b9f9d36cb55c2, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
```

Question: Is Bruna planning to get any new certifications?
````

- recorded answer [mini-D4]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [h45-D4]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025. Additionally, she is considering the credential recognition process for her physical therapy qualifications in Portugal.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [mini-A3]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}
- recorded answer [h45-A3]: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.  ← {'stale_use_tau_gold': True, 'stale_use': False, 'stale_cov': 0.5714285714285714}

## PRESENT, licensed record in view: `frbank:amara:amara_q04:FULL` (state -)

### policy ALWAYS -- 5 lines, view sha bf9c811cd3b760c4, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: OBLIGATIONS | attribute: health_disclosure_preference | age: 505 days | text: User is reluctant to disclose health condition to clerks to avoid being moved off more demanding briefs
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 505 days | text: User has endometriosis.
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: friend | age: 456 days | text: User's friend has no dietary restrictions and enjoys Turkish and Middle Eastern food.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 505 days | text: User has endometriosis and was diagnosed at age twenty-eight
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: colleague | age: 99 days | text: User has a practice manager named Helen who can assist with administrative tasks
```

Question: Does Amara have any health conditions to be aware of?
````

- recorded answer [mini-D4]: Yes, Amara has endometriosis and was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [h45-D4]: The store contains information about a user's health condition, but does not identify the user as Amara. According to the active entries, the user has endometriosis, which was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [mini-A3]: Yes, Amara has endometriosis and was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [h45-A3]: The store contains entries indicating the user has endometriosis, diagnosed at age twenty-eight. However, the question asks about 'Amara,' and the store entries do not identify the user by this name, so I cannot confirm whether these health conditions apply to the person you're asking about.  ← {'correct': True, 'gold_cov': 0.6666666666666666}

### policy MODEL -- 5 lines, view sha bf9c811cd3b760c4, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: OBLIGATIONS | attribute: health_disclosure_preference | age: 505 days | text: User is reluctant to disclose health condition to clerks to avoid being moved off more demanding briefs
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 505 days | text: User has endometriosis.
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: friend | age: 456 days | text: User's friend has no dietary restrictions and enjoys Turkish and Middle Eastern food.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 505 days | text: User has endometriosis and was diagnosed at age twenty-eight
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: colleague | age: 99 days | text: User has a practice manager named Helen who can assist with administrative tasks
```

Question: Does Amara have any health conditions to be aware of?
````

- recorded answer [mini-D4]: Yes, Amara has endometriosis and was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [h45-D4]: The store contains information about a user's health condition, but does not identify the user as Amara. According to the active entries, the user has endometriosis, which was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [mini-A3]: Yes, Amara has endometriosis and was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [h45-A3]: The store contains entries indicating the user has endometriosis, diagnosed at age twenty-eight. However, the question asks about 'Amara,' and the store entries do not identify the user by this name, so I cannot confirm whether these health conditions apply to the person you're asking about.  ← {'correct': True, 'gold_cov': 0.6666666666666666}

### policy ORACLE -- 5 lines, view sha bf9c811cd3b760c4, abstain False

User message:
````
Entries from this user's memory store, each with the lifecycle metadata the store records for it:

```
[1] lifecycle: active | category: OBLIGATIONS | attribute: health_disclosure_preference | age: 505 days | text: User is reluctant to disclose health condition to clerks to avoid being moved off more demanding briefs
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 505 days | text: User has endometriosis.
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: friend | age: 456 days | text: User's friend has no dietary restrictions and enjoys Turkish and Middle Eastern food.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 505 days | text: User has endometriosis and was diagnosed at age twenty-eight
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: colleague | age: 99 days | text: User has a practice manager named Helen who can assist with administrative tasks
```

Question: Does Amara have any health conditions to be aware of?
````

- recorded answer [mini-D4]: Yes, Amara has endometriosis and was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [h45-D4]: The store contains information about a user's health condition, but does not identify the user as Amara. According to the active entries, the user has endometriosis, which was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [mini-A3]: Yes, Amara has endometriosis and was diagnosed at age twenty-eight.  ← {'correct': True, 'gold_cov': 0.6666666666666666}
- recorded answer [h45-A3]: The store contains entries indicating the user has endometriosis, diagnosed at age twenty-eight. However, the question asks about 'Amara,' and the store entries do not identify the user by this name, so I cannot confirm whether these health conditions apply to the person you're asking about.  ← {'correct': True, 'gold_cov': 0.6666666666666666}

## Checklist (computed)

```json
{
 "selected_items": {
  "PN supersession, three distinct views": "frbank:aisha:aisha_q02:FULL",
  "PN untagged reached record (retraction/expiry printed active)": "frbank:bruna:bruna_q06:FULL",
  "PRESENT, licensed record in view": "frbank:amara:amara_q04:FULL"
 },
 "tags_present_in_views": {
  "active": 21616,
  "expired": 2390,
  "retracted": 192,
  "superseded": 2015
 },
 "tags_explained_in_system_prompt": true,
 "tag_format": "inline field `lifecycle: <tag>` per line; multi-tag entries print a comma list",
 "pinned_time_or_current_date_given": false,
 "time_information_per_line": "relative `age: N days` only (no absolute date, no t_now)",
 "truncation": {
  "views_n_lines_equals_ids": true,
  "max_view_lines": 27,
  "plus_more_fragments": 0,
  "per_lane_tokens": {
   "mini-D4": {
    "max_tok_in": 1455,
    "max_tok_out": 74,
    "n_tok_out_ge_200": 0,
    "status_not_ok": 0,
    "answer_none": 0,
    "retries": 0
   },
   "h45-D4": {
    "max_tok_in": 1610,
    "max_tok_out": 123,
    "n_tok_out_ge_200": 0,
    "status_not_ok": 0,
    "answer_none": 0,
    "retries": 0
   },
   "mini-A3": {
    "max_tok_in": 1517,
    "max_tok_out": 73,
    "n_tok_out_ge_200": 0,
    "status_not_ok": 0,
    "answer_none": 0,
    "retries": 0
   },
   "h45-A3": {
    "max_tok_in": 1675,
    "max_tok_out": 115,
    "n_tok_out_ge_200": 0,
    "status_not_ok": 0,
    "answer_none": 0,
    "retries": 0
   },
   "mini-D4-V3": {
    "max_tok_in": 1455,
    "max_tok_out": 74,
    "n_tok_out_ge_200": 0,
    "status_not_ok": 0,
    "answer_none": 0,
    "retries": 0
   }
  }
 },
 "question_present": true,
 "answer_format": "JSON object {\"answer\": ...}; mini in JSON mode; Haiku fenced ```json blocks parsed by last_json",
 "parse_failures_total": 0,
 "final_answer_rerun_triggered": false,
 "final_answer_rerun_note": "not triggered: 0 parse failures, 0 retries, no max-token hit; a re-run would need a model call and this script has no API path"
}
```
