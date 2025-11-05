# Congratulations! 🎉

You have successfully upgraded your Q&A application with **tooling**, a powerful feature that allows your Gemini-powered app to interact with external systems and access real-time information.

---

## Continued Experimentation

There are many options for continuing to optimize your prompt. Here are some to consider:

### Adjust Model Parameters

- **Experiment with `temperature` and `top_p`** and see how it changes the response given by the LLM
- Try extreme values to understand their effects:
  - Very low temperature (0.1) for highly deterministic responses
  - Higher temperature (1.0+) for creative, varied outputs

### Explore Additional Parameters

- Refer to the [`GenerateContentConfig`](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini) in our API reference for a complete list of configurable parameters and their descriptions
- Try defining more parameters and adjusting them to see what happens!
- Some parameters to explore:
  - `max_output_tokens`: Control response length
  - `top_k`: Alternative sampling strategy
  - `candidate_count`: Generate multiple response candidates

### Add More Tools

- Create additional function declarations for other travel-related data:
  - Flight information
  - Hotel availability
  - Local attractions
  - Currency conversion
  - Travel advisories

### Enhance System Instructions

- Refine your system instructions to make the bot even more specialized
- Add specific guidelines for handling edge cases
- Include examples of ideal responses

---

## Recap

In this lab, you did the following:

### ✅ Development Environment

- **Utilized the Cloud Shell Editor and terminal** for development
- Set up a Python virtual environment with `uv`
- Managed dependencies with `requirements.txt`

### ✅ Vertex AI Integration

- **Used the Vertex AI Python SDK** to connect your application to a Gemini model
- Initialized the Vertex AI client with proper authentication
- Learned to use the `genai` library for model interactions

### ✅ Prompt Engineering

- **Applied system instructions** to guide the LLM's responses
- Configured **model parameters** (temperature, top_p) to control output style
- Understood how to balance consistency and creativity

### ✅ Function Calling (Tooling)

- **Learned the concept of tooling** (function calling) and its benefits
- Understood the multi-step process of tool-calling workflows
- Defined a tool for the model using a **function declaration**
- Implemented the **Python function** to provide the tool's logic
- Wrote the code to **handle the model's function call requests** and return the results

### ✅ Best Practices

- **Refactored your code to use a stateful chat session**, a best practice for conversational AI
- Implemented proper error handling
- Used logging for debugging and monitoring
- Organized code with helper functions (`get_chat`)

---

## What You Built

You created a **fully functional travel assistant chatbot** that:

1. ✈️ Provides personalized travel recommendations
2. 🌤️ Fetches real-time weather data
3. 💬 Maintains conversational context across multiple turns
4. 🎯 Follows professional system instructions
5. ⚙️ Uses configurable parameters for optimal responses

---

## Key Concepts Mastered

- **Generative AI Models**: Understanding how to work with large language models
- **System Instructions**: Shaping AI behavior through prompts
- **Model Parameters**: Fine-tuning output characteristics
- **Function Calling**: Extending AI capabilities with external tools
- **Chat Sessions**: Managing stateful conversations
- **API Integration**: Connecting to external data sources

---

## Next Steps in Your AI Journey

### Explore More Features

- **Multi-modal inputs**: Add image understanding to your chatbot
- **Streaming responses**: Implement real-time token streaming for faster perceived responses
- **Context caching**: Optimize for repeated system instructions
- **Safety settings**: Configure content filtering and safety controls

### Production Considerations

- **Error handling**: Implement robust error handling and fallbacks
- **Rate limiting**: Add rate limiting to manage API costs
- **User authentication**: Secure your application with proper auth
- **Monitoring**: Set up logging and analytics
- **Scaling**: Deploy to production environments (Cloud Run, App Engine)

### Learn More

- 📚 [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- 🔧 [Gemini API Reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini)
- 💡 [Prompt Engineering Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design)
- 🛠️ [Function Calling Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling)

---

## Clean Up Resources

To avoid incurring charges to your Google Cloud account:

1. **Stop the Streamlit application** (CTRL+C in the terminal)
2. **Delete the project** (optional, if you created a new project for this lab):
   ```shell
   gcloud projects delete PROJECT_ID
   ```
3. **Or disable billing** on the project if you want to keep it

---

## Share Your Success! 🌟

You've built something awesome! Consider:
- Extending this project with additional features
- Sharing your learnings with your team
- Exploring other Gemini models and capabilities
- Building other AI-powered applications

---

> **🎓 Final Thoughts**  
> You now have the foundational skills to build production-ready generative AI applications using Vertex AI and the Gemini model. The techniques you've learned—from basic prompting to advanced function calling—are applicable to a wide range of AI use cases. Keep experimenting, keep learning, and keep building!

---

**Thank you for completing this lab!** 🚀