import datetime
import random
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def roll_dice(sides: int) -> dict:
    """Rolls a dice with the specified number of sides and returns the result.
    
    Args:
        sides (int): The number of sides on the dice (must be a positive integer).
    
    Returns:
        dict: status and result containing the dice roll outcome, or error message.
    """
    if not isinstance(sides, int) or sides < 1:
        return {
            "status": "error",
            "error_message": "Number of sides must be a positive integer (1 or greater)."
        }
    
    roll_result = random.randint(1, sides)
    return {
        "status": "success",
        "report": f"Rolled a {sides}-sided dice and got: {roll_result}"
    }


# def get_weather(city: str) -> dict:
#     """Retrieves the current weather report for a specified city.
     
#     Args:
#         city (str): The name of the city for which to retrieve the weather report.
     
#     Returns:
#         dict: status and result or error msg.
#     """
#     if city.lower() == "new york":
#         return {
#             "status": "success",
#             "report": (
#                 "The weather in New York is sunny with a temperature of 25 degrees"
#                 " Celsius (77 degrees Fahrenheit)."
#             ),
#         }
#     else:
#         return {
#             "status": "error",
#             "error_message": f"Weather information for '{city}' is not available.",
#         }


# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city.
     
#     Args:
#         city (str): The name of the city for which to retrieve the current time.
     
#     Returns:
#         dict: status and result or error msg.
#     """
    
#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {
#             "status": "error",
#             "error_message": (
#                 f"Sorry, I don't have timezone information for {city}."
#             ),
#         }
    
#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     report = (
#         f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
#     )
#     return {"status": "success", "report": report}




root_agent = Agent(
    name='root_agent',
    model="gemini-2.0-flash",
    description='Agent to answer questions and roll dice.',
    instruction='You are a helpful agent who can roll dice with any number of sides for games or random number generation.',
    tools=[roll_dice],
)