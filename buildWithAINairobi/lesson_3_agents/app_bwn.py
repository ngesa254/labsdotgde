# Imports
import os
import logging
import re
import time
from typing import Dict, List, Optional, Any
import json
import requests # Make sure this is imported
from bs4 import BeautifulSoup # Still useful for Lagos and potentially description cleaning
from dataclasses import dataclass
from dotenv import load_dotenv
from datetime import datetime
import ast # For parsing JavaScript object string

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Google GenAI dependencies
try:
    import google.generativeai as genai

    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable not set or .env file not loaded.")
        raise ValueError("GEMINI_API_KEY not found. Check .env file and ensure python-dotenv is installed.")
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("✅ Initialized Google GenAI Client")

except ImportError as e:
    logger.error(f"Error importing Google GenAI dependencies: {e}")
    logger.error("Please install the required package using: pip install google-generativeai python-dotenv")
    raise
except ValueError as e:
    logger.error(e)
    raise


@dataclass
class DevFestSession:
    """Data class for storing session information"""
    title: str
    speaker: str
    time: str
    track: str
    day: str
    room: str
    session_type: str

# Initialize LLM model
try:
    MODEL_NAME = "gemini-1.5-pro-latest"
    llm = genai.GenerativeModel(MODEL_NAME)
    logger.info(f"✅ Initialized Google GenAI Model: {MODEL_NAME}")
except Exception as e:
    logger.error(f"Error initializing Google GenAI Model ({MODEL_NAME}): {e}")
    try:
        MODEL_NAME = "gemini-1.5-flash-latest" # Fallback
        llm = genai.GenerativeModel(MODEL_NAME)
        logger.info(f"✅ Initialized Google GenAI Model with fallback: {MODEL_NAME}")
    except Exception as e_fallback:
        logger.error(f"Error initializing fallback Google GenAI Model ({MODEL_NAME}): {e_fallback}")
        raise

# ================================
# LAGOS SCRAPER FUNCTIONS
# (Keep your existing Lagos scraper as is)
# ================================
def get_devfest_lagos_schedule() -> Dict[str, List[Dict]]:
    """
    Scrape and return the DevFest Lagos schedule as JSON data.
    Returns a dictionary with days as keys and lists of session information as values.
    """
    schedule = {'day1': [], 'day2': []}
    try:
        session_http = requests.Session()
        session_http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
        response = session_http.get("https://2024.devfestlagos.com/schedule")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        schedule_container = soup.find('div', class_='schedule_scheduleItemsContainer__wkWNt')
        
        current_day_key = 'day1'

        if schedule_container:
            general_events = schedule_container.find_all('div', class_='EventBlock_event__UsJua')
            for event_block in general_events:
                title_tag = event_block.find('h3')
                time_tag = event_block.find('div', class_='EventBlock_time__RQGQz')
                venue_tag_container = event_block.find('div', class_='EventBlock_venue__wjpVu')
                venue_span = venue_tag_container.find('span') if venue_tag_container else None
                
                room_text = "Main Hall"
                if venue_span and venue_span.text.strip():
                    room_text = venue_span.text.strip()
                elif venue_tag_container and venue_tag_container.text.strip():
                    room_text = venue_tag_container.text.strip()

                session_info = {
                    'title': title_tag.text.strip() if title_tag else "No Title",
                    'time': time_tag.text.strip() if time_tag else "Time not specified",
                    'room': room_text,
                    'speaker': "N/A",
                    'track': "General",
                    'session_type': "General",
                    'day': current_day_key,
                    'description': ""
                }
                if "keynote" in session_info['title'].lower():
                    session_info['session_type'] = "Keynote"
                elif "break" in session_info['title'].lower() or "lunch" in session_info['title'].lower() or "networking" in session_info['title'].lower():
                    session_info['session_type'] = "Break/Networking"
                elif "registration" in session_info['title'].lower():
                    session_info['session_type'] = "Admin/Opening"
                schedule[current_day_key].append(session_info)

            breakout_schedule_container = schedule_container.find('div', class_='EventCategory_eventSchedule__events__cCu22')
            if breakout_schedule_container:
                breakout_events = breakout_schedule_container.find_all('div', class_='EventCategory_eventSchedule__event__AhbY3')
                for event_block in breakout_events:
                    title_tag = event_block.find('h3', class_='EventCategory_eventSchedule__event-title__F2air')
                    speaker_tag = event_block.find('p', class_='EventCategory_eventSchedule__event-facilitator__nWvuU')
                    time_tag_container = event_block.find('div', class_='EventCategory_eventSchedule__event-time__f_zfq')
                    time_span = time_tag_container.find('span', class_ = 'text-sm') if time_tag_container else None

                    session_info = {
                        'title': title_tag.text.strip() if title_tag else "No Title",
                        'speaker': speaker_tag.text.strip() if speaker_tag else "Not specified",
                        'time': time_span.text.strip() if time_span else (time_tag_container.text.strip() if time_tag_container else "Time not specified"),
                        'room': "Breakout Room",
                        'track': "Breakout",
                        'session_type': "Breakout Session",
                        'day': current_day_key,
                        'description': ""
                    }
                    schedule[current_day_key].append(session_info)
        
        if not schedule.get('day2'):
            schedule.pop('day2', None)
        if not schedule.get('day1') and not schedule.get('day2'):
             logger.warning("Lagos scraper finished but found 0 sessions overall.")

        if schedule.get('day1'):
            def sort_key_lagos(session_dict):
                time_str = session_dict.get('time', '12:00 AM - 12:00 AM').split(' - ')[0].strip()
                try:
                    return datetime.strptime(time_str, "%I:%M %p")
                except ValueError:
                    try: 
                        return datetime.strptime(time_str, "%H:%M")
                    except ValueError:
                        return datetime.min 
            schedule['day1'].sort(key=sort_key_lagos)
            logger.info("Lagos: Successfully sorted Day 1 sessions by time.")

        logger.info(f"Scraped {sum(len(s) for s in schedule.values())} sessions for DevFest Lagos.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error during HTTP request for Lagos schedule: {str(e)}")
        return {'day1': []} 
    except Exception as e:
        logger.error(f"Error scraping Lagos schedule: {str(e)}", exc_info=True)
        return {'day1': []} 
    return schedule

# ================================
# NAIROBI SCRAPER FUNCTIONS
# (New version based on your working JS object extraction)
# ================================
def get_devfest_nairobi_schedule() -> Dict[str, List[Dict]]:
    """
    Fetch and parse the DevFest Nairobi schedule by extracting
    the Globals.eventInfo JavaScript object.
    """
    schedule_output: Dict[str, List[Dict]] = {'day1': []}
    url = "https://gdg.community.dev/events/details/google-gdg-nairobi-presents-devfest-nairobi-2024-1/"
    
    logger.info(f"Nairobi Scraper (JS Object): Fetching schedule from: {url}")

    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
        response.raise_for_status()
        
        # Extract the JavaScript object containing the schedule
        js_pattern = r'Globals\.eventInfo\s*=\s*({.*?});' # {.*?}); is non-greedy
        js_match = re.search(js_pattern, response.text, re.DOTALL)
        
        if not js_match:
            logger.error("Nairobi Scraper (JS Object): Could not find Globals.eventInfo object in page source.")
            return schedule_output # Return empty
            
        event_info_str = js_match.group(1)
        
        try:
            # Basic replacements to make it more Python-like before ast.literal_eval
            # ast.literal_eval is safer than eval() for untrusted strings
            event_info_str_py = event_info_str.replace('false', 'False').replace('true', 'True').replace('null', 'None')
            # Remove trailing commas before closing braces/brackets if any (can cause issues with ast)
            event_info_str_py = re.sub(r',\s*([\}\]])', r'\1', event_info_str_py)

            event_info = ast.literal_eval(event_info_str_py)
            
            agenda_data = event_info.get('agenda', {})
            days_data = agenda_data.get('days', [])
            
            if not days_data:
                logger.warning("Nairobi Scraper (JS Object): No 'days' data found within agenda in Globals.eventInfo.")
                return schedule_output
                
            # Assuming single day event for now, or take the first day
            day_data = days_data[0] 
            day_agenda_items = day_data.get('agenda', []) # 'agenda' key within the day object
            
            if not day_agenda_items:
                logger.warning("Nairobi Scraper (JS Object): No session items found in 'days'[0]['agenda'].")
                return schedule_output

            for session_js in day_agenda_items:
                activity = session_js.get('activity', '')
                description_from_js = session_js.get('description', '') # This is often speaker names

                room = ""
                title = activity
                
                room_match = re.match(r'\[([^\]]+)\]\s*(.*)', activity)
                if room_match:
                    room = room_match.group(1).strip()
                    title = room_match.group(2).strip()
                
                # Speaker extraction from description_from_js (which seems to hold speaker names in this object)
                # The description_from_js field seems to contain speaker names separated by " & " or on new lines.
                # Let's try splitting by common separators if it's a multi-speaker string.
                speakers = []
                if description_from_js:
                    # Clean up HTML if any (though less likely in JS object strings)
                    desc_soup = BeautifulSoup(description_from_js, 'html.parser')
                    cleaned_desc_text = desc_soup.get_text(separator=' & ', strip=True) # Use & as a common separator
                    
                    # Split by ' & ' or handle simple cases
                    potential_speakers = [s.strip() for s in cleaned_desc_text.split(' & ') if s.strip()]
                    speakers = [s for s in potential_speakers if len(s) < 70] # Avoid very long "speakers"

                speaker_str = " & ".join(speakers) if speakers else "N/A"


                session_data = {
                    'title': title.strip(),
                    'time': session_js.get('time', 'Time not specified').strip(),
                    'room': room.strip() if room else "Main Hall", # Default if no room extracted
                    'speaker': speaker_str,
                    'description': "", # The 'description' in JS object seems to be speakers. Actual description needs separate handling if present.
                    'audience_type': session_js.get('audience_type', 'IN_PERSON'), # from your example
                    'day': "Day 1", # Assuming first day from days_data[0]
                    # Track and Session Type Inference (can be improved)
                    'track': "General", 
                    'session_type': "Talk" 
                }

                # Infer Track and Session Type based on title/room
                title_lower = session_data['title'].lower()
                room_lower = session_data['room'].lower()

                if "malewa hall" in room_lower: session_data['track'] = "Track 1 (Malewa)"
                elif "main hall" in room_lower: session_data['track'] = "Track 2 (Main)" # Default if not specific
                elif "turkwell hall" in room_lower: session_data['track'] = "Track 3 (Turkwell)"
                elif "rooftop hall" in room_lower: session_data['track'] = "Track 4 (Rooftop)"
                
                if "ai" in title_lower or "gemini" in title_lower: session_data['track'] = "AI"
                elif "dsa" in title_lower or "problem-solving" in title_lower : session_data['track'] = "CS Fundamentals"
                elif "cloud" in title_lower: session_data['track'] = "Cloud"
                elif "web" in title_lower or "angular" in title_lower: session_data['track'] = "Web"
                elif "android" in title_lower: session_data['track'] = "Android"
                elif "flutter" in title_lower or "firebase" in title_lower: session_data['track'] = "Mobile/Firebase"


                if "keynote" in title_lower: session_data['session_type'] = "Keynote"
                elif "workshop" in title_lower or "hands-on" in title_lower: session_data['session_type'] = "Workshop"
                elif "registration" in title_lower or "welcome" in title_lower or "intro" in title_lower: session_data['session_type'] = "Admin/Opening"
                elif "closing remarks" in title_lower: session_data['session_type'] = "Closing"
                elif "lunch" in title_lower or "networking" in title_lower or "photo session" in title_lower or "q&a" in title_lower: session_data['session_type'] = "General/Networking"
                elif "partner session" in title_lower: session_data['session_type'] = "Partner Session"


                schedule_output['day1'].append(session_data)
                
            logger.info(f"Nairobi Scraper (JS Object): Successfully processed {len(schedule_output['day1'])} sessions.")

            if schedule_output.get('day1'):
                def sort_key_nairobi_js(session_dict):
                    try:
                        time_str = session_dict.get('time', '12:00 AM').split(' - ')[0].strip() # Handle ranges if any
                        return datetime.strptime(time_str, "%I:%M %p") # Expecting "8:00 AM"
                    except ValueError:
                        try: # Try H:M format if I:M %p fails
                             return datetime.strptime(time_str, "%H:%M")
                        except ValueError:
                            return datetime.min 
                schedule_output['day1'].sort(key=sort_key_nairobi_js)
                logger.info("Nairobi Scraper (JS Object): Successfully sorted sessions by time.")
            
        except ast.literal_eval_error as ae:
            logger.error(f"Nairobi Scraper (JS Object): Error parsing JS object string with ast.literal_eval: {ae}")
            logger.debug(f"Problematic string for ast.literal_eval: {event_info_str_py[:1000]}...") # Log part of string
            return schedule_output # Return empty
        except Exception as e_parse:
            logger.error(f"Nairobi Scraper (JS Object): Error processing parsed event info: {e_parse}", exc_info=True)
            return schedule_output # Return empty
            
    except requests.exceptions.RequestException as e_req:
        logger.error(f"Nairobi Scraper (JS Object): HTTP Request error: {e_req}")
        return schedule_output
    except Exception as e_main:
        logger.error(f"Nairobi Scraper (JS Object): An unexpected error occurred: {e_main}", exc_info=True)
        return schedule_output
        
    return schedule_output

# ================================
# HELPER AND ASSISTANT CLASSES/FUNCTIONS
# (Keep these as they were in your "scraper-only" version)
# ================================

def format_schedule_to_text(schedule_data: Dict[str, List[Dict]], event_name: str) -> str:
    if not schedule_data or not any(day_sessions for day_sessions in schedule_data.values()):
        return f"No schedule data currently available for {event_name} from the official source."

    text_parts = [f"Schedule for {event_name}:\n"]
    for day, sessions in schedule_data.items():
        if not sessions: continue
        text_parts.append(f"\n--- {day.replace('day', 'Day ')} ---")
        
        # Sessions should be sorted by the scraper functions
        for session in sessions: # Assumes sessions are pre-sorted
            session_info = [
                f"Title: {session.get('title', 'N/A')}",
                f"Time: {session.get('time', 'N/A')}",
                f"Room: {session.get('room', 'N/A')}",
                f"Speaker: {session.get('speaker', 'N/A')}",
                f"Track: {session.get('track', 'General')}",
                f"Session Type: {session.get('session_type', 'Session')}",
            ]
            # Use the 'description' field we intend for actual descriptions, not the one from JS object that had speakers
            if session.get('description') and str(session.get('description')).strip(): 
                session_info.append(f"Description: {str(session.get('description')).strip()}")
            if session.get('audience_type'):
                session_info.append(f"Audience: {session.get('audience_type')}")

            text_parts.append("\n" + "\n".join(session_info))
            text_parts.append("-" * 20)
    return "\n".join(text_parts)


class DevFestDataProvider:
    def __init__(self, event_location="Lagos"):
        self.schedule_data_raw: Optional[Dict[str, List[Dict]]] = None
        self.schedule_data_text: Optional[str] = None
        self.event_location = event_location
        self.event_name = f"DevFest {event_location} 2024" 

    def get_schedule_raw(self) -> Dict[str, List[Dict]]:
        if self.schedule_data_raw is None:
            if self.event_location.lower() == "lagos":
                self.schedule_data_raw = get_devfest_lagos_schedule()
                logger.info(f"Retrieved Lagos schedule with {sum(len(day_sessions) for day_sessions in self.schedule_data_raw.values())} sessions")
            elif self.event_location.lower() == "nairobi":
                self.schedule_data_raw = get_devfest_nairobi_schedule() # Calls the new JS object scraper
                logger.info(f"Retrieved Nairobi schedule with {sum(len(day_sessions) for day_sessions in self.schedule_data_raw.values())} sessions")
            else:
                logger.error(f"Unknown event location: {self.event_location}")
                self.schedule_data_raw = {"day1": []} 
        return self.schedule_data_raw

    def get_schedule_text(self) -> str:
        if self.schedule_data_text is None:
            raw_data = self.get_schedule_raw()
            self.schedule_data_text = format_schedule_to_text(raw_data, self.event_name)
            if "No schedule data currently available" not in self.schedule_data_text :
                logger.info(f"Formatted schedule for {self.event_name} into text.")
            else:
                logger.warning(f"No schedule data was available to format for {self.event_name}.")
        return self.schedule_data_text

    def save_schedule_json(self, filename: str = None):
        if filename is None:
            filename = f"devfest_{self.event_location.lower()}_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        schedule_data = self.get_schedule_raw()
        if not any(schedule_data.values()): 
            logger.info(f"No schedule data to save for {self.event_location}.")
            return
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Raw schedule saved to {filename}")
        except Exception as e:
            logger.error(f"Could not save schedule to {filename}: {e}")

    def display_schedule_raw(self, show_details: bool = False):
        print(f"\n=== {self.event_name} Schedule (Raw Scraped) ===\n")
        schedule_data = self.get_schedule_raw()
        display_raw_schedule_data(schedule_data, show_details)


def display_raw_schedule_data(schedule_data: Dict[str, List[Dict]], show_details: bool = True):
    if not schedule_data or not any(day_sessions for day_sessions in schedule_data.values()):
        print("\nNo schedule data available to display (scraper might have found nothing or failed).")
        return

    for day, sessions in schedule_data.items():
        if not sessions: continue
        print(f"\n=== {day.replace('day', 'Day ')} ===")
        for session in sessions: # Assumes pre-sorted
            print(f"  Time: {session.get('time', 'N/A')}")
            print(f"  Title: {session.get('title', 'N/A')}")
            if session.get('room'):
                print(f"  Room: {session.get('room')}")
            if session.get('speaker') and session.get('speaker') != 'N/A':
                print(f"  Speaker: {session.get('speaker')}")
            if session.get('track') and session.get('track') != 'General':
                 print(f"  Track: {session.get('track')}")
            if session.get('session_type'):
                print(f"  Type: {session.get('session_type')}")
            if show_details and session.get('description') and str(session.get('description')).strip():
                print(f"  Description: {str(session.get('description')).strip()}")
            print("  " + "-" * 40)


class DevFestAssistant:
    def __init__(self):
        self.lagos_provider = DevFestDataProvider(event_location="Lagos")
        self.nairobi_provider = DevFestDataProvider(event_location="Nairobi")
        self.llm = llm 
        logger.info("DevFestAssistant initialized.")

    def query(self, query_text: str):
        logger.info(f"Received query: {query_text}")
        query_lower = query_text.lower()
        context_parts = []
        prompt_intro = "You are a helpful DevFest Schedule Assistant.\n"

        use_lagos = "lagos" in query_lower
        use_nairobi = "nairobi" in query_lower
        needs_schedule_keywords = ["session", "talk", "speaker", "track", "workshop", "keynote", "schedule", "agenda", "when is", "what time", "who is speaking", "room for"]
        implies_need_for_schedule = any(keyword in query_lower for keyword in needs_schedule_keywords)

        lagos_text = ""
        nairobi_text = ""

        if use_lagos:
            lagos_text = self.lagos_provider.get_schedule_text()
            if "No schedule data currently available" not in lagos_text:
                context_parts.append(lagos_text)
        if use_nairobi:
            nairobi_text = self.nairobi_provider.get_schedule_text()
            if "No schedule data currently available" not in nairobi_text:
                context_parts.append(nairobi_text)

        if use_lagos and use_nairobi:
            prompt_intro += "You have access to DevFest schedules for BOTH Lagos and Nairobi if available from their official sources.\n"
            if not context_parts: 
                print("Assistant: I currently don't have schedule details for either DevFest Lagos or DevFest Nairobi from their official sources. Please check back later or visit their official websites.")
                return "I currently don't have schedule details for either DevFest Lagos or DevFest Nairobi from their official sources. Please check back later or visit their official websites."
        elif use_lagos:
            prompt_intro += "You have access to the DevFest Lagos schedule if available from its official source.\n"
            if not context_parts: 
                print("Assistant: I currently don't have schedule details for DevFest Lagos from the official source. Please check back later or visit the official DevFest Lagos website.")
                return "I currently don't have schedule details for DevFest Lagos from the official source. Please check back later or visit the official DevFest Lagos website."
        elif use_nairobi:
            prompt_intro += "You have access to the DevFest Nairobi schedule if available from its official source.\n"
            if not context_parts: 
                print("Assistant: I currently don't have schedule details for DevFest Nairobi from the official source (the scraper couldn't fetch it or it's not published yet). Please check the official DevFest Nairobi website for the latest updates.")
                return "I currently don't have schedule details for DevFest Nairobi from the official source (the scraper couldn't fetch it or it's not published yet). Please check the official DevFest Nairobi website for the latest updates."
        
        elif not use_lagos and not use_nairobi and implies_need_for_schedule:
            clarification_message = "To help you with schedule information, could you please specify whether you're interested in DevFest Lagos or DevFest Nairobi?"
            logger.info("Query implies need for schedule but no city specified. Asking for clarification.")
            print(f"Assistant: {clarification_message}")
            return clarification_message
        
        context_string = "\n\n".join(context_parts)
        
        if not context_string.strip() and (use_lagos or use_nairobi or implies_need_for_schedule):
            no_data_response = "It seems I don't have detailed schedule data for the requested location(s) from the official sources at the moment. Please try again later or check the official DevFest website(s)."
            logger.warning("No actual schedule data to provide to LLM for a specific query after filtering.")
            print(f"Assistant: {no_data_response}")
            return no_data_response
        
        if context_string.strip(): 
            final_prompt = f"""
{prompt_intro}
Answer the user's question based *only* on the provided schedule information below.
If the information to answer the question is not in the schedule, clearly state that "Based on the currently available schedule, that information is not listed."
Do not make up information or assume details not present.

--- START OF SCHEDULE DATA ---
{context_string}
--- END OF SCHEDULE DATA ---

User Question: {query_text}

Assistant Response:
"""
        else: 
            final_prompt = f"""
You are a helpful DevFest Schedule Assistant.
The user asked: "{query_text}"
This query does not specify a DevFest location (e.g., Lagos or Nairobi) and might be a general question.
Please respond to the user.
If the question can be answered generally about DevFests without needing specific schedules (e.g., "What is a DevFest?"), please do so.
If you suspect they MIGHT need schedule data but didn't ask directly (e.g. "Tell me about AI"), you can briefly answer generally and then offer to provide schedule details if they specify a location.
Do not invent schedule details if none were provided for context.
"""
            logger.info("General query, no city. Using general LLM prompt without specific schedule context.")

        logger.info("Sending query to LLM.")
        if context_string.strip():
            logger.debug(f"LLM Context included (first 500 chars): {context_string[:500]}...") 
        else:
            logger.debug("LLM Context is empty (general query or no data found by scrapers).")

        print(f"Assistant: ", end="")
        full_response_text = ""
        try:
            if not hasattr(self.llm, 'generate_content'):
                logger.error("LLM object is not correctly initialized or is not a GenerativeModel instance.")
                raise TypeError("LLM not properly initialized.")

            response_stream = self.llm.generate_content(final_prompt, stream=True)
            for chunk in response_stream:
                print(chunk.text, end="", flush=True)
                full_response_text += chunk.text
            print() 
        except Exception as e:
            logger.error(f"Error during GenAI call: {e}", exc_info=True)
            error_message = f"\nSorry, I encountered an error processing your request. Please try again. (Error: {type(e).__name__})"
            print(error_message)
            full_response_text = f"Error: {e}"
        return full_response_text

def main():
    print("\n=== DevFest Schedule Assistant (Google GenAI Version - Scraper Only) ===")
    print("Initializing assistant...")
    
    # Optional: Test scrapers directly at the start
    # print("\n--- Direct Scraper Test: Lagos ---")
    # lagos_test_data = get_devfest_lagos_schedule()
    # display_raw_schedule_data(lagos_test_data, show_details=True)
    # if any(lagos_test_data.values()):
    #     with open(f"devfest_lagos_scraped_initial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f: json.dump(lagos_test_data, f, indent=2)

    # print("\n--- Direct Scraper Test: Nairobi ---") # This will now use the JS object scraper
    # nairobi_test_data = get_devfest_nairobi_schedule()
    # display_raw_schedule_data(nairobi_test_data, show_details=True)
    # if any(nairobi_test_data.values()):
    #     with open(f"devfest_nairobi_scraped_initial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f: json.dump(nairobi_test_data, f, indent=2)
    # print("-" * 50)

    try:
        assistant = DevFestAssistant()
    except Exception as e:
        logger.critical(f"Failed to initialize DevFestAssistant: {e}", exc_info=True)
        print(f"Critical error: Could not start the assistant. Please check logs. Error: {e}")
        return

    example_queries = [
        "Find me sessions about AI and machine learning in DevFest Nairobi",
        "What web development talks are available at DevFest Lagos?",
        "Compare the keynote sessions between Lagos and Nairobi DevFest events.",
        "What is DevFest?",
        "Are there any workshops in Nairobi?",
        "Tell me about the speakers for 'Building Web Apps That Work Offline and Beyond' in Lagos.",
        "Any sessions on Firebase in Lagos?"
    ]

    print("\nReady to answer questions!")
    
    for i, query_str in enumerate(example_queries):
        print(f"\n--- Example Query {i+1} ---")
        print(f"User: {query_str}")
        assistant.query(query_str)
        if i < len(example_queries) -1: 
            time.sleep(1.1) # Slightly increased to be safe with API calls

    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_query = input("\nEnter your query (or 'exit' to quit): ")
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("Exiting assistant. Goodbye!")
                break
            if not user_query.strip():
                continue
            assistant.query(user_query)
        except KeyboardInterrupt:
            print("\nExiting assistant. Goodbye!")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred in the interactive loop: {e}", exc_info=True)
            print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()
