from dotenv import load_dotenv
from google import genai
import json
import os
from pathlib import Path
from fastmcp import Client
import asyncio

load_dotenv()
gemini_client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))




#def process_query(query: str):

async def main():
    server_path = Path(__file__).with_name("Server.py")

    async with Client(server_path) as client:

       

        query = input("Enter your query: ")

        while query.lower() != "exit":
            try:
                resource= await client.read_resource("feedback://get_feedback_list")
                question = await client.get_prompt("get_prompt", {"query": query, "data": json.loads(resource[0].text)})
               # print(f"Question: {question}")
                # print(type(question))
                

                response = await gemini_client.aio.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=question.messages[0].content.text,
                    config = genai.types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=500,
                        top_p=0.8,
                    ),



                )
                print(f"Response: {response.output_text}")



                
            except Exception as e:
                print(f"Error occurred: {e}")
            query = input("Enter your query: ")




            
     



if __name__ == "__main__":
    asyncio.run(main())

    
    

