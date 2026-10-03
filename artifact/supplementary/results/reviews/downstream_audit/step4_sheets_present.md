# Step 4 -- PRESENT answers marked incorrect with the licensed record in view (ORACLE view = ALWAYS view)

Lanes: mini-D4 (required: the 28), h45-D4 (beside); appendix: the A3-prompt lanes.

## mini-D4 (gpt-4.1-mini, prompt D4)

28 answers.

### [mini-D4] frbank:billy:billy_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:billy:billy_q05:FULL|bc807c9cb9e79e3b`
- question: What health issues does Billy have?
- gold (YAML `fact`): Has frostbite damage on three fingers of his left hand — partial feeling lost
- licensed (gold) records: lb_00040 [active] rank absent: "User has three fingers on their left hand due to frostbite." (entry passes detector: True); lb_00043 [active] rank 5: "User lost three fingers on their left hand due to frostbite from an incident in 2009 during a whiteout while working on a machine in extreme cold." (entry passes detector: True); lb_00044 [active] rank absent: "User's three fingers on the left hand have lost temperature sensation and cannot feel hot or cold." (entry passes detector: True); lb_00045 [active] rank absent: "User has frostbite on three fingers of their left hand resulting in loss of temperature sensation in those fingers" (entry passes detector: True); lb_00048 [active] rank absent: "User lost three fingers on their left hand due to frostbite from a whiteout incident in 2009." (entry passes detector: True); lb_00051 [active] rank 4: "User has had frostbite on three fingers of their left hand since 2009, resulting in loss of temperature sensation in those fingers." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00043': 0.0, 'lb_00051': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: family_member | age: 172 days | text: Annie's mother is 74 years old, lives in Tuk, and has some health concerns that could change quickly.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: family_member | age: 172 days | text: Annie's mother is 74 years old, lives in Tuk, and has some health concerns that require proximity to hospital care in Inuvik or Yellowknife.
[3] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: experience_with_darkness | age: 528 days | text: User has lived with long periods of darkness their whole life
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 513 days | text: User has had frostbite on three fingers of their left hand since 2009, resulting in loss of temperature sensation in those fingers.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 513 days | text: User lost three fingers on their left hand due to frostbite from an incident in 2009 during a whiteout while working on a machine in extreme cold.
````


### [mini-D4] frbank:callum:callum_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:callum:callum_q05:FULL|199ef5dc1bd227ea`
- question: Does Callum have any upcoming events?
- gold (YAML `fact`): Highland Vets annual conference — Edinburgh, May 8-9, 2026
- licensed (gold) records: lb_00378 [active] rank 2: "User has a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False); lb_00380 [active] rank absent: "User's conference topics include clinical updates such as parasitology and antimicrobial stewardship, as well as practice management and client communication." (entry passes detector: False); lb_00383 [active] rank 4: "User will attend a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False)
- detector: gold_cov 0.4286; answer covers in-view entry text: {'lb_00378': 1.0, 'lb_00383': 0.8571}; is_abstention False
- **answer**: Callum has a mandatory practice conference on May 8th and 9th in Edinburgh.
- raw[:400]: `{"answer": "Callum has a mandatory practice conference on May 8th and 9th in Edinburgh."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HOBBIES_RECREATION | attribute: attendance_habit | age: 292 days | text: User attends Caley Thistle matches when possible, not every week but enough.
[2] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User has a mandatory practice conference on May 8th and 9th in Edinburgh.
[3] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User has four farm calls booked on a morning
[4] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User will attend a mandatory practice conference on May 8th and 9th in Edinburgh.
[5] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User had four farm calls booked on the morning of 2025-04-18
````


### [mini-D4] frbank:callum:callum_q08:CAT-ABLATED -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:CAT-ABLATED|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00050': 0.0}; is_abstention False
- **answer**: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
- raw[:400]: `{"answer":"User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [mini-D4] frbank:callum:callum_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:FULL|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00050': 0.0}; is_abstention False
- **answer**: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
- raw[:400]: `{"answer": "User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [mini-D4] frbank:callum:callum_q09:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:callum:callum_q09:CAT-ABLATED|9d5c500649967d49`
- question: What's Callum's background?
- gold (YAML `fact`): Grew up on a sheep farm near Aviemore
- licensed (gold) records: lb_00023 [active] rank 2: "User grew up on a sheep farm near Aviemore." (entry passes detector: True); lb_00024 [active] rank absent: "User's father still runs a smaller sheep farm with about 300 blackface ewes near Aviemore." (entry passes detector: True); lb_00028 [active] rank absent: "User's father runs a sheep farm with about 300 blackface ewes on hill ground near Aviemore." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00023': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer":"The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: sports_team_support | age: 292 days | text: User supports Caley Thistle football team.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: childhood_environment | age: 531 days | text: User grew up on a sheep farm near Aviemore.
[3] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 454 days | text: User plays rugby in Caledonia Division 2 league.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 20 days | text: User is involved in naming a child and prefers the name Hamish.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 513 days | text: User has a sister named Fiona who is 32 years old and works as a midwife in Glasgow
````


### [mini-D4] frbank:callum:callum_q09:FULL -- PRESENT, section stable_identity
- key: `frbank:callum:callum_q09:FULL|9d5c500649967d49`
- question: What's Callum's background?
- gold (YAML `fact`): Grew up on a sheep farm near Aviemore
- licensed (gold) records: lb_00023 [active] rank 2: "User grew up on a sheep farm near Aviemore." (entry passes detector: True); lb_00024 [active] rank absent: "User's father still runs a smaller sheep farm with about 300 blackface ewes near Aviemore." (entry passes detector: True); lb_00028 [active] rank absent: "User's father runs a sheep farm with about 300 blackface ewes on hill ground near Aviemore." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00023': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer":"The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: sports_team_support | age: 292 days | text: User supports Caley Thistle football team.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: childhood_environment | age: 531 days | text: User grew up on a sheep farm near Aviemore.
[3] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 454 days | text: User plays rugby in Caledonia Division 2 league.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 20 days | text: User is involved in naming a child and prefers the name Hamish.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 513 days | text: User has a sister named Fiona who is 32 years old and works as a midwife in Glasgow
````


### [mini-D4] frbank:diane:diane_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:diane:diane_q04:FULL|3cf1876c69c43346`
- question: Does Diane have any health conditions?
- gold (YAML `fact`): Osteoarthritis in both knees
- licensed (gold) records: lb_00063 [active] rank absent: "User has osteoarthritis in their knees" (entry passes detector: True); lb_00064 [active] rank absent: "User has osteoarthritis in both knees." (entry passes detector: True); lb_00065 [active] rank absent: "User's osteoarthritis in knees has been worsening over the last two years." (entry passes detector: True); lb_00071 [active] rank 5: "User has osteoarthritis in both knees that has been worsening over the past six to seven years, with significant decline in the last two years" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00071': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 503 days | text: User had a visit with a woman named Eleanor who is ninety-one years old and is dying well.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: colleague | age: 205 days | text: User has a close professional relationship with a nurse named Sandra from Four Seasons Compassion for Life.
[3] lifecycle: active | category: OBLIGATIONS | attribute: occupation_patient_relationship | age: 145 days | text: User is a caregiver or healthcare provider with patients who request her specifically
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 290 days | text: Margaret told me she had lived long enough to stop being afraid of anything except unkindness.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 440 days | text: User has osteoarthritis in both knees that has been worsening over the past six to seven years, with significant decline in the last two years
````


### [mini-D4] frbank:diane:diane_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:diane:diane_q05:FULL|25a725c91f24c8d0`
- question: Does Diane have any upcoming events?
- gold (YAML `fact`): Greg's woodworking show at the Folk Art Center — July 12, 2026
- licensed (gold) records: lb_00398 [active] rank 5: "Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026." (entry passes detector: True); lb_00401 [active] rank 1: "Greg was accepted into the Folk Art Center summer show on July 12th, 2026" (entry passes detector: True); lb_00403 [active] rank 3: "Greg has been accepted into the Folk Art Center summer show on July 12th, 2026." (entry passes detector: True); lb_00407 [active] rank 2: "Greg has been accepted into the Folk Art Center summer show on July 12th." (entry passes detector: True); lb_00412 [active] rank absent: "User feels nervous about Greg's acceptance into the Folk Art Center summer show and hopes people will appreciate his work" (entry passes detector: True); lb_00416 [active] rank absent: "User's partner Greg will be building a rocking chair and other pieces in his workshop over the next six months." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00398': 0.0, 'lb_00401': 0.0, 'lb_00403': 0.0, 'lb_00407': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show on July 12th, 2026
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th, 2026.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: birthday | age: 16 days | text: Greg's birthday is on Saturday, March 14, 2026
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026.
````


### [mini-D4] frbank:fatima:fatima_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:CAT-ABLATED|8496763e2470a08b`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 2: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
[5] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 317 days | text: User promised to attend Omar's school science fair on May 15th
````


### [mini-D4] frbank:fatima:fatima_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:FULL|06a840f434c701e6`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 3: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: city | age: 468 days | text: User lives in Riyadh and manages all transportation for her children, including driving Khalid to football practice three times a week.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
````


### [mini-D4] frbank:ingrid:ingrid_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:ingrid:ingrid_q05:FULL|82fbc8ac2f06e090`
- question: What health conditions does Ingrid have?
- gold (YAML `fact`): Has Raynaud's syndrome — circulation in fingers shuts down in cold
- licensed (gold) records: lb_00043 [active] rank 1: "User has Raynaud's syndrome affecting their fingers in cold conditions." (entry passes detector: True)
- detector: gold_cov 0.4286; answer covers in-view entry text: {'lb_00043': 0.5}; is_abstention False
- **answer**: Ingrid has Raynaud's syndrome (also referred to as Raynaud's disease) which causes blood vessel spasms in her fingers below about 5 degrees Celsius, leading to white, numb fingers and loss of fine manipulation ability.
- raw[:400]: `{"answer": "Ingrid has Raynaud's syndrome (also referred to as Raynaud's disease) which causes blood vessel spasms in her fingers below about 5 degrees Celsius, leading to white, numb fingers and loss of fine manipulation ability."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's syndrome affecting their fingers in cold conditions.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: dietary_restrictions | age: 418 days | text: User has no dietary restrictions among the three people.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's disease, which causes blood vessel spasms in fingers below about 5 degrees Celsius, leading to white and numb fingers.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's disease which causes finger vasospasm below about 5 degrees Celsius, leading to white and numb fingers and loss of fine manipulation ability.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's syndrome which affects finger dexterity below about 5 degrees Celsius.
````


### [mini-D4] frbank:jake:jake_q03:FULL -- PRESENT, section stable_identity
- key: `frbank:jake:jake_q03:FULL|0aa1c0c015b4b7a2`
- question: What does Jake's mom do?
- gold (YAML `fact`): Mom works at the Eire Pub in Dorchester — been waitressing there 20 years
- licensed (gold) records: lb_00047 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00051 [active] rank 3: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00054 [active] rank 2: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00061 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00051': 0.0, 'lb_00054': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 106 days | text: User's mother is very involved and stressed about Bridget's wedding preparations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 43 days | text: User's mom is sentimental and cries at Hallmark commercials.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 455 days | text: User lives in Boston and Megan lives in Dorchester near user's mom's workplace
````


### [mini-D4] frbank:lily:lily_q09:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:lily:lily_q09:CAT-ABLATED|e1426bab79e22e41`
- question: What's Lily's family background?
- gold (YAML `fact`): Parents run a Chinese restaurant — Golden Lotus in Box Hill
- licensed (gold) records: lb_00018 [active] rank absent: "User's parents own a Chinese restaurant in Box Hill." (entry passes detector: True); lb_00021 [active] rank absent: "User's parents own a Chinese restaurant called Golden Lotus in Box Hill." (entry passes detector: True); lb_00026 [active] rank 3: "User helps out at their parents' Chinese restaurant called Golden Lotus in Box Hill." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00026': 0.0}; is_abstention False
- **answer**: Lily is of Asian heritage and their family speaks a mix of Cantonese and English.
- raw[:400]: `{"answer": "Lily is of Asian heritage and their family speaks a mix of Cantonese and English."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 271 days | text: User is named Lily
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: ethnic_background | age: 451 days | text: User is of Asian heritage and their family speaks a mix of Cantonese and English
[3] lifecycle: active | category: OBLIGATIONS | attribute: family_business | age: 500 days | text: User helps out at their parents' Chinese restaurant called Golden Lotus in Box Hill.
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: identity_future_self | age: 256 days | text: User identifies as a future worm mother, plant enthusiast, and environmental science enthusiast.
[5] lifecycle: active | category: HOBBIES_RECREATION | attribute: culinary_background | age: 322 days | text: User grew up eating really good dumplings
````


### [mini-D4] frbank:marcus:marcus_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:marcus:marcus_q04:FULL|b2caf21c1a00de0a`
- question: What health conditions should be considered for Marcus?
- gold (YAML `fact`): Has Type 2 diabetes — manages with metformin and diet
- licensed (gold) records: lb_00031 [active] rank 4: "User takes metformin for type 2 diabetes" (entry passes detector: True)
- detector: gold_cov 0.4; answer covers in-view entry text: {'lb_00031': 0.5}; is_abstention False
- **answer**: Marcus has type 2 diabetes.
- raw[:400]: `{"answer": "Marcus has type 2 diabetes."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: medication | age: 531 days | text: User takes metformin for type 2 diabetes
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: employee | age: 272 days | text: User plans to have Carlos work up front with Jerome to improve customer interaction skills.
````


### [mini-D4] frbank:nadia:nadia_q07:FULL -- PRESENT, section contradictions
- key: `frbank:nadia:nadia_q07:FULL|5fba739403e54d49`
- question: Would Nadia ever open her own restaurant?
- gold (YAML `new_fact`): Mentions she's been looking at commercial spaces in Mile End for a pop-up concept
- licensed (gold) records: lb_00432 [active] rank 2: "User is planning to open a pop-up restaurant in Mile End with a Russian-French fusion concept." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00432': 0.1818}; is_abstention False
- **answer**: Nadia will never open her own restaurant due to the high financial risk and personal toll, and she prefers to focus on cooking rather than business ownership.
- raw[:400]: `{"answer": "Nadia will never open her own restaurant due to the high financial risk and personal toll, and she prefers to focus on cooking rather than business ownership."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: career_plan | age: 422 days | text: User will never open their own restaurant.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 132 days | text: User is planning to open a pop-up restaurant in Mile End with a Russian-French fusion concept.
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: career_preference | age: 422 days | text: User does not want to open their own restaurant due to the high financial risk and personal toll.
[4] lifecycle: active | category: PREFERENCES_HABITS | attribute: career_preference | age: 422 days | text: User does not want to open their own restaurant due to the high financial risk.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: career_preference | age: 422 days | text: User does not want to open a restaurant and prefers to focus on cooking rather than business ownership.
````


### [mini-D4] frbank:raj:raj_q07:FULL -- PRESENT, section contradictions
- key: `frbank:raj:raj_q07:FULL|ca392bb4b60bb3ce`
- question: Does Raj work weekends?
- gold (YAML `new_fact`): Mentions working three Saturdays in a row because of emergency callouts
- licensed (gold) records: lb_00390 [active] rank absent: "User has been working emergency callouts on Saturdays for three consecutive weeks." (entry passes detector: True); lb_00393 [active] rank absent: "User has been working three consecutive Saturdays on emergency callouts." (entry passes detector: True); lb_00394 [active] rank absent: "Simran is someone close to the user who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00396 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays" (entry passes detector: True); lb_00399 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays." (entry passes detector: True); lb_00400 [active] rank 2: "User's partner Simran is not happy about the user working three Saturdays in a row." (entry passes detector: True); lb_00403 [active] rank absent: "User has a partner named Simran who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00407 [active] rank absent: "User has been working three consecutive Saturdays on emergency plumbing callouts" (entry passes detector: True)
- detector: gold_cov 0.125; answer covers in-view entry text: {'lb_00400': 0.1429}; is_abstention False
- **answer**: No, Raj does not work on weekends and prioritizes family time on Saturdays and Sundays.
- raw[:400]: `{"answer": "No, Raj does not work on weekends and prioritizes family time on Saturdays and Sundays."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_feelings_about_work | age: 150 days | text: User's partner Simran is not happy about the user working three Saturdays in a row.
[3] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends and prioritizes family time on Saturdays and Sundays.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 150 days | text: User's partner is named Simran and is not happy about the frequent Saturday work
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User works Monday to Friday from 8 to 6 with emergency callouts on weekday evenings only, and does not work weekends.
````


### [mini-D4] frbank:raj:raj_q08:CAT-ABLATED -- PRESENT, section ambiguous
- key: `frbank:raj:raj_q08:CAT-ABLATED|7cc325c0fc913a3f`
- question: Where does Raj live?
- gold (YAML `existing_fact`): Lives in Sparkhill, Birmingham — renting a 3-bed semi
- licensed (gold) records: lb_00027 [active] rank 3: "User lives in a 3-bedroom semi-detached house in Sparkhill." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00027': 0.1667}; is_abstention False
- **answer**: Raj currently lives in Moseley.
- raw[:400]: `{"answer": "Raj currently lives in Moseley."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 472 days | text: User's name is Raj
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 534 days | text: User lives in Birmingham
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: residence | age: 534 days | text: User lives in a 3-bedroom semi-detached house in Sparkhill.
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 195 days | text: User lives in Moseley.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: citizenship | age: 294 days | text: User and Simran are both British citizens.
````


### [mini-D4] frbank:saga:saga_q06:FULL -- PRESENT, section expiring_logistics
- key: `frbank:saga:saga_q06:FULL|84664519969f2865`
- question: Does Saga have any upcoming events?
- gold (YAML `fact`): Data conference talk in Copenhagen — August 8, 2026
- licensed (gold) records: lb_00306 [active] rank 2: "User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026" (entry passes detector: True); lb_00309 [active] rank absent: "User will present a talk on causal inference in recommendation systems at the Nordic Data Science Summit in Copenhagen on August 8, 2026." (entry passes detector: True); lb_00312 [active] rank 4: "User will present at the Nordic Data Science Summit in Copenhagen on August 8" (entry passes detector: True); lb_00315 [active] rank absent: "User has started preparing for the August conference by drafting 18 slides as of January." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00306': 0.0, 'lb_00312': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026
[3] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 389 days | text: User is responsible for giving a speech at Erik's wedding on August 23 in Gothenburg.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 157 days | text: User plans to be near his brother Erik in Gothenburg from roughly October through December to be present for the newborn.
````


### [mini-D4] frbank:saga:saga_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:CAT-ABLATED|174abf8cd8636faf`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 3: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00009': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [mini-D4] frbank:saga:saga_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:FULL|587c999f85ed78c2`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 4: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00009': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [mini-D4] frbank:thanh:thanh_q13:CAT-ABLATED -- PRESENT, section expiring_logistics
- key: `frbank:thanh:thanh_q13:CAT-ABLATED|24fc7028a5ba7661`
- question: Does Thanh have any upcoming family events?
- gold (YAML `fact`): Duc's wedding celebration — July 12, 2026
- licensed (gold) records: lb_00462 [active] rank absent: "User's son Duc is getting married on July 12, 2026" (entry passes detector: True); lb_00468 [active] rank 4: "User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides" (entry passes detector: False); lb_00469 [active] rank absent: "User is planning a wedding for their son Duc on July 12, 2026" (entry passes detector: True); lb_00470 [active] rank absent: "User estimates the wedding budget to be 45 million dong" (entry passes detector: False); lb_00472 [active] rank absent: "User's wedding is planned for July 12, 2026" (entry passes detector: True); lb_00474 [active] rank absent: "User is planning a wedding with about 150 guests" (entry passes detector: False); lb_00475 [active] rank absent: "User's wedding budget is approximately 45 million dong" (entry passes detector: False); lb_00476 [active] rank absent: "User's wedding menu will include shrimp, pork, chicken, duck, spring roll, soup, and rice in delta style" (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00468': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 378 days | text: User lives in or near Can Tho city in Vietnam.
[2] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: preference | age: 312 days | text: User plans to bring about 9 kilograms of shrimp for the next Tet family dinner
[4] lifecycle: active | category: OBLIGATIONS | attribute: event_guest_count | age: 145 days | text: User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides
[5] lifecycle: active | category: PREFERENCES_HABITS | attribute: food_brought | age: 312 days | text: User brought about 6 kilograms of shrimp to the last Tet family dinner.
````


### [mini-D4] frbank:tom:tom_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:tom:tom_q04:FULL|0595f1ca735118b0`
- question: Does Tom have any health conditions?
- gold (YAML `fact`): Has atrial fibrillation — takes warfarin (blood thinners)
- licensed (gold) records: lb_00045 [active] rank absent: "User takes warfarin as a blood thinner medication." (entry passes detector: True); lb_00046 [active] rank 3: "User has atrial fibrillation and takes warfarin as a blood thinner" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00046': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 183 days | text: User's friend Gerald has knee problems and can no longer manage the walk to the pub quiz.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation and takes warfarin as a blood thinner
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 413 days | text: User has been attending the pub quiz with Gerald for twelve or thirteen years.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 141 days | text: User knows a walking group member named Bernard who has a replacement hip and finds stiles challenging.
````


### [mini-D4] frbank:tom:tom_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:tom:tom_q08:FULL|e2a4bb700ca93242`
- question: Where does Tom live?
- gold (YAML `existing_fact`): Lives alone in the village house he shared with Margaret
- licensed (gold) records: lb_00023 [active] rank absent: "User lives alone in a house they have occupied for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00027 [active] rank 4: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00031 [active] rank 5: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00027': 0.0, 'lb_00031': 0.0}; is_abstention False
- **answer**: Tom lives in the Cotswolds, Gloucestershire.
- raw[:400]: `{"answer": "Tom lives in the Cotswolds, Gloucestershire."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 197 days | text: User lives in the Cotswolds.
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 211 days | text: User lives in the Cotswolds
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 442 days | text: User lives in Gloucestershire
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
````


### [mini-D4] frbank:valentina:valentina_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q05:FULL|3cb0d0591dddde1e`
- question: What mental health conditions does Valentina have?
- gold (YAML `fact`): Has PTSD from covering armed conflict in Arauca and Catatumbo
- licensed (gold) records: lb_00046 [active] rank absent: "User reported in conflict zones Arauca and Catatumbo for almost two years" (entry passes detector: True); lb_00047 [active] rank 3: "User has PTSD diagnosed from reporting in conflict zones Arauca and Catatumbo" (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00047': 0.2857}; is_abstention False
- **answer**: Valentina has PTSD diagnosed and is in treatment.
- raw[:400]: `{"answer": "Valentina has PTSD diagnosed and is in treatment."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 503 days | text: User has PTSD diagnosed and is in treatment
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: coping_tool | age: 503 days | text: User finds hearing a voice memo of Lucía's voice could help during PTSD episodes.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 503 days | text: User has PTSD diagnosed from reporting in conflict zones Arauca and Catatumbo
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 214 days | text: User has a close relationship with Lucía, who notices and comments on the user's recurring pre-publication anxiety pattern.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 214 days | text: User experiences physical panic symptoms before publishing major work despite intellectual confidence in the quality.
````


### [mini-D4] frbank:valentina:valentina_q07:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:CAT-ABLATED|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00036': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [mini-D4] frbank:valentina:valentina_q07:FULL -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:FULL|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00036': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [mini-D4] frbank:yoli:yoli_q06:FULL -- PRESENT, section expiring_logistics
- key: `frbank:yoli:yoli_q06:FULL|1b0be2729fef3d13`
- question: Does Yoli have any upcoming deadlines?
- gold (YAML `fact`): JUNO Awards submission deadline for Best Electronic Album — August 29, 2026
- licensed (gold) records: lb_00376 [active] rank absent: "User wants to submit an EP for the JUNOs this year in the Best Electronic Album category." (entry passes detector: False); lb_00377 [active] rank absent: "User plans to finish and master an 8-track EP by August 29, 2026." (entry passes detector: False); lb_00378 [active] rank absent: "User is working on an EP with 8 tracks aiming for submission to the JUNOs for Best Electronic Album." (entry passes detector: False); lb_00379 [active] rank absent: "User currently has 3 tracks nearly finished, 2 tracks halfway done, and needs to create 3 new tracks from scratch for the EP." (entry passes detector: False); lb_00387 [active] rank 2: "User is creating an 8-track EP with a submission deadline of August 29, 2026" (entry passes detector: True)
- detector: gold_cov 0.4; answer covers in-view entry text: {'lb_00387': 0.75}; is_abstention False
- **answer**: Yes, Yoli has an upcoming deadline to submit an 8-track EP by August 29, 2026.
- raw[:400]: `{"answer": "Yes, Yoli has an upcoming deadline to submit an 8-track EP by August 29, 2026."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: stage_name | age: 519 days | text: User's DJ name is YOLI
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 85 days | text: User is creating an 8-track EP with a submission deadline of August 29, 2026
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 52 days | text: User plans to submit to festival lineups in April 2026.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 52 days | text: User plans to submit to festival lineups in April
[5] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 139 days | text: User plans to ship a care package to their grandmother by December 28, 2025.
````


### [mini-D4] frbank:zara:zara_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:zara:zara_q05:FULL|3416758f4e29193f`
- question: Where is Zara's grandmother?
- gold (YAML `fact`): Grandmother Haboba Zahra lives in Khartoum — they've never met in person
- licensed (gold) records: lb_00033 [active] rank 3: "User has a grandmother named Haboba Zahra who is 82 years old and lives in Khartoum, Sudan" (entry passes detector: True); lb_00036 [active] rank 4: "User's grandmother, Haboba Zahra, is 82 years old and lives in Khartoum." (entry passes detector: True); lb_00042 [active] rank 2: "User's grandmother Haboba Zahra is 82 years old and lives in Khartoum in a relatively quiet neighborhood." (entry passes detector: True); lb_00043 [active] rank absent: "User has never met their grandmother Haboba Zahra in person due to visa issues and the war in Sudan." (entry passes detector: True); lb_00047 [active] rank absent: "User has never met their grandmother Haboba Zahra in person and has never been to Sudan." (entry passes detector: True)
- detector: gold_cov 0.4444; answer covers in-view entry text: {'lb_00033': 0.4545, 'lb_00036': 0.5, 'lb_00042': 0.3636}; is_abstention False
- **answer**: Zahra, the user's grandmother, lives in Khartoum, Sudan.
- raw[:400]: `{"answer": "Zahra, the user's grandmother, lives in Khartoum, Sudan."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother is named Haboba Zahra and is 82 years old.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother Haboba Zahra is 82 years old and lives in Khartoum in a relatively quiet neighborhood.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User has a grandmother named Haboba Zahra who is 82 years old and lives in Khartoum, Sudan
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother, Haboba Zahra, is 82 years old and lives in Khartoum.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother, Haboba Zahra, is 82 years old.
````


## h45-D4 (claude-haiku-4-5-20251001, prompt D4)

27 answers.

### [h45-D4] frbank:billy:billy_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:billy:billy_q05:FULL|bc807c9cb9e79e3b`
- question: What health issues does Billy have?
- gold (YAML `fact`): Has frostbite damage on three fingers of his left hand — partial feeling lost
- licensed (gold) records: lb_00040 [active] rank absent: "User has three fingers on their left hand due to frostbite." (entry passes detector: True); lb_00043 [active] rank 5: "User lost three fingers on their left hand due to frostbite from an incident in 2009 during a whiteout while working on a machine in extreme cold." (entry passes detector: True); lb_00044 [active] rank absent: "User's three fingers on the left hand have lost temperature sensation and cannot feel hot or cold." (entry passes detector: True); lb_00045 [active] rank absent: "User has frostbite on three fingers of their left hand resulting in loss of temperature sensation in those fingers" (entry passes detector: True); lb_00048 [active] rank absent: "User lost three fingers on their left hand due to frostbite from a whiteout incident in 2009." (entry passes detector: True); lb_00051 [active] rank 4: "User has had frostbite on three fingers of their left hand since 2009, resulting in loss of temperature sensation in those fingers." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00043': 0.0, 'lb_00051': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries provided are about a user named Annie, not Billy.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries provided are about a user named Annie, not Billy."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: family_member | age: 172 days | text: Annie's mother is 74 years old, lives in Tuk, and has some health concerns that could change quickly.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: family_member | age: 172 days | text: Annie's mother is 74 years old, lives in Tuk, and has some health concerns that require proximity to hospital care in Inuvik or Yellowknife.
[3] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: experience_with_darkness | age: 528 days | text: User has lived with long periods of darkness their whole life
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 513 days | text: User has had frostbite on three fingers of their left hand since 2009, resulting in loss of temperature sensation in those fingers.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 513 days | text: User lost three fingers on their left hand due to frostbite from an incident in 2009 during a whiteout while working on a machine in extreme cold.
````


### [h45-D4] frbank:callum:callum_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:callum:callum_q05:FULL|199ef5dc1bd227ea`
- question: Does Callum have any upcoming events?
- gold (YAML `fact`): Highland Vets annual conference — Edinburgh, May 8-9, 2026
- licensed (gold) records: lb_00378 [active] rank 2: "User has a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False); lb_00380 [active] rank absent: "User's conference topics include clinical updates such as parasitology and antimicrobial stewardship, as well as practice management and client communication." (entry passes detector: False); lb_00383 [active] rank 4: "User will attend a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00378': 0.0, 'lb_00383': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The question asks about 'Callum,' but the memory store entries do not identify the user by name, so I cannot confirm whether these entries belong to someone named Callum.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The question asks about 'Callum,' but the memory store entries do not identify the user by name, so I cannot confirm whether these entries belong to someone named Callum."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HOBBIES_RECREATION | attribute: attendance_habit | age: 292 days | text: User attends Caley Thistle matches when possible, not every week but enough.
[2] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User has a mandatory practice conference on May 8th and 9th in Edinburgh.
[3] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User has four farm calls booked on a morning
[4] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User will attend a mandatory practice conference on May 8th and 9th in Edinburgh.
[5] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User had four farm calls booked on the morning of 2025-04-18
````


### [h45-D4] frbank:callum:callum_q08:CAT-ABLATED -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:CAT-ABLATED|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.2; answer covers in-view entry text: {'lb_00050': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While there are active entries indicating the user is in an early-stage romantic relationship with Eilidh, a vet nurse, there is also an older active entry stating the user is single, creating a contradiction that cannot be resolved from the view alone.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While there are active entries indicating the user is in an early-stage romantic relationship with Eilidh, a vet nurse, there is also an older active entry stating the user is single, creating a contradiction that cannot be resolved from the view alone."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [h45-D4] frbank:callum:callum_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:FULL|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.2; answer covers in-view entry text: {'lb_00050': 0.25}; is_abstention False
- **answer**: The store contains conflicting active entries about the user's relationship status. Entries [1-3] indicate the user is in an early-stage romantic relationship with Eilidh, a vet nurse, while entry [4] states the user is single. The more recent entries [1-3] (147 days old) supersede the older entry [4] (513 days old), so the current relationship status is that the user is in an early-stage romantic relationship with Eilidh.
- raw[:400]: ````json
{
  "answer": "The store contains conflicting active entries about the user's relationship status. Entries [1-3] indicate the user is in an early-stage romantic relationship with Eilidh, a vet nurse, while entry [4] states the user is single. The more recent entries [1-3] (147 days old) supersede the older entry [4] (513 days old), so the current relationship status is that the user is in `
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [h45-D4] frbank:callum:callum_q09:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:callum:callum_q09:CAT-ABLATED|9d5c500649967d49`
- question: What's Callum's background?
- gold (YAML `fact`): Grew up on a sheep farm near Aviemore
- licensed (gold) records: lb_00023 [active] rank 2: "User grew up on a sheep farm near Aviemore." (entry passes detector: True); lb_00024 [active] rank absent: "User's father still runs a smaller sheep farm with about 300 blackface ewes near Aviemore." (entry passes detector: True); lb_00028 [active] rank absent: "User's father runs a sheep farm with about 300 blackface ewes on hill ground near Aviemore." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00023': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. While the view includes information about the user's childhood environment and family, it does not contain any entry identifying the user as 'Callum' or providing background information under that name.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the view includes information about the user's childhood environment and family, it does not contain any entry identifying the user as 'Callum' or providing background information under that name."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: sports_team_support | age: 292 days | text: User supports Caley Thistle football team.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: childhood_environment | age: 531 days | text: User grew up on a sheep farm near Aviemore.
[3] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 454 days | text: User plays rugby in Caledonia Division 2 league.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 20 days | text: User is involved in naming a child and prefers the name Hamish.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 513 days | text: User has a sister named Fiona who is 32 years old and works as a midwife in Glasgow
````


### [h45-D4] frbank:callum:callum_q09:FULL -- PRESENT, section stable_identity
- key: `frbank:callum:callum_q09:FULL|9d5c500649967d49`
- question: What's Callum's background?
- gold (YAML `fact`): Grew up on a sheep farm near Aviemore
- licensed (gold) records: lb_00023 [active] rank 2: "User grew up on a sheep farm near Aviemore." (entry passes detector: True); lb_00024 [active] rank absent: "User's father still runs a smaller sheep farm with about 300 blackface ewes near Aviemore." (entry passes detector: True); lb_00028 [active] rank absent: "User's father runs a sheep farm with about 300 blackface ewes on hill ground near Aviemore." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00023': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. While the view includes information about the user's childhood environment and family, it does not contain any entry identifying the user as 'Callum' or providing background information under that name.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the view includes information about the user's childhood environment and family, it does not contain any entry identifying the user as 'Callum' or providing background information under that name."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: sports_team_support | age: 292 days | text: User supports Caley Thistle football team.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: childhood_environment | age: 531 days | text: User grew up on a sheep farm near Aviemore.
[3] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 454 days | text: User plays rugby in Caledonia Division 2 league.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 20 days | text: User is involved in naming a child and prefers the name Hamish.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 513 days | text: User has a sister named Fiona who is 32 years old and works as a midwife in Glasgow
````


### [h45-D4] frbank:david:david_q08:FULL -- PRESENT, section stable_identity
- key: `frbank:david:david_q08:FULL|102b28d17f2c3532`
- question: What's David's family background?
- gold (YAML `fact`): Adopted from South Korea at age 3 — raised by white parents in Oregon
- licensed (gold) records: lb_00060 [active] rank 2: "User was adopted from South Korea at age three and raised by white parents in Oregon." (entry passes detector: True); lb_00063 [active] rank 3: "User was adopted from South Korea at age three and raised by white parents in Oregon." (entry passes detector: True); lb_00064 [active] rank absent: "User was adopted from South Korea at age three and raised by white parents in Oregon." (entry passes detector: True); lb_00067 [active] rank 4: "User was adopted from South Korea at age three and raised by white parents in Oregon." (entry passes detector: True); lb_00070 [active] rank 5: "User was adopted from South Korea at age three and raised by white parents in Oregon." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00060': 0.0, 'lb_00063': 0.0, 'lb_00067': 0.0, 'lb_00070': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. While the entries describe the user's adoption background, the question asks specifically about 'David's' family background, and the store does not contain information identifying the user as David.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the entries describe the user's adoption background, the question asks specifically about 'David's' family background, and the store does not contain information identifying the user as David."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: professional_background | age: 86 days | text: User has a background in teaching history
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: adoption_origin | age: 476 days | text: User was adopted from South Korea at age three and raised by white parents in Oregon.
[3] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: adoption_background | age: 476 days | text: User was adopted from South Korea at age three and raised by white parents in Oregon.
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: adoption_background | age: 476 days | text: User was adopted from South Korea at age three and raised by white parents in Oregon.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: adoption_background | age: 476 days | text: User was adopted from South Korea at age three and raised by white parents in Oregon.
````


### [h45-D4] frbank:david:david_q10:CAT-ABLATED -- PRESENT, section expiring_logistics
- key: `frbank:david:david_q10:CAT-ABLATED|1f79fac9a79216af`
- question: Does David have any upcoming events?
- gold (YAML `fact`): Debate team state tournament — May 9, 2026
- licensed (gold) records: lb_00477 [active] rank absent: "User's debate team qualified two teams (four students) for the state tournament on May 9th." (entry passes detector: True); lb_00486 [active] rank 5: "User coaches two Public Forum debate teams that qualified for state tournament on May 9, 2026" (entry passes detector: True); lb_00496 [active] rank 1: "User has a coaching responsibility for a debate tournament on May 9th." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00486': 0.0, 'lb_00496': 0.0}; is_abstention True
- **answer**: The store does not currently contain information about whether someone named David has upcoming events. The entries in this view are about the user's own obligations and projects, not about someone named David.
- raw[:400]: ````json
{"answer": "The store does not currently contain information about whether someone named David has upcoming events. The entries in this view are about the user's own obligations and projects, not about someone named David."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: coaching_event_date | age: 86 days | text: User has a coaching responsibility for a debate tournament on May 9th.
[2] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 395 days | text: User has parent-teacher conferences on March 12, 2025
[3] lifecycle: expired | category: OBLIGATIONS | attribute: upcoming_challenging_conferences | age: 395 days | text: User has three difficult parent-teacher conversations upcoming on March 12, 2025
[4] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: trip | age: 171 days | text: User is planning a trip to the Olympic Peninsula with Sarah from July 15th to July 20th.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 86 days | text: User coaches two Public Forum debate teams that qualified for state tournament on May 9, 2026
````


### [h45-D4] frbank:david:david_q10:FULL -- PRESENT, section expiring_logistics
- key: `frbank:david:david_q10:FULL|ad9309e7d5c80d8c`
- question: Does David have any upcoming events?
- gold (YAML `fact`): Debate team state tournament — May 9, 2026
- licensed (gold) records: lb_00477 [active] rank absent: "User's debate team qualified two teams (four students) for the state tournament on May 9th." (entry passes detector: True); lb_00486 [active] rank absent: "User coaches two Public Forum debate teams that qualified for state tournament on May 9, 2026" (entry passes detector: True); lb_00496 [active] rank 1: "User has a coaching responsibility for a debate tournament on May 9th." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00496': 0.6667}; is_abstention True
- **answer**: The store does not currently contain information about whether someone named David has upcoming events. The active entries in this user's memory store describe the user's own coaching responsibility on May 9th and their Portland-area location, but do not mention David or his events.
- raw[:400]: ````json
{"answer": "The store does not currently contain information about whether someone named David has upcoming events. The active entries in this user's memory store describe the user's own coaching responsibility on May 9th and their Portland-area location, but do not mention David or his events."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: coaching_event_date | age: 86 days | text: User has a coaching responsibility for a debate tournament on May 9th.
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 86 days | text: User lives in the Portland area and has connections with other Portland-area school debate coaches.
[3] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 395 days | text: User has parent-teacher conferences on March 12, 2025
[4] lifecycle: expired | category: OBLIGATIONS | attribute: upcoming_challenging_conferences | age: 395 days | text: User has three difficult parent-teacher conversations upcoming on March 12, 2025
[5] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: trip | age: 171 days | text: User is planning a trip to the Olympic Peninsula with Sarah from July 15th to July 20th.
````


### [h45-D4] frbank:diane:diane_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:diane:diane_q05:FULL|25a725c91f24c8d0`
- question: Does Diane have any upcoming events?
- gold (YAML `fact`): Greg's woodworking show at the Folk Art Center — July 12, 2026
- licensed (gold) records: lb_00398 [active] rank 5: "Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026." (entry passes detector: True); lb_00401 [active] rank 1: "Greg was accepted into the Folk Art Center summer show on July 12th, 2026" (entry passes detector: True); lb_00403 [active] rank 3: "Greg has been accepted into the Folk Art Center summer show on July 12th, 2026." (entry passes detector: True); lb_00407 [active] rank 2: "Greg has been accepted into the Folk Art Center summer show on July 12th." (entry passes detector: True); lb_00412 [active] rank absent: "User feels nervous about Greg's acceptance into the Folk Art Center summer show and hopes people will appreciate his work" (entry passes detector: True); lb_00416 [active] rank absent: "User's partner Greg will be building a rocking chair and other pieces in his workshop over the next six months." (entry passes detector: False)
- detector: gold_cov 0.1111; answer covers in-view entry text: {'lb_00398': 0.0769, 'lb_00401': 0.0833, 'lb_00403': 0.0833, 'lb_00407': 0.0909}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries in the memory store are about Greg, not Diane.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries in the memory store are about Greg, not Diane."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show on July 12th, 2026
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th, 2026.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: birthday | age: 16 days | text: Greg's birthday is on Saturday, March 14, 2026
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026.
````


### [h45-D4] frbank:fatima:fatima_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:CAT-ABLATED|8496763e2470a08b`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 2: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer to this question about Fatima's educational background.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer to this question about Fatima's educational background."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
[5] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 317 days | text: User promised to attend Omar's school science fair on May 15th
````


### [h45-D4] frbank:jake:jake_q03:FULL -- PRESENT, section stable_identity
- key: `frbank:jake:jake_q03:FULL|0aa1c0c015b4b7a2`
- question: What does Jake's mom do?
- gold (YAML `fact`): Mom works at the Eire Pub in Dorchester — been waitressing there 20 years
- licensed (gold) records: lb_00047 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00051 [active] rank 3: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00054 [active] rank 2: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00061 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00051': 0.0, 'lb_00054': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe the user's mother, not someone named Jake's mother.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe the user's mother, not someone named Jake's mother."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 106 days | text: User's mother is very involved and stressed about Bridget's wedding preparations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 43 days | text: User's mom is sentimental and cries at Hallmark commercials.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 455 days | text: User lives in Boston and Megan lives in Dorchester near user's mom's workplace
````


### [h45-D4] frbank:jake:jake_q12:FULL -- PRESENT, section stable_identity
- key: `frbank:jake:jake_q12:FULL|c5b8bbe4f14d9360`
- question: What's Jake's work situation?
- gold (YAML `fact`): Dad is a union electrician — runs Brennan & Sons Electric
- licensed (gold) records: lb_00010 [active] rank 1: "User works for his dad's company Brennan and Sons Electric." (entry passes detector: True); lb_00012 [active] rank absent: "User's dad has been a union electrician for about 30 years." (entry passes detector: True); lb_00013 [active] rank 4: "User has been apprenticing under his dad at Brennan and Sons Electric since he got out of high school." (entry passes detector: True); lb_00015 [active] rank 3: "User works for his dad's company Brennan and Sons Electric, where his dad has been a union electrician for about 30 years." (entry passes detector: True); lb_00016 [active] rank absent: "User has been apprenticing under his dad at Brennan and Sons Electric for almost 6 years." (entry passes detector: True); lb_00017 [active] rank 2: "User works with his dad's company Brennan and Sons Electric." (entry passes detector: True); lb_00018 [active] rank absent: "User's dad has been a union electrician for about 30 years." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00010': 0.0, 'lb_00013': 0.0, 'lb_00015': 0.0, 'lb_00017': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe a user's work situation but do not identify the user as Jake, so I cannot confirm this information applies to Jake.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. The entries describe a user's work situation but do not identify the user as Jake, so I cannot confirm this information applies to Jake."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 483 days | text: User works for his dad's company Brennan and Sons Electric.
[2] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 483 days | text: User works with his dad's company Brennan and Sons Electric.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: employer | age: 483 days | text: User works for his dad's company Brennan and Sons Electric, where his dad has been a union electrician for about 30 years.
[4] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 483 days | text: User has been apprenticing under his dad at Brennan and Sons Electric since he got out of high school.
[5] lifecycle: active | category: OBLIGATIONS | attribute: job_type | age: 260 days | text: User works on job sites all day
````


### [h45-D4] frbank:kofi:kofi_q09:FULL -- PRESENT, section ambiguous
- key: `frbank:kofi:kofi_q09:FULL|1c59cb8e93531764`
- question: Is Kofi selling cocoa directly to the Belgian chocolate maker?
- gold (YAML `existing_fact`): Sells all cocoa through the cooperative buying agent system
- licensed (gold) records: lb_00008 [active] rank 3: "User sells cocoa through a cooperative system in their village." (entry passes detector: True); lb_00014 [superseded] rank 5: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag." (entry passes detector: True)
- detector: gold_cov 0.125; answer covers in-view entry text: {'lb_00008': 0.1667, 'lb_00014': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While there is an active entry indicating the user has a direct contact with a Belgian artisan chocolate buyer interested in purchasing 20-30 bags of cocoa per year, there is no entry that confirms whether an actual sale or direct selling arrangement with this buyer has been established.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While there is an active entry indicating the user has a direct contact with a Belgian artisan chocolate buyer interested in purchasing 20-30 bags of cocoa per year, there is no entry that confirms whether an actual sale or direct selling arrangement with this buyer has been established."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: contact | age: 122 days | text: User has a direct contact with a Belgian artisan chocolate buyer who wants to buy 20-30 bags of cocoa per year.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: business_activity | age: 419 days | text: User currently sells raw cocoa beans
[3] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 240 days | text: User led negotiations with Kuapa Kokoo along with 3 elders to secure a premium price for cocoa.
[5] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [h45-D4] frbank:marcus:marcus_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:marcus:marcus_q04:FULL|b2caf21c1a00de0a`
- question: What health conditions should be considered for Marcus?
- gold (YAML `fact`): Has Type 2 diabetes — manages with metformin and diet
- licensed (gold) records: lb_00031 [active] rank 4: "User takes metformin for type 2 diabetes" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00031': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe health conditions for the user, but do not contain information about health conditions for someone named Marcus.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe health conditions for the user, but do not contain information about health conditions for someone named Marcus."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: medication | age: 531 days | text: User takes metformin for type 2 diabetes
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: employee | age: 272 days | text: User plans to have Carlos work up front with Jerome to improve customer interaction skills.
````


### [h45-D4] frbank:nadia:nadia_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:nadia:nadia_q04:FULL|97e46e376ed92a5f`
- question: What languages does Nadia speak?
- gold (YAML `fact`): Speaks three languages — Russian, French, English — but still dreams in Russian
- licensed (gold) records: lb_00044 [active] rank 4: "User speaks French, Russian, and English and switches between them frequently." (entry passes detector: True); lb_00045 [active] rank 2: "User speaks French, English, and Russian." (entry passes detector: True); lb_00049 [active] rank 1: "User speaks three languages: Russian, French, and English." (entry passes detector: True); lb_00062 [active] rank 3: "User speaks three languages: Russian, French, and English, but is fluent in all three and native in none." (entry passes detector: True)
- detector: gold_cov 0.1429; answer covers in-view entry text: {'lb_00044': 0.0, 'lb_00045': 0.0, 'lb_00049': 0.1667, 'lb_00062': 0.2}; is_abstention True
- **answer**: The store does not currently contain the answer. While multiple entries describe languages spoken by the user, none of them identify the user as 'Nadia,' so I cannot confirm these language entries apply to someone by that name.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While multiple entries describe languages spoken by the user, none of them identify the user as 'Nadia,' so I cannot confirm these language entries apply to someone by that name."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks three languages: Russian, French, and English.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks French, English, and Russian.
[3] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks three languages: Russian, French, and English, but is fluent in all three and native in none.
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks French, Russian, and English and switches between them frequently.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: language_fluency | age: 474 days | text: User is fluent in Russian, French, and English but native in none.
````


### [h45-D4] frbank:pan:pan_q10:FULL -- PRESENT, section stable_identity
- key: `frbank:pan:pan_q10:FULL|6d60df716b296f2f`
- question: Who taught Pan her khao man gai recipe?
- gold (YAML `fact`): Mother taught her the khao man gai recipe — passed down through 3 generations from grandmother
- licensed (gold) records: lb_00026 [active] rank 4: "User's khao man gai recipe is a family treasure passed down through three generations." (entry passes detector: True)
- detector: gold_cov 0.3636; answer covers in-view entry text: {'lb_00026': 0.2727}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a user who learned khao man gai from their mother, but do not identify the user as someone named Pan.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries refer to a user who learned khao man gai from their mother, but do not identify the user as someone named Pan."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 468 days | text: User learned to cook khao man gai from their mother, who learned it from the user's grandmother.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: recipe_heritage | age: 170 days | text: User's khao man gai recipe has been passed down for three generations
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: cooking_method | age: 415 days | text: User cooks khao man gai on a charcoal stove as taught by their mother.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 468 days | text: User's khao man gai recipe is a family treasure passed down through three generations.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: family_recipe_sauce | age: 468 days | text: User's khao man gai sauce is a secret recipe from their grandmother that they cannot disclose but want others to know it is special.
````


### [h45-D4] frbank:raj:raj_q07:FULL -- PRESENT, section contradictions
- key: `frbank:raj:raj_q07:FULL|ca392bb4b60bb3ce`
- question: Does Raj work weekends?
- gold (YAML `new_fact`): Mentions working three Saturdays in a row because of emergency callouts
- licensed (gold) records: lb_00390 [active] rank absent: "User has been working emergency callouts on Saturdays for three consecutive weeks." (entry passes detector: True); lb_00393 [active] rank absent: "User has been working three consecutive Saturdays on emergency callouts." (entry passes detector: True); lb_00394 [active] rank absent: "Simran is someone close to the user who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00396 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays" (entry passes detector: True); lb_00399 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays." (entry passes detector: True); lb_00400 [active] rank 2: "User's partner Simran is not happy about the user working three Saturdays in a row." (entry passes detector: True); lb_00403 [active] rank absent: "User has a partner named Simran who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00407 [active] rank absent: "User has been working three consecutive Saturdays on emergency plumbing callouts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00400': 0.2857}; is_abstention True
- **answer**: The store does not currently contain information about a user named Raj. The entries refer to a user whose partner is named Simran, but do not identify the user's own name. Based on the available entries, the user (whose name is not specified as Raj) does not work weekends.
- raw[:400]: ````json
{"answer": "The store does not currently contain information about a user named Raj. The entries refer to a user whose partner is named Simran, but do not identify the user's own name. Based on the available entries, the user (whose name is not specified as Raj) does not work weekends."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_feelings_about_work | age: 150 days | text: User's partner Simran is not happy about the user working three Saturdays in a row.
[3] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends and prioritizes family time on Saturdays and Sundays.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 150 days | text: User's partner is named Simran and is not happy about the frequent Saturday work
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User works Monday to Friday from 8 to 6 with emergency callouts on weekday evenings only, and does not work weekends.
````


### [h45-D4] frbank:saga:saga_q06:FULL -- PRESENT, section expiring_logistics
- key: `frbank:saga:saga_q06:FULL|84664519969f2865`
- question: Does Saga have any upcoming events?
- gold (YAML `fact`): Data conference talk in Copenhagen — August 8, 2026
- licensed (gold) records: lb_00306 [active] rank 2: "User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026" (entry passes detector: True); lb_00309 [active] rank absent: "User will present a talk on causal inference in recommendation systems at the Nordic Data Science Summit in Copenhagen on August 8, 2026." (entry passes detector: True); lb_00312 [active] rank 4: "User will present at the Nordic Data Science Summit in Copenhagen on August 8" (entry passes detector: True); lb_00315 [active] rank absent: "User has started preparing for the August conference by drafting 18 slides as of January." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00306': 0.0, 'lb_00312': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe that the user is an aunt to a newborn girl named Saga, but there is no information about any upcoming events for Saga herself.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe that the user is an aunt to a newborn girl named Saga, but there is no information about any upcoming events for Saga herself."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026
[3] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 389 days | text: User is responsible for giving a speech at Erik's wedding on August 23 in Gothenburg.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 157 days | text: User plans to be near his brother Erik in Gothenburg from roughly October through December to be present for the newborn.
````


### [h45-D4] frbank:saga:saga_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:CAT-ABLATED|174abf8cd8636faf`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 3: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00009': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer."}
```

The memory store indicates that Saga is the user's newborn niece, but it contains no information about Saga's siblings or brother.`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [h45-D4] frbank:saga:saga_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:FULL|587c999f85ed78c2`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 4: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.2; answer covers in-view entry text: {'lb_00009': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While the store indicates that Saga is the user's newborn niece, it does not contain information about Saga's siblings or brother.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the store indicates that Saga is the user's newborn niece, it does not contain information about Saga's siblings or brother."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [h45-D4] frbank:thanh:thanh_q13:CAT-ABLATED -- PRESENT, section expiring_logistics
- key: `frbank:thanh:thanh_q13:CAT-ABLATED|24fc7028a5ba7661`
- question: Does Thanh have any upcoming family events?
- gold (YAML `fact`): Duc's wedding celebration — July 12, 2026
- licensed (gold) records: lb_00462 [active] rank absent: "User's son Duc is getting married on July 12, 2026" (entry passes detector: True); lb_00468 [active] rank 4: "User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides" (entry passes detector: False); lb_00469 [active] rank absent: "User is planning a wedding for their son Duc on July 12, 2026" (entry passes detector: True); lb_00470 [active] rank absent: "User estimates the wedding budget to be 45 million dong" (entry passes detector: False); lb_00472 [active] rank absent: "User's wedding is planned for July 12, 2026" (entry passes detector: True); lb_00474 [active] rank absent: "User is planning a wedding with about 150 guests" (entry passes detector: False); lb_00475 [active] rank absent: "User's wedding budget is approximately 45 million dong" (entry passes detector: False); lb_00476 [active] rank absent: "User's wedding menu will include shrimp, pork, chicken, duck, spring roll, soup, and rice in delta style" (entry passes detector: False)
- detector: gold_cov 0.3333; answer covers in-view entry text: {'lb_00468': 0.4545}; is_abstention True
- **answer**: The store does not currently contain information about whether someone named Thanh has upcoming family events. The entries reference a user's planned doctor visit and Duc's wedding with about 150 expected guests, but do not identify the user as Thanh or confirm Thanh's involvement in these events.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain information about whether someone named Thanh has upcoming family events. The entries reference a user's planned doctor visit and Duc's wedding with about 150 expected guests, but do not identify the user as Thanh or confirm Thanh's involvement in these events."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 378 days | text: User lives in or near Can Tho city in Vietnam.
[2] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: preference | age: 312 days | text: User plans to bring about 9 kilograms of shrimp for the next Tet family dinner
[4] lifecycle: active | category: OBLIGATIONS | attribute: event_guest_count | age: 145 days | text: User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides
[5] lifecycle: active | category: PREFERENCES_HABITS | attribute: food_brought | age: 312 days | text: User brought about 6 kilograms of shrimp to the last Tet family dinner.
````


### [h45-D4] frbank:tom:tom_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:tom:tom_q04:FULL|0595f1ca735118b0`
- question: Does Tom have any health conditions?
- gold (YAML `fact`): Has atrial fibrillation — takes warfarin (blood thinners)
- licensed (gold) records: lb_00045 [active] rank absent: "User takes warfarin as a blood thinner medication." (entry passes detector: True); lb_00046 [active] rank 3: "User has atrial fibrillation and takes warfarin as a blood thinner" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00046': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe health conditions for the user, but do not contain information about someone named Tom.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe health conditions for the user, but do not contain information about someone named Tom."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 183 days | text: User's friend Gerald has knee problems and can no longer manage the walk to the pub quiz.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation and takes warfarin as a blood thinner
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 413 days | text: User has been attending the pub quiz with Gerald for twelve or thirteen years.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 141 days | text: User knows a walking group member named Bernard who has a replacement hip and finds stiles challenging.
````


### [h45-D4] frbank:tom:tom_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:tom:tom_q08:FULL|e2a4bb700ca93242`
- question: Where does Tom live?
- gold (YAML `existing_fact`): Lives alone in the village house he shared with Margaret
- licensed (gold) records: lb_00023 [active] rank absent: "User lives alone in a house they have occupied for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00027 [active] rank 4: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00031 [active] rank 5: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00027': 0.0, 'lb_00031': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. While the entries indicate the user lives in the Cotswolds and Gloucestershire, they do not provide information about someone named Tom.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the entries indicate the user lives in the Cotswolds and Gloucestershire, they do not provide information about someone named Tom."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 197 days | text: User lives in the Cotswolds.
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 211 days | text: User lives in the Cotswolds
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 442 days | text: User lives in Gloucestershire
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
````


### [h45-D4] frbank:valentina:valentina_q07:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:CAT-ABLATED|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.2857; answer covers in-view entry text: {'lb_00036': 0.375}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries reference a user with a partner named Lucía, but do not identify the user as Valentina.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries reference a user with a partner named Lucía, but do not identify the user as Valentina."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [h45-D4] frbank:valentina:valentina_q07:FULL -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:FULL|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.2857; answer covers in-view entry text: {'lb_00036': 0.375}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries reference a partner named Lucía, but the question asks about someone named Valentina, and there is no entry in the store identifying the user as Valentina.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries reference a partner named Lucía, but the question asks about someone named Valentina, and there is no entry in the store identifying the user as Valentina."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [h45-D4] frbank:zara:zara_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:zara:zara_q05:FULL|3416758f4e29193f`
- question: Where is Zara's grandmother?
- gold (YAML `fact`): Grandmother Haboba Zahra lives in Khartoum — they've never met in person
- licensed (gold) records: lb_00033 [active] rank 3: "User has a grandmother named Haboba Zahra who is 82 years old and lives in Khartoum, Sudan" (entry passes detector: True); lb_00036 [active] rank 4: "User's grandmother, Haboba Zahra, is 82 years old and lives in Khartoum." (entry passes detector: True); lb_00042 [active] rank 2: "User's grandmother Haboba Zahra is 82 years old and lives in Khartoum in a relatively quiet neighborhood." (entry passes detector: True); lb_00043 [active] rank absent: "User has never met their grandmother Haboba Zahra in person due to visa issues and the war in Sudan." (entry passes detector: True); lb_00047 [active] rank absent: "User has never met their grandmother Haboba Zahra in person and has never been to Sudan." (entry passes detector: True)
- detector: gold_cov 0.3333; answer covers in-view entry text: {'lb_00033': 0.3636, 'lb_00036': 0.375, 'lb_00042': 0.2727}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a grandmother named Haboba Zahra, not Zara, so this question cannot be answered from the available information.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries refer to a grandmother named Haboba Zahra, not Zara, so this question cannot be answered from the available information."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother is named Haboba Zahra and is 82 years old.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother Haboba Zahra is 82 years old and lives in Khartoum in a relatively quiet neighborhood.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User has a grandmother named Haboba Zahra who is 82 years old and lives in Khartoum, Sudan
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother, Haboba Zahra, is 82 years old and lives in Khartoum.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother, Haboba Zahra, is 82 years old.
````


## Appendix -- mini-A3 (gpt-4.1-mini, prompt A3)

26 answers.

### [mini-A3] frbank:callum:callum_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:callum:callum_q05:FULL|199ef5dc1bd227ea`
- question: Does Callum have any upcoming events?
- gold (YAML `fact`): Highland Vets annual conference — Edinburgh, May 8-9, 2026
- licensed (gold) records: lb_00378 [active] rank 2: "User has a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False); lb_00380 [active] rank absent: "User's conference topics include clinical updates such as parasitology and antimicrobial stewardship, as well as practice management and client communication." (entry passes detector: False); lb_00383 [active] rank 4: "User will attend a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False)
- detector: gold_cov 0.4286; answer covers in-view entry text: {'lb_00378': 1.0, 'lb_00383': 0.8571}; is_abstention False
- **answer**: Yes, Callum has a mandatory practice conference on May 8th and 9th in Edinburgh.
- raw[:400]: `{"answer": "Yes, Callum has a mandatory practice conference on May 8th and 9th in Edinburgh."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HOBBIES_RECREATION | attribute: attendance_habit | age: 292 days | text: User attends Caley Thistle matches when possible, not every week but enough.
[2] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User has a mandatory practice conference on May 8th and 9th in Edinburgh.
[3] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User has four farm calls booked on a morning
[4] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User will attend a mandatory practice conference on May 8th and 9th in Edinburgh.
[5] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User had four farm calls booked on the morning of 2025-04-18
````


### [mini-A3] frbank:callum:callum_q08:CAT-ABLATED -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:CAT-ABLATED|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00050': 0.0}; is_abstention False
- **answer**: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
- raw[:400]: `{"answer": "User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [mini-A3] frbank:callum:callum_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:FULL|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00050': 0.0}; is_abstention False
- **answer**: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
- raw[:400]: `{"answer":"User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [mini-A3] frbank:callum:callum_q09:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:callum:callum_q09:CAT-ABLATED|9d5c500649967d49`
- question: What's Callum's background?
- gold (YAML `fact`): Grew up on a sheep farm near Aviemore
- licensed (gold) records: lb_00023 [active] rank 2: "User grew up on a sheep farm near Aviemore." (entry passes detector: True); lb_00024 [active] rank absent: "User's father still runs a smaller sheep farm with about 300 blackface ewes near Aviemore." (entry passes detector: True); lb_00028 [active] rank absent: "User's father runs a sheep farm with about 300 blackface ewes on hill ground near Aviemore." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00023': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: sports_team_support | age: 292 days | text: User supports Caley Thistle football team.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: childhood_environment | age: 531 days | text: User grew up on a sheep farm near Aviemore.
[3] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 454 days | text: User plays rugby in Caledonia Division 2 league.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 20 days | text: User is involved in naming a child and prefers the name Hamish.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 513 days | text: User has a sister named Fiona who is 32 years old and works as a midwife in Glasgow
````


### [mini-A3] frbank:callum:callum_q09:FULL -- PRESENT, section stable_identity
- key: `frbank:callum:callum_q09:FULL|9d5c500649967d49`
- question: What's Callum's background?
- gold (YAML `fact`): Grew up on a sheep farm near Aviemore
- licensed (gold) records: lb_00023 [active] rank 2: "User grew up on a sheep farm near Aviemore." (entry passes detector: True); lb_00024 [active] rank absent: "User's father still runs a smaller sheep farm with about 300 blackface ewes near Aviemore." (entry passes detector: True); lb_00028 [active] rank absent: "User's father runs a sheep farm with about 300 blackface ewes on hill ground near Aviemore." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00023': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: sports_team_support | age: 292 days | text: User supports Caley Thistle football team.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: childhood_environment | age: 531 days | text: User grew up on a sheep farm near Aviemore.
[3] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 454 days | text: User plays rugby in Caledonia Division 2 league.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 20 days | text: User is involved in naming a child and prefers the name Hamish.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 513 days | text: User has a sister named Fiona who is 32 years old and works as a midwife in Glasgow
````


### [mini-A3] frbank:diane:diane_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:diane:diane_q04:FULL|3cf1876c69c43346`
- question: Does Diane have any health conditions?
- gold (YAML `fact`): Osteoarthritis in both knees
- licensed (gold) records: lb_00063 [active] rank absent: "User has osteoarthritis in their knees" (entry passes detector: True); lb_00064 [active] rank absent: "User has osteoarthritis in both knees." (entry passes detector: True); lb_00065 [active] rank absent: "User's osteoarthritis in knees has been worsening over the last two years." (entry passes detector: True); lb_00071 [active] rank 5: "User has osteoarthritis in both knees that has been worsening over the past six to seven years, with significant decline in the last two years" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00071': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 503 days | text: User had a visit with a woman named Eleanor who is ninety-one years old and is dying well.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: colleague | age: 205 days | text: User has a close professional relationship with a nurse named Sandra from Four Seasons Compassion for Life.
[3] lifecycle: active | category: OBLIGATIONS | attribute: occupation_patient_relationship | age: 145 days | text: User is a caregiver or healthcare provider with patients who request her specifically
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 290 days | text: Margaret told me she had lived long enough to stop being afraid of anything except unkindness.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 440 days | text: User has osteoarthritis in both knees that has been worsening over the past six to seven years, with significant decline in the last two years
````


### [mini-A3] frbank:diane:diane_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:diane:diane_q05:FULL|25a725c91f24c8d0`
- question: Does Diane have any upcoming events?
- gold (YAML `fact`): Greg's woodworking show at the Folk Art Center — July 12, 2026
- licensed (gold) records: lb_00398 [active] rank 5: "Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026." (entry passes detector: True); lb_00401 [active] rank 1: "Greg was accepted into the Folk Art Center summer show on July 12th, 2026" (entry passes detector: True); lb_00403 [active] rank 3: "Greg has been accepted into the Folk Art Center summer show on July 12th, 2026." (entry passes detector: True); lb_00407 [active] rank 2: "Greg has been accepted into the Folk Art Center summer show on July 12th." (entry passes detector: True); lb_00412 [active] rank absent: "User feels nervous about Greg's acceptance into the Folk Art Center summer show and hopes people will appreciate his work" (entry passes detector: True); lb_00416 [active] rank absent: "User's partner Greg will be building a rocking chair and other pieces in his workshop over the next six months." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00398': 0.0, 'lb_00401': 0.0, 'lb_00403': 0.0, 'lb_00407': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show on July 12th, 2026
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th, 2026.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: birthday | age: 16 days | text: Greg's birthday is on Saturday, March 14, 2026
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026.
````


### [mini-A3] frbank:fatima:fatima_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:CAT-ABLATED|8496763e2470a08b`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 2: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
[5] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 317 days | text: User promised to attend Omar's school science fair on May 15th
````


### [mini-A3] frbank:fatima:fatima_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:FULL|06a840f434c701e6`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 3: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer":"The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: city | age: 468 days | text: User lives in Riyadh and manages all transportation for her children, including driving Khalid to football practice three times a week.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
````


### [mini-A3] frbank:ingrid:ingrid_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:ingrid:ingrid_q05:FULL|82fbc8ac2f06e090`
- question: What health conditions does Ingrid have?
- gold (YAML `fact`): Has Raynaud's syndrome — circulation in fingers shuts down in cold
- licensed (gold) records: lb_00043 [active] rank 1: "User has Raynaud's syndrome affecting their fingers in cold conditions." (entry passes detector: True)
- detector: gold_cov 0.4286; answer covers in-view entry text: {'lb_00043': 0.5}; is_abstention False
- **answer**: Ingrid has Raynaud's syndrome, also referred to as Raynaud's disease, which causes blood vessel spasms in her fingers below about 5 degrees Celsius, leading to white, numb fingers and loss of fine manipulation ability.
- raw[:400]: `{"answer": "Ingrid has Raynaud's syndrome, also referred to as Raynaud's disease, which causes blood vessel spasms in her fingers below about 5 degrees Celsius, leading to white, numb fingers and loss of fine manipulation ability."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's syndrome affecting their fingers in cold conditions.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: dietary_restrictions | age: 418 days | text: User has no dietary restrictions among the three people.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's disease, which causes blood vessel spasms in fingers below about 5 degrees Celsius, leading to white and numb fingers.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's disease which causes finger vasospasm below about 5 degrees Celsius, leading to white and numb fingers and loss of fine manipulation ability.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 500 days | text: User has Raynaud's syndrome which affects finger dexterity below about 5 degrees Celsius.
````


### [mini-A3] frbank:jake:jake_q03:FULL -- PRESENT, section stable_identity
- key: `frbank:jake:jake_q03:FULL|0aa1c0c015b4b7a2`
- question: What does Jake's mom do?
- gold (YAML `fact`): Mom works at the Eire Pub in Dorchester — been waitressing there 20 years
- licensed (gold) records: lb_00047 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00051 [active] rank 3: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00054 [active] rank 2: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00061 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00051': 0.0, 'lb_00054': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer":"The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 106 days | text: User's mother is very involved and stressed about Bridget's wedding preparations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 43 days | text: User's mom is sentimental and cries at Hallmark commercials.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 455 days | text: User lives in Boston and Megan lives in Dorchester near user's mom's workplace
````


### [mini-A3] frbank:kenji:kenji_q12:FULL -- PRESENT, section stable_identity
- key: `frbank:kenji:kenji_q12:FULL|1c9c2009de7dbd61`
- question: What's Kenji's educational background?
- gold (YAML `fact`): BFA from Tama Art University in Tokyo
- licensed (gold) records: lb_00065 [active] rank 1: "User attended Tama Art University in Tokyo for their BFA." (entry passes detector: True); lb_00068 [active] rank absent: "User received financial aid for their education at Tama Art University, but it was still a financial stretch for their family." (entry passes detector: True); lb_00069 [active] rank absent: "User developed a deep interest and love for type design during their studies at Tama Art University." (entry passes detector: True); lb_00071 [active] rank absent: "User's design education at Tama Art University was transformative, especially due to the typography program and critique culture." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00065': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: education_bfa | age: 399 days | text: User attended Tama Art University in Tokyo for their BFA.
[2] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: intellectual_interest | age: 204 days | text: User is interested in design history and philosophy, especially the work of Yanagi Soetsu and the mingei movement.
[3] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: intellectual_interest | age: 204 days | text: User is deeply interested in design philosophy, especially related to mingei and Soetsu Yanagi's work.
[4] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: intellectual_interest | age: 204 days | text: User has a strong intellectual interest in the mingei movement and its philosophy.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 399 days | text: User's younger cousin is interested in illustration and character design and is considering art schools like Musashino, Kyoto Seika, and vocational schools in Osaka.
````


### [mini-A3] frbank:lily:lily_q09:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:lily:lily_q09:CAT-ABLATED|e1426bab79e22e41`
- question: What's Lily's family background?
- gold (YAML `fact`): Parents run a Chinese restaurant — Golden Lotus in Box Hill
- licensed (gold) records: lb_00018 [active] rank absent: "User's parents own a Chinese restaurant in Box Hill." (entry passes detector: True); lb_00021 [active] rank absent: "User's parents own a Chinese restaurant called Golden Lotus in Box Hill." (entry passes detector: True); lb_00026 [active] rank 3: "User helps out at their parents' Chinese restaurant called Golden Lotus in Box Hill." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00026': 0.0}; is_abstention False
- **answer**: Lily is of Asian heritage and their family speaks a mix of Cantonese and English.
- raw[:400]: `{"answer": "Lily is of Asian heritage and their family speaks a mix of Cantonese and English."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 271 days | text: User is named Lily
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: ethnic_background | age: 451 days | text: User is of Asian heritage and their family speaks a mix of Cantonese and English
[3] lifecycle: active | category: OBLIGATIONS | attribute: family_business | age: 500 days | text: User helps out at their parents' Chinese restaurant called Golden Lotus in Box Hill.
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: identity_future_self | age: 256 days | text: User identifies as a future worm mother, plant enthusiast, and environmental science enthusiast.
[5] lifecycle: active | category: HOBBIES_RECREATION | attribute: culinary_background | age: 322 days | text: User grew up eating really good dumplings
````


### [mini-A3] frbank:marcus:marcus_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:marcus:marcus_q04:FULL|b2caf21c1a00de0a`
- question: What health conditions should be considered for Marcus?
- gold (YAML `fact`): Has Type 2 diabetes — manages with metformin and diet
- licensed (gold) records: lb_00031 [active] rank 4: "User takes metformin for type 2 diabetes" (entry passes detector: True)
- detector: gold_cov 0.4; answer covers in-view entry text: {'lb_00031': 0.5}; is_abstention False
- **answer**: Marcus has type 2 diabetes.
- raw[:400]: `{"answer": "Marcus has type 2 diabetes."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: medication | age: 531 days | text: User takes metformin for type 2 diabetes
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: employee | age: 272 days | text: User plans to have Carlos work up front with Jerome to improve customer interaction skills.
````


### [mini-A3] frbank:nadia:nadia_q07:FULL -- PRESENT, section contradictions
- key: `frbank:nadia:nadia_q07:FULL|5fba739403e54d49`
- question: Would Nadia ever open her own restaurant?
- gold (YAML `new_fact`): Mentions she's been looking at commercial spaces in Mile End for a pop-up concept
- licensed (gold) records: lb_00432 [active] rank 2: "User is planning to open a pop-up restaurant in Mile End with a Russian-French fusion concept." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00432': 0.1818}; is_abstention False
- **answer**: Nadia will never open her own restaurant and prefers to focus on cooking rather than business ownership due to the high financial risk and personal toll.
- raw[:400]: `{"answer": "Nadia will never open her own restaurant and prefers to focus on cooking rather than business ownership due to the high financial risk and personal toll."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: career_plan | age: 422 days | text: User will never open their own restaurant.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 132 days | text: User is planning to open a pop-up restaurant in Mile End with a Russian-French fusion concept.
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: career_preference | age: 422 days | text: User does not want to open their own restaurant due to the high financial risk and personal toll.
[4] lifecycle: active | category: PREFERENCES_HABITS | attribute: career_preference | age: 422 days | text: User does not want to open their own restaurant due to the high financial risk.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: career_preference | age: 422 days | text: User does not want to open a restaurant and prefers to focus on cooking rather than business ownership.
````


### [mini-A3] frbank:raj:raj_q07:FULL -- PRESENT, section contradictions
- key: `frbank:raj:raj_q07:FULL|ca392bb4b60bb3ce`
- question: Does Raj work weekends?
- gold (YAML `new_fact`): Mentions working three Saturdays in a row because of emergency callouts
- licensed (gold) records: lb_00390 [active] rank absent: "User has been working emergency callouts on Saturdays for three consecutive weeks." (entry passes detector: True); lb_00393 [active] rank absent: "User has been working three consecutive Saturdays on emergency callouts." (entry passes detector: True); lb_00394 [active] rank absent: "Simran is someone close to the user who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00396 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays" (entry passes detector: True); lb_00399 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays." (entry passes detector: True); lb_00400 [active] rank 2: "User's partner Simran is not happy about the user working three Saturdays in a row." (entry passes detector: True); lb_00403 [active] rank absent: "User has a partner named Simran who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00407 [active] rank absent: "User has been working three consecutive Saturdays on emergency plumbing callouts" (entry passes detector: True)
- detector: gold_cov 0.125; answer covers in-view entry text: {'lb_00400': 0.1429}; is_abstention False
- **answer**: No, Raj does not work on weekends and prioritizes family time on Saturdays and Sundays.
- raw[:400]: `{"answer": "No, Raj does not work on weekends and prioritizes family time on Saturdays and Sundays."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_feelings_about_work | age: 150 days | text: User's partner Simran is not happy about the user working three Saturdays in a row.
[3] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends and prioritizes family time on Saturdays and Sundays.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 150 days | text: User's partner is named Simran and is not happy about the frequent Saturday work
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User works Monday to Friday from 8 to 6 with emergency callouts on weekday evenings only, and does not work weekends.
````


### [mini-A3] frbank:raj:raj_q08:CAT-ABLATED -- PRESENT, section ambiguous
- key: `frbank:raj:raj_q08:CAT-ABLATED|7cc325c0fc913a3f`
- question: Where does Raj live?
- gold (YAML `existing_fact`): Lives in Sparkhill, Birmingham — renting a 3-bed semi
- licensed (gold) records: lb_00027 [active] rank 3: "User lives in a 3-bedroom semi-detached house in Sparkhill." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00027': 0.1667}; is_abstention False
- **answer**: Raj currently lives in Moseley.
- raw[:400]: `{"answer": "Raj currently lives in Moseley."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 472 days | text: User's name is Raj
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 534 days | text: User lives in Birmingham
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: residence | age: 534 days | text: User lives in a 3-bedroom semi-detached house in Sparkhill.
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 195 days | text: User lives in Moseley.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: citizenship | age: 294 days | text: User and Simran are both British citizens.
````


### [mini-A3] frbank:saga:saga_q06:FULL -- PRESENT, section expiring_logistics
- key: `frbank:saga:saga_q06:FULL|84664519969f2865`
- question: Does Saga have any upcoming events?
- gold (YAML `fact`): Data conference talk in Copenhagen — August 8, 2026
- licensed (gold) records: lb_00306 [active] rank 2: "User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026" (entry passes detector: True); lb_00309 [active] rank absent: "User will present a talk on causal inference in recommendation systems at the Nordic Data Science Summit in Copenhagen on August 8, 2026." (entry passes detector: True); lb_00312 [active] rank 4: "User will present at the Nordic Data Science Summit in Copenhagen on August 8" (entry passes detector: True); lb_00315 [active] rank absent: "User has started preparing for the August conference by drafting 18 slides as of January." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00306': 0.0, 'lb_00312': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026
[3] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 389 days | text: User is responsible for giving a speech at Erik's wedding on August 23 in Gothenburg.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 157 days | text: User plans to be near his brother Erik in Gothenburg from roughly October through December to be present for the newborn.
````


### [mini-A3] frbank:saga:saga_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:CAT-ABLATED|174abf8cd8636faf`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 3: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00009': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [mini-A3] frbank:saga:saga_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:FULL|587c999f85ed78c2`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 4: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00009': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [mini-A3] frbank:thanh:thanh_q13:CAT-ABLATED -- PRESENT, section expiring_logistics
- key: `frbank:thanh:thanh_q13:CAT-ABLATED|24fc7028a5ba7661`
- question: Does Thanh have any upcoming family events?
- gold (YAML `fact`): Duc's wedding celebration — July 12, 2026
- licensed (gold) records: lb_00462 [active] rank absent: "User's son Duc is getting married on July 12, 2026" (entry passes detector: True); lb_00468 [active] rank 4: "User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides" (entry passes detector: False); lb_00469 [active] rank absent: "User is planning a wedding for their son Duc on July 12, 2026" (entry passes detector: True); lb_00470 [active] rank absent: "User estimates the wedding budget to be 45 million dong" (entry passes detector: False); lb_00472 [active] rank absent: "User's wedding is planned for July 12, 2026" (entry passes detector: True); lb_00474 [active] rank absent: "User is planning a wedding with about 150 guests" (entry passes detector: False); lb_00475 [active] rank absent: "User's wedding budget is approximately 45 million dong" (entry passes detector: False); lb_00476 [active] rank absent: "User's wedding menu will include shrimp, pork, chicken, duck, spring roll, soup, and rice in delta style" (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00468': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 378 days | text: User lives in or near Can Tho city in Vietnam.
[2] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: preference | age: 312 days | text: User plans to bring about 9 kilograms of shrimp for the next Tet family dinner
[4] lifecycle: active | category: OBLIGATIONS | attribute: event_guest_count | age: 145 days | text: User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides
[5] lifecycle: active | category: PREFERENCES_HABITS | attribute: food_brought | age: 312 days | text: User brought about 6 kilograms of shrimp to the last Tet family dinner.
````


### [mini-A3] frbank:tom:tom_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:tom:tom_q04:FULL|0595f1ca735118b0`
- question: Does Tom have any health conditions?
- gold (YAML `fact`): Has atrial fibrillation — takes warfarin (blood thinners)
- licensed (gold) records: lb_00045 [active] rank absent: "User takes warfarin as a blood thinner medication." (entry passes detector: True); lb_00046 [active] rank 3: "User has atrial fibrillation and takes warfarin as a blood thinner" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00046': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 183 days | text: User's friend Gerald has knee problems and can no longer manage the walk to the pub quiz.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation and takes warfarin as a blood thinner
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 413 days | text: User has been attending the pub quiz with Gerald for twelve or thirteen years.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 141 days | text: User knows a walking group member named Bernard who has a replacement hip and finds stiles challenging.
````


### [mini-A3] frbank:tom:tom_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:tom:tom_q08:FULL|e2a4bb700ca93242`
- question: Where does Tom live?
- gold (YAML `existing_fact`): Lives alone in the village house he shared with Margaret
- licensed (gold) records: lb_00023 [active] rank absent: "User lives alone in a house they have occupied for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00027 [active] rank 4: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00031 [active] rank 5: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00027': 0.0, 'lb_00031': 0.0}; is_abstention False
- **answer**: Tom lives in the Cotswolds, Gloucestershire.
- raw[:400]: `{"answer": "Tom lives in the Cotswolds, Gloucestershire."}`
- auto_label: wrong_value
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 197 days | text: User lives in the Cotswolds.
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 211 days | text: User lives in the Cotswolds
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 442 days | text: User lives in Gloucestershire
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
````


### [mini-A3] frbank:valentina:valentina_q07:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:CAT-ABLATED|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00036': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [mini-A3] frbank:valentina:valentina_q07:FULL -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:FULL|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00036': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [mini-A3] frbank:yoli:yoli_q06:FULL -- PRESENT, section expiring_logistics
- key: `frbank:yoli:yoli_q06:FULL|1b0be2729fef3d13`
- question: Does Yoli have any upcoming deadlines?
- gold (YAML `fact`): JUNO Awards submission deadline for Best Electronic Album — August 29, 2026
- licensed (gold) records: lb_00376 [active] rank absent: "User wants to submit an EP for the JUNOs this year in the Best Electronic Album category." (entry passes detector: False); lb_00377 [active] rank absent: "User plans to finish and master an 8-track EP by August 29, 2026." (entry passes detector: False); lb_00378 [active] rank absent: "User is working on an EP with 8 tracks aiming for submission to the JUNOs for Best Electronic Album." (entry passes detector: False); lb_00379 [active] rank absent: "User currently has 3 tracks nearly finished, 2 tracks halfway done, and needs to create 3 new tracks from scratch for the EP." (entry passes detector: False); lb_00387 [active] rank 2: "User is creating an 8-track EP with a submission deadline of August 29, 2026" (entry passes detector: True)
- detector: gold_cov 0.4; answer covers in-view entry text: {'lb_00387': 0.75}; is_abstention False
- **answer**: Yes, Yoli has an upcoming deadline to submit an 8-track EP by August 29, 2026.
- raw[:400]: `{"answer": "Yes, Yoli has an upcoming deadline to submit an 8-track EP by August 29, 2026."}`
- auto_label: correct_different_format
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: stage_name | age: 519 days | text: User's DJ name is YOLI
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 85 days | text: User is creating an 8-track EP with a submission deadline of August 29, 2026
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 52 days | text: User plans to submit to festival lineups in April 2026.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 52 days | text: User plans to submit to festival lineups in April
[5] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 139 days | text: User plans to ship a care package to their grandmother by December 28, 2025.
````


## Appendix -- h45-A3 (claude-haiku-4-5-20251001, prompt A3)

24 answers.

### [h45-A3] frbank:billy:billy_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:billy:billy_q05:FULL|bc807c9cb9e79e3b`
- question: What health issues does Billy have?
- gold (YAML `fact`): Has frostbite damage on three fingers of his left hand — partial feeling lost
- licensed (gold) records: lb_00040 [active] rank absent: "User has three fingers on their left hand due to frostbite." (entry passes detector: True); lb_00043 [active] rank 5: "User lost three fingers on their left hand due to frostbite from an incident in 2009 during a whiteout while working on a machine in extreme cold." (entry passes detector: True); lb_00044 [active] rank absent: "User's three fingers on the left hand have lost temperature sensation and cannot feel hot or cold." (entry passes detector: True); lb_00045 [active] rank absent: "User has frostbite on three fingers of their left hand resulting in loss of temperature sensation in those fingers" (entry passes detector: True); lb_00048 [active] rank absent: "User lost three fingers on their left hand due to frostbite from a whiteout incident in 2009." (entry passes detector: True); lb_00051 [active] rank 4: "User has had frostbite on three fingers of their left hand since 2009, resulting in loss of temperature sensation in those fingers." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00043': 0.0, 'lb_00051': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries in the memory store are about a user named Annie, not Billy.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries in the memory store are about a user named Annie, not Billy."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: family_member | age: 172 days | text: Annie's mother is 74 years old, lives in Tuk, and has some health concerns that could change quickly.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: family_member | age: 172 days | text: Annie's mother is 74 years old, lives in Tuk, and has some health concerns that require proximity to hospital care in Inuvik or Yellowknife.
[3] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: experience_with_darkness | age: 528 days | text: User has lived with long periods of darkness their whole life
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 513 days | text: User has had frostbite on three fingers of their left hand since 2009, resulting in loss of temperature sensation in those fingers.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 513 days | text: User lost three fingers on their left hand due to frostbite from an incident in 2009 during a whiteout while working on a machine in extreme cold.
````


### [h45-A3] frbank:callum:callum_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:callum:callum_q05:FULL|199ef5dc1bd227ea`
- question: Does Callum have any upcoming events?
- gold (YAML `fact`): Highland Vets annual conference — Edinburgh, May 8-9, 2026
- licensed (gold) records: lb_00378 [active] rank 2: "User has a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False); lb_00380 [active] rank absent: "User's conference topics include clinical updates such as parasitology and antimicrobial stewardship, as well as practice management and client communication." (entry passes detector: False); lb_00383 [active] rank 4: "User will attend a mandatory practice conference on May 8th and 9th in Edinburgh." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00378': 0.0, 'lb_00383': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The question asks about 'Callum,' but the memory store entries do not identify the user by name, so I cannot confirm whether these entries pertain to someone named Callum.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The question asks about 'Callum,' but the memory store entries do not identify the user by name, so I cannot confirm whether these entries pertain to someone named Callum."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HOBBIES_RECREATION | attribute: attendance_habit | age: 292 days | text: User attends Caley Thistle matches when possible, not every week but enough.
[2] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User has a mandatory practice conference on May 8th and 9th in Edinburgh.
[3] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User has four farm calls booked on a morning
[4] lifecycle: active | category: OBLIGATIONS | attribute: event | age: 63 days | text: User will attend a mandatory practice conference on May 8th and 9th in Edinburgh.
[5] lifecycle: active | category: OBLIGATIONS | attribute: obligation | age: 384 days | text: User had four farm calls booked on the morning of 2025-04-18
````


### [h45-A3] frbank:callum:callum_q08:CAT-ABLATED -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:CAT-ABLATED|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.2; answer covers in-view entry text: {'lb_00050': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While there are active entries indicating the user is in an early-stage romantic relationship with Eilidh, a vet nurse, there is a conflicting active entry from 513 days ago stating the user is single, making the current relationship status unclear from these entries alone.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While there are active entries indicating the user is in an early-stage romantic relationship with Eilidh, a vet nurse, there is a conflicting active entry from 513 days ago stating the user is single, making the current relationship status unclear from these entries alone."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [h45-A3] frbank:callum:callum_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:callum:callum_q08:FULL|8ee34ab8220ecd63`
- question: What's Callum's relationship status?
- gold (YAML `existing_fact`): Single — hasn't dated since uni
- licensed (gold) records: lb_00050 [active] rank 4: "User is single and has not dated since university." (entry passes detector: True)
- detector: gold_cov 0.2; answer covers in-view entry text: {'lb_00050': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While there are active entries indicating the user is in an early-stage romantic relationship with Eilidh, a vet nurse, there is a conflicting active entry from 513 days ago stating the user is single, making the current relationship status unclear from these entries alone.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While there are active entries indicating the user is in an early-stage romantic relationship with Eilidh, a vet nurse, there is a conflicting active entry from 513 days ago stating the user is single, making the current relationship status unclear from these entries alone."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User is in an early-stage romantic relationship with Eilidh, a vet nurse at their practice.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a wee bit and they are in the early days of a relationship.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 147 days | text: User has been seeing Eilidh, a vet nurse at their practice, for a short time in a romantic relationship.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship_status | age: 513 days | text: User is single and has not dated since university.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 358 days | text: User is going to call Fiona at lunch to say something borderline emotional about her pregnancy.
````


### [h45-A3] frbank:diane:diane_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:diane:diane_q04:FULL|3cf1876c69c43346`
- question: Does Diane have any health conditions?
- gold (YAML `fact`): Osteoarthritis in both knees
- licensed (gold) records: lb_00063 [active] rank absent: "User has osteoarthritis in their knees" (entry passes detector: True); lb_00064 [active] rank absent: "User has osteoarthritis in both knees." (entry passes detector: True); lb_00065 [active] rank absent: "User's osteoarthritis in knees has been worsening over the last two years." (entry passes detector: True); lb_00071 [active] rank 5: "User has osteoarthritis in both knees that has been worsening over the past six to seven years, with significant decline in the last two years" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00071': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries do not mention anyone named Diane; they contain information about a user, but do not identify the user as Diane.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries do not mention anyone named Diane; they contain information about a user, but do not identify the user as Diane."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 503 days | text: User had a visit with a woman named Eleanor who is ninety-one years old and is dying well.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: colleague | age: 205 days | text: User has a close professional relationship with a nurse named Sandra from Four Seasons Compassion for Life.
[3] lifecycle: active | category: OBLIGATIONS | attribute: occupation_patient_relationship | age: 145 days | text: User is a caregiver or healthcare provider with patients who request her specifically
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 290 days | text: Margaret told me she had lived long enough to stop being afraid of anything except unkindness.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 440 days | text: User has osteoarthritis in both knees that has been worsening over the past six to seven years, with significant decline in the last two years
````


### [h45-A3] frbank:diane:diane_q05:FULL -- PRESENT, section expiring_logistics
- key: `frbank:diane:diane_q05:FULL|25a725c91f24c8d0`
- question: Does Diane have any upcoming events?
- gold (YAML `fact`): Greg's woodworking show at the Folk Art Center — July 12, 2026
- licensed (gold) records: lb_00398 [active] rank 5: "Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026." (entry passes detector: True); lb_00401 [active] rank 1: "Greg was accepted into the Folk Art Center summer show on July 12th, 2026" (entry passes detector: True); lb_00403 [active] rank 3: "Greg has been accepted into the Folk Art Center summer show on July 12th, 2026." (entry passes detector: True); lb_00407 [active] rank 2: "Greg has been accepted into the Folk Art Center summer show on July 12th." (entry passes detector: True); lb_00412 [active] rank absent: "User feels nervous about Greg's acceptance into the Folk Art Center summer show and hopes people will appreciate his work" (entry passes detector: True); lb_00416 [active] rank absent: "User's partner Greg will be building a rocking chair and other pieces in his workshop over the next six months." (entry passes detector: False)
- detector: gold_cov 0.1111; answer covers in-view entry text: {'lb_00398': 0.0769, 'lb_00401': 0.0833, 'lb_00403': 0.0833, 'lb_00407': 0.0909}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries in the memory store are about Greg, not Diane.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries in the memory store are about Greg, not Diane."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show on July 12th, 2026
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg has been accepted into the Folk Art Center summer show on July 12th, 2026.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: birthday | age: 16 days | text: Greg's birthday is on Saturday, March 14, 2026
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: relationship | age: 80 days | text: Greg was accepted into the Folk Art Center summer show in Asheville on July 12th, 2026.
````


### [h45-A3] frbank:fatima:fatima_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:CAT-ABLATED|8496763e2470a08b`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 2: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: `{"answer": "The store does not currently contain the answer."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
[5] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 317 days | text: User promised to attend Omar's school science fair on May 15th
````


### [h45-A3] frbank:fatima:fatima_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:fatima:fatima_q11:FULL|06a840f434c701e6`
- question: What is Fatima's educational background?
- gold (YAML `fact`): BFA from Central Saint Martins in London
- licensed (gold) records: lb_00083 [active] rank absent: "User did their BFA at Central Saint Martins in London twenty years ago." (entry passes detector: True); lb_00086 [active] rank 3: "User was mentored by Margaret Hale during their BFA at Central Saint Martins." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00086': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer to this question about Fatima's educational background.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer to this question about Fatima's educational background."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: city | age: 468 days | text: User lives in Riyadh and manages all transportation for her children, including driving Khalid to football practice three times a week.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: firm_affiliation | age: 367 days | text: User is associated with the Al-Faisal family firm
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: mentor | age: 418 days | text: User was mentored by Margaret Hale during their BFA at Central Saint Martins.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: project_manager | age: 439 days | text: User has a project manager named Nour who has been with them for eight months and trained at Dar Al-Hekma.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 32 days | text: User has a younger child named Habibi who wants to learn to paint with actual artist-grade acrylics on canvas.
````


### [h45-A3] frbank:jake:jake_q03:FULL -- PRESENT, section stable_identity
- key: `frbank:jake:jake_q03:FULL|0aa1c0c015b4b7a2`
- question: What does Jake's mom do?
- gold (YAML `fact`): Mom works at the Eire Pub in Dorchester — been waitressing there 20 years
- licensed (gold) records: lb_00047 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00051 [active] rank 3: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00054 [active] rank 2: "User's mom has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True); lb_00061 [active] rank absent: "User's mother has worked at the Eire Pub in Dorchester for about 20 years" (entry passes detector: True)
- detector: gold_cov 0.125; answer covers in-view entry text: {'lb_00051': 0.1429, 'lb_00054': 0.1429}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe the user's mom, not someone named Jake's mom.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe the user's mom, not someone named Jake's mom."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 106 days | text: User's mother is very involved and stressed about Bridget's wedding preparations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 455 days | text: User's mom has worked at the Eire Pub in Dorchester for about 20 years
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 43 days | text: User's mom is sentimental and cries at Hallmark commercials.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 455 days | text: User lives in Boston and Megan lives in Dorchester near user's mom's workplace
````


### [h45-A3] frbank:jake:jake_q12:FULL -- PRESENT, section stable_identity
- key: `frbank:jake:jake_q12:FULL|c5b8bbe4f14d9360`
- question: What's Jake's work situation?
- gold (YAML `fact`): Dad is a union electrician — runs Brennan & Sons Electric
- licensed (gold) records: lb_00010 [active] rank 1: "User works for his dad's company Brennan and Sons Electric." (entry passes detector: True); lb_00012 [active] rank absent: "User's dad has been a union electrician for about 30 years." (entry passes detector: True); lb_00013 [active] rank 4: "User has been apprenticing under his dad at Brennan and Sons Electric since he got out of high school." (entry passes detector: True); lb_00015 [active] rank 3: "User works for his dad's company Brennan and Sons Electric, where his dad has been a union electrician for about 30 years." (entry passes detector: True); lb_00016 [active] rank absent: "User has been apprenticing under his dad at Brennan and Sons Electric for almost 6 years." (entry passes detector: True); lb_00017 [active] rank 2: "User works with his dad's company Brennan and Sons Electric." (entry passes detector: True); lb_00018 [active] rank absent: "User's dad has been a union electrician for about 30 years." (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00010': 0.0, 'lb_00013': 0.0, 'lb_00015': 0.0, 'lb_00017': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a user's work situation but do not identify this user as 'Jake,' so I cannot confirm these entries describe Jake's work situation.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. The entries refer to a user's work situation but do not identify this user as 'Jake,' so I cannot confirm these entries describe Jake's work situation."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 483 days | text: User works for his dad's company Brennan and Sons Electric.
[2] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 483 days | text: User works with his dad's company Brennan and Sons Electric.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: employer | age: 483 days | text: User works for his dad's company Brennan and Sons Electric, where his dad has been a union electrician for about 30 years.
[4] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 483 days | text: User has been apprenticing under his dad at Brennan and Sons Electric since he got out of high school.
[5] lifecycle: active | category: OBLIGATIONS | attribute: job_type | age: 260 days | text: User works on job sites all day
````


### [h45-A3] frbank:kofi:kofi_q09:FULL -- PRESENT, section ambiguous
- key: `frbank:kofi:kofi_q09:FULL|1c59cb8e93531764`
- question: Is Kofi selling cocoa directly to the Belgian chocolate maker?
- gold (YAML `existing_fact`): Sells all cocoa through the cooperative buying agent system
- licensed (gold) records: lb_00008 [active] rank 3: "User sells cocoa through a cooperative system in their village." (entry passes detector: True); lb_00014 [superseded] rank 5: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag." (entry passes detector: True)
- detector: gold_cov 0.125; answer covers in-view entry text: {'lb_00008': 0.1667, 'lb_00014': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While there is an active entry indicating the user has a direct contact with a Belgian artisan chocolate buyer interested in purchasing 20-30 bags of cocoa per year, there is no entry that confirms whether an actual sale or direct selling arrangement with this buyer has been established.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While there is an active entry indicating the user has a direct contact with a Belgian artisan chocolate buyer interested in purchasing 20-30 bags of cocoa per year, there is no entry that confirms whether an actual sale or direct selling arrangement with this buyer has been established."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: contact | age: 122 days | text: User has a direct contact with a Belgian artisan chocolate buyer who wants to buy 20-30 bags of cocoa per year.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: business_activity | age: 419 days | text: User currently sells raw cocoa beans
[3] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 240 days | text: User led negotiations with Kuapa Kokoo along with 3 elders to secure a premium price for cocoa.
[5] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [h45-A3] frbank:marcus:marcus_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:marcus:marcus_q04:FULL|b2caf21c1a00de0a`
- question: What health conditions should be considered for Marcus?
- gold (YAML `fact`): Has Type 2 diabetes — manages with metformin and diet
- licensed (gold) records: lb_00031 [active] rank 4: "User takes metformin for type 2 diabetes" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00031': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe health conditions for the user, not for someone named Marcus.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries describe health conditions for the user, not for someone named Marcus."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes diagnosed a few years ago
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 531 days | text: User has type 2 diabetes.
[4] lifecycle: active | category: HEALTH_WELLBEING | attribute: medication | age: 531 days | text: User takes metformin for type 2 diabetes
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: employee | age: 272 days | text: User plans to have Carlos work up front with Jerome to improve customer interaction skills.
````


### [h45-A3] frbank:nadia:nadia_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:nadia:nadia_q04:FULL|97e46e376ed92a5f`
- question: What languages does Nadia speak?
- gold (YAML `fact`): Speaks three languages — Russian, French, English — but still dreams in Russian
- licensed (gold) records: lb_00044 [active] rank 4: "User speaks French, Russian, and English and switches between them frequently." (entry passes detector: True); lb_00045 [active] rank 2: "User speaks French, English, and Russian." (entry passes detector: True); lb_00049 [active] rank 1: "User speaks three languages: Russian, French, and English." (entry passes detector: True); lb_00062 [active] rank 3: "User speaks three languages: Russian, French, and English, but is fluent in all three and native in none." (entry passes detector: True)
- detector: gold_cov 0.2857; answer covers in-view entry text: {'lb_00044': 0.1429, 'lb_00045': 0.25, 'lb_00049': 0.3333, 'lb_00062': 0.2}; is_abstention True
- **answer**: The store does not currently contain the answer. While multiple entries describe languages the user speaks, the question asks specifically about 'Nadia,' and the store entries do not identify the user by that name, so I cannot confirm these entries apply to the person being asked about.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While multiple entries describe languages the user speaks, the question asks specifically about 'Nadia,' and the store entries do not identify the user by that name, so I cannot confirm these entries apply to the person being asked about."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks three languages: Russian, French, and English.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks French, English, and Russian.
[3] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks three languages: Russian, French, and English, but is fluent in all three and native in none.
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: languages_spoken | age: 474 days | text: User speaks French, Russian, and English and switches between them frequently.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: language_fluency | age: 474 days | text: User is fluent in Russian, French, and English but native in none.
````


### [h45-A3] frbank:pan:pan_q10:FULL -- PRESENT, section stable_identity
- key: `frbank:pan:pan_q10:FULL|6d60df716b296f2f`
- question: Who taught Pan her khao man gai recipe?
- gold (YAML `fact`): Mother taught her the khao man gai recipe — passed down through 3 generations from grandmother
- licensed (gold) records: lb_00026 [active] rank 4: "User's khao man gai recipe is a family treasure passed down through three generations." (entry passes detector: True)
- detector: gold_cov 0.3636; answer covers in-view entry text: {'lb_00026': 0.2727}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a user who learned khao man gai from their mother, but do not identify the user as 'Pan' or confirm that this user is the person being asked about.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries refer to a user who learned khao man gai from their mother, but do not identify the user as 'Pan' or confirm that this user is the person being asked about."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 468 days | text: User learned to cook khao man gai from their mother, who learned it from the user's grandmother.
[2] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: recipe_heritage | age: 170 days | text: User's khao man gai recipe has been passed down for three generations
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: cooking_method | age: 415 days | text: User cooks khao man gai on a charcoal stove as taught by their mother.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 468 days | text: User's khao man gai recipe is a family treasure passed down through three generations.
[5] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: family_recipe_sauce | age: 468 days | text: User's khao man gai sauce is a secret recipe from their grandmother that they cannot disclose but want others to know it is special.
````


### [h45-A3] frbank:raj:raj_q07:FULL -- PRESENT, section contradictions
- key: `frbank:raj:raj_q07:FULL|ca392bb4b60bb3ce`
- question: Does Raj work weekends?
- gold (YAML `new_fact`): Mentions working three Saturdays in a row because of emergency callouts
- licensed (gold) records: lb_00390 [active] rank absent: "User has been working emergency callouts on Saturdays for three consecutive weeks." (entry passes detector: True); lb_00393 [active] rank absent: "User has been working three consecutive Saturdays on emergency callouts." (entry passes detector: True); lb_00394 [active] rank absent: "Simran is someone close to the user who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00396 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays" (entry passes detector: True); lb_00399 [active] rank absent: "User has been doing emergency plumbing callouts on three consecutive Saturdays." (entry passes detector: True); lb_00400 [active] rank 2: "User's partner Simran is not happy about the user working three Saturdays in a row." (entry passes detector: True); lb_00403 [active] rank absent: "User has a partner named Simran who is not thrilled about the user working three Saturdays in a row." (entry passes detector: True); lb_00407 [active] rank absent: "User has been working three consecutive Saturdays on emergency plumbing callouts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00400': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. While multiple entries state that the user does not work weekends, the entries do not identify the user as 'Raj,' so I cannot confirm whether this information applies to someone by that name.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While multiple entries state that the user does not work weekends, the entries do not identify the user as 'Raj,' so I cannot confirm whether this information applies to someone by that name."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_feelings_about_work | age: 150 days | text: User's partner Simran is not happy about the user working three Saturdays in a row.
[3] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User does not work on weekends and prioritizes family time on Saturdays and Sundays.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 150 days | text: User's partner is named Simran and is not happy about the frequent Saturday work
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 429 days | text: User works Monday to Friday from 8 to 6 with emergency callouts on weekday evenings only, and does not work weekends.
````


### [h45-A3] frbank:saga:saga_q06:FULL -- PRESENT, section expiring_logistics
- key: `frbank:saga:saga_q06:FULL|84664519969f2865`
- question: Does Saga have any upcoming events?
- gold (YAML `fact`): Data conference talk in Copenhagen — August 8, 2026
- licensed (gold) records: lb_00306 [active] rank 2: "User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026" (entry passes detector: True); lb_00309 [active] rank absent: "User will present a talk on causal inference in recommendation systems at the Nordic Data Science Summit in Copenhagen on August 8, 2026." (entry passes detector: True); lb_00312 [active] rank 4: "User will present at the Nordic Data Science Summit in Copenhagen on August 8" (entry passes detector: True); lb_00315 [active] rank absent: "User has started preparing for the August conference by drafting 18 slides as of January." (entry passes detector: False)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00306': 0.0, 'lb_00312': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe that the user is an aunt to a newborn girl named Saga, but there is no information about any upcoming events for Saga herself.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries describe that the user is an aunt to a newborn girl named Saga, but there is no information about any upcoming events for Saga herself."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8, 2026
[3] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 389 days | text: User is responsible for giving a speech at Erik's wedding on August 23 in Gothenburg.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 121 days | text: User will present at the Nordic Data Science Summit in Copenhagen on August 8
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: project | age: 157 days | text: User plans to be near his brother Erik in Gothenburg from roughly October through December to be present for the newborn.
````


### [h45-A3] frbank:saga:saga_q11:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:CAT-ABLATED|174abf8cd8636faf`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 3: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00009': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer."}
```

The entries provided describe Saga as the user's newborn niece, but they do not contain information about Saga's siblings or brother.`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [h45-A3] frbank:saga:saga_q11:FULL -- PRESENT, section stable_identity
- key: `frbank:saga:saga_q11:FULL|587c999f85ed78c2`
- question: Who is Saga's brother?
- gold (YAML `fact`): Twin brother Erik is an architect in Gothenburg
- licensed (gold) records: lb_00009 [active] rank 4: "User has a twin brother named Erik" (entry passes detector: True); lb_00010 [active] rank absent: "User's twin brother Erik is an architect in Gothenburg" (entry passes detector: True); lb_00012 [active] rank absent: "User has a twin brother named Erik who is an architect in Gothenburg specializing in residential buildings" (entry passes detector: True); lb_00015 [active] rank absent: "User's twin brother Erik is practical and uncomfortable with sentimental gifts" (entry passes detector: True)
- detector: gold_cov 0.2; answer covers in-view entry text: {'lb_00009': 0.25}; is_abstention True
- **answer**: The store does not currently contain the answer. While the store indicates that Saga is the user's niece (newborn girl), it does not contain information about Saga's siblings or brother.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the store indicates that Saga is the user's niece (newborn girl), it does not contain information about Saga's siblings or brother."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 49 days | text: User is an aunt to a newborn girl named Saga.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 389 days | text: User's brother Erik is their twin brother.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 157 days | text: User has a twin brother named Erik
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 543 days | text: User has a twin brother named Erik
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 528 days | text: User has a twin brother named Erik.
````


### [h45-A3] frbank:thanh:thanh_q13:CAT-ABLATED -- PRESENT, section expiring_logistics
- key: `frbank:thanh:thanh_q13:CAT-ABLATED|24fc7028a5ba7661`
- question: Does Thanh have any upcoming family events?
- gold (YAML `fact`): Duc's wedding celebration — July 12, 2026
- licensed (gold) records: lb_00462 [active] rank absent: "User's son Duc is getting married on July 12, 2026" (entry passes detector: True); lb_00468 [active] rank 4: "User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides" (entry passes detector: False); lb_00469 [active] rank absent: "User is planning a wedding for their son Duc on July 12, 2026" (entry passes detector: True); lb_00470 [active] rank absent: "User estimates the wedding budget to be 45 million dong" (entry passes detector: False); lb_00472 [active] rank absent: "User's wedding is planned for July 12, 2026" (entry passes detector: True); lb_00474 [active] rank absent: "User is planning a wedding with about 150 guests" (entry passes detector: False); lb_00475 [active] rank absent: "User's wedding budget is approximately 45 million dong" (entry passes detector: False); lb_00476 [active] rank absent: "User's wedding menu will include shrimp, pork, chicken, duck, spring roll, soup, and rice in delta style" (entry passes detector: False)
- detector: gold_cov 0.3333; answer covers in-view entry text: {'lb_00468': 0.3636}; is_abstention True
- **answer**: The store does not currently contain the answer. While there is an entry about Duc's wedding with 150 expected guests, it does not specify whether this is an upcoming event or provide a date for it.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While there is an entry about Duc's wedding with 150 expected guests, it does not specify whether this is an upcoming event or provide a date for it."
}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 378 days | text: User lives in or near Can Tho city in Vietnam.
[2] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
[3] lifecycle: active | category: PREFERENCES_HABITS | attribute: preference | age: 312 days | text: User plans to bring about 9 kilograms of shrimp for the next Tet family dinner
[4] lifecycle: active | category: OBLIGATIONS | attribute: event_guest_count | age: 145 days | text: User expects about 150 guests at Duc's wedding, including family, neighbors, and friends from both sides
[5] lifecycle: active | category: PREFERENCES_HABITS | attribute: food_brought | age: 312 days | text: User brought about 6 kilograms of shrimp to the last Tet family dinner.
````


### [h45-A3] frbank:tom:tom_q04:FULL -- PRESENT, section stable_identity
- key: `frbank:tom:tom_q04:FULL|0595f1ca735118b0`
- question: Does Tom have any health conditions?
- gold (YAML `fact`): Has atrial fibrillation — takes warfarin (blood thinners)
- licensed (gold) records: lb_00045 [active] rank absent: "User takes warfarin as a blood thinner medication." (entry passes detector: True); lb_00046 [active] rank 3: "User has atrial fibrillation and takes warfarin as a blood thinner" (entry passes detector: True)
- detector: gold_cov 0.0; answer covers in-view entry text: {'lb_00046': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries describe health conditions for the user, but do not contain information about someone named Tom.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe health conditions for the user, but do not contain information about someone named Tom."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 183 days | text: User's friend Gerald has knee problems and can no longer manage the walk to the pub quiz.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation.
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: health_condition | age: 463 days | text: User has atrial fibrillation and takes warfarin as a blood thinner
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 413 days | text: User has been attending the pub quiz with Gerald for twelve or thirteen years.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: friend | age: 141 days | text: User knows a walking group member named Bernard who has a replacement hip and finds stiles challenging.
````


### [h45-A3] frbank:tom:tom_q08:FULL -- PRESENT, section ambiguous
- key: `frbank:tom:tom_q08:FULL|e2a4bb700ca93242`
- question: Where does Tom live?
- gold (YAML `existing_fact`): Lives alone in the village house he shared with Margaret
- licensed (gold) records: lb_00023 [active] rank absent: "User lives alone in a house they have occupied for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00027 [active] rank 4: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True); lb_00031 [active] rank 5: "User has lived in the same house for over thirty years, which was shared with Margaret." (entry passes detector: True)
- detector: gold_cov 0.1667; answer covers in-view entry text: {'lb_00027': 0.0, 'lb_00031': 0.0}; is_abstention True
- **answer**: The store does not currently contain the answer. While the entries indicate the user lives in the Cotswolds (in Gloucestershire), they do not confirm the user's name is Tom.
- raw[:400]: `{"answer": "The store does not currently contain the answer. While the entries indicate the user lives in the Cotswolds (in Gloucestershire), they do not confirm the user's name is Tom."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 197 days | text: User lives in the Cotswolds.
[2] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_region | age: 211 days | text: User lives in the Cotswolds
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 442 days | text: User lives in Gloucestershire
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 491 days | text: User has lived in the same house for over thirty years, which was shared with Margaret.
````


### [h45-A3] frbank:valentina:valentina_q07:CAT-ABLATED -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:CAT-ABLATED|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.2857; answer covers in-view entry text: {'lb_00036': 0.375}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a user with a partner named Lucía, but do not identify the user as Valentina.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries refer to a user with a partner named Lucía, but do not identify the user as Valentina."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [h45-A3] frbank:valentina:valentina_q07:FULL -- PRESENT, section stable_identity
- key: `frbank:valentina:valentina_q07:FULL|6107ff7f202cacd2`
- question: Who is Valentina's partner?
- gold (YAML `fact`): Partner Lucía is a human rights lawyer at a Bogotá NGO
- licensed (gold) records: lb_00035 [active] rank absent: "User's partner Lucía is a human rights lawyer with more demanding work hours than the user" (entry passes detector: True); lb_00036 [active] rank 5: "User's partner is named Lucía and is a human rights lawyer with demanding hours." (entry passes detector: True); lb_00041 [active] rank absent: "User has a partner named Lucía who is a human rights lawyer with demanding and unpredictable work hours." (entry passes detector: True)
- detector: gold_cov 0.2857; answer covers in-view entry text: {'lb_00036': 0.375}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a user's partner named Lucía, but there is no information in the store identifying the user as 'Valentina'.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries refer to a user's partner named Lucía, but there is no information in the store identifying the user as 'Valentina'."}
````
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 453 days | text: User has a partner named Lucía who made Valentine's Day dinner reservations.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User has a partner named Lucía
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 202 days | text: User's partner is Lucía
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner_name | age: 453 days | text: User's partner is named Lucía.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 521 days | text: User's partner is named Lucía and is a human rights lawyer with demanding hours.
````


### [h45-A3] frbank:zara:zara_q05:FULL -- PRESENT, section stable_identity
- key: `frbank:zara:zara_q05:FULL|3416758f4e29193f`
- question: Where is Zara's grandmother?
- gold (YAML `fact`): Grandmother Haboba Zahra lives in Khartoum — they've never met in person
- licensed (gold) records: lb_00033 [active] rank 3: "User has a grandmother named Haboba Zahra who is 82 years old and lives in Khartoum, Sudan" (entry passes detector: True); lb_00036 [active] rank 4: "User's grandmother, Haboba Zahra, is 82 years old and lives in Khartoum." (entry passes detector: True); lb_00042 [active] rank 2: "User's grandmother Haboba Zahra is 82 years old and lives in Khartoum in a relatively quiet neighborhood." (entry passes detector: True); lb_00043 [active] rank absent: "User has never met their grandmother Haboba Zahra in person due to visa issues and the war in Sudan." (entry passes detector: True); lb_00047 [active] rank absent: "User has never met their grandmother Haboba Zahra in person and has never been to Sudan." (entry passes detector: True)
- detector: gold_cov 0.3333; answer covers in-view entry text: {'lb_00033': 0.3636, 'lb_00036': 0.375, 'lb_00042': 0.2727}; is_abstention True
- **answer**: The store does not currently contain the answer. The entries refer to a grandmother named 'Haboba Zahra,' not 'Zara,' so this question does not match the user's stored information.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries refer to a grandmother named 'Haboba Zahra,' not 'Zara,' so this question does not match the user's stored information."}`
- auto_label: abstained
- label: (step4_labels.json)

view (ORACLE = ALWAYS):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother is named Haboba Zahra and is 82 years old.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother Haboba Zahra is 82 years old and lives in Khartoum in a relatively quiet neighborhood.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User has a grandmother named Haboba Zahra who is 82 years old and lives in Khartoum, Sudan
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother, Haboba Zahra, is 82 years old and lives in Khartoum.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 527 days | text: User's grandmother, Haboba Zahra, is 82 years old.
````

