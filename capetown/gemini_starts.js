const { GoogleGenerativeAI } = require("@google/generative-ai");
const dotenv = require("dotenv");

// Load environment variables from .env file
dotenv.config();

// Access your API key from environment variables
const apiKey = process.env.API_KEY;

// Initialize Google Generative AI with your API key
const genAI = new GoogleGenerativeAI(apiKey);

async function run() {
    // For text-only input, use the gemini-pro model
    const model = genAI.getGenerativeModel({ model: "gemini-pro"});
  
    const prompt = "Write a story about a magic backpack."
  
    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    console.log(text);
}

run();
