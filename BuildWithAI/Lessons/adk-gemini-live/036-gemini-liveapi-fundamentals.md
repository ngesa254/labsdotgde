# Lesson 3.6: Multimodal Live API Quickstart (Prep Lab)

📓 `Kisumu_buildwithai_liveapi_fundermentals.ipynb`  
**Colab:** https://colab.research.google.com/drive/1v6JnpWr3xDBFip6HRxBHiQWxe6-N9jMc

## Challenge: Gemini Live API Fundamentals 🎙️🖼️⚡

Use the **Gemini 2.5 Flash Live API (preview)** to create a real-time, multimodal chat demo in Colab.

## Prerequisites
* Python + Colab runtime.
* Google GenAI SDK installed:

```bash
%pip install -U google-genai
```

* API key loaded into environment variable `GOOGLE_API_KEY`.

## Concept
Unlike batch prompts, the **Live API** supports **low-latency, streaming conversations** across modalities:
* Text → Text
* Text → Audio (native `.wav`)
* (Preview) Image/Video input

It also supports **resumable sessions**, letting agents remember across runs.

## Task

### 1. Run a turn-based chat
Send "Hello" → receive Gemini's reply as text.

### 2. Switch to audio output
Update `config = {"response_modalities": ["AUDIO"]}` Save response chunks to `audio.wav` and play back.

### 3. Wrap into a loop
Build a simple `AudioLoop` class that alternates sending text and receiving audio.

### 4. Try resumable sessions
Capture the `session_handle`, restart, and resume the conversation.

## Outcome
You'll have a Colab demo that:
* Streams **text→audio replies**
* Plays **native Gemini voice output**
* Continues conversations with **session resumption**

## Question
What challenges arise when moving from **turn-based demos** to **true real-time streaming** (interruptions, async tasks, audio latency)? How might you solve them in production?