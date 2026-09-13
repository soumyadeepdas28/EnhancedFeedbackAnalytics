from pathlib import Path
from typing import Any

from fastmcp import FastMCP
import pandas as pd


mcp = FastMCP("feedback_analytics")

@mcp.resource("feedback://get_feedback_list")
def fetch_feedback_list():

    path = Path(__file__).with_name("hotel_booking_feedback.xlsx")

    if not path.is_file():
        raise FileNotFoundError(f"Feedback workbook not found: {path}")

    try:
        df = pd.read_excel(path)

    except Exception as error:
        return f"Unable to read feedback workbook: {error}"

    return df.to_json(orient='records')


@mcp.tool()
def get_feedback_by_category(category: str, data: list[dict]):
    if(len(category)<=0):
        return data 

    df = pd.DataFrame(data)

    categories = ["Application UI", "User-friendly", "Billing", "Rooms", "Customer Assistance"]
    if category not in categories:
        return "Invalid Category entered"
    if(len(df)<=0):
        return "Dataframe is empty"

    try:

        filtered_df=df[df['Category']==category]

    except KeyError as error:
        return f"Missing column: {error.args[0]}"


    return filtered_df.to_json(orient='records')

@mcp.tool()
def get_feedback_by_sentiment(sentiment: str, data: list[dict]):

    if(len(sentiment)<=0):
        return data
    sentiments=['Positive','Neutral','Negative']

    df = pd.DataFrame(data)


    if sentiment not in sentiments:
        return 'Invalid sentiment entered'

    if(len(df)<=0):

        return 'Dataframe is empty'

    try:
        filtered_df=df[df['Sentiment']==sentiment]
    except KeyError as error:
        return f"Missing column: {error.args[0]}"
    
    
    return filtered_df.to_json(orient='records')


if __name__ == "__main__":

    print('starting feedback analytics server')
    mcp.run(transport="stdio")

    


    



    



    













