import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

chat = llm.invoke("What is the meaning of life")
# print(chat)

#Let us use LangChains

tweet_prompt = PromptTemplate.from_template(
    "You are a content creator. Write me a tweet about {topic}."
    )

tweet_chain = LLMChain(llm=llm, prompt=tweet_prompt, verbose=True)

if __name__=="__main__":
    topic = "how ai is really cool"
    resp = tweet_chain.run(topic=topic)
    # print(resp)

