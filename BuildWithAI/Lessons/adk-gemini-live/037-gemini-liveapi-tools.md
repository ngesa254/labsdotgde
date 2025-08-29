# Lesson 3.7: Multimodal Live API With Tools (Prep Lab)

📓 `gemini_liveapi_tools.ipynb`  
**Colab:** https://colab.research.google.com/drive/1Rn6SM4yKCKftM6zz2EN0P5uNw98vtKmO

## Challenge: Tool Use With the Live API 🎙️🖼️⚡

Add **tools** to your multimodal agent and watch Gemini 2.5 use them in real time.

## Prerequisites
* Completion of Lesson 3.6 (*Live API Fundamentals*)
* Working knowledge of function declarations in ADK (from Lesson 1 & 2)

## Concept
Gemini 2.5 Live API supports:
* **Google Search** (grounding in fresh web results)
* **Code Execution** (write & run Python)
* **Function Declarations** (your custom tools)

Unlike earlier models, all tools in Gemini 2.5 are executed via the **code execution system**, which lets the model chain multiple tools in a single block of reasoning.

## Task

### 1. Register at least one **mock tool** (`get_weather_vegas`) and a **system tool** (`code_execution`).

### 2. Test **blocking vs. non-blocking** behavior (`BLOCKING`, `INTERRUPT`, `WHEN_IDLE`, `SILENT`).

### 3. Combine tools: let Gemini calculate a math problem, fetch live search results, and call your function in a single interaction.

## Prompts to Try
* "What's the weather in Vegas? In the meantime tell me about Paris casino."
* "Compute the largest prime palindrome under 100000 and search for the latest earthquake in California."

## Outcome
You'll see **async function calling**, **interruptible responses**, and multi-tool reasoning in action.

## Question
What scenarios benefit most from **non-blocking async function calling**? How would you integrate this into a production agent (e.g., event assistants, customer support)?