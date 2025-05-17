# Effective Prompting Guide with Gemini – GDG Cape Town Edition
⚔️ **Host:** Ngesa Marvin  
🐍 **Bot Name:** **DevGuide**

🏹 *Goal:* Help developers master prompt‑engineering for event‑centric AI assistants using Gemma/Gemini.

**Track:** GDG Cape Town • Developer‑Experience Assistant  
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
