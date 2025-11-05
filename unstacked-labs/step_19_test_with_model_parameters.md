# Test with Model Parameters

## Overview

Now that you've added model parameters to control the output style, let's test how they affect the chatbot's responses.

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

### 4. Ask the Same Question

Try the same question as before:

```
I'm looking for something to do in New York today. What do you recommend? Would it be a good day to go to Ellis Island?
```

### 5. Compare the Responses

Press **ENTER**. Compare this response to earlier responses.

---

## What to Observe

With the model parameters configured (`temperature = 0.2`, `top_p = 0.95`), you should notice:

### Response Characteristics

- **More Consistent**: The low temperature (0.2) makes responses more focused and deterministic
- **Professional Tone**: Responses should be more structured and professional
- **Factual Focus**: The model should prioritize accuracy over creativity
- **Less Variation**: Asking the same question multiple times should produce similar (but not identical) responses

### Comparing to Previous Responses

**Without Parameters (Default Behavior):**
- Responses may have varied more in style and structure
- Potentially more creative but less predictable

**With Parameters (temperature=0.2, top_p=0.95):**
- Responses are more focused and consistent
- Better suited for a professional travel assistant
- Maintains reliability while still incorporating real-time weather data

---

## Experiment with Different Parameters

To see how parameters affect output, try modifying the values at the top of `app.py`:

### Test 1: Very Low Temperature (Highly Deterministic)

```python
temperature = 0.1
top_p = 0.8
```

**Expected Result**: Very consistent, focused responses with minimal variation

### Test 2: Higher Temperature (More Creative)

```python
temperature = 0.8
top_p = 0.95
```

**Expected Result**: More varied and creative responses, potentially with more diverse phrasing

### Test 3: High Temperature (Very Creative)

```python
temperature = 1.5
top_p = 1.0
```

**Expected Result**: Highly creative and varied responses, though potentially less focused

> **💡 Tip**  
> After changing parameter values, remember to restart the application and refresh the browser to see the effects!

---

## Finding the Right Balance

For a travel assistant chatbot, the current settings (`temperature = 0.2`, `top_p = 0.95`) strike a good balance:

- **Professional and Reliable**: Low temperature ensures consistent, accurate information
- **Appropriate Variety**: High top_p allows for natural, varied phrasing without sacrificing quality
- **User Trust**: Predictable, factual responses build user confidence in the assistant

---

## Try Additional Questions

Test the parameter effects with various questions:

```
What are the best hotels in Tokyo for families?
```

```
I have a 2-hour layover in Paris. What should I do?
```

```
Can you suggest a 5-day itinerary for Iceland?
```

---

> **✅ Key Understanding**  
> Model parameters are powerful tools for shaping AI behavior. The right parameter settings depend on your use case—assistants benefit from lower temperature for consistency, while creative writing tools might use higher values for variety.

---

**Next Steps:** Congratulations! You've built a fully functional travel assistant chatbot with system instructions, function calling, and customized parameters. In the final steps, you'll learn about cleanup and best practices.