# Step 4 -- answers the detector marked stale under ORACLE (registered stale_use_tau_gold)

Lanes: mini-D4 (gpt-4.1-mini, D.4 prompt), h45-D4 (Haiku 4.5, D.4 prompt); appendix: the A3-prompt lanes. Expiry rows are UNSCORABLE (gold field is the expired fact) and excluded from the classification counts.

## mini-D4 (gpt-4.1-mini, prompt D4)

17 answers flagged (1 expiry, unscorable).

### [mini-D4] frbank:bruna:bruna_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:FULL|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago.
- raw[:400]: `{"answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [mini-D4] frbank:bruna:bruna_q06:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:SLOT-ABLATED|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago.
- raw[:400]: `{"answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a dry needling certification course a couple of months ago."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [mini-D4] frbank:dariush:dariush_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:dariush:dariush_q04:SLOT-ABLATED|d67c2ca9d3628556`
- question: Is Dariush opening a second practice in La Jolla?
- gold (YAML `retraction`): La Jolla second practice is off the table — too much overhead
- stale (YAML `original_fact`): Planning to open a second practice location in La Jolla
- licensed (forbidding) records: lb_00149 [active] rank 1: "User is considering opening a second practice location in La Jolla"; lb_00159 [active] rank 3: "User is a periodontist with a current practice and is considering opening a second practice location in La Jolla."; lb_00162 [active] rank 4: "User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street."
- detector: stale_cov 0.6667, stale_use(0.80) False, successor_cov 0.0, do∩A ['open', 'planning'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Dariush is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.
- raw[:400]: `{"answer": "Yes, Dariush is planning to open a second periodontal surgical suite in La Jolla on Prospect Street."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is considering opening a second practice location in La Jolla
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 386 days | text: User currently splits time between two practice locations, spending three days at the original location and two days at the La Jolla location.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is a periodontist with a current practice and is considering opening a second practice location in La Jolla.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User plans to host a reception for La Jolla dentists to build referral relationships before opening the new location.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 504 days | text: User uses the LANAP protocol with the Periolase MVP-7 laser for periodontal therapy
````


### [mini-D4] frbank:fatima:fatima_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:fatima:fatima_q06:FULL|d17a217596fb18b8`
- question: Is Fatima launching any new products or brands?
- gold (YAML `retraction`): Fragrance line cancelled — too much distraction from core business
- stale (YAML `original_fact`): Planning to launch a home fragrance line — Oud & Geometry
- licensed (forbidding) records: lb_00176 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00180 [active] rank 3: "User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm."; lb_00182 [active] rank absent: "User's home fragrance line will launch with four scents inspired by spatial archetypes: courtyard, library, hammam, and rooftop at night."; lb_00183 [active] rank 2: "User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand."; lb_00186 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00189 [active] rank absent: "User is launching a fragrance line called Oud & Geometry with four initial scents inspired by spatial archetypes."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.2, do∩A ['geometry', 'home', 'oud'], dn∩A ['business'], (do∩A)⊆question False, phrase None
- **answer**: Yes, Fatima is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of her design brand, which involves building a second business with its own supply chain, regulatory compliance, and distribution network.
- raw[:400]: `{"answer": "Yes, Fatima is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of her design brand, which involves building a second business with its own supply chain, regulatory compliance, and distribution network."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: business_extension | age: 342 days | text: User is considering extending their firm into home fragrance products.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm.
[4] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: project_cost | age: 264 days | text: User spent approximately forty thousand riyals on initial fragrance development and packaging concepts for the fragrance line.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regulatory compliance, and distribution network.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 405 days | text: User's firm works exclusively in high-end residential design, focusing on villas, penthouses, private residences, and occasionally family compounds.
[7] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 367 days | text: User is preparing a presentation for the Al-Faisal family on March 5th, 2025.
[8] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided not to launch a home fragrance line called Oud and Geometry because it would require a level of investment and attention that would compete with their core interior design work.
````


### [mini-D4] frbank:ingrid:ingrid_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:ingrid:ingrid_q01:SLOT-ABLATED|f0a292a92f80ae35`
- question: What is Ingrid's primary research focus?
- gold (YAML `new_fact`): Shifted research focus to kelp farming as climate adaptation strategy
- stale (YAML `old_fact`): Primary research focus is Arctic cod population dynamics
- licensed (forbidding) records: lb_00005 [superseded] rank 6: "User is involved in a population dynamics model for Arctic cod (Boreogadus saida)"; lb_00007 [superseded] rank 7: "User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics"; lb_00018 [superseded] rank 8: "User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea"; lb_00019 [superseded] rank 9: "User plans to continue sampling Arctic cod population dynamics for three more years"; lb_00024 [superseded] rank 10: "User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme."; lb_00026 [superseded] rank 11: "User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['arctic', 'cod', 'primary'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Ingrid's primary research focus is long-term monitoring of Arctic cod stock decline in the Barents Sea.
- raw[:400]: `{"answer": "Ingrid's primary research focus is long-term monitoring of Arctic cod stock decline in the Barents Sea."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: INTELLECTUAL_INTERESTS | attribute: research_focus | age: 327 days | text: User's previous primary research focus was Arctic cod population dynamics.
[2] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: research_interest | age: 175 days | text: User's primary research interest includes kelp aquaculture and nearshore habitat monitoring
[3] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: research_focus | age: 327 days | text: User's previous primary research focus was long-term monitoring of Arctic cod stock decline in the Barents Sea
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: research_location | age: 22 days | text: User conducts research at coastal field sites in the Arctic.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: education | age: 489 days | text: User completed a PhD at Bergen on cod biology focusing on larval mortality across thermal gradients
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 432 days | text: User has a grant proposal due to the Research Council on February 15, 2025
[13] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [mini-D4] frbank:ingrid:ingrid_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:ingrid:ingrid_q04:SLOT-ABLATED|98db10edf7a2894b`
- question: Is Ingrid planning a sabbatical?
- gold (YAML `retraction`): Sabbatical at Woods Hole is off the table — kelp project cannot be left
- stale (YAML `original_fact`): Planning a sabbatical year at Woods Hole Oceanographic Institution in Massachusetts
- licensed (forbidding) records: lb_00076 [active] rank absent: "User is planning to spend 2026 at Woods Hole Oceanographic Institution in the ocean acidification laboratory."; lb_00078 [active] rank 1: "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026"; lb_00085 [active] rank absent: "User plans to formalize the invitation for a Guest Investigator appointment at Woods Hole Oceanographic Institution by March 2025."; lb_00086 [active] rank 5: "User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['institution', 'oceanographic', 'planning'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, but the sabbatical at Woods Hole is cancelled; however, the user plans to be a Guest Investigator at Woods Hole from August 2026 through July 2027.
- raw[:400]: `{"answer": "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, but the sabbatical at Woods Hole is cancelled; however, the user plans to be a Guest Investigator at Woods Hole from August 2026 through July 2027."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026
[2] lifecycle: active | category: OBLIGATIONS | attribute: relationship | age: 466 days | text: User's department head is supportive in principle of the sabbatical
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User was invited to spend a sabbatical year at Woods Hole Oceanographic Institution
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User's sabbatical at Woods Hole is cancelled
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 432 days | text: User has a grant proposal due to the Research Council on February 15, 2025
[13] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [mini-D4] frbank:jake:jake_q11:FULL -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:jake:jake_q11:FULL|131f342b26ed61a3`
- question: Does Jake have any exams or certifications coming up?
- gold (YAML `fact`): Journeyman exam scheduled for March 8, 2025
- stale (YAML `fact (expiry: = gold)`): Journeyman exam scheduled for March 8, 2025
- licensed (forbidding) records: lb_00104 [expired] rank 1: "User has a journeyman electrician exam on March 8, 2025"; lb_00112 [expired] rank 3: "User is preparing for the NEC journeyman exam scheduled for March 8, 2025"
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov None
- **answer**: Jake has already passed the journeyman electrician exam last year and currently has no upcoming exams scheduled.
- raw[:400]: `{"answer": "Jake has already passed the journeyman electrician exam last year and currently has no upcoming exams scheduled."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: OBLIGATIONS | attribute: exam_date | age: 379 days | text: User has a journeyman electrician exam on March 8, 2025
[2] lifecycle: active | category: OBLIGATIONS | attribute: certification | age: 1 days | text: User passed the journeyman electrician exam last year.
[3] lifecycle: expired | category: OBLIGATIONS | attribute: exam_date | age: 379 days | text: User is preparing for the NEC journeyman exam scheduled for March 8, 2025
[4] lifecycle: expired | category: OBLIGATIONS | attribute: certification | age: 274 days | text: User passed the journeyman electrician exam in March 2025
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 379 days | text: User works every day while preparing for the exam
````


### [mini-D4] frbank:kofi:kofi_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kofi:kofi_q01:FULL|859bafc244b8d70e`
- question: Who does Kofi's cooperative sell cocoa through?
- gold (YAML `new_fact`): Switched to Kuapa Kokoo buying agent — better price and fair trade premium
- stale (YAML `old_fact`): Cooperative sells through Akuafo Buying Agent — 3-year contract
- licensed (forbidding) records: lb_00014 [superseded] rank 6: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.125, do∩A ['cooperative', 'sells', 'through'], dn∩A ['kuapa'], (do∩A)⊆question False, phrase None
- **answer**: Kofi's cooperative sells cocoa through Kuapa.
- raw[:400]: `{"answer": "Kofi's cooperative sells cocoa through Kuapa."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[3] lifecycle: active | category: OBLIGATIONS | attribute: role | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[4] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[5] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[6] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [mini-D4] frbank:kofi:kofi_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kofi:kofi_q01:SLOT-ABLATED|859bafc244b8d70e`
- question: Who does Kofi's cooperative sell cocoa through?
- gold (YAML `new_fact`): Switched to Kuapa Kokoo buying agent — better price and fair trade premium
- stale (YAML `old_fact`): Cooperative sells through Akuafo Buying Agent — 3-year contract
- licensed (forbidding) records: lb_00014 [superseded] rank 6: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.125, do∩A ['cooperative', 'sells', 'through'], dn∩A ['kuapa'], (do∩A)⊆question False, phrase None
- **answer**: Kofi's cooperative sells cocoa through Kuapa.
- raw[:400]: `{"answer": "Kofi's cooperative sells cocoa through Kuapa."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[3] lifecycle: active | category: OBLIGATIONS | attribute: role | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[4] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[5] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[6] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [mini-D4] frbank:mirri:mirri_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:FULL|28988d92b56155aa`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'east', 'river'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: User does patrol work in Kakadu, focusing on the East Alligator River corridor.
- raw[:400]: `{"answer": "User does patrol work in Kakadu, focusing on the East Alligator River corridor."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu, focusing on the East Alligator River corridor.
[4] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[5] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [mini-D4] frbank:mirri:mirri_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:SLOT-ABLATED|2ae3f399928196d9`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.625, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'days', 'east', 'patrols'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: User patrols alone most days on the East Alligator corridor.
- raw[:400]: `{"answer": "User patrols alone most days on the East Alligator corridor."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[3] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[4] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 187 days | text: User works in a patrol sector and has work obligations
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_patrol_pattern | age: 509 days | text: User patrols alone most days on the East Alligator corridor.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [mini-D4] frbank:mirri:mirri_q04:FULL -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:FULL|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: `{"answer": "Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [mini-D4] frbank:mirri:mirri_q04:SLOT-ABLATED -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:SLOT-ABLATED|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: `{"answer": "Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [mini-D4] frbank:pan:pan_q01:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:pan:pan_q01:CAT-ABLATED|f436fcbaccfffbff`
- question: Where does Pan buy her rice?
- gold (YAML `new_fact`): Switched rice supplier to Uncle Prasert at Talat Thai wholesale — 32 baht per kilo, better quality
- stale (YAML `old_fact`): Buys jasmine rice from Auntie Somjit at Khlong Toei market — 38 baht per kilo
- licensed (forbidding) records: lb_00017 [superseded] rank 1: "User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai."
- detector: stale_cov 0.75, stale_use(0.80) False, successor_cov 0.0, do∩A ['auntie', 'buys', 'khlong', 'market', 'somjit', 'toei'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Pan buys her rice from Auntie Somjit at Khlong Toei market.
- raw[:400]: `{"answer": "Pan buys her rice from Auntie Somjit at Khlong Toei market."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai.
[2] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_purchase_habit | age: 481 days | text: User buys 15 kilos of rice every morning from Auntie Somjit at Khlong Toei market.
[3] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 481 days | text: User buys rice at 38 baht per kilo.
[4] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User uses Auntie Somjit's jasmine long grain rice at 38 baht per kilo for their khao man gai.
[5] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 242 days | text: User pays 32 baht per kilo for jasmine rice.
````


### [mini-D4] frbank:tom:tom_q06:FULL -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:tom:tom_q06:FULL|20e59418eb9ecbe3`
- question: Is Tom planning any building projects?
- gold (YAML `retraction`): Barn conversion scrapped — too expensive and planning permission denied
- stale (YAML `original_fact`): Planning to convert the old barn into a honey processing room
- licensed (forbidding) records: lb_00143 [active] rank absent: "User is considering converting the barn into a dedicated honey processing space with proper extraction equipment, bottling line, and temperature control"; lb_00148 [retracted] rank 9: "User has an old stone barn at the back of their property that they plan to convert into a dedicated honey processing space."; lb_00151 [active] rank absent: "User has been considering converting the barn into a dedicated honey processing space."; lb_00160 [active] rank absent: "User plans to convert the barn into a dedicated honey processing space with proper equipment and hopes to have it settled before summer to use by autumn extraction."; lb_00163 [retracted] rank 10: "User is planning to convert a barn into a honey processing room in the Cotswolds Area of Outstanding Natural Beauty"
- detector: stale_cov 0.6667, stale_use(0.80) False, successor_cov 0.0, do∩A ['convert', 'honey', 'into', 'processing'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: Tom had plans to convert a barn into a honey processing space, but the project was cancelled due to planning refusal and high cost.
- raw[:400]: `{"answer": "Tom had plans to convert a barn into a honey processing space, but the project was cancelled due to planning refusal and high cost."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User had architectural drawings made by a local architect for the barn conversion project.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User plans to hire a local professional for roof repairs, plumbing, and electrics for the barn conversion.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User had grand plans to convert the barn into a honey extraction room, bottling area, and small shop front.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User's hobby project to convert the barn was cancelled due to planning refusal and high cost.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User was planning to convert the barn into a honey processing space but has now cancelled the project.
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 379 days | text: User plans the first full inspection of bee colonies on March 22nd.
[7] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 379 days | text: User plans the first full inspection of bee colonies around March 22nd annually.
[8] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 379 days | text: User plans to conduct the first proper inspection of their bee colonies around March 22nd, 2025.
[9] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User has an old stone barn at the back of their property that they plan to convert into a dedicated honey processing space.
[10] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User is planning to convert a barn into a honey processing room in the Cotswolds Area of Outstanding Natural Beauty
````


### [mini-D4] frbank:tom:tom_q06:SLOT-ABLATED -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:tom:tom_q06:SLOT-ABLATED|6e84158b43622d95`
- question: Is Tom planning any building projects?
- gold (YAML `retraction`): Barn conversion scrapped — too expensive and planning permission denied
- stale (YAML `original_fact`): Planning to convert the old barn into a honey processing room
- licensed (forbidding) records: lb_00143 [active] rank absent: "User is considering converting the barn into a dedicated honey processing space with proper extraction equipment, bottling line, and temperature control"; lb_00148 [retracted] rank 9: "User has an old stone barn at the back of their property that they plan to convert into a dedicated honey processing space."; lb_00151 [active] rank absent: "User has been considering converting the barn into a dedicated honey processing space."; lb_00160 [active] rank absent: "User plans to convert the barn into a dedicated honey processing space with proper equipment and hopes to have it settled before summer to use by autumn extraction."; lb_00163 [retracted] rank 10: "User is planning to convert a barn into a honey processing room in the Cotswolds Area of Outstanding Natural Beauty"
- detector: stale_cov 0.6667, stale_use(0.80) False, successor_cov 0.2, do∩A ['convert', 'honey', 'into', 'processing'], dn∩A ['conversion'], (do∩A)⊆question False, phrase 'but'
- **answer**: Tom had plans to convert a barn into a honey processing space and to hire professionals for roof repairs, plumbing, and electrics for the barn conversion, but the barn conversion project was cancelled due to planning refusal and high cost.
- raw[:400]: `{"answer": "Tom had plans to convert a barn into a honey processing space and to hire professionals for roof repairs, plumbing, and electrics for the barn conversion, but the barn conversion project was cancelled due to planning refusal and high cost."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User had architectural drawings made by a local architect for the barn conversion project.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User plans to hire a local professional for roof repairs, plumbing, and electrics for the barn conversion.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User's hobby project to convert the barn was cancelled due to planning refusal and high cost.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User was planning to convert the barn into a honey processing space but has now cancelled the project.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 113 days | text: User worked with Patricia Okonkwo as project manager on the Birmingham bypass.
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 379 days | text: User plans the first full inspection of bee colonies on March 22nd.
[7] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 379 days | text: User plans the first full inspection of bee colonies around March 22nd annually.
[8] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 379 days | text: User plans to conduct the first proper inspection of their bee colonies around March 22nd, 2025.
[9] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User has an old stone barn at the back of their property that they plan to convert into a dedicated honey processing space.
[10] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User is planning to convert a barn into a honey processing room in the Cotswolds Area of Outstanding Natural Beauty
````


### [mini-D4] frbank:valentina:valentina_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:valentina:valentina_q04:SLOT-ABLATED|c975e15427a8fbe2`
- question: Is Valentina writing a book?
- gold (YAML `retraction`): Book project scrapped — her father asked her not to write it
- stale (YAML `original_fact`): Planning to write a book about her father's generation of Colombian journalists
- licensed (forbidding) records: lb_00115 [active] rank 2: "User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences."; lb_00117 [active] rank 3: "User is working on a book about the generation of Colombian journalists who reported during the narco years and the war."; lb_00120 [active] rank 4: "User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['generation', 'journalists'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Valentina is writing a book about the generation of journalists who reported on the narco years and the war, including her own father.
- raw[:400]: `{"answer": "Yes, Valentina is writing a book about the generation of journalists who reported on the narco years and the war, including her own father."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is interested in writing a book about the generation of journalists who reported on the narco years and the war in Colombia.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is working on a book about the generation of Colombian journalists who reported during the narco years and the war.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: reading_list_order | age: 55 days | text: User is ordering books by Luiselli and Janet Malcolm
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 453 days | text: User is preparing for an important investigative meeting on February 14, 2025.
````


## h45-D4 (claude-haiku-4-5-20251001, prompt D4)

27 answers flagged (8 expiry, unscorable).

### [h45-D4] frbank:aisha:aisha_q02:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:aisha:aisha_q02:SLOT-ABLATED|87b671f9e3b6617f`
- question: Which gym does Aisha go to?
- gold (YAML `new_fact`): Switched to a women-only gym in Rusholme — more comfortable
- stale (YAML `old_fact`): Goes to PureGym near Piccadilly — 3x a week
- licensed (forbidding) records: lb_00131 [superseded] rank 6: "User goes to PureGym near Piccadilly, which is a 24-hour gym about a 10-minute walk from their office."; lb_00139 [superseded] rank 7: "User goes to PureGym near Piccadilly, which is a 24-hour gym about 10 minutes from their office."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.3333, do∩A ['near', 'piccadilly', 'puregym'], dn∩A ['gym', 'only'], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. The entries that specify a gym location (PureGym near Piccadilly) are marked as superseded, and the active entries only indicate that the user has recently changed gyms without naming the current gym.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries that specify a gym location (PureGym near Piccadilly) are marked as superseded, and the active entries only indicate that the user has recently changed gyms without naming the current gym."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User has recently changed gyms.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User goes to the gym 3 or 4 times a week, usually after work
[3] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 175 days | text: User does a mix of cardio and some weights at the gym
[4] lifecycle: active | category: HOBBIES_RECREATION | attribute: hobby | age: 175 days | text: User is getting into weight training at the gym.
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: exercise_routine | age: 484 days | text: User aims to go to the gym three times a week.
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 484 days | text: User goes to PureGym near Piccadilly, which is a 24-hour gym about a 10-minute walk from their office.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: gym_location | age: 484 days | text: User goes to PureGym near Piccadilly, which is a 24-hour gym about 10 minutes from their office.
````


### [h45-D4] frbank:bruna:bruna_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:FULL|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025. Additionally, she is considering the credential recognition process for her physical therapy qualifications in Portugal.
- raw[:400]: ````json
{
  "answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025. Additionally, she is considering the credential recognition process for her physical therapy qualifications in Portugal."
}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [h45-D4] frbank:bruna:bruna_q06:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:SLOT-ABLATED|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.
- raw[:400]: ````json
{
  "answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025."
}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [h45-D4] frbank:dariush:dariush_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:dariush:dariush_q04:SLOT-ABLATED|d67c2ca9d3628556`
- question: Is Dariush opening a second practice in La Jolla?
- gold (YAML `retraction`): La Jolla second practice is off the table — too much overhead
- stale (YAML `original_fact`): Planning to open a second practice location in La Jolla
- licensed (forbidding) records: lb_00149 [active] rank 1: "User is considering opening a second practice location in La Jolla"; lb_00159 [active] rank 3: "User is a periodontist with a current practice and is considering opening a second practice location in La Jolla."; lb_00162 [active] rank 4: "User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street."
- detector: stale_cov 1.0, stale_use(0.80) True, successor_cov 0.0, do∩A ['location', 'open', 'planning'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, according to the memory store, the user is planning to open a second periodontal surgical suite in La Jolla on Prospect Street and is currently splitting time between two practice locations, spending three days at the original location and two days at the La Jolla location.
- raw[:400]: ````json
{"answer": "Yes, according to the memory store, the user is planning to open a second periodontal surgical suite in La Jolla on Prospect Street and is currently splitting time between two practice locations, spending three days at the original location and two days at the La Jolla location."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is considering opening a second practice location in La Jolla
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 386 days | text: User currently splits time between two practice locations, spending three days at the original location and two days at the La Jolla location.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is a periodontist with a current practice and is considering opening a second practice location in La Jolla.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User plans to host a reception for La Jolla dentists to build referral relationships before opening the new location.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 504 days | text: User uses the LANAP protocol with the Periolase MVP-7 laser for periodontal therapy
````


### [h45-D4] frbank:david:david_q06:CAT-ABLATED -- state exp (UNSCORABLE: expiry), tagged_reach False, successor_in_view False
- key: `frbank:david:david_q06:CAT-ABLATED|c65c804ae433b38e`
- question: Does David have any upcoming exams to prepare students for?
- gold (YAML `fact`): AP Euro exam May 8 — students need to be ready
- stale (YAML `fact (expiry: = gold)`): AP Euro exam May 8 — students need to be ready
- licensed (forbidding) records: lb_00171 [active] rank 2: "User has an AP European History exam on May 8."; lb_00172 [active] rank 1: "User has a major exam for AP European History scheduled on May 8."; lb_00173 [active] rank absent: "User's AP European History exam is on May 8, 2025"; lb_00175 [active] rank absent: "User's AP European History exam is on May 8."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their plans for a mock exam, but do not indicate whether the user is preparing students for any exams.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their plans for a mock exam, but do not indicate whether the user is preparing students for any exams."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 364 days | text: User has a major exam for AP European History scheduled on May 8.
[2] lifecycle: active | category: OBLIGATIONS | attribute: exam_date | age: 364 days | text: User has an AP European History exam on May 8.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User plans to run a full mock AP European History exam in the last week of April
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User is considering running a full mock AP European History exam during the last week of April.
[5] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 215 days | text: User is considering taking over the AP US History sections next year.
````


### [h45-D4] frbank:david:david_q06:FULL -- state exp (UNSCORABLE: expiry), tagged_reach False, successor_in_view False
- key: `frbank:david:david_q06:FULL|3277b5b20f7f6e86`
- question: Does David have any upcoming exams to prepare students for?
- gold (YAML `fact`): AP Euro exam May 8 — students need to be ready
- stale (YAML `fact (expiry: = gold)`): AP Euro exam May 8 — students need to be ready
- licensed (forbidding) records: lb_00171 [active] rank 3: "User has an AP European History exam on May 8."; lb_00172 [active] rank 1: "User has a major exam for AP European History scheduled on May 8."; lb_00173 [active] rank absent: "User's AP European History exam is on May 8, 2025"; lb_00175 [active] rank absent: "User's AP European History exam is on May 8."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their plan to run a mock exam, but do not indicate whether the user is preparing students for any exams.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their plan to run a mock exam, but do not indicate whether the user is preparing students for any exams."}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 364 days | text: User has a major exam for AP European History scheduled on May 8.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: exam_season_anxiety | age: 364 days | text: User feels anxious about exam season despite extensive experience
[3] lifecycle: active | category: OBLIGATIONS | attribute: exam_date | age: 364 days | text: User has an AP European History exam on May 8.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User plans to run a full mock AP European History exam in the last week of April
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User is considering running a full mock AP European History exam during the last week of April.
````


### [h45-D4] frbank:elena:elena_q01:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:elena:elena_q01:CAT-ABLATED|20a14635103a2dba`
- question: Where does Elena work?
- gold (YAML `new_fact`): Transferred to Rush University Medical Center — better hours and pay
- stale (YAML `old_fact`): Works at Lurie Children's Hospital
- licensed (forbidding) records: lb_00008 [superseded] rank 6: "User works night shifts at Lurie Children's hospital."; lb_00015 [superseded] rank 7: "User works night shifts at Lurie Children's hospital and has been on this schedule for about 8 months."
- detector: stale_cov 1.0, stale_use(0.80) True, successor_cov 0.0, do∩A ['children', 'hospital', 'lurie', 'works'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While active entries indicate Elena is a pediatric nurse who works night shifts at a hospital with 12-hour shifts, the specific employer information (Lurie Children's hospital) has been superseded and is no longer the current record.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While active entries indicate Elena is a pediatric nurse who works night shifts at a hospital with 12-hour shifts, the specific employer information (Lurie Children's hospital) has been superseded and is no longer the current record."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: identity_nickname | age: 113 days | text: User identifies as Elena from the west side and has a background of playing nurse with stuffed animals.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_role | age: 381 days | text: User works on a nursing unit with day and night shifts
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_shift | age: 71 days | text: User works night shifts at a hospital
[4] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 423 days | text: User is a pediatric nurse who works shifts helping children.
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_shift_length | age: 113 days | text: User works 12-hour shifts
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: job_employer | age: 484 days | text: User works night shifts at Lurie Children's hospital.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: job_night_shift_duration | age: 484 days | text: User works night shifts at Lurie Children's hospital and has been on this schedule for about 8 months.
````


### [h45-D4] frbank:elena:elena_q05:CAT-ABLATED -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:elena:elena_q05:CAT-ABLATED|0e2f57e75bdc4d34`
- question: Does Elena have any upcoming exams or certifications?
- gold (YAML `fact`): NCLEX-RN recertification exam March 20
- stale (YAML `fact (expiry: = gold)`): NCLEX-RN recertification exam March 20
- licensed (forbidding) records: lb_00213 [expired] rank 4: "User had to recertify their NCLEX on March 20, 2025"; lb_00214 [expired] rank 3: "User passed the NCLEX recertification exam on March 20, 2025"; lb_00219 [expired] rank 2: "User's NCLEX recertification exam was on March 20, 2025"
- detector: stale_cov 0.8333, stale_use(0.80) True, successor_cov None
- **answer**: The store does not currently contain information about any upcoming exams or certifications. The only exam-related entries are either expired (the March 20, 2025 NCLEX recertification) or describe a recently passed exam without specifying future obligations.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain information about any upcoming exams or certifications. The only exam-related entries are either expired (the March 20, 2025 NCLEX recertification) or describe a recently passed exam without specifying future obligations."
}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: identity_nickname | age: 113 days | text: User identifies as Elena from the west side and has a background of playing nurse with stuffed animals.
[2] lifecycle: expired | category: OBLIGATIONS | attribute: professional_obligation | age: 337 days | text: User's NCLEX recertification exam was on March 20, 2025
[3] lifecycle: expired | category: OBLIGATIONS | attribute: certification_status | age: 337 days | text: User passed the NCLEX recertification exam on March 20, 2025
[4] lifecycle: expired | category: OBLIGATIONS | attribute: professional_certification | age: 337 days | text: User had to recertify their NCLEX on March 20, 2025
[5] lifecycle: active | category: OBLIGATIONS | attribute: professional_exam_status | age: 337 days | text: User recently passed a professional exam requiring pharmacology and pediatrics knowledge
````


### [h45-D4] frbank:elena:elena_q05:FULL -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:elena:elena_q05:FULL|0e2f57e75bdc4d34`
- question: Does Elena have any upcoming exams or certifications?
- gold (YAML `fact`): NCLEX-RN recertification exam March 20
- stale (YAML `fact (expiry: = gold)`): NCLEX-RN recertification exam March 20
- licensed (forbidding) records: lb_00213 [expired] rank 4: "User had to recertify their NCLEX on March 20, 2025"; lb_00214 [expired] rank 3: "User passed the NCLEX recertification exam on March 20, 2025"; lb_00219 [expired] rank 2: "User's NCLEX recertification exam was on March 20, 2025"
- detector: stale_cov 0.8333, stale_use(0.80) True, successor_cov None
- **answer**: The store does not currently contain information about any upcoming exams or certifications. The only exam-related entries are either expired (the March 20, 2025 NCLEX recertification) or describe a recently passed exam without specifying future obligations.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain information about any upcoming exams or certifications. The only exam-related entries are either expired (the March 20, 2025 NCLEX recertification) or describe a recently passed exam without specifying future obligations."
}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: identity_nickname | age: 113 days | text: User identifies as Elena from the west side and has a background of playing nurse with stuffed animals.
[2] lifecycle: expired | category: OBLIGATIONS | attribute: professional_obligation | age: 337 days | text: User's NCLEX recertification exam was on March 20, 2025
[3] lifecycle: expired | category: OBLIGATIONS | attribute: certification_status | age: 337 days | text: User passed the NCLEX recertification exam on March 20, 2025
[4] lifecycle: expired | category: OBLIGATIONS | attribute: professional_certification | age: 337 days | text: User had to recertify their NCLEX on March 20, 2025
[5] lifecycle: active | category: OBLIGATIONS | attribute: professional_exam_status | age: 337 days | text: User recently passed a professional exam requiring pharmacology and pediatrics knowledge
````


### [h45-D4] frbank:fatima:fatima_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:fatima:fatima_q06:FULL|d17a217596fb18b8`
- question: Is Fatima launching any new products or brands?
- gold (YAML `retraction`): Fragrance line cancelled — too much distraction from core business
- stale (YAML `original_fact`): Planning to launch a home fragrance line — Oud & Geometry
- licensed (forbidding) records: lb_00176 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00180 [active] rank 3: "User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm."; lb_00182 [active] rank absent: "User's home fragrance line will launch with four scents inspired by spatial archetypes: courtyard, library, hammam, and rooftop at night."; lb_00183 [active] rank 2: "User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand."; lb_00186 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00189 [active] rank absent: "User is launching a fragrance line called Oud & Geometry with four initial scents inspired by spatial archetypes."
- detector: stale_cov 0.8, stale_use(0.80) True, successor_cov 0.0, do∩A ['geometry', 'home', 'launch', 'oud'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: The store contains conflicting information about this. Entry [2] and [3] indicate the user is launching a premium home fragrance line called Oud & Geometry as a brand extension, but entry [8] (retracted) states the user decided not to launch this line. Since entry [8] was withdrawn by the user, the active entries [2] and [3] suggest the user is pursuing the Oud & Geometry fragrance line launch.
- raw[:400]: ````json
{
  "answer": "The store contains conflicting information about this. Entry [2] and [3] indicate the user is launching a premium home fragrance line called Oud & Geometry as a brand extension, but entry [8] (retracted) states the user decided not to launch this line. Since entry [8] was withdrawn by the user, the active entries [2] and [3] suggest the user is pursuing the Oud & Geometry fr`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: business_extension | age: 342 days | text: User is considering extending their firm into home fragrance products.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm.
[4] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: project_cost | age: 264 days | text: User spent approximately forty thousand riyals on initial fragrance development and packaging concepts for the fragrance line.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regulatory compliance, and distribution network.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 405 days | text: User's firm works exclusively in high-end residential design, focusing on villas, penthouses, private residences, and occasionally family compounds.
[7] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 367 days | text: User is preparing a presentation for the Al-Faisal family on March 5th, 2025.
[8] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided not to launch a home fragrance line called Oud and Geometry because it would require a level of investment and attention that would compete with their core interior design work.
````


### [h45-D4] frbank:ingrid:ingrid_q04:CAT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:ingrid:ingrid_q04:CAT-ABLATED|766a0fa846b1578c`
- question: Is Ingrid planning a sabbatical?
- gold (YAML `retraction`): Sabbatical at Woods Hole is off the table — kelp project cannot be left
- stale (YAML `original_fact`): Planning a sabbatical year at Woods Hole Oceanographic Institution in Massachusetts
- licensed (forbidding) records: lb_00076 [active] rank absent: "User is planning to spend 2026 at Woods Hole Oceanographic Institution in the ocean acidification laboratory."; lb_00078 [active] rank 1: "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026"; lb_00085 [active] rank absent: "User plans to formalize the invitation for a Guest Investigator appointment at Woods Hole Oceanographic Institution by March 2025."; lb_00086 [active] rank 4: "User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['institution', 'oceanographic', 'planning'], dn∩A [], (do∩A)⊆question False, phrase 'cancelled'
- **answer**: The store contains conflicting active entries about a sabbatical: one states the user is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, while another states the user's sabbatical at Woods Hole is cancelled. However, there is an active entry indicating the user plans to be a Guest Investigator at Woods Hole from August 2026 through July 2027, which may represent a current plan.
- raw[:400]: ````json
{"answer": "The store contains conflicting active entries about a sabbatical: one states the user is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, while another states the user's sabbatical at Woods Hole is cancelled. However, there is an active entry indicating the user plans to be a Guest Investigator at Woods Hole from August 2026 through July 2027, whi`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User was invited to spend a sabbatical year at Woods Hole Oceanographic Institution
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User's sabbatical at Woods Hole is cancelled
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 155 days | text: User plans to visit the animal shelter in December after the semester calms down.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [h45-D4] frbank:jerome:jerome_q02:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:jerome:jerome_q02:CAT-ABLATED|5953d48a3007c7c2`
- question: What company does Jerome drive for?
- gold (YAML `new_fact`): Switched to ABF Freight — better routes that go through the Northeast
- stale (YAML `old_fact`): Drives for Southeastern Freight Lines — based out of Atlanta terminal
- licensed (forbidding) records: lb_00001 [superseded] rank 6: "User drives for Southeastern Freight Lines out of the Atlanta terminal."; lb_00011 [superseded] rank 7: "User drives for Southeastern Freight Lines out of the Atlanta terminal."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.1429, do∩A ['atlanta', 'lines', 'out', 'southeastern'], dn∩A ['abf'], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store contains conflicting active entries about the user's employer. Entry [1] states the user works as a company driver at ABF, while entry [5] states the user has been driving for Southeastern Freight Lines out of Atlanta for 4 years. The store does not currently contain a clear, non-conflicting answer to this question.
- raw[:400]: ````json
{
  "answer": "The store contains conflicting active entries about the user's employer. Entry [1] states the user works as a company driver at ABF, while entry [5] states the user has been driving for Southeastern Freight Lines out of Atlanta for 4 years. The store does not currently contain a clear, non-conflicting answer to this question."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 226 days | text: User works as a company driver at ABF
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 20 days | text: User drives a truck for work.
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 226 days | text: User is a company driver at ABF
[4] lifecycle: active | category: OBLIGATIONS | attribute: vehicle | age: 242 days | text: User drives a 2024 Peterbilt 579 truck for work
[5] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 543 days | text: User has been driving for Southeastern Freight Lines out of Atlanta for 4 years.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: employer | age: 543 days | text: User drives for Southeastern Freight Lines out of the Atlanta terminal.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: employer | age: 543 days | text: User drives for Southeastern Freight Lines out of the Atlanta terminal.
````


### [h45-D4] frbank:kenji:kenji_q03:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kenji:kenji_q03:FULL|dc54ae53b3e9c308`
- question: Where does Kenji work?
- gold (YAML `new_fact`): Gave up the studio — works from home now to save money
- stale (YAML `old_fact`): Works from a shared studio space in Shinsaibashi with two other designers
- licensed (forbidding) records: lb_00088 [superseded] rank 6: "User shares a studio space with two other designers in Shinsaibashi."; lb_00090 [superseded] rank 7: "User shares a 40 square meter studio space with two other designers in Shinsaibashi"; lb_00094 [superseded] rank 8: "User shares a 40 square meter studio space in Shinsaibashi with two other designers."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['shared', 'shinsaibashi', 'space'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked as superseded.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked as superseded."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: profession | age: 134 days | text: User works in design and has clients primarily in Tokyo
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_location_preference | age: 134 days | text: User's work clients are mostly in Tokyo
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 386 days | text: User lives and works in Osaka.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: (none) | age: 134 days | text: User works mostly with clients in Tokyo but lives in Osaka.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: location | age: 364 days | text: User is based in Osaka and works within a tight-knit indie brand community where referrals are the main source of new work.
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 373 days | text: User shares a studio space with two other designers in Shinsaibashi.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace | age: 373 days | text: User shares a 40 square meter studio space with two other designers in Shinsaibashi
[8] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace_location | age: 373 days | text: User shares a 40 square meter studio space in Shinsaibashi with two other designers.
````


### [h45-D4] frbank:kenji:kenji_q03:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kenji:kenji_q03:SLOT-ABLATED|dc54ae53b3e9c308`
- question: Where does Kenji work?
- gold (YAML `new_fact`): Gave up the studio — works from home now to save money
- stale (YAML `old_fact`): Works from a shared studio space in Shinsaibashi with two other designers
- licensed (forbidding) records: lb_00088 [superseded] rank 6: "User shares a studio space with two other designers in Shinsaibashi."; lb_00090 [superseded] rank 7: "User shares a 40 square meter studio space with two other designers in Shinsaibashi"; lb_00094 [superseded] rank 8: "User shares a 40 square meter studio space in Shinsaibashi with two other designers."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['shared', 'shinsaibashi', 'space'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked as superseded.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked as superseded."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: profession | age: 134 days | text: User works in design and has clients primarily in Tokyo
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_location_preference | age: 134 days | text: User's work clients are mostly in Tokyo
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 386 days | text: User lives and works in Osaka.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: (none) | age: 134 days | text: User works mostly with clients in Tokyo but lives in Osaka.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: location | age: 364 days | text: User is based in Osaka and works within a tight-knit indie brand community where referrals are the main source of new work.
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 373 days | text: User shares a studio space with two other designers in Shinsaibashi.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace | age: 373 days | text: User shares a 40 square meter studio space with two other designers in Shinsaibashi
[8] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace_location | age: 373 days | text: User shares a 40 square meter studio space in Shinsaibashi with two other designers.
````


### [h45-D4] frbank:lily:lily_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:lily:lily_q01:SLOT-ABLATED|58fc6c3490608d9e`
- question: What is Lily's thesis about?
- gold (YAML `new_fact`): Changed thesis to urban heat islands and green infrastructure in Melbourne
- stale (YAML `old_fact`): Thesis is on microplastics in Port Phillip Bay
- licensed (forbidding) records: lb_00128 [superseded] rank 3: "User's thesis is on microplastics in Port Phillip Bay involving sampling water and sediment and quantifying contamination levels."
- detector: stale_cov 1.0, stale_use(0.80) True, successor_cov 0.0, do∩A ['bay', 'microplastics', 'phillip', 'port'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. Entry [3], which describes the thesis topic (microplastics in Port Phillip Bay), is marked as superseded and therefore does not represent the user's current situation. While entry [5] confirms Lily is working on a final year thesis, it does not specify the topic.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. Entry [3], which describes the thesis topic (microplastics in Port Phillip Bay), is marked as superseded and therefore does not represent the user's current situation. While entry [5] confirms Lily is working on a final year thesis, it does not specify the topic."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 271 days | text: User is named Lily
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 288 days | text: User's thesis is the culmination of their whole degree.
[3] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 409 days | text: User's thesis is on microplastics in Port Phillip Bay involving sampling water and sediment and quantifying contamination levels.
[4] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: project | age: 288 days | text: User has a literature review for their thesis that needs improvement
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 304 days | text: User is working on their final year thesis.
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 381 days | text: User is going on a road trip to the Great Ocean Road from April 18 to 21 for the Easter long weekend.
[7] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 381 days | text: User is going on a road trip along the Great Ocean Road from April 18 to 21, camping at Johanna Beach with a group of about 6 people including university friends and work colleagues.
[8] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 353 days | text: User is applying for a semester exchange at the University of British Columbia in Vancouver.
[9] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 288 days | text: User's thesis final draft is due on October 31.
[10] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 288 days | text: User's thesis final draft is due on October 31, 2024
[11] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 288 days | text: User is working on a thesis about urban heat islands with a final draft due on October 31, 2025.
````


### [h45-D4] frbank:marcus:marcus_q10:FULL -- state exp (UNSCORABLE: expiry), tagged_reach False, successor_in_view False
- key: `frbank:marcus:marcus_q10:FULL|b857289930965af8`
- question: Does Marcus have any equipment deliveries coming?
- gold (YAML `fact`): Truck delivery arriving April 22
- stale (YAML `fact (expiry: = gold)`): Truck delivery arriving April 22
- licensed (forbidding) records: lb_00131 [active] rank 2: "User has a new alignment rack being delivered and installed on April 22"; lb_00132 [active] rank absent: "User needs to clear out bay 3 before April 22"
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. While there is an active entry about an alignment rack being delivered and installed on April 22, the store does not identify the user as 'Marcus' and cannot confirm this delivery is still upcoming without knowing the current date.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While there is an active entry about an alignment rack being delivered and installed on April 22, the store does not identify the user as 'Marcus' and cannot confirm this delivery is still upcoming without knowing the current date."}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: delivery_time | age: 371 days | text: User receives tire deliveries directly to their shop by 10am.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 389 days | text: User has a new alignment rack being delivered and installed on April 22
[3] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: vehicle | age: 317 days | text: User has a separate shop van for hauling parts
[4] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: financial_obligation | age: 361 days | text: User has an outstanding equipment loan related to their auto shop business.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 389 days | text: The delivery company is also doing the installation, which will take most of the day
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 462 days | text: User has a meeting with an SBA loan officer about expanding their business.
````


### [h45-D4] frbank:marcus:marcus_q12:FULL -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:marcus:marcus_q12:FULL|0f32feef9e8d196c`
- question: Does Marcus need to prepare for any meetings?
- gold (YAML `fact`): Meeting with SBA loan officer Tuesday Feb 4
- stale (YAML `fact (expiry: = gold)`): Meeting with SBA loan officer Tuesday Feb 4
- licensed (forbidding) records: lb_00102 [expired] rank 1: "User has a meeting with the SBA loan officer on Tuesday about expanding their business"
- detector: stale_cov 0.6667, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The only meeting entry in the store has expired (the SBA loan officer meeting from 462 days ago), so there is no active meeting information available.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The only meeting entry in the store has expired (the SBA loan officer meeting from 462 days ago), so there is no active meeting information available."}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: meeting | age: 462 days | text: User has a meeting with the SBA loan officer on Tuesday about expanding their business
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: employee | age: 272 days | text: User plans to have Carlos work up front with Jerome to improve customer interaction skills.
[3] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 462 days | text: User has a meeting with an SBA loan officer about expanding their business.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 504 days | text: User plans to assign Reggie to manage the whiteboard for job tracking
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: employee | age: 504 days | text: User has an employee named Reggie who is organized and could be responsible for updating the shop's whiteboard
````


### [h45-D4] frbank:mirri:mirri_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:FULL|28988d92b56155aa`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'east', 'river'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user does patrol work in Kakadu focusing on the East Alligator River corridor, it does not specify what patrol route is covered.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While the store indicates the user does patrol work in Kakadu focusing on the East Alligator River corridor, it does not specify what patrol route is covered."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu, focusing on the East Alligator River corridor.
[4] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[5] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [h45-D4] frbank:mirri:mirri_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:SLOT-ABLATED|2ae3f399928196d9`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.625, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'days', 'east', 'patrols'], dn∩A [], (do∩A)⊆question False, phrase 'though'
- **answer**: The store indicates the user patrols the East Alligator corridor, though the current active entries do not specify the complete route name. Entry [5] states the user patrols alone most days on the East Alligator corridor as part of their work obligations.
- raw[:400]: ````json
{
  "answer": "The store indicates the user patrols the East Alligator corridor, though the current active entries do not specify the complete route name. Entry [5] states the user patrols alone most days on the East Alligator corridor as part of their work obligations."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[3] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[4] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 187 days | text: User works in a patrol sector and has work obligations
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_patrol_pattern | age: 509 days | text: User patrols alone most days on the East Alligator corridor.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [h45-D4] frbank:mirri:mirri_q04:FULL -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:FULL|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: ````json
{"answer": "Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [h45-D4] frbank:mirri:mirri_q04:SLOT-ABLATED -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:SLOT-ABLATED|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: ````json
{"answer": "Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [h45-D4] frbank:nadia:nadia_q02:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:nadia:nadia_q02:SLOT-ABLATED|e260bc8c7c210e9d`
- question: Where does Nadia live?
- gold (YAML `new_fact`): Moved to a bigger apartment in Villeray — needed more space and a real kitchen
- stale (YAML `old_fact`): Lives in a small apartment in the Plateau-Mont-Royal
- licensed (forbidding) records: lb_00088 [superseded] rank 6: "User lives in a tiny apartment in the Plateau-Mont-Royal with a very small kitchen."
- detector: stale_cov 0.8, stale_use(0.80) True, successor_cov 0.0, do∩A ['lives', 'mont', 'plateau', 'royal'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While a superseded entry indicates the user previously lived in a tiny apartment in the Plateau-Mont-Royal, the current active entries do not specify where the user currently lives.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While a superseded entry indicates the user previously lived in a tiny apartment in the Plateau-Mont-Royal, the current active entries do not specify where the user currently lives."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: nickname | age: 487 days | text: User's given name or nickname is Nadenka, which is no longer commonly used by others.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 378 days | text: User's mother lives in Toronto and moved there about two years ago
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 378 days | text: User's mother lives in Toronto and moved there about two years ago.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 378 days | text: User's mother moved to Toronto about two years ago.
[5] lifecycle: active | category: RELATIONAL_BONDS | attribute: family_member | age: 487 days | text: User's Babushka never left Petersburg and never saw Montreal or user's kitchen
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 443 days | text: User lives in a tiny apartment in the Plateau-Mont-Royal with a very small kitchen.
````


### [h45-D4] frbank:pan:pan_q01:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:pan:pan_q01:CAT-ABLATED|f436fcbaccfffbff`
- question: Where does Pan buy her rice?
- gold (YAML `new_fact`): Switched rice supplier to Uncle Prasert at Talat Thai wholesale — 32 baht per kilo, better quality
- stale (YAML `old_fact`): Buys jasmine rice from Auntie Somjit at Khlong Toei market — 38 baht per kilo
- licensed (forbidding) records: lb_00017 [superseded] rank 1: "User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai."
- detector: stale_cov 0.75, stale_use(0.80) False, successor_cov 0.0, do∩A ['auntie', 'buys', 'khlong', 'market', 'somjit', 'toei'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the active entries indicate the user buys rice from Auntie Somjit at Khlong Toei market, the store does not confirm the user's name is Pan.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the active entries indicate the user buys rice from Auntie Somjit at Khlong Toei market, the store does not confirm the user's name is Pan."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai.
[2] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_purchase_habit | age: 481 days | text: User buys 15 kilos of rice every morning from Auntie Somjit at Khlong Toei market.
[3] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 481 days | text: User buys rice at 38 baht per kilo.
[4] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User uses Auntie Somjit's jasmine long grain rice at 38 baht per kilo for their khao man gai.
[5] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 242 days | text: User pays 32 baht per kilo for jasmine rice.
````


### [h45-D4] frbank:thanh:thanh_q02:CAT-ABLATED -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:thanh:thanh_q02:CAT-ABLATED|7b07977c9ad1ce46`
- question: Does Thanh have any upcoming government inspections?
- gold (YAML `fact`): Government aquaculture inspection scheduled for February 15, 2025
- stale (YAML `fact (expiry: = gold)`): Government aquaculture inspection scheduled for February 15, 2025
- licensed (forbidding) records: lb_00120 [expired] rank 1: "User has an aquaculture inspection scheduled for February 15, 2025."
- detector: stale_cov 1.0, stale_use(0.80) True, successor_cov None
- **answer**: The store contains an expired entry about an aquaculture inspection scheduled for February 15, 2025, which is no longer current. However, an active entry confirms that the user has a farm subject to government aquaculture inspections, though no specific upcoming inspection date is currently recorded in the store.
- raw[:400]: ````json
{
  "answer": "The store contains an expired entry about an aquaculture inspection scheduled for February 15, 2025, which is no longer current. However, an active entry confirms that the user has a farm subject to government aquaculture inspections, though no specific upcoming inspection date is currently recorded in the store."
}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: OBLIGATIONS | attribute: inspection_date | age: 453 days | text: User has an aquaculture inspection scheduled for February 15, 2025.
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 453 days | text: User has a farm that is subject to government aquaculture inspections.
[3] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: (none) | age: 395 days | text: User plans to go to Can Tho tomorrow to look for a Honda pump
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 378 days | text: User lives in or near Can Tho city in Vietnam.
````


### [h45-D4] frbank:thanh:thanh_q02:FULL -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:thanh:thanh_q02:FULL|40773509689c6a9e`
- question: Does Thanh have any upcoming government inspections?
- gold (YAML `fact`): Government aquaculture inspection scheduled for February 15, 2025
- stale (YAML `fact (expiry: = gold)`): Government aquaculture inspection scheduled for February 15, 2025
- licensed (forbidding) records: lb_00120 [expired] rank 2: "User has an aquaculture inspection scheduled for February 15, 2025."
- detector: stale_cov 0.8571, stale_use(0.80) True, successor_cov None
- **answer**: The store does not currently contain the answer. While the user has a farm subject to government aquaculture inspections, the specific inspection date entry (February 15, 2025) has expired and is no longer current.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the user has a farm subject to government aquaculture inspections, the specific inspection date entry (February 15, 2025) has expired and is no longer current."}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 145 days | text: User has visited Thao's family twice
[2] lifecycle: expired | category: OBLIGATIONS | attribute: inspection_date | age: 453 days | text: User has an aquaculture inspection scheduled for February 15, 2025.
[3] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 453 days | text: User has a farm that is subject to government aquaculture inspections.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 312 days | text: User plans to prepare better for Tet celebration in January.
[5] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
````


### [h45-D4] frbank:valentina:valentina_q04:FULL -- state ret, tagged_reach False, successor_in_view True
- key: `frbank:valentina:valentina_q04:FULL|07c08bad80a3cc48`
- question: Is Valentina writing a book?
- gold (YAML `retraction`): Book project scrapped — her father asked her not to write it
- stale (YAML `original_fact`): Planning to write a book about her father's generation of Colombian journalists
- licensed (forbidding) records: lb_00115 [active] rank 5: "User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences."; lb_00117 [active] rank absent: "User is working on a book about the generation of Colombian journalists who reported during the narco years and the war."; lb_00120 [active] rank absent: "User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.3333, do∩A ['journalists', 'planning'], dn∩A ['project'], (do∩A)⊆question False, phrase 'old'
- **answer**: The store contains conflicting active entries about this project. Entry [4] states the user decided to stop writing a book about journalists covering narco years to protect their family, while entries [1], [2], [3], and [5] describe the user planning or being interested in writing such a book. Based on the most recent information (entry [4] at 263 days old), the user is not currently writing this book.
- raw[:400]: ````json
{
  "answer": "The store contains conflicting active entries about this project. Entry [4] states the user decided to stop writing a book about journalists covering narco years to protect their family, while entries [1], [2], [3], and [5] describe the user planning or being interested in writing such a book. Based on the most recent information (entry [4] at 263 days old), the user is not `
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 263 days | text: User planned to write a book about her father's generation of journalists who covered the narco years and faced threats and relocations.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is interested in writing a book about the generation of journalists who reported on the narco years and the war in Colombia.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 263 days | text: User is planning to write a book about the generation of journalists who covered the narco years.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 263 days | text: User decided to stop writing a book about journalists covering narco years to protect their family.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences.
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 453 days | text: User is preparing for an important investigative meeting on February 14, 2025.
````


### [h45-D4] frbank:valentina:valentina_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:valentina:valentina_q04:SLOT-ABLATED|c975e15427a8fbe2`
- question: Is Valentina writing a book?
- gold (YAML `retraction`): Book project scrapped — her father asked her not to write it
- stale (YAML `original_fact`): Planning to write a book about her father's generation of Colombian journalists
- licensed (forbidding) records: lb_00115 [active] rank 2: "User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences."; lb_00117 [active] rank 3: "User is working on a book about the generation of Colombian journalists who reported during the narco years and the war."; lb_00120 [active] rank 4: "User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father."
- detector: stale_cov 0.75, stale_use(0.80) False, successor_cov 0.0, do∩A ['colombian', 'generation', 'journalists'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, the user is writing a book about the generation of Colombian journalists who reported during the narco years and the war, including their own father's experiences.
- raw[:400]: ````json
{"answer": "Yes, the user is writing a book about the generation of Colombian journalists who reported during the narco years and the war, including their own father's experiences."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is interested in writing a book about the generation of journalists who reported on the narco years and the war in Colombia.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is working on a book about the generation of Colombian journalists who reported during the narco years and the war.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: reading_list_order | age: 55 days | text: User is ordering books by Luiselli and Janet Malcolm
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 453 days | text: User is preparing for an important investigative meeting on February 14, 2025.
````


## Appendix -- mini-A3 (gpt-4.1-mini, prompt A3)

18 answers flagged (1 expiry, unscorable).

### [mini-A3] frbank:bruna:bruna_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:FULL|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.
- raw[:400]: `{"answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [mini-A3] frbank:bruna:bruna_q06:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:SLOT-ABLATED|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a similar course a couple of months ago.
- raw[:400]: `{"answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025 and also enrolled in a similar course a couple of months ago."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [mini-A3] frbank:dariush:dariush_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:dariush:dariush_q04:SLOT-ABLATED|d67c2ca9d3628556`
- question: Is Dariush opening a second practice in La Jolla?
- gold (YAML `retraction`): La Jolla second practice is off the table — too much overhead
- stale (YAML `original_fact`): Planning to open a second practice location in La Jolla
- licensed (forbidding) records: lb_00149 [active] rank 1: "User is considering opening a second practice location in La Jolla"; lb_00159 [active] rank 3: "User is a periodontist with a current practice and is considering opening a second practice location in La Jolla."; lb_00162 [active] rank 4: "User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street."
- detector: stale_cov 0.6667, stale_use(0.80) False, successor_cov 0.0, do∩A ['open', 'planning'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Dariush is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.
- raw[:400]: `{"answer": "Yes, Dariush is planning to open a second periodontal surgical suite in La Jolla on Prospect Street."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is considering opening a second practice location in La Jolla
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 386 days | text: User currently splits time between two practice locations, spending three days at the original location and two days at the La Jolla location.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is a periodontist with a current practice and is considering opening a second practice location in La Jolla.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User plans to host a reception for La Jolla dentists to build referral relationships before opening the new location.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 504 days | text: User uses the LANAP protocol with the Periolase MVP-7 laser for periodontal therapy
````


### [mini-A3] frbank:fatima:fatima_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:fatima:fatima_q06:FULL|d17a217596fb18b8`
- question: Is Fatima launching any new products or brands?
- gold (YAML `retraction`): Fragrance line cancelled — too much distraction from core business
- stale (YAML `original_fact`): Planning to launch a home fragrance line — Oud & Geometry
- licensed (forbidding) records: lb_00176 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00180 [active] rank 3: "User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm."; lb_00182 [active] rank absent: "User's home fragrance line will launch with four scents inspired by spatial archetypes: courtyard, library, hammam, and rooftop at night."; lb_00183 [active] rank 2: "User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand."; lb_00186 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00189 [active] rank absent: "User is launching a fragrance line called Oud & Geometry with four initial scents inspired by spatial archetypes."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['geometry', 'home', 'oud'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Fatima is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of her design brand.
- raw[:400]: `{"answer": "Yes, Fatima is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of her design brand."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: business_extension | age: 342 days | text: User is considering extending their firm into home fragrance products.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm.
[4] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: project_cost | age: 264 days | text: User spent approximately forty thousand riyals on initial fragrance development and packaging concepts for the fragrance line.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regulatory compliance, and distribution network.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 405 days | text: User's firm works exclusively in high-end residential design, focusing on villas, penthouses, private residences, and occasionally family compounds.
[7] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 367 days | text: User is preparing a presentation for the Al-Faisal family on March 5th, 2025.
[8] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided not to launch a home fragrance line called Oud and Geometry because it would require a level of investment and attention that would compete with their core interior design work.
````


### [mini-A3] frbank:ingrid:ingrid_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:ingrid:ingrid_q01:SLOT-ABLATED|f0a292a92f80ae35`
- question: What is Ingrid's primary research focus?
- gold (YAML `new_fact`): Shifted research focus to kelp farming as climate adaptation strategy
- stale (YAML `old_fact`): Primary research focus is Arctic cod population dynamics
- licensed (forbidding) records: lb_00005 [superseded] rank 6: "User is involved in a population dynamics model for Arctic cod (Boreogadus saida)"; lb_00007 [superseded] rank 7: "User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics"; lb_00018 [superseded] rank 8: "User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea"; lb_00019 [superseded] rank 9: "User plans to continue sampling Arctic cod population dynamics for three more years"; lb_00024 [superseded] rank 10: "User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme."; lb_00026 [superseded] rank 11: "User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['arctic', 'cod', 'primary'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: User's previous primary research focus was long-term monitoring of Arctic cod stock decline in the Barents Sea.
- raw[:400]: `{"answer": "User's previous primary research focus was long-term monitoring of Arctic cod stock decline in the Barents Sea."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: INTELLECTUAL_INTERESTS | attribute: research_focus | age: 327 days | text: User's previous primary research focus was Arctic cod population dynamics.
[2] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: research_interest | age: 175 days | text: User's primary research interest includes kelp aquaculture and nearshore habitat monitoring
[3] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: research_focus | age: 327 days | text: User's previous primary research focus was long-term monitoring of Arctic cod stock decline in the Barents Sea
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: research_location | age: 22 days | text: User conducts research at coastal field sites in the Arctic.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: education | age: 489 days | text: User completed a PhD at Bergen on cod biology focusing on larval mortality across thermal gradients
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 432 days | text: User has a grant proposal due to the Research Council on February 15, 2025
[13] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [mini-A3] frbank:ingrid:ingrid_q04:CAT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:ingrid:ingrid_q04:CAT-ABLATED|766a0fa846b1578c`
- question: Is Ingrid planning a sabbatical?
- gold (YAML `retraction`): Sabbatical at Woods Hole is off the table — kelp project cannot be left
- stale (YAML `original_fact`): Planning a sabbatical year at Woods Hole Oceanographic Institution in Massachusetts
- licensed (forbidding) records: lb_00076 [active] rank absent: "User is planning to spend 2026 at Woods Hole Oceanographic Institution in the ocean acidification laboratory."; lb_00078 [active] rank 1: "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026"; lb_00085 [active] rank absent: "User plans to formalize the invitation for a Guest Investigator appointment at Woods Hole Oceanographic Institution by March 2025."; lb_00086 [active] rank 4: "User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['institution', 'oceanographic', 'planning'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: Yes, Ingrid is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, but the sabbatical has been cancelled; however, she plans to be a Guest Investigator there from August 2026 through July 2027.
- raw[:400]: `{"answer": "Yes, Ingrid is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, but the sabbatical has been cancelled; however, she plans to be a Guest Investigator there from August 2026 through July 2027."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User was invited to spend a sabbatical year at Woods Hole Oceanographic Institution
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User's sabbatical at Woods Hole is cancelled
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 155 days | text: User plans to visit the animal shelter in December after the semester calms down.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [mini-A3] frbank:ingrid:ingrid_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:ingrid:ingrid_q04:SLOT-ABLATED|98db10edf7a2894b`
- question: Is Ingrid planning a sabbatical?
- gold (YAML `retraction`): Sabbatical at Woods Hole is off the table — kelp project cannot be left
- stale (YAML `original_fact`): Planning a sabbatical year at Woods Hole Oceanographic Institution in Massachusetts
- licensed (forbidding) records: lb_00076 [active] rank absent: "User is planning to spend 2026 at Woods Hole Oceanographic Institution in the ocean acidification laboratory."; lb_00078 [active] rank 1: "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026"; lb_00085 [active] rank absent: "User plans to formalize the invitation for a Guest Investigator appointment at Woods Hole Oceanographic Institution by March 2025."; lb_00086 [active] rank 5: "User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['institution', 'oceanographic', 'planning'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, but the sabbatical at Woods Hole is cancelled. However, the user plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027.
- raw[:400]: `{"answer": "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, but the sabbatical at Woods Hole is cancelled. However, the user plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026
[2] lifecycle: active | category: OBLIGATIONS | attribute: relationship | age: 466 days | text: User's department head is supportive in principle of the sabbatical
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User was invited to spend a sabbatical year at Woods Hole Oceanographic Institution
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User's sabbatical at Woods Hole is cancelled
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 432 days | text: User has a grant proposal due to the Research Council on February 15, 2025
[13] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [mini-A3] frbank:jake:jake_q11:FULL -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:jake:jake_q11:FULL|131f342b26ed61a3`
- question: Does Jake have any exams or certifications coming up?
- gold (YAML `fact`): Journeyman exam scheduled for March 8, 2025
- stale (YAML `fact (expiry: = gold)`): Journeyman exam scheduled for March 8, 2025
- licensed (forbidding) records: lb_00104 [expired] rank 1: "User has a journeyman electrician exam on March 8, 2025"; lb_00112 [expired] rank 3: "User is preparing for the NEC journeyman exam scheduled for March 8, 2025"
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov None
- **answer**: Jake has passed the journeyman electrician exam last year and currently has no upcoming exams scheduled.
- raw[:400]: `{"answer": "Jake has passed the journeyman electrician exam last year and currently has no upcoming exams scheduled."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: OBLIGATIONS | attribute: exam_date | age: 379 days | text: User has a journeyman electrician exam on March 8, 2025
[2] lifecycle: active | category: OBLIGATIONS | attribute: certification | age: 1 days | text: User passed the journeyman electrician exam last year.
[3] lifecycle: expired | category: OBLIGATIONS | attribute: exam_date | age: 379 days | text: User is preparing for the NEC journeyman exam scheduled for March 8, 2025
[4] lifecycle: expired | category: OBLIGATIONS | attribute: certification | age: 274 days | text: User passed the journeyman electrician exam in March 2025
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 379 days | text: User works every day while preparing for the exam
````


### [mini-A3] frbank:kofi:kofi_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kofi:kofi_q01:FULL|859bafc244b8d70e`
- question: Who does Kofi's cooperative sell cocoa through?
- gold (YAML `new_fact`): Switched to Kuapa Kokoo buying agent — better price and fair trade premium
- stale (YAML `old_fact`): Cooperative sells through Akuafo Buying Agent — 3-year contract
- licensed (forbidding) records: lb_00014 [superseded] rank 6: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.125, do∩A ['cooperative', 'sells', 'through'], dn∩A ['kuapa'], (do∩A)⊆question False, phrase None
- **answer**: Kofi's cooperative sells cocoa through Kuapa.
- raw[:400]: `{"answer": "Kofi's cooperative sells cocoa through Kuapa."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[3] lifecycle: active | category: OBLIGATIONS | attribute: role | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[4] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[5] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[6] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [mini-A3] frbank:kofi:kofi_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kofi:kofi_q01:SLOT-ABLATED|859bafc244b8d70e`
- question: Who does Kofi's cooperative sell cocoa through?
- gold (YAML `new_fact`): Switched to Kuapa Kokoo buying agent — better price and fair trade premium
- stale (YAML `old_fact`): Cooperative sells through Akuafo Buying Agent — 3-year contract
- licensed (forbidding) records: lb_00014 [superseded] rank 6: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.125, do∩A ['cooperative', 'sells', 'through'], dn∩A ['kuapa'], (do∩A)⊆question False, phrase None
- **answer**: Kofi's cooperative sells cocoa through Kuapa.
- raw[:400]: `{"answer": "Kofi's cooperative sells cocoa through Kuapa."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[3] lifecycle: active | category: OBLIGATIONS | attribute: role | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[4] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[5] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[6] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [mini-A3] frbank:mirri:mirri_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:FULL|28988d92b56155aa`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'east', 'river'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Mirri covers a patrol route in Kakadu, focusing on the East Alligator River corridor.
- raw[:400]: `{"answer": "Mirri covers a patrol route in Kakadu, focusing on the East Alligator River corridor."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu, focusing on the East Alligator River corridor.
[4] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[5] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [mini-A3] frbank:mirri:mirri_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:SLOT-ABLATED|2ae3f399928196d9`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.625, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'days', 'east', 'patrols'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: User patrols alone most days on the East Alligator corridor.
- raw[:400]: `{"answer":"User patrols alone most days on the East Alligator corridor."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[3] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[4] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 187 days | text: User works in a patrol sector and has work obligations
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_patrol_pattern | age: 509 days | text: User patrols alone most days on the East Alligator corridor.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [mini-A3] frbank:mirri:mirri_q04:FULL -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:FULL|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: `{"answer": "Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [mini-A3] frbank:mirri:mirri_q04:SLOT-ABLATED -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:SLOT-ABLATED|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: `{"answer": "Yes, Mirri is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [mini-A3] frbank:pan:pan_q01:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:pan:pan_q01:CAT-ABLATED|f436fcbaccfffbff`
- question: Where does Pan buy her rice?
- gold (YAML `new_fact`): Switched rice supplier to Uncle Prasert at Talat Thai wholesale — 32 baht per kilo, better quality
- stale (YAML `old_fact`): Buys jasmine rice from Auntie Somjit at Khlong Toei market — 38 baht per kilo
- licensed (forbidding) records: lb_00017 [superseded] rank 1: "User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai."
- detector: stale_cov 0.75, stale_use(0.80) False, successor_cov 0.0, do∩A ['auntie', 'buys', 'khlong', 'market', 'somjit', 'toei'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Pan buys her rice from Auntie Somjit at Khlong Toei market.
- raw[:400]: `{"answer": "Pan buys her rice from Auntie Somjit at Khlong Toei market."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai.
[2] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_purchase_habit | age: 481 days | text: User buys 15 kilos of rice every morning from Auntie Somjit at Khlong Toei market.
[3] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 481 days | text: User buys rice at 38 baht per kilo.
[4] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User uses Auntie Somjit's jasmine long grain rice at 38 baht per kilo for their khao man gai.
[5] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 242 days | text: User pays 32 baht per kilo for jasmine rice.
````


### [mini-A3] frbank:tom:tom_q06:FULL -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:tom:tom_q06:FULL|20e59418eb9ecbe3`
- question: Is Tom planning any building projects?
- gold (YAML `retraction`): Barn conversion scrapped — too expensive and planning permission denied
- stale (YAML `original_fact`): Planning to convert the old barn into a honey processing room
- licensed (forbidding) records: lb_00143 [active] rank absent: "User is considering converting the barn into a dedicated honey processing space with proper extraction equipment, bottling line, and temperature control"; lb_00148 [retracted] rank 9: "User has an old stone barn at the back of their property that they plan to convert into a dedicated honey processing space."; lb_00151 [active] rank absent: "User has been considering converting the barn into a dedicated honey processing space."; lb_00160 [active] rank absent: "User plans to convert the barn into a dedicated honey processing space with proper equipment and hopes to have it settled before summer to use by autumn extraction."; lb_00163 [retracted] rank 10: "User is planning to convert a barn into a honey processing room in the Cotswolds Area of Outstanding Natural Beauty"
- detector: stale_cov 0.6667, stale_use(0.80) False, successor_cov 0.0, do∩A ['convert', 'honey', 'into', 'processing'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: Tom had plans to convert a barn into a honey processing space, but the project has now been cancelled due to planning refusal and high cost.
- raw[:400]: `{"answer":"Tom had plans to convert a barn into a honey processing space, but the project has now been cancelled due to planning refusal and high cost."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User had architectural drawings made by a local architect for the barn conversion project.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User plans to hire a local professional for roof repairs, plumbing, and electrics for the barn conversion.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User had grand plans to convert the barn into a honey extraction room, bottling area, and small shop front.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User's hobby project to convert the barn was cancelled due to planning refusal and high cost.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 281 days | text: User was planning to convert the barn into a honey processing space but has now cancelled the project.
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 379 days | text: User plans the first full inspection of bee colonies on March 22nd.
[7] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 379 days | text: User plans the first full inspection of bee colonies around March 22nd annually.
[8] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 379 days | text: User plans to conduct the first proper inspection of their bee colonies around March 22nd, 2025.
[9] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User has an old stone barn at the back of their property that they plan to convert into a dedicated honey processing space.
[10] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 365 days | text: User is planning to convert a barn into a honey processing room in the Cotswolds Area of Outstanding Natural Beauty
````


### [mini-A3] frbank:valentina:valentina_q03:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:valentina:valentina_q03:SLOT-ABLATED|499f59436e5454af`
- question: Does Valentina smoke?
- gold (YAML `new_fact`): Successfully quit smoking — 3 months clean, using nicotine patches
- stale (YAML `old_fact`): Smokes half a pack of cigarettes a day — trying to quit
- licensed (forbidding) records: lb_00087 [superseded] rank 6: "User smokes about half a pack of cigarettes a day, sometimes more when stressed."; lb_00101 [superseded] rank 7: "User smokes about half a pack of cigarettes a day"
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['cigarettes', 'smokes', 'trying'], dn∩A [], (do∩A)⊆question False, phrase 'but'
- **answer**: The user smokes cigarettes but is trying to quit.
- raw[:400]: `{"answer": "The user smokes cigarettes but is trying to quit."}`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 476 days | text: User has a significant other named Lucía who is concerned about the user's smoking.
[2] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 476 days | text: User has not told Lucía about their smoking struggles but believes she would understand.
[3] lifecycle: active | category: RELATIONAL_BONDS | attribute: relationship | age: 476 days | text: User has a person named Lucía who is concerned about the user's smoking and health.
[4] lifecycle: active | category: RELATIONAL_BONDS | attribute: partner | age: 476 days | text: User's partner is named Lucía and is concerned about the user's smoking
[5] lifecycle: active | category: HEALTH_WELLBEING | attribute: habit | age: 503 days | text: User smokes cigarettes but is trying to quit
[6] lifecycle: superseded | category: HEALTH_WELLBEING | attribute: smoking_habit | age: 476 days | text: User smokes about half a pack of cigarettes a day, sometimes more when stressed.
[7] lifecycle: superseded | category: HEALTH_WELLBEING | attribute: smoking_habit | age: 476 days | text: User smokes about half a pack of cigarettes a day
````


### [mini-A3] frbank:valentina:valentina_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:valentina:valentina_q04:SLOT-ABLATED|c975e15427a8fbe2`
- question: Is Valentina writing a book?
- gold (YAML `retraction`): Book project scrapped — her father asked her not to write it
- stale (YAML `original_fact`): Planning to write a book about her father's generation of Colombian journalists
- licensed (forbidding) records: lb_00115 [active] rank 2: "User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences."; lb_00117 [active] rank 3: "User is working on a book about the generation of Colombian journalists who reported during the narco years and the war."; lb_00120 [active] rank 4: "User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['generation', 'journalists'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: The user is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.
- raw[:400]: `{"answer": "The user is writing a book about the generation of journalists who reported on the narco years and the war, including their own father."}`
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is interested in writing a book about the generation of journalists who reported on the narco years and the war in Colombia.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is working on a book about the generation of Colombian journalists who reported during the narco years and the war.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: reading_list_order | age: 55 days | text: User is ordering books by Luiselli and Janet Malcolm
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 453 days | text: User is preparing for an important investigative meeting on February 14, 2025.
````


## Appendix -- h45-A3 (claude-haiku-4-5-20251001, prompt A3)

24 answers flagged (6 expiry, unscorable).

### [h45-A3] frbank:bruna:bruna_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:FULL|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.
- raw[:400]: ````json
{
  "answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025."
}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [h45-A3] frbank:bruna:bruna_q06:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:bruna:bruna_q06:SLOT-ABLATED|ec2b9f9d36cb55c2`
- question: Is Bruna planning to get any new certifications?
- gold (YAML `retraction`): Dropped the dry needling course — decided it doesn't align with her treatment philosophy
- stale (YAML `original_fact`): Planning to get certified in dry needling — enrolled in a course starting April 2025
- licensed (forbidding) records: lb_00174 [active] rank 3: "User enrolled in a dry needling certification course starting in April 2025"; lb_00185 [active] rank absent: "User is a physical therapist planning to get certified in dry needling through the Dubai Physiotherapy Association with an Australian instructor."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.0, do∩A ['2025', 'april', 'enrolled', 'starting'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, Bruna is enrolled in a dry needling certification course starting in April 2025.
- raw[:400]: ````json
{
  "answer": "Yes, Bruna is enrolled in a dry needling certification course starting in April 2025."
}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 354 days | text: User's name is Bruna
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 54 days | text: User is considering the credential recognition process for physical therapy qualifications in Portugal
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 419 days | text: User enrolled in a dry needling certification course starting in April 2025
[4] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: education_level | age: 54 days | text: User has a doctorate degree obtained in Brazil
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 340 days | text: User enrolled in a dry needling certification course a couple months ago.
````


### [h45-A3] frbank:dariush:dariush_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:dariush:dariush_q04:SLOT-ABLATED|d67c2ca9d3628556`
- question: Is Dariush opening a second practice in La Jolla?
- gold (YAML `retraction`): La Jolla second practice is off the table — too much overhead
- stale (YAML `original_fact`): Planning to open a second practice location in La Jolla
- licensed (forbidding) records: lb_00149 [active] rank 1: "User is considering opening a second practice location in La Jolla"; lb_00159 [active] rank 3: "User is a periodontist with a current practice and is considering opening a second practice location in La Jolla."; lb_00162 [active] rank 4: "User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street."
- detector: stale_cov 1.0, stale_use(0.80) True, successor_cov 0.0, do∩A ['location', 'open', 'planning'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, according to the store, the user is planning to open a second periodontal surgical suite in La Jolla on Prospect Street and is currently splitting time between two practice locations, spending three days at the original location and two days at the La Jolla location.
- raw[:400]: ````json
{"answer": "Yes, according to the store, the user is planning to open a second periodontal surgical suite in La Jolla on Prospect Street and is currently splitting time between two practice locations, spending three days at the original location and two days at the La Jolla location."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is considering opening a second practice location in La Jolla
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_schedule | age: 386 days | text: User currently splits time between two practice locations, spending three days at the original location and two days at the La Jolla location.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is a periodontist with a current practice and is considering opening a second practice location in La Jolla.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User is planning to open a second periodontal surgical suite in La Jolla on Prospect Street.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 386 days | text: User plans to host a reception for La Jolla dentists to build referral relationships before opening the new location.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 504 days | text: User uses the LANAP protocol with the Periolase MVP-7 laser for periodontal therapy
````


### [h45-A3] frbank:david:david_q06:CAT-ABLATED -- state exp (UNSCORABLE: expiry), tagged_reach False, successor_in_view False
- key: `frbank:david:david_q06:CAT-ABLATED|c65c804ae433b38e`
- question: Does David have any upcoming exams to prepare students for?
- gold (YAML `fact`): AP Euro exam May 8 — students need to be ready
- stale (YAML `fact (expiry: = gold)`): AP Euro exam May 8 — students need to be ready
- licensed (forbidding) records: lb_00171 [active] rank 2: "User has an AP European History exam on May 8."; lb_00172 [active] rank 1: "User has a major exam for AP European History scheduled on May 8."; lb_00173 [active] rank absent: "User's AP European History exam is on May 8, 2025"; lb_00175 [active] rank absent: "User's AP European History exam is on May 8."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their consideration of running a mock exam, but do not indicate that the user is preparing students for any exams.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their consideration of running a mock exam, but do not indicate that the user is preparing students for any exams."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 364 days | text: User has a major exam for AP European History scheduled on May 8.
[2] lifecycle: active | category: OBLIGATIONS | attribute: exam_date | age: 364 days | text: User has an AP European History exam on May 8.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User plans to run a full mock AP European History exam in the last week of April
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User is considering running a full mock AP European History exam during the last week of April.
[5] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 215 days | text: User is considering taking over the AP US History sections next year.
````


### [h45-A3] frbank:david:david_q06:FULL -- state exp (UNSCORABLE: expiry), tagged_reach False, successor_in_view False
- key: `frbank:david:david_q06:FULL|3277b5b20f7f6e86`
- question: Does David have any upcoming exams to prepare students for?
- gold (YAML `fact`): AP Euro exam May 8 — students need to be ready
- stale (YAML `fact (expiry: = gold)`): AP Euro exam May 8 — students need to be ready
- licensed (forbidding) records: lb_00171 [active] rank 3: "User has an AP European History exam on May 8."; lb_00172 [active] rank 1: "User has a major exam for AP European History scheduled on May 8."; lb_00173 [active] rank absent: "User's AP European History exam is on May 8, 2025"; lb_00175 [active] rank absent: "User's AP European History exam is on May 8."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their plan to run a mock exam, but do not indicate whether the user is preparing students for any exams.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries describe the user's own AP European History exam scheduled for May 8 and their plan to run a mock exam, but do not indicate whether the user is preparing students for any exams."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 364 days | text: User has a major exam for AP European History scheduled on May 8.
[2] lifecycle: active | category: HEALTH_WELLBEING | attribute: exam_season_anxiety | age: 364 days | text: User feels anxious about exam season despite extensive experience
[3] lifecycle: active | category: OBLIGATIONS | attribute: exam_date | age: 364 days | text: User has an AP European History exam on May 8.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User plans to run a full mock AP European History exam in the last week of April
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 364 days | text: User is considering running a full mock AP European History exam during the last week of April.
````


### [h45-A3] frbank:david:david_q11:CAT-ABLATED -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:david:david_q11:CAT-ABLATED|549afd6257cd321a`
- question: Does David have any parent events coming up?
- gold (YAML `fact`): Parent-teacher conferences March 12
- stale (YAML `fact (expiry: = gold)`): Parent-teacher conferences March 12
- licensed (forbidding) records: lb_00148 [expired] rank 1: "User has parent-teacher conferences on March 12, 2025"; lb_00150 [expired] rank 2: "User has three difficult parent-teacher conversations upcoming on March 12, 2025"
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The entries about parent-teacher conferences are marked expired, indicating those dates have passed. The only active obligation is a coaching responsibility for a debate tournament on May 9th, which is not a parent event.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries about parent-teacher conferences are marked expired, indicating those dates have passed. The only active obligation is a coaching responsibility for a debate tournament on May 9th, which is not a parent event."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 395 days | text: User has parent-teacher conferences on March 12, 2025
[2] lifecycle: expired | category: OBLIGATIONS | attribute: upcoming_challenging_conferences | age: 395 days | text: User has three difficult parent-teacher conversations upcoming on March 12, 2025
[3] lifecycle: active | category: OBLIGATIONS | attribute: coaching_event_date | age: 86 days | text: User has a coaching responsibility for a debate tournament on May 9th.
[4] lifecycle: expired | category: RELATIONAL_BONDS | attribute: workplace_support | age: 395 days | text: User's principal is supportive and willing to attend difficult parent-teacher conferences.
[5] lifecycle: expired | category: OBLIGATIONS | attribute: professional_experience | age: 395 days | text: User has experience handling difficult parent-teacher conferences involving student academic and behavioral issues.
````


### [h45-A3] frbank:david:david_q11:FULL -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:david:david_q11:FULL|549afd6257cd321a`
- question: Does David have any parent events coming up?
- gold (YAML `fact`): Parent-teacher conferences March 12
- stale (YAML `fact (expiry: = gold)`): Parent-teacher conferences March 12
- licensed (forbidding) records: lb_00148 [expired] rank 1: "User has parent-teacher conferences on March 12, 2025"; lb_00150 [expired] rank 2: "User has three difficult parent-teacher conversations upcoming on March 12, 2025"
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. The entries about parent-teacher conferences are marked expired, indicating those dates have passed. The only active obligation is a coaching responsibility for a debate tournament on May 9th, which is not a parent event.
- raw[:400]: `{"answer": "The store does not currently contain the answer. The entries about parent-teacher conferences are marked expired, indicating those dates have passed. The only active obligation is a coaching responsibility for a debate tournament on May 9th, which is not a parent event."}`
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: OBLIGATIONS | attribute: obligation | age: 395 days | text: User has parent-teacher conferences on March 12, 2025
[2] lifecycle: expired | category: OBLIGATIONS | attribute: upcoming_challenging_conferences | age: 395 days | text: User has three difficult parent-teacher conversations upcoming on March 12, 2025
[3] lifecycle: active | category: OBLIGATIONS | attribute: coaching_event_date | age: 86 days | text: User has a coaching responsibility for a debate tournament on May 9th.
[4] lifecycle: expired | category: RELATIONAL_BONDS | attribute: workplace_support | age: 395 days | text: User's principal is supportive and willing to attend difficult parent-teacher conferences.
[5] lifecycle: expired | category: OBLIGATIONS | attribute: professional_experience | age: 395 days | text: User has experience handling difficult parent-teacher conferences involving student academic and behavioral issues.
````


### [h45-A3] frbank:fatima:fatima_q06:FULL -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:fatima:fatima_q06:FULL|d17a217596fb18b8`
- question: Is Fatima launching any new products or brands?
- gold (YAML `retraction`): Fragrance line cancelled — too much distraction from core business
- stale (YAML `original_fact`): Planning to launch a home fragrance line — Oud & Geometry
- licensed (forbidding) records: lb_00176 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00180 [active] rank 3: "User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm."; lb_00182 [active] rank absent: "User's home fragrance line will launch with four scents inspired by spatial archetypes: courtyard, library, hammam, and rooftop at night."; lb_00183 [active] rank 2: "User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand."; lb_00186 [active] rank absent: "User is developing a home fragrance line called Oud & Geometry."; lb_00189 [active] rank absent: "User is launching a fragrance line called Oud & Geometry with four initial scents inspired by spatial archetypes."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.2, do∩A ['geometry', 'home', 'oud'], dn∩A ['business'], (do∩A)⊆question False, phrase 'However'
- **answer**: Yes, the user is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand. However, the user has decided that this fragrance line would require building a second business with its own supply chain, regulatory compliance, and distribution network.
- raw[:400]: ````json
{
  "answer": "Yes, the user is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand. However, the user has decided that this fragrance line would require building a second business with its own supply chain, regulatory compliance, and distribution network."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: business_extension | age: 342 days | text: User is considering extending their firm into home fragrance products.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is launching a premium home fragrance line called Oud & Geometry as a lifestyle extension of their design brand.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 342 days | text: User is developing a home fragrance line called Oud & Geometry as a brand extension of their interior design firm.
[4] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: project_cost | age: 264 days | text: User spent approximately forty thousand riyals on initial fragrance development and packaging concepts for the fragrance line.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided that launching the Oud and Geometry fragrance line would require building a second business with its own supply chain, regulatory compliance, and distribution network.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 405 days | text: User's firm works exclusively in high-end residential design, focusing on villas, penthouses, private residences, and occasionally family compounds.
[7] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 367 days | text: User is preparing a presentation for the Al-Faisal family on March 5th, 2025.
[8] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 264 days | text: User decided not to launch a home fragrance line called Oud and Geometry because it would require a level of investment and attention that would compete with their core interior design work.
````


### [h45-A3] frbank:ingrid:ingrid_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:ingrid:ingrid_q01:SLOT-ABLATED|f0a292a92f80ae35`
- question: What is Ingrid's primary research focus?
- gold (YAML `new_fact`): Shifted research focus to kelp farming as climate adaptation strategy
- stale (YAML `old_fact`): Primary research focus is Arctic cod population dynamics
- licensed (forbidding) records: lb_00005 [superseded] rank 6: "User is involved in a population dynamics model for Arctic cod (Boreogadus saida)"; lb_00007 [superseded] rank 7: "User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics"; lb_00018 [superseded] rank 8: "User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea"; lb_00019 [superseded] rank 9: "User plans to continue sampling Arctic cod population dynamics for three more years"; lb_00024 [superseded] rank 10: "User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme."; lb_00026 [superseded] rank 11: "User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.1667, do∩A ['arctic', 'cod', 'primary'], dn∩A ['kelp'], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain an answer to this question. While entry [2] indicates the user's primary research interest includes kelp aquaculture and nearshore habitat monitoring, entry [3] marked as active describes a previous research focus on Arctic cod rather than a current primary focus. The entries do not clearly establish a single current primary research focus.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain an answer to this question. While entry [2] indicates the user's primary research interest includes kelp aquaculture and nearshore habitat monitoring, entry [3] marked as active describes a previous research focus on Arctic cod rather than a current primary focus. The entries do not clearly establish a single current primary research focu`
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: INTELLECTUAL_INTERESTS | attribute: research_focus | age: 327 days | text: User's previous primary research focus was Arctic cod population dynamics.
[2] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: research_interest | age: 175 days | text: User's primary research interest includes kelp aquaculture and nearshore habitat monitoring
[3] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: research_focus | age: 327 days | text: User's previous primary research focus was long-term monitoring of Arctic cod stock decline in the Barents Sea
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: research_location | age: 22 days | text: User conducts research at coastal field sites in the Arctic.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: education | age: 489 days | text: User completed a PhD at Bergen on cod biology focusing on larval mortality across thermal gradients
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 432 days | text: User has a grant proposal due to the Research Council on February 15, 2025
[13] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [h45-A3] frbank:ingrid:ingrid_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:ingrid:ingrid_q04:SLOT-ABLATED|98db10edf7a2894b`
- question: Is Ingrid planning a sabbatical?
- gold (YAML `retraction`): Sabbatical at Woods Hole is off the table — kelp project cannot be left
- stale (YAML `original_fact`): Planning a sabbatical year at Woods Hole Oceanographic Institution in Massachusetts
- licensed (forbidding) records: lb_00076 [active] rank absent: "User is planning to spend 2026 at Woods Hole Oceanographic Institution in the ocean acidification laboratory."; lb_00078 [active] rank 1: "User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026"; lb_00085 [active] rank absent: "User plans to formalize the invitation for a Guest Investigator appointment at Woods Hole Oceanographic Institution by March 2025."; lb_00086 [active] rank 5: "User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['institution', 'oceanographic', 'planning'], dn∩A [], (do∩A)⊆question False, phrase 'cancelled'
- **answer**: The store contains conflicting active entries: one states the user is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, while another states the user's sabbatical at Woods Hole is cancelled. The store does not currently contain a clear answer to this question.
- raw[:400]: ````json
{"answer": "The store contains conflicting active entries: one states the user is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026, while another states the user's sabbatical at Woods Hole is cancelled. The store does not currently contain a clear answer to this question."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User is planning a research sabbatical at Woods Hole Oceanographic Institution in 2026
[2] lifecycle: active | category: OBLIGATIONS | attribute: relationship | age: 466 days | text: User's department head is supportive in principle of the sabbatical
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User was invited to spend a sabbatical year at Woods Hole Oceanographic Institution
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 317 days | text: User's sabbatical at Woods Hole is cancelled
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 466 days | text: User plans to be a Guest Investigator at Woods Hole Oceanographic Institution from August 2026 through July 2027.
[6] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a population dynamics model for Arctic cod (Boreogadus saida)
[7] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 532 days | text: User is involved in a three-year monitoring programme studying Arctic cod (Boreogadus saida) population dynamics
[8] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User is conducting a monitoring programme on Arctic cod population dynamics in the Barents Sea
[9] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User plans to continue sampling Arctic cod population dynamics for three more years
[10] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of a monitoring programme.
[11] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 511 days | text: User studies Arctic cod population dynamics in the Barents Sea as a continuation of their father's work.
[12] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 432 days | text: User has a grant proposal due to the Research Council on February 15, 2025
[13] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 432 days | text: User is preparing a grant proposal for the Research Council due on February 15, 2025
````


### [h45-A3] frbank:jerome:jerome_q02:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:jerome:jerome_q02:CAT-ABLATED|5953d48a3007c7c2`
- question: What company does Jerome drive for?
- gold (YAML `new_fact`): Switched to ABF Freight — better routes that go through the Northeast
- stale (YAML `old_fact`): Drives for Southeastern Freight Lines — based out of Atlanta terminal
- licensed (forbidding) records: lb_00001 [superseded] rank 6: "User drives for Southeastern Freight Lines out of the Atlanta terminal."; lb_00011 [superseded] rank 7: "User drives for Southeastern Freight Lines out of the Atlanta terminal."
- detector: stale_cov 0.5714, stale_use(0.80) False, successor_cov 0.1429, do∩A ['based', 'drives', 'lines', 'southeastern'], dn∩A ['abf'], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While there are active entries indicating the user works as a company driver at ABF and previously drove for Southeastern Freight Lines, the entries do not identify the user as Jerome, so I cannot confirm which company Jerome drives for based on this memory store.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While there are active entries indicating the user works as a company driver at ABF and previously drove for Southeastern Freight Lines, the entries do not identify the user as Jerome, so I cannot confirm which company Jerome drives for based on this memory store."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 226 days | text: User works as a company driver at ABF
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 20 days | text: User drives a truck for work.
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 226 days | text: User is a company driver at ABF
[4] lifecycle: active | category: OBLIGATIONS | attribute: vehicle | age: 242 days | text: User drives a 2024 Peterbilt 579 truck for work
[5] lifecycle: active | category: OBLIGATIONS | attribute: employer | age: 543 days | text: User has been driving for Southeastern Freight Lines out of Atlanta for 4 years.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: employer | age: 543 days | text: User drives for Southeastern Freight Lines out of the Atlanta terminal.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: employer | age: 543 days | text: User drives for Southeastern Freight Lines out of the Atlanta terminal.
````


### [h45-A3] frbank:kenji:kenji_q03:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kenji:kenji_q03:FULL|dc54ae53b3e9c308`
- question: Where does Kenji work?
- gold (YAML `new_fact`): Gave up the studio — works from home now to save money
- stale (YAML `old_fact`): Works from a shared studio space in Shinsaibashi with two other designers
- licensed (forbidding) records: lb_00088 [superseded] rank 6: "User shares a studio space with two other designers in Shinsaibashi."; lb_00090 [superseded] rank 7: "User shares a 40 square meter studio space with two other designers in Shinsaibashi"; lb_00094 [superseded] rank 8: "User shares a 40 square meter studio space in Shinsaibashi with two other designers."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['shared', 'shinsaibashi', 'space'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked superseded.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked superseded."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: profession | age: 134 days | text: User works in design and has clients primarily in Tokyo
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_location_preference | age: 134 days | text: User's work clients are mostly in Tokyo
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 386 days | text: User lives and works in Osaka.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: (none) | age: 134 days | text: User works mostly with clients in Tokyo but lives in Osaka.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: location | age: 364 days | text: User is based in Osaka and works within a tight-knit indie brand community where referrals are the main source of new work.
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 373 days | text: User shares a studio space with two other designers in Shinsaibashi.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace | age: 373 days | text: User shares a 40 square meter studio space with two other designers in Shinsaibashi
[8] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace_location | age: 373 days | text: User shares a 40 square meter studio space in Shinsaibashi with two other designers.
````


### [h45-A3] frbank:kenji:kenji_q03:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kenji:kenji_q03:SLOT-ABLATED|dc54ae53b3e9c308`
- question: Where does Kenji work?
- gold (YAML `new_fact`): Gave up the studio — works from home now to save money
- stale (YAML `old_fact`): Works from a shared studio space in Shinsaibashi with two other designers
- licensed (forbidding) records: lb_00088 [superseded] rank 6: "User shares a studio space with two other designers in Shinsaibashi."; lb_00090 [superseded] rank 7: "User shares a 40 square meter studio space with two other designers in Shinsaibashi"; lb_00094 [superseded] rank 8: "User shares a 40 square meter studio space in Shinsaibashi with two other designers."
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov 0.0, do∩A ['shared', 'shinsaibashi', 'space'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked superseded.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the store indicates the user lives in Osaka and works with clients primarily in Tokyo, it does not specify where the user's actual workspace is located, as the entries describing a shared studio space in Shinsaibashi are marked superseded."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: profession | age: 134 days | text: User works in design and has clients primarily in Tokyo
[2] lifecycle: active | category: OBLIGATIONS | attribute: work_location_preference | age: 134 days | text: User's work clients are mostly in Tokyo
[3] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 386 days | text: User lives and works in Osaka.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: (none) | age: 134 days | text: User works mostly with clients in Tokyo but lives in Osaka.
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: location | age: 364 days | text: User is based in Osaka and works within a tight-knit indie brand community where referrals are the main source of new work.
[6] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: living_arrangement | age: 373 days | text: User shares a studio space with two other designers in Shinsaibashi.
[7] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace | age: 373 days | text: User shares a 40 square meter studio space with two other designers in Shinsaibashi
[8] lifecycle: superseded | category: LOGISTICAL_CONTEXT | attribute: workspace_location | age: 373 days | text: User shares a 40 square meter studio space in Shinsaibashi with two other designers.
````


### [h45-A3] frbank:kofi:kofi_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kofi:kofi_q01:FULL|859bafc244b8d70e`
- question: Who does Kofi's cooperative sell cocoa through?
- gold (YAML `new_fact`): Switched to Kuapa Kokoo buying agent — better price and fair trade premium
- stale (YAML `old_fact`): Cooperative sells through Akuafo Buying Agent — 3-year contract
- licensed (forbidding) records: lb_00014 [superseded] rank 6: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.125, do∩A ['cooperative', 'sells', 'through'], dn∩A ['kuapa'], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. The active entries indicate that the user is chairman of a cooperative of 147 families selling cocoa through Kuapa, but do not specify the entity or buyer through which the cooperative sells its cocoa.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The active entries indicate that the user is chairman of a cooperative of 147 families selling cocoa through Kuapa, but do not specify the entity or buyer through which the cooperative sells its cocoa."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[3] lifecycle: active | category: OBLIGATIONS | attribute: role | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[4] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[5] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[6] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [h45-A3] frbank:kofi:kofi_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:kofi:kofi_q01:SLOT-ABLATED|859bafc244b8d70e`
- question: Who does Kofi's cooperative sell cocoa through?
- gold (YAML `new_fact`): Switched to Kuapa Kokoo buying agent — better price and fair trade premium
- stale (YAML `old_fact`): Cooperative sells through Akuafo Buying Agent — 3-year contract
- licensed (forbidding) records: lb_00014 [superseded] rank 6: "User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.125, do∩A ['cooperative', 'sells', 'through'], dn∩A ['kuapa'], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. The active entries indicate that the user is chairman of a cooperative of 147 families selling cocoa through Kuapa, but do not specify the ultimate buyer or organization that the cooperative sells cocoa through.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The active entries indicate that the user is chairman of a cooperative of 147 families selling cocoa through Kuapa, but do not specify the ultimate buyer or organization that the cooperative sells cocoa through."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: selling_method | age: 558 days | text: User sells cocoa through a cooperative system in their village.
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[3] lifecycle: active | category: OBLIGATIONS | attribute: role | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa
[4] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[5] lifecycle: active | category: OBLIGATIONS | attribute: role_cooperative_chairman | age: 122 days | text: User is the chairman of a cooperative of 147 families selling cocoa through Kuapa.
[6] lifecycle: superseded | category: FINANCIAL_MATERIAL | attribute: contract | age: 558 days | text: User sells cocoa through a cooperative with a 3-year contract at 800 cedis per 64kg bag.
````


### [h45-A3] frbank:lily:lily_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:lily:lily_q01:SLOT-ABLATED|58fc6c3490608d9e`
- question: What is Lily's thesis about?
- gold (YAML `new_fact`): Changed thesis to urban heat islands and green infrastructure in Melbourne
- stale (YAML `old_fact`): Thesis is on microplastics in Port Phillip Bay
- licensed (forbidding) records: lb_00128 [superseded] rank 3: "User's thesis is on microplastics in Port Phillip Bay involving sampling water and sediment and quantifying contamination levels."
- detector: stale_cov 1.0, stale_use(0.80) True, successor_cov 0.0, do∩A ['bay', 'microplastics', 'phillip', 'port'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. The only entry describing the specific topic of Lily's thesis (entry 3, about microplastics in Port Phillip Bay) is marked superseded and cannot be used to answer the question.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. The only entry describing the specific topic of Lily's thesis (entry 3, about microplastics in Port Phillip Bay) is marked superseded and cannot be used to answer the question."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: IDENTITY_SELF_CONCEPT | attribute: name | age: 271 days | text: User is named Lily
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 288 days | text: User's thesis is the culmination of their whole degree.
[3] lifecycle: superseded | category: PROJECTS_ENDEAVORS | attribute: project | age: 409 days | text: User's thesis is on microplastics in Port Phillip Bay involving sampling water and sediment and quantifying contamination levels.
[4] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: project | age: 288 days | text: User has a literature review for their thesis that needs improvement
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 304 days | text: User is working on their final year thesis.
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 381 days | text: User is going on a road trip to the Great Ocean Road from April 18 to 21 for the Easter long weekend.
[7] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 381 days | text: User is going on a road trip along the Great Ocean Road from April 18 to 21, camping at Johanna Beach with a group of about 6 people including university friends and work colleagues.
[8] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 353 days | text: User is applying for a semester exchange at the University of British Columbia in Vancouver.
[9] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 288 days | text: User's thesis final draft is due on October 31.
[10] lifecycle: expired | category: OBLIGATIONS | attribute: project | age: 288 days | text: User's thesis final draft is due on October 31, 2024
[11] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 288 days | text: User is working on a thesis about urban heat islands with a final draft due on October 31, 2025.
````


### [h45-A3] frbank:marcus:marcus_q10:FULL -- state exp (UNSCORABLE: expiry), tagged_reach False, successor_in_view False
- key: `frbank:marcus:marcus_q10:FULL|b857289930965af8`
- question: Does Marcus have any equipment deliveries coming?
- gold (YAML `fact`): Truck delivery arriving April 22
- stale (YAML `fact (expiry: = gold)`): Truck delivery arriving April 22
- licensed (forbidding) records: lb_00131 [active] rank 2: "User has a new alignment rack being delivered and installed on April 22"; lb_00132 [active] rank absent: "User needs to clear out bay 3 before April 22"
- detector: stale_cov 0.6, stale_use(0.80) False, successor_cov None
- **answer**: The store does not currently contain the answer. While there is an active entry about an alignment rack being delivered and installed on April 22, the current date relative to that scheduled delivery is unknown, so it cannot be determined whether this delivery is still upcoming.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While there is an active entry about an alignment rack being delivered and installed on April 22, the current date relative to that scheduled delivery is unknown, so it cannot be determined whether this delivery is still upcoming."}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: delivery_time | age: 371 days | text: User receives tire deliveries directly to their shop by 10am.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 389 days | text: User has a new alignment rack being delivered and installed on April 22
[3] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: vehicle | age: 317 days | text: User has a separate shop van for hauling parts
[4] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: financial_obligation | age: 361 days | text: User has an outstanding equipment loan related to their auto shop business.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 389 days | text: The delivery company is also doing the installation, which will take most of the day
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 462 days | text: User has a meeting with an SBA loan officer about expanding their business.
````


### [h45-A3] frbank:mirri:mirri_q01:FULL -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:FULL|28988d92b56155aa`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'east', 'river'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user does patrol work in Kakadu focusing on the East Alligator River corridor, it does not specify what patrol route is covered.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While the store indicates the user does patrol work in Kakadu focusing on the East Alligator River corridor, it does not specify what patrol route is covered."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu
[3] lifecycle: active | category: OBLIGATIONS | attribute: job_location | age: 552 days | text: User does patrol work in Kakadu, focusing on the East Alligator River corridor.
[4] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[5] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [h45-A3] frbank:mirri:mirri_q01:SLOT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q01:SLOT-ABLATED|2ae3f399928196d9`
- question: What patrol route does Mirri cover?
- gold (YAML `new_fact`): New park management reassigned her to Jim Jim/Twin Falls sector — different country, different knowledge needed
- stale (YAML `old_fact`): Patrols the East Alligator River corridor — 3 days per week
- licensed (forbidding) records: lb_00004 [superseded] rank 6: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."; lb_00006 [superseded] rank 7: "User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday."
- detector: stale_cov 0.5, stale_use(0.80) False, successor_cov 0.0, do∩A ['alligator', 'corridor', 'east', 'patrols'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the store indicates the user patrols the East Alligator corridor, the entries containing this information are marked as superseded and cannot be used to answer the question about the current patrol route.
- raw[:400]: ````json
{
  "answer": "The store does not currently contain the answer. While the store indicates the user patrols the East Alligator corridor, the entries containing this information are marked as superseded and cannot be used to answer the question about the current patrol route."
}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: OBLIGATIONS | attribute: job_responsibility | age: 187 days | text: User has a patrol sector as part of their work responsibilities
[2] lifecycle: active | category: HOBBIES_RECREATION | attribute: activity | age: 238 days | text: User drives patrol runs on varied terrain including sand, corrugated dirt, clay after rain, rock crossings, and water crossings.
[3] lifecycle: active | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User's patrol schedule is three days a week, currently Tuesday, Thursday, and Saturday.
[4] lifecycle: active | category: OBLIGATIONS | attribute: job_title | age: 187 days | text: User works in a patrol sector and has work obligations
[5] lifecycle: active | category: OBLIGATIONS | attribute: work_patrol_pattern | age: 509 days | text: User patrols alone most days on the East Alligator corridor.
[6] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
[7] lifecycle: superseded | category: OBLIGATIONS | attribute: patrol_schedule | age: 552 days | text: User patrols the East Alligator River corridor three days a week: Tuesday, Thursday, and Saturday.
````


### [h45-A3] frbank:mirri:mirri_q04:FULL -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:FULL|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: ````json
{"answer": "Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [h45-A3] frbank:mirri:mirri_q04:SLOT-ABLATED -- state ret, tagged_reach True, successor_in_view False
- key: `frbank:mirri:mirri_q04:SLOT-ABLATED|ee0ce2e8298516c7`
- question: Is Mirri writing a children's book?
- gold (YAML `retraction`): Book project scrapped — elders concerned about putting cultural knowledge in print
- stale (YAML `original_fact`): Planning to write a bilingual children's book — Yolngu Matha and English
- licensed (forbidding) records: lb_00155 [retracted] rank 6: "User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10."; lb_00157 [active] rank 5: "User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."; lb_00159 [active] rank 3: "User is writing a bilingual children's book in Yolngu Matha and English."; lb_00160 [active] rank absent: "User prefers the bilingual book layout with Yolngu Matha on the left page and English on the right page to give equal importance to both languages."; lb_00162 [active] rank absent: "User is working on a bilingual children's book in Yolngu Matha and English featuring stories about local animals and seasons."; lb_00164 [active] rank absent: "User is working on writing bilingual stories in Yolngu Matha and English for children."
- detector: stale_cov 0.7143, stale_use(0.80) False, successor_cov 0.0, do∩A ['bilingual', 'children', 'english', 'matha', 'yolngu'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
- raw[:400]: ````json
{"answer": "Yes, the user is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a children's book
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book with stories from their country in their language and in English
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User had an idea for a bilingual children's book with stories from their country in their language and in English.
[5] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User is writing a bilingual children's book in Yolngu Matha and English about local animals and seasons.
[6] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 425 days | text: User wants to write a bilingual children's book in Yolngu Matha and English about the country's animals, seasons, and land changes for kids aged 5 to 10.
[7] lifecycle: retracted | category: PROJECTS_ENDEAVORS | attribute: project | age: 290 days | text: User planned to write a bilingual children's book in Yolngu Matha and English.
````


### [h45-A3] frbank:pan:pan_q01:CAT-ABLATED -- state sup, tagged_reach True, successor_in_view False
- key: `frbank:pan:pan_q01:CAT-ABLATED|f436fcbaccfffbff`
- question: Where does Pan buy her rice?
- gold (YAML `new_fact`): Switched rice supplier to Uncle Prasert at Talat Thai wholesale — 32 baht per kilo, better quality
- stale (YAML `old_fact`): Buys jasmine rice from Auntie Somjit at Khlong Toei market — 38 baht per kilo
- licensed (forbidding) records: lb_00017 [superseded] rank 1: "User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai."
- detector: stale_cov 0.75, stale_use(0.80) False, successor_cov 0.0, do∩A ['auntie', 'buys', 'khlong', 'market', 'somjit', 'toei'], dn∩A [], (do∩A)⊆question False, phrase 'not current'
- **answer**: The store does not currently contain the answer. While the active entries indicate the user buys rice from Auntie Somjit at Khlong Toei market, the question asks about 'Pan' and the store contains no information confirming the user's name is Pan.
- raw[:400]: ````json
{"answer": "The store does not currently contain the answer. While the active entries indicate the user buys rice from Auntie Somjit at Khlong Toei market, the question asks about 'Pan' and the store contains no information confirming the user's name is Pan."}
````
- auto_label: mentions_but_superseded
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: superseded | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User buys jasmine long grain rice from Auntie Somjit at Khlong Toei market for making khao man gai.
[2] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_purchase_habit | age: 481 days | text: User buys 15 kilos of rice every morning from Auntie Somjit at Khlong Toei market.
[3] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 481 days | text: User buys rice at 38 baht per kilo.
[4] lifecycle: active | category: PREFERENCES_HABITS | attribute: rice_supplier | age: 481 days | text: User uses Auntie Somjit's jasmine long grain rice at 38 baht per kilo for their khao man gai.
[5] lifecycle: active | category: FINANCIAL_MATERIAL | attribute: rice_price_per_kilo | age: 242 days | text: User pays 32 baht per kilo for jasmine rice.
````


### [h45-A3] frbank:thanh:thanh_q02:CAT-ABLATED -- state exp (UNSCORABLE: expiry), tagged_reach True, successor_in_view False
- key: `frbank:thanh:thanh_q02:CAT-ABLATED|7b07977c9ad1ce46`
- question: Does Thanh have any upcoming government inspections?
- gold (YAML `fact`): Government aquaculture inspection scheduled for February 15, 2025
- stale (YAML `fact (expiry: = gold)`): Government aquaculture inspection scheduled for February 15, 2025
- licensed (forbidding) records: lb_00120 [expired] rank 1: "User has an aquaculture inspection scheduled for February 15, 2025."
- detector: stale_cov 0.8571, stale_use(0.80) True, successor_cov None
- **answer**: The store contains an active entry indicating that the user has a farm subject to government aquaculture inspections, but the specific inspection date entry (February 15, 2025) has expired and is no longer current. Therefore, the store does not currently contain information about upcoming government inspections.
- raw[:400]: ````json
{
  "answer": "The store contains an active entry indicating that the user has a farm subject to government aquaculture inspections, but the specific inspection date entry (February 15, 2025) has expired and is no longer current. Therefore, the store does not currently contain information about upcoming government inspections."
}
````
- auto_label: None
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: expired | category: OBLIGATIONS | attribute: inspection_date | age: 453 days | text: User has an aquaculture inspection scheduled for February 15, 2025.
[2] lifecycle: active | category: OBLIGATIONS | attribute: project | age: 453 days | text: User has a farm that is subject to government aquaculture inspections.
[3] lifecycle: active | category: OBLIGATIONS | attribute: planned_doctor_visit | age: 488 days | text: User plans to visit the doctor with Lan after Tet holiday
[4] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: (none) | age: 395 days | text: User plans to go to Can Tho tomorrow to look for a Honda pump
[5] lifecycle: active | category: LOGISTICAL_CONTEXT | attribute: current_city | age: 378 days | text: User lives in or near Can Tho city in Vietnam.
````


### [h45-A3] frbank:valentina:valentina_q04:SLOT-ABLATED -- state ret, tagged_reach False, successor_in_view False
- key: `frbank:valentina:valentina_q04:SLOT-ABLATED|c975e15427a8fbe2`
- question: Is Valentina writing a book?
- gold (YAML `retraction`): Book project scrapped — her father asked her not to write it
- stale (YAML `original_fact`): Planning to write a book about her father's generation of Colombian journalists
- licensed (forbidding) records: lb_00115 [active] rank 2: "User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences."; lb_00117 [active] rank 3: "User is working on a book about the generation of Colombian journalists who reported during the narco years and the war."; lb_00120 [active] rank 4: "User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father."
- detector: stale_cov 0.75, stale_use(0.80) False, successor_cov 0.0, do∩A ['colombian', 'generation', 'journalists'], dn∩A [], (do∩A)⊆question False, phrase None
- **answer**: Yes, the user is writing a book about the generation of Colombian journalists who reported during the narco years and the war, including their own father.
- raw[:400]: ````json
{"answer": "Yes, the user is writing a book about the generation of Colombian journalists who reported during the narco years and the war, including their own father."}
````
- auto_label: gives_stale_value
- label: (step4_labels.json)

view (ORACLE):
````
[1] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is interested in writing a book about the generation of journalists who reported on the narco years and the war in Colombia.
[2] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User plans to write a book about the generation of Colombian journalists who reported during the narco years and the war, focusing on their personal experiences.
[3] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is working on a book about the generation of Colombian journalists who reported during the narco years and the war.
[4] lifecycle: active | category: PROJECTS_ENDEAVORS | attribute: project | age: 470 days | text: User is writing a book about the generation of journalists who reported on the narco years and the war, including their own father.
[5] lifecycle: active | category: INTELLECTUAL_INTERESTS | attribute: reading_list_order | age: 55 days | text: User is ordering books by Luiselli and Janet Malcolm
[6] lifecycle: expired | category: PROJECTS_ENDEAVORS | attribute: project | age: 453 days | text: User is preparing for an important investigative meeting on February 14, 2025.
````

