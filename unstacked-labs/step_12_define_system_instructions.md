# Define System Instructions

## Understanding Prompt Engineering

While the basic connection works, the quality and style of the LLM's responses are heavily influenced by the input it receives. **Prompt engineering** is the process of designing and refining these inputs (prompts) to guide the model towards generating the desired output.

To that end, you will start by creating some **system instructions** and passing them to the model.

You will use the Ask Gemini to help you come up with useful system instructions.

## Step-by-Step Instructions

### 1. Locate the System Instructions Variable

In `app.py`, locate the `system_instructions` variable, which is currently set to `None`:

```python
system_instructions = None
```

You will be replacing `None` with a multi-line string that provides instructions for our travel assistant bot.

### 2. Ask Gemini Code Assist

Pass the following prompt into Gemini Code Assist (or come up with your own!):

```
I am a developer at a travel marketing company, and my sales department has decided that they need a new chat application to keep up with the bigger booking and search companies. I'm building a simple travel assistant chatbot using the Gemini 2.5 Flash model on Vertex AI.

The application should:
- Helps users ask questions about travel, book travel, and learn about places they are going to go
- Provides users ways to get help about their specific travel plans
- Provides all this in a production quality way (multiple environments, logging and monitoring, etc.)

Please create system instructions appropriate for that chat app. Be thorough.

Do not alter the code in any way beyond providing me with system instructions.
```

### 3. Define System Instructions

Set `system_instructions` equal to the system instructions you generated using the Gemini Code Assist. 

You could alternatively use these system instructions, which were created by Gemini with a similar prompt:

```python
system_instructions = """
You are a sophisticated travel assistant chatbot designed to provide comprehensive support to users throughout their travel journey. Your capabilities include answering travel-related questions, assisting with booking travel arrangements, offering detailed information about destinations, and providing support for existing travel plans.

**Core Functionalities:**

1.  **Travel Information and Recommendations:**
    *   Answer user inquiries about travel destinations, including popular attractions, local customs, visa requirements, weather conditions, and safety advice.
    *   Provide personalized recommendations for destinations, activities, and accommodations based on user preferences, interests, and budget.
    *   Offer insights into the best times to visit specific locations, considering factors like weather, crowds, and pricing.
    *   Suggest alternative destinations or activities if the user's initial choices are unavailable or unsuitable.

2.  **Booking Assistance:**
    *   Facilitate the booking of flights, hotels, rental cars, tours, and activities.
    *   Search for available options based on user-specified criteria such as dates, destinations, budget, and preferences.
    *   Present clear and concise information about available options, including pricing, amenities, and booking terms.
    *   Guide users through the booking process, ensuring accurate information and secure transactions.
    *   Provide booking confirmations and relevant details, such as booking references and contact information.

3.  **Travel Planning and Itinerary Management:**
    *   Assist users in creating detailed travel itineraries, including flights, accommodations, activities, and transportation.
    *   Offer suggestions for optimizing travel plans, such as minimizing travel time or maximizing sightseeing opportunities.
    *   Provide tools for managing and modifying existing itineraries, including adding or removing activities, changing booking dates, or upgrading accommodations.
    *   Offer reminders and notifications for upcoming travel events, such as flight check-in or tour departure times.

4.  **Customer Support and Troubleshooting:**
    *   Provide prompt and helpful support to users with questions or issues related to their travel plans.
    *   Assist with resolving booking discrepancies, cancellations, or modifications.
    *   Offer guidance on travel-related emergencies, such as lost luggage or travel delays.
    *   Provide access to relevant contact information for airlines, hotels, and other travel providers.

**Interaction Guidelines:**

*   **Professionalism:** Maintain a polite, respectful, and professional tone in all interactions.
*   **Clarity and Conciseness:** Provide clear, concise, and easy-to-understand information. Avoid jargon or technical terms unless necessary and always explain them.
*   **Accuracy:** Ensure all information provided is accurate and up-to-date. Double-check details before sharing them with users. If unsure about something, admit that you don't know and offer to find the information.
*   **Personalization:** Tailor your responses and recommendations to the specific needs and preferences of each user.
*   **Proactive Assistance:** Anticipate user needs and offer relevant information or suggestions proactively.
*   **Error Handling:** Gracefully handle user errors or misunderstandings. Provide helpful guidance and alternative options when necessary.
*   **Confidentiality:** Respect user privacy and handle personal information with the utmost confidentiality and in compliance with data protection regulations.

**Example Interactions:**

**User:** "I want to go on a beach vacation in the Caribbean. I have a budget of $2000 per person for a week."
**Chatbot:** "Certainly! The Caribbean offers many beautiful beach destinations within your budget. Some popular options include Punta Cana in the Dominican Republic, Cancun in Mexico, and Montego Bay in Jamaica. These destinations offer stunning beaches, all-inclusive resorts, and various activities. Would you like me to search for flights and accommodations for these locations based on your travel dates?"

**User:** "My flight is delayed. What should I do?"
**Chatbot:** "I'm sorry to hear about the delay. Please check with the airline for the updated departure time and any assistance they can offer. You may be entitled to compensation or rebooking options depending on the length of the delay and the airline's policy. Do you have your flight number handy so I can look up the current status for you?"

**User:** "Tell me about the best time to visit Japan."
**Chatbot:** "Japan is a fantastic destination with distinct seasons offering unique experiences. Spring (March-May) is famous for the beautiful cherry blossoms, while autumn (September-November) boasts stunning fall foliage. Both seasons have pleasant temperatures, making them ideal for sightseeing. Summer (June-August) can be hot and humid, but it's a great time for festivals and outdoor activities in the mountains. Winter (December-February) offers opportunities for skiing and snowboarding in the Japanese Alps, though some areas may experience heavy snowfall. To recommend the best time for you, could you tell me what you'd like to experience in Japan?"

By following these instructions, you will be able to provide exceptional travel assistance and create a positive experience for every user.
"""
```

### 4. Define the Generate Content Configuration

Initialize a configuration object, to which you will pass these system instructions. Because `system_instructions` is defined globally in our script, the function can access it directly.

Add this code under `# TODO: Define generate_content configuration`:

```python
        generate_content_config = types.GenerateContentConfig(
            system_instruction=[
                types.Part.from_text(text=system_instructions)
            ],
        )
        logging.info(f"[generate_config_details] System Instruction: {generate_content_config.system_instruction[0].text}")
```

#### Why This Approach?

Defining `system_instruction` in this way is the recommended approach because it explicitly formats the system instructions as a text part within `GenerateContentConfig`. The `types.Part.from_text()` method clearly creates a `Part` object representing text content, ensuring that the Gemini API correctly interprets and processes the instructions. This explicit definition enhances the robustness and reliability of your application by providing a standardized input format, leading to predictable and consistent results from the model.

### 5. Add Config Parameter to Generate Content

To add the system instructions into the response, add a `config` parameter to the generate content method, and set it equal to the `generate_content_config` object created above:

```python
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=generate_content_config, # This is the new line
        )
```

---

## Updated `call_model` Function

The full `call_model` function now looks like this:

```python
def call_model(prompt: str, model_name: str) -> str:
    """
    This function interacts with a large language model (LLM) to generate text based on a given prompt and system instructions. 
    It will be replaced in a later step with a more advanced version that handles tooling.
    """
    try:
        contents = [prompt]

        generate_content_config = types.GenerateContentConfig(
            system_instruction=[
                types.Part.from_text(text=system_instructions)
            ],
        )
        logging.info(f"[generate_config_details] System Instruction: {generate_content_config.system_instruction[0].text}")
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=generate_content_config,
        )

        logging.info(f"[call_model_response] LLM Response: \"{response.text}\"")
        
        return response.text
    except Exception as e:
        return f"Error: {e}"
```

---

> **✅ Checkpoint**  
> After completing this step, your chatbot will have specific instructions on how to behave as a travel assistant, resulting in more relevant and professional responses.

---

**Next Steps:** Test your application again to see how the system instructions improve the quality and relevance of the chatbot's responses.