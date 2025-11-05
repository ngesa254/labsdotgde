# Test the App with System Instructions

## Overview

Now that you've added system instructions to your chatbot, it's time to test how these instructions improve the quality and relevance of the model's responses.

## Testing Instructions

### 1. Restart the Application

Within the terminal, terminate the currently running process by pressing:

```
CTRL+C
```

### 2. Start the Application Again

Re-run the command to start the Streamlit application again:

```shell
streamlit run app.py --browser.serverAddress=localhost --server.enableCORS=false --server.enableXsrfProtection=false --server.port 8080
```

### 3. Refresh the Application

Refresh the Streamlit application. If the Streamlit application is still running, you can simply refresh the web preview page in your browser.

### 4. Ask the Same Question

Try the same question as before:

```
What is the best time of year to go to Iceland?
```

### 5. Compare the Responses

Press **ENTER**. Compare how it responds this time compared to last time.

---

## What to Observe

With system instructions, you should notice:

- **More Professional Tone**: The response should sound more like a travel assistant
- **More Structured Information**: Better organization of the information
- **More Comprehensive**: Additional relevant details about travel considerations
- **More Personalized**: The bot may ask follow-up questions to better understand your needs
- **More Helpful**: Proactive suggestions and recommendations

### Example Differences

**Without System Instructions:**
- Generic, factual response about Iceland's weather and seasons

**With System Instructions:**
- Professional travel assistant tone
- Detailed information about seasons, weather, and activities
- Follow-up questions to personalize recommendations
- Consideration of factors like crowds, pricing, and specific experiences

---

## Try More Questions

Test the improved chatbot with various travel-related questions:

```
I want to plan a week-long trip to Japan with a budget of $3000. What do you recommend?
```

```
What should I pack for a summer trip to Norway?
```

```
Can you suggest some family-friendly destinations in Europe?
```

---

> **💡 Key Insight**  
> System instructions are a powerful way to shape the behavior, tone, and expertise of your LLM application. They act as persistent context that guides every response the model generates.

---

**Next Steps:** In the following steps, you'll learn how to further customize the model's behavior using parameters like temperature and top_p.