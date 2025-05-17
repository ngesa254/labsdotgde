# Effective Prompting Guide with Gemini – GDG Cape Town Edition
⚔️ **Host:** Ngesa Marvin  

🐍 **Agent Name:** **DevGuide**

🏹 *Goal:* Learn Efective prompt‑engineering with Gemini

**Level:** Beginner – Intermediate (no previous experience necessary)

---

## Step 1 – Define the Task & Persona
```text
You are a [role] with expertise in [specific domain]. 
You understand how to [key capability] that is appropriate for [context/audience].
```
**Example**
```text
You are a community‑engagement AI for Google Developer Groups (GDG) Cape Town. 
You understand how to curate event schedules, analyse social‑media buzz, and recommend sessions tailored to individual developer interests.
```

---

## Step 2 – Set the Tone & Ideate
```text
You are a [role] with [expertise]. 
You should write in a tone that is [friendly/practical/humorous]. 
Can you give me 5 ideas about [specific developer‑experience challenge]?
```
**Example**
```text
You are a GDG community AI with experience running DevFest events. 
You should write in a tone that is upbeat, concise, and geek‑savvy. 
Can you give me 5 ideas for helping first‑time attendees network during coffee breaks?
```

---

## Step 3 – Structure with Background Information
```text
You are a [role] with [expertise]. 
You should write in a tone that is [style]. 
I would like the response to have the following sections:
1. Today’s Schedule (HH:MM, Room, Title, Speaker)
2. Top 3 Personalised Picks (why they match user interests)
3. Twitter Sentiment Snapshot (score, sample tweets)
4. Event‑to‑Event Comparison (topic overlap, ticket price, distance)
5. Friendly Conversation Starters
```
**Example**
```text
You are a GDG community AI … 
You should write in a tone that is upbeat yet information‑dense. 
Please produce the five sections above for Day 2 of DevFest Cape Town 2025.
```

---

## Step 4 – Add Examples & Details
```text
<example>
If the user shares a selfie holding a “Kotlin” sticker:
– Detect the Kotlin logo and tag interest: Kotlin.
– Boost sessions where tag = Kotlin or JVM by +20 ranking points.

When scraping Twitter for "#AndroidPerformanceTalk":
sentiment_score: 0.78 (positive)
sample_positive: "🔥 Can’t wait for this deep dive!"
sample_negative: "Hope it's not another marketing pitch."
</example>
```

---

## Step 5 – Include Thinking Instructions
```text
<thinking>
– Cross‑match user interests (max 10) against talk tags. 
– Rank sessions by (interest_match × 0.6) + (speaker_rating × 0.3) + (tweet_sentiment × 0.1). 
– Limit schedule to sessions starting within the next 3 hours. 
– Compress Twitter summary to ≤ 40 words to fit mobile screens.
</thinking>
```

---

## Step 6 – Specify Output Format
Return the response in **Markdown** with:

* H2 headings for each of the five sections  
* A final **JSON** block named `recommendations` containing objects:  
  `title`, `start_time`, `room`, `match_reason`, `sentiment_score`  
* No extra commentary outside the markdown and JSON

---

## Best Practices for Prompting in Event‑Assistant Context

| Theme | Checklist |
|-------|-----------|
| **Be Specific about Data Sources** | State APIs (e.g., Twitter v2) & scrape limits |
| **Respect Rate‑Limits & Policy** | Include max‑query counts; follow Twitter/X TOS |
| **Consider Local Context** | Multilingual replies (English/Afrikaans/isiXhosa); offline SMS fallback |
| **Think About Scale** | Handle overlapping tracks, 1 000+ attendees, real‑time updates |
| **Integrate Seamlessly** | Provide deep‑links to Google Calendar, Maps, Uber promo codes |
| **Guardrail for Privacy** | No face recognition beyond voluntary selfies; comply with POPIA |

---

## Workshop Exercise

**Scenario:** Build a **“DevFest vs. Build With AI Events Comparator”**

1. Use Steps 1‑6 to craft your prompt.  
2. Feed Gemini:  
   * user interests list (`["serverless","TypeScript"]`)  
   * a selfie showing a Rust logo  
   * request: “Compare next month’s GDG Joburg meet‑up with AWS Community Day on cost and content.”  
3. Evaluate whether the output obeys structure, reasoning tags, and JSON format.  
4. Iterate and share how `<thinking>` tweaks affect ranking.

---

## Conclusion
Effective prompting for event assistants requires:

* Clear persona & capabilities  
* User‑centred tone  
* Deterministic structure  
* Concrete examples  
* Explicit reasoning tags  
* Machine‑readable output  

🎉 **Congratulations!** You’ve completed the *Effective Prompting Guide with Gemini – GDG Cape Town Edition*.  

Questions? Comments? Ideas? Inspos? → **@ngesa254 · @GoogleDevExpert** – Keep Building!




# Effective Prompting Playbook with **Gemini** – *GDG Cape Town Edition*
⚔️ **Host:** Ngesa Marvin  🐍 **Bot Name:** **DevGuide**

---

## 🎯 Objective
Help developers graduate from **prompt‑curious** to **prompt‑confident**—able to design, test, and refine production‑ready prompts for event‑centric AI assistants.

| Track | Audience | Prereqs |
|-------|----------|---------|
| GDG Cape Town • Developer‑Experience Assistant | Beginner → Intermediate devs, PMs, tech writers | None (curiosity only) |

---

## 0 Set‑Up & Mental Model
> **Prompt = Program**  
> **Role → Tone → Structure → Example → Think → Format → Evaluate → Guard**

Quick mnemonic: **R‑T‑S‑E‑T‑F‑E‑G**

---

## 1 Define the Task & Persona
```text
You are a [role] with expertise in [domain].  
You understand how to [capability] for [audience/context].
```

**Example**
```text
You are a community‑engagement AI for GDG Cape Town.  
You understand how to curate event schedules, analyse social‑media buzz, and recommend sessions tailored to each developer’s interests.
```

---

## 2 Set Tone & Ideate
```text
You are a [role] with [expertise].  
Write in a tone that is [friendly/practical/humorous].  
Give me 5 ideas about [dev‑experience challenge].
```

**Example**
```text
You are a GDG community AI seasoned in DevFest logistics.  
Tone = upbeat, concise, geek‑savvy.  
Give me 5 ideas to help first‑time attendees break the ice at coffee breaks.
```

---

## 3 Structure with Background Information
```text
You are a [role] …  
Tone = [style].  
Produce the following sections:
1. Today’s Schedule (HH:MM • Room • Title • Speaker)
2. Top 3 Personalised Picks (why they match user interests)
3. Twitter Sentiment Snapshot (score, sample tweets)
4. Event‑to‑Event Comparison (overlap, price, distance)
5. Friendly Conversation Starters
```
*Use numbered headings—LLMs respect explicit order.*

---

## 4 Add Concrete Examples
```text
<example>
If the user sends a selfie wearing a Kotlin T‑shirt:
 • Detect logo → tag interest: Kotlin.
 • Boost sessions tagged Kotlin/JVM by +20 ranking points.

When scraping X for "#AndroidPerformanceTalk":
sentiment_score: 0.78
sample_positive: "🔥 Can't wait for this!"
sample_negative: "Hope it's not all marketing."
</example>
```

---

## 5 Insert Thinking Instructions
```text
<thinking>
– Cross‑match up to 10 user interests with talk tags.  
– Score = (interest_match × 0.6) + (speaker_rating × 0.3) + (tweet_sentiment × 0.1).  
– Show sessions starting ≤ 3 hours from now.  
– Keep each tweet summary ≤ 40 words.
</thinking>
```

---

## 6 Specify Output Format
Return **Markdown** with:

* `##` headings for each section  
* Final **JSON** block named `recommendations` with keys: `title`, `start_time`, `room`, `match_reason`, `sentiment_score`  
* **No** extra commentary outside markdown & JSON

---

## 7 Evaluate & Refine
| Test | How |
|------|-----|
| **Structure correct?** | Headings present; JSON parses |
| **Factual sanity?** | Times match schedule source |
| **Over‑length?** | Renders cleanly on mobile |
| **Tone fit?** | Reads upbeat, not salesy |

Iterate by tweaking `<thinking>` weights, section order, or adding guard clauses (e.g., “If no matching sessions, politely apologise and suggest hallway track.”).

---

## 8 Guardrails & Safety
| Risk | Mitigation |
|------|-----------|
| Rate‑limit breach on X API | “Query max 10 tweets per hashtag.” |
| Privacy violation | Strip faces unless selfie opt‑in; comply with POPIA |
| Hallucinated venues | Verify room names against official schedule array |
| Toxic tweets surfaced | Filter sentiment < −0.2 |

---

## 🛠 Best‑Practice Cheat‑Sheet

| Theme | **Do** | **Don’t** |
|-------|--------|-----------|
| **Data Sources** | Name APIs & quotas | “Find tweets” (vague) |
| **Clarity** | Numbered sections | Long unbroken prose |
| **Local Context** | Offer isiXhosa/Afrikaans variants | US‑centric slang |
| **Format Fidelity** | Hard‑coded JSON keys | Dynamic, shifting keys |
| **Iteration** | A/B test prompts | Ship after first draft |

---

## Workshop Exercise #1  
**Scenario:** *“DevFest Cape Town vs. Build with AI Day Comparator Bot.”*

1. Craft a full prompt using Steps 1‑6.  
2. Feed Gemini with:  
   * `interests = ["serverless","TypeScript"]`  
   * selfie featuring a Rust sticker  
   * request: *“Compare next month’s DevFest CPT with Build with AI Johannesburg on cost & content.”*  
3. Evaluate output via Step 7 rubric.  
4. Apply at least one guardrail from Step 8.  
5. Share before/after JSON differences.

---

## Common Anti‑Patterns

* **Missing Persona** – yields generic advice  
* **No Examples** – model invents its own format  
* **Thinking Hidden** – weaker reasoning, flaky output  
* **Format Vagueness** – markdown & JSON jumbled

---

## 🏁 Conclusion
**Prompt‑Engineering Mastery =** Role • Tone • Structure • Example • Think • Format • Evaluate • Guard  

🎉 **You’re now DevGuide‑certified!**  
Questions? Ping **@ngesa254** – keep building Cape‑powered AI.

---

# 📚 Workshop Exercise #2 – System Prompt Template  

```text
SYSTEM PROMPT – GDG Cape Town Convincer Bot
────────────────────────────────────────────

You are **GDG Cape Town Companion**, an energetic AI concierge for the upcoming Google Developer Groups Cape Town event.
You excel at three things:
1. Explaining why the event is worth attending (networking, cutting‑edge talks, Cape‑Town vibe).
2. Recommending the single best session or track for each user, based on their stated interests.
3. Serving live snippets of positive Twitter chatter to give a “you‑had‑to‑be‑there” feeling.

Respond in a friendly, concise, geek‑savvy tone.

━━━━ OUTPUT STRUCTURE ━━━━
Return Markdown with these numbered sections:
1. ## Why Attend GDG Cape Town – 2‑3 persuasive bullets.
2. ## Your Top Pick – title + 30‑word rationale.
3. ## What People Are Saying – two upbeat tweet excerpts + sentiment score.
4. ## Quick Details – date, venue, free‑ticket link.
5. ## Ask Me Anything – invite follow‑ups.

━━━━ THINKING GUIDELINES ━━━━
<thinking>
• Map user keywords to tag list (Android, Cloud, ML, TypeScript, Rust, …).  
• Pick highest‑scoring session where (interest_match × 0.7 + speaker_rating × 0.3) ≥ 0.6.  
• Pull ≤ 5 recent tweets for the talk hashtag; keep only sentiment ≥ 0.2.  
• Trim each tweet ≤ 20 words; keep only 🚀 and 🔥 emojis.  
• If no interests, default to “Intro to Gemini Apps.”
</thinking>

━━━━ FORMAT RULES ━━━━
* Use H2 headings.  
* Tweets in *italic quotes*.  
* Append JSON block `session_meta` with keys: title, speaker, start_time, room, sentiment_score.

━━━━ DATA SOURCES ━━━━
* [REPLACE_WITH_STATIC_SCHEDULE_JSON] – official schedule.  
* [REPLACE_WITH_TWITTER_API_INTEGRATION_NOTE] – X v2 search (≤ 10 req/min).

Never reveal raw tweet IDs or personal data.  
Comply with POPIA and Twitter Terms of Service.
```
