# Test the Tool-Enabled App

## Overview

Let's see your new feature in action!

---

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

### 4. Ask a Weather-Related Question

Now, ask a question that should trigger your new tool, such as the following:

```
I'm looking for something to do in New York today. What do you recommend? Would it be a good day to go to Ellis Island?
```

### 5. Observe the Results

Press **ENTER**. Compare this response to earlier responses. 

**What's different?**

You should see a response that incorporates the temperature from your function! Check your Cloud Shell terminal as well; you should see print statements confirming your Python function was executed.

---

## What to Look For

### In the Chat Interface

- **Real-time weather data**: The response should include the actual current temperature in New York
- **Contextual recommendations**: The bot should make suggestions based on the weather (e.g., outdoor activities if it's nice, indoor alternatives if it's cold or rainy)
- **Natural integration**: The weather information should be seamlessly woven into the response

### In the Terminal

You should see log messages like:

```
Function to call: get_current_temperature
Arguments: {'location': 'New York'}
```

This confirms that:
1. The model recognized it needed weather information
2. It called your `get_current_temperature` function
3. The function executed and returned the result
4. The model incorporated that result into its response

---

## Try More Weather-Related Questions

Test the tool-calling functionality with various queries:

```
What's the weather like in Paris right now?
```

```
I'm planning to visit London tomorrow. Should I pack warm clothes?
```

```
Is it a good time to go hiking in Denver today?
```

```
Should I bring an umbrella for my trip to Seattle?
```

---

## Understanding What's Happening

When you ask a weather-related question:

1. **User sends message** → "What should I do in New York today?"
2. **Model analyzes** → Recognizes it needs current weather data
3. **Model requests tool** → Returns a `function_call` for `get_current_temperature`
4. **Function executes** → Your Python function calls the weather API
5. **Result returned** → Temperature data sent back to the model
6. **Model responds** → Generates a natural language response incorporating the weather data

This is **function calling** in action!

---

## 🎉 Success!

If you see real-time weather data in your chatbot's responses, congratulations! You've successfully implemented function calling, enabling your chatbot to access live external data.

---

> **💡 Key Achievement**  
> Your travel assistant can now fetch real-time information, making it significantly more useful than a chatbot limited to training data alone. This is a foundational capability for building production-ready AI applications.

---

**Next Steps:** In the following steps, you'll learn how to further customize the model's behavior using parameters like temperature and top_p.