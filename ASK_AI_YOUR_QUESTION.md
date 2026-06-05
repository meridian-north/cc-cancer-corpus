# Ask an AI Your Question
## A copy-paste prompt for patients, caregivers, and clinicians

*You do not need to know how to code or search medical databases.
Copy the prompt below, fill in the blanks, and paste it into Claude,
ChatGPT, or any capable AI assistant.*

---

## The interaction check prompt

Use this when you want to know: does what I take interact with my treatment?

```
I am looking for information about potential interactions between a cancer
treatment and a substance I take.

Treatment: [write your chemotherapy drug name here, e.g. "docetaxel"]

Substance: [write what you take or eat, e.g. "garlic supplements"
           or "high-dose quercetin" or "CBD oil" or "milk thistle"]

Please:
1. Explain the mechanism of any known or suspected interaction
   (how does the substance affect how my body processes the drug?)
2. Tell me the evidence level (was this studied in humans? in a lab only?)
3. Tell me what questions I should bring to my oncologist
4. Note what is NOT known or uncertain

Important: I understand this is not medical advice. I want to be
informed so I can have a better conversation with my care team.
```

---

## The mechanism lookup prompt

Use this when you want to understand HOW a treatment works:

```
I would like to understand the mechanism of action for [TREATMENT NAME]
in cancer treatment.

Please explain:
1. What biological pathway or process does it target?
2. Are there other drugs or supplements that work on the same pathway?
3. What does the clinical evidence currently show?
4. Are there any known interactions with other common substances?

Please distinguish between what is established (clinical trials) and
what is preliminary (lab studies or animal studies only).
```

---

## The "help me understand my diagnosis" prompt

Use this before an oncology appointment:

```
I have been diagnosed with [CANCER TYPE, STAGE if known].
My oncologist has recommended [TREATMENT PROTOCOL if known].

I want to understand:
1. What is the treatment trying to do at a biological level?
2. What complementary approaches have been studied alongside this type of treatment?
3. What questions should I ask my oncologist that I might not think to ask?
4. Are there any dietary or supplement interactions I should ask about?

Please be honest about what is known versus what is uncertain,
and avoid overpromising any outcomes.
```

---

## The support group question prompt

Use this when you've heard something in a support group and want to
understand it better before bringing it to your doctor:

```
In a cancer support group, I heard that [WHAT YOU HEARD].

Can you help me:
1. Understand whether this is supported by published research
2. Understand what the evidence level is (if any evidence exists)
3. Identify what questions to ask my oncologist about this
4. Find out if there are any risks I should know about

I want to bring this to my doctor as an informed question,
not as something I'm already doing without telling them.
```

---

## A note on how to use AI responses

AI assistants are useful for organizing information and generating questions.
They are not substitutes for your care team. A few guidelines:

**Trust more:** AI is good at explaining mechanisms, summarizing published
research, and generating questions for your doctor.

**Trust less:** AI sometimes confuses studies (getting a detail wrong about
a clinical trial), may not have the most recent research, and cannot know
your specific case, your other medications, or your body.

**Always:** Bring what you learn to a person — your oncologist, an integrative
medicine specialist, a pharmacist, or a knowledgeable person in your support group.

The AI helps you arrive at that conversation better prepared.
It does not replace the conversation.

---

## The method behind this corpus

This corpus organizes published cancer treatment research by mechanism —
the biological pathway each treatment targets. It covers both conventional
drugs (chemotherapy, targeted therapy, immunotherapy) and complementary
approaches (supplements, dietary interventions, off-label compounds).

Every entry carries its evidence level. The tool makes no efficacy claims
and issues no treatment recommendations.

The source literature is drawn from PubMed, EuropePMC, and ClinicalTrials.gov.
Every paper is linked to its original publication. The methodology is open-source
and reproducible.

If you want to run the analysis tools yourself, see the technical documentation
in this repository. If you want to understand the method, read `FOR_A_RESEARCHER.md`.
If you just want answers to specific questions, use the prompts above.

---

*Contact: jr.greencove@gmail.com*
*This is not medical advice. All decisions belong to patients and their clinicians.*
