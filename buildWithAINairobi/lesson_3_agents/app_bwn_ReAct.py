# Imports
import os
import logging
import re 
import time
from typing import Dict, List, Optional, Any
import json
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime
import ast
from dotenv import load_dotenv 

# Load environment variables from .env file
load_dotenv()

# Configure logging (should be done early)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LlamaIndex and Google GenAI specific imports
try:
    from llama_index.core import Document, VectorStoreIndex, Settings
    from llama_index.core.agent import ReActAgent
    from llama_index.core.tools import QueryEngineTool, ToolMetadata
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    # --- CORRECTED IMPORT based on documentation ---
    from llama_index.llms.gemini import Gemini 
    # --- END CORRECTION ---
        
except ImportError as e:
    logger.error(f"Error importing LlamaIndex or Gemini LLM dependencies: {e}")
    logger.error("Please ensure you have installed the necessary packages: "
                 "pip install -U llama-index llama-index-llms-gemini llama-index-embeddings-huggingface " # Use llama-index-llms-gemini
                 "beautifulsoup4 requests python-dotenv google-generativeai")
    raise

# Dataclass for scraped sessions
@dataclass
class DevFestSessionFromScraper:
    title: str
    speaker: str
    time: str
    track: str
    day: str
    room: str
    session_type: str
    description: Optional[str] = ""
    audience_type: Optional[str] = "IN_PERSON"


# Initialize models - embed_model and llm (LlamaIndex specific)
try:
    embed_model_name = "BAAI/bge-small-en-v1.5"
    logger.info(f"Initializing HuggingFace embedding model: {embed_model_name}")
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    logger.info(f"✅ Initialized HuggingFace embedding model ({embed_model_name}) successfully")
    
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        # The LlamaIndex Gemini llm might also look for GOOGLE_API_KEY
        GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY") 
        if not GEMINI_API_KEY:
            logger.error("Neither GEMINI_API_KEY nor GOOGLE_API_KEY environment variable not set.")
            raise ValueError("API Key for Google Gemini not found in environment variables (GEMINI_API_KEY or GOOGLE_API_KEY).")
        else:
            logger.info("Using GOOGLE_API_KEY for Gemini.")
    else:
        logger.info("Using GEMINI_API_KEY for Gemini.")

    # Model names for direct Gemini API (not Vertex AI publisher paths)
    # The "models/" prefix is important for the direct API.
    llm_model_name_gemini_api = "models/gemini-1.5-pro-latest" 
    
    try:
        logger.info(f"Initializing LlamaIndex Gemini LLM with model: {llm_model_name_gemini_api} using API Key.")
        # Pass the API key directly as per documentation
        llm = Gemini(model_name=llm_model_name_gemini_api, api_key=GEMINI_API_KEY)
        logger.info(f"✅ Initialized LlamaIndex Gemini LLM with {llm_model_name_gemini_api}")
    except Exception as e_llm:
        logger.warning(f"Failed to initialize LlamaIndex Gemini LLM ({llm_model_name_gemini_api}): {e_llm}")
        try:
            # Fallback model for direct Gemini API
            llm_fallback_gemini_api = "models/gemini-pro" # More stable direct API model
            logger.info(f"Attempting fallback LlamaIndex Gemini LLM: {llm_fallback_gemini_api}")
            llm = Gemini(model_name=llm_fallback_gemini_api, api_key=GEMINI_API_KEY)
            logger.info(f"✅ Initialized LlamaIndex Gemini LLM with {llm_fallback_gemini_api}")
        except Exception as e_fallback1:
            logger.error(f"Failed to initialize fallback LlamaIndex Gemini LLM {llm_fallback_gemini_api}: {e_fallback1}")
            raise 
            
    Settings.embed_model = embed_model
    Settings.llm = llm
    logger.info("✅ LlamaIndex Global Settings updated with embed_model and llm (using Google GenAI API Key via llama-index-llms-gemini).")
    
except Exception as e:
    logger.error(f"Error initializing LlamaIndex models: {e}", exc_info=True)
    raise

# ================================
# SCRAPER FUNCTIONS (Keep your working scrapers for Lagos and Nairobi)
# These are the functions from your previously working app_bwn.py (non-ReAct version)
# ================================
def get_devfest_lagos_schedule() -> Dict[str, List[Dict]]:
    schedule = {'day1': [], 'day2': []}
    try:
        session_http = requests.Session()
        session_http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
        response = session_http.get("https://devfestlagos.com/schedule")
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
                if venue_span and venue_span.text.strip(): room_text = venue_span.text.strip()
                elif venue_tag_container and venue_tag_container.text.strip(): room_text = venue_tag_container.text.strip()
                session_info = {'title': title_tag.text.strip() if title_tag else "No Title", 'time': time_tag.text.strip() if time_tag else "Time not specified",'room': room_text,'speaker': "N/A",'track': "General",'session_type': "General",'day': current_day_key,'description': ""}
                if "keynote" in session_info['title'].lower(): session_info['session_type'] = "Keynote"
                elif any(kw in session_info['title'].lower() for kw in ["break", "lunch", "networking"]): session_info['session_type'] = "Break/Networking"
                elif "registration" in session_info['title'].lower(): session_info['session_type'] = "Admin/Opening"
                schedule[current_day_key].append(session_info)
            breakout_schedule_container = schedule_container.find('div', class_='EventCategory_eventSchedule__events__cCu22')
            if breakout_schedule_container:
                breakout_events = breakout_schedule_container.find_all('div', class_='EventCategory_eventSchedule__event__AhbY3')
                for event_block in breakout_events:
                    title_tag = event_block.find('h3', class_='EventCategory_eventSchedule__event-title__F2air')
                    speaker_tag = event_block.find('p', class_='EventCategory_eventSchedule__event-facilitator__nWvuU')
                    time_tag_container = event_block.find('div', class_='EventCategory_eventSchedule__event-time__f_zfq')
                    time_span = time_tag_container.find('span', class_='text-sm') if time_tag_container else None
                    session_info = {'title': title_tag.text.strip() if title_tag else "No Title",'speaker': speaker_tag.text.strip() if speaker_tag else "Not specified",'time': time_span.text.strip() if time_span else (time_tag_container.text.strip() if time_tag_container else "Time not specified"),'room': "Breakout Room",'track': "Breakout",'session_type': "Breakout Session",'day': current_day_key,'description': ""}
                    schedule[current_day_key].append(session_info)
        if not schedule.get('day2'): schedule.pop('day2', None)
        if not schedule.get('day1') and not schedule.get('day2'): logger.warning("Lagos scraper: 0 sessions.")
        if schedule.get('day1'):
            def sort_key_lagos(session_dict):
                time_str = session_dict.get('time', '12:00 AM - 12:00 AM').split(' - ')[0].strip()
                parsed_time = datetime.min 
                try: parsed_time = datetime.strptime(time_str, "%I:%M %p")
                except ValueError:
                    try: parsed_time = datetime.strptime(time_str, "%H:%M")
                    except ValueError: pass
                return parsed_time
            schedule['day1'].sort(key=sort_key_lagos)
            logger.info("Lagos: Successfully sorted Day 1 sessions by time.")
        logger.info(f"Lagos scraper: Found {sum(len(s) for s in schedule.values())} sessions.")
    except requests.exceptions.RequestException as e: logger.error(f"Lagos scraper HTTP error: {e}"); return {'day1': []}
    except Exception as e: logger.error(f"Lagos scraper error: {e}", exc_info=True); return {'day1': []}
    return schedule

def get_devfest_nairobi_schedule() -> Dict[str, List[Dict]]:
    schedule_output: Dict[str, List[Dict]] = {'day1': []}
    url = "https://gdg.community.dev/events/details/google-gdg-nairobi-presents-devfest-nairobi-2024-1/"
    logger.info(f"Nairobi Scraper (JS Object): Fetching schedule from: {url}")
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0','Accept': 'text/html'})
        response.raise_for_status()
        js_pattern = r'Globals\.eventInfo\s*=\s*({.*?});'
        js_match = re.search(js_pattern, response.text, re.DOTALL)
        if not js_match: logger.error("Nairobi: No Globals.eventInfo."); return schedule_output
        event_info_str = js_match.group(1)
        try:
            event_info_str_py = re.sub(r',\s*([\}\]])', r'\1', event_info_str.replace('false','False').replace('true','True').replace('null','None'))
            event_info = ast.literal_eval(event_info_str_py)
            days_data = event_info.get('agenda', {}).get('days', [])
            if not days_data: logger.warning("Nairobi: No 'days' data."); return schedule_output
            day_agenda_items = days_data[0].get('agenda', [])
            if not day_agenda_items: logger.warning("Nairobi: No session items."); return schedule_output
            for item_js in day_agenda_items:
                activity, desc_js = item_js.get('activity',''), item_js.get('description','')
                room, title = "", activity
                rm = re.match(r'\[([^\]]+)\]\s*(.*)', activity)
                if rm: room,title = rm.group(1).strip(), rm.group(2).strip()
                speakers = [s.strip() for s in BeautifulSoup(desc_js,'html.parser').get_text(separator=' & ',strip=True).split(' & ') if s.strip() and len(s)<70] if desc_js else []
                s_data={'title':title.strip(),'time':item_js.get('time','').strip(),'room':room.strip() if room else "Main Hall",'speaker':" & ".join(speakers) if speakers else "N/A",'description':"",'audience_type':item_js.get('audience_type','IN_PERSON'),'day':"Day 1",'track':"General",'session_type':"Talk"}
                tl,rl = s_data['title'].lower(),s_data['room'].lower() # tl=title_lower, rl=room_lower
                if "malewa hall" in rl: s_data['track'] = "Track 1 (Malewa)"
                elif "main hall" in rl: s_data['track'] = "Track 2 (Main)"
                elif "turkwell hall" in rl: s_data['track'] = "Track 3 (Turkwell)"
                elif "rooftop hall" in rl: s_data['track'] = "Track 4 (Rooftop)"
                if any(k in tl for k in ["ai","gemini", "gemma"]): s_data['track']="AI" # Added gemma
                elif any(k in tl for k in ["dsa","problem-solving", "algorithm"]): s_data['track']="CS Fundamentals" # Added algorithm
                elif "cloud" in tl: s_data['track']="Cloud"
                elif any(k in tl for k in ["web","angular"]): s_data['track']="Web"
                elif "android" in tl: s_data['track']="Android"
                elif any(k in tl for k in ["flutter","firebase"]): s_data['track']="Mobile/Firebase"
                if "keynote" in tl: s_data['session_type']="Keynote"
                elif any(k in tl for k in ["workshop","hands-on"]): s_data['session_type']="Workshop"
                elif any(k in tl for k in ["registration","welcome","intro", "preshow", "guidelines"]): s_data['session_type']="Admin/Opening" # Added preshow, guidelines
                elif "closing remarks" in tl: s_data['session_type']="Closing"
                elif any(k in tl for k in ["lunch","networking","photo session","q&a"]): s_data['session_type']="General/Networking"
                elif "partner session" in tl: s_data['session_type']="Partner Session"
                schedule_output['day1'].append(s_data)
            logger.info(f"Nairobi Scraper (JS Object): Successfully processed {len(schedule_output['day1'])} sessions.")
            if schedule_output.get('day1'):
                def sort_key_nairobi_js(session_dict):
                    time_str = session_dict.get('time', '12:00 AM').split(' - ')[0].strip()
                    parsed_time = datetime.min
                    try: parsed_time = datetime.strptime(time_str, "%I:%M %p")
                    except ValueError:
                        try: parsed_time = datetime.strptime(time_str, "%H:%M")
                        except ValueError: pass
                    return parsed_time
                schedule_output['day1'].sort(key=sort_key_nairobi_js)
                logger.info("Nairobi Scraper (JS Object): Successfully sorted sessions by time.")
        except ast.literal_eval_error as ae: logger.error(f"Nairobi Scraper (JS Object): Error parsing JS object: {ae}")
        except Exception as e_parse: logger.error(f"Nairobi Scraper (JS Object): Error processing parsed event info: {e_parse}", exc_info=True)
    except requests.exceptions.RequestException as e_req: logger.error(f"Nairobi Scraper (JS Object): HTTP Request error: {e_req}")
    except Exception as e_main: logger.error(f"Nairobi Scraper (JS Object): Unexpected error: {e_main}", exc_info=True)
    return schedule_output


# ================================
# LLAMAINDEX DATA CONVERSION AND TOOLS
# ================================
def convert_to_documents(schedule_data: Dict[str, List[Dict]], event_name: str) -> List[Document]:
    documents = []
    if not schedule_data or not any(schedule_data.values()):
        logger.warning(f"No schedule data provided to convert_to_documents for {event_name}. Returning empty list.")
        return []
    for day_key, sessions in schedule_data.items():
        if not sessions: continue
        for session in sessions:
            title = session.get('title', "No Title Provided")
            time_val = session.get('time', "Time Not Specified")
            room = session.get('room', "Room Not Specified")
            speaker = session.get('speaker', "N/A")
            track = session.get('track', "General")
            session_type = session.get('session_type', "Session")
            description = session.get('description', "") 
            audience_type = session.get('audience_type', "IN_PERSON")
            day_str = day_key.replace('day', 'Day ')
            content = f"""Event: {event_name}
Day: {day_str}
Time: {time_val}
Title: {title}
Speaker(s): {speaker}
Room: {room}
Track: {track}
Session Type: {session_type}
Description: {description}
Audience: {audience_type}
"""
            metadata = {
                "event_name": event_name, "day": day_str, "time": time_val,
                "title": title, "speaker": speaker, "room": room, "track": track,
                "session_type": session_type, "description": description,
                "audience_type": audience_type,
            }
            doc = Document(text=content, metadata=metadata)
            documents.append(doc)
    logger.info(f"Converted {len(documents)} sessions from {event_name} into LlamaIndex Documents.")
    return documents

class DevFestScheduleLlamaTool:
    def __init__(self, event_location: str):
        self.event_location = event_location
        self.event_name = f"DevFest {event_location} 2024"
        self._raw_schedule_data: Optional[Dict[str, List[Dict]]] = None
        self._documents: Optional[List[Document]] = None

    def _fetch_schedule_raw(self) -> Dict[str, List[Dict]]:
        if self.event_location.lower() == "lagos": return get_devfest_lagos_schedule()
        elif self.event_location.lower() == "nairobi": return get_devfest_nairobi_schedule()
        logger.error(f"Unknown LlamaTool location: {self.event_location}"); return {"day1": []}

    def get_raw_schedule(self) -> Dict[str, List[Dict]]:
        if self._raw_schedule_data is None:
            logger.info(f"LlamaTool: Fetching raw for {self.event_name}...")
            self._raw_schedule_data = self._fetch_schedule_raw()
            if not self._raw_schedule_data or not any(self._raw_schedule_data.values()):
                logger.warning(f"LlamaTool: No raw data for {self.event_name}."); self._raw_schedule_data = {"day1":[]}
        return self._raw_schedule_data
    
    def get_documents(self) -> List[Document]:
        if self._documents is None: self._documents = convert_to_documents(self.get_raw_schedule(), self.event_name)
        return self._documents

    def save_schedule_json(self, filename: Optional[str] = None):
        if filename is None:
            filename = f"devfest_{self.event_location.lower()}_schedule_llamaindex_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        schedule_data = self.get_raw_schedule()
        if not any(schedule_data.values()):
             logger.info(f"No schedule data to save for {self.event_name} (LlamaTool).")
             return
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(schedule_data, f, ensure_ascii=False, indent=2)
            logger.info(f"LlamaTool: Raw schedule for {self.event_name} saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving LlamaTool schedule for {self.event_name}: {e}")


# ================================
# LLAMAINDEX ReAct AGENT ASSISTANT
# ================================
class DevFestReActAssistant:
    def __init__(self):
        self.lagos_data_tool = DevFestScheduleLlamaTool(event_location="Lagos")
        self.nairobi_data_tool = DevFestScheduleLlamaTool(event_location="Nairobi")
        self.lagos_index: Optional[VectorStoreIndex] = None
        self.nairobi_index: Optional[VectorStoreIndex] = None
        self.agent: Optional[ReActAgent] = None
        os.makedirs("./storage/devfest_lagos", exist_ok=True)
        os.makedirs("./storage/devfest_nairobi", exist_ok=True)
        
    def _build_or_load_index(self, data_tool: DevFestScheduleLlamaTool, persist_dir: str) -> VectorStoreIndex:
        documents = data_tool.get_documents()
        if not documents:
            logger.warning(f"No docs for {data_tool.event_name}, empty index."); return VectorStoreIndex.from_documents([]) 
        logger.info(f"Building index for {data_tool.event_name}...")
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=persist_dir)
        logger.info(f"Index for {data_tool.event_name} built & persisted to {persist_dir}")
        return index

    def build_indices(self):
        logger.info("Building indices...")
        self.lagos_index = self._build_or_load_index(self.lagos_data_tool, "./storage/devfest_lagos")
        self.nairobi_index = self._build_or_load_index(self.nairobi_data_tool, "./storage/devfest_nairobi")
        logger.info("Indices built.")
        
    def build_agent(self):
        if self.lagos_index is None or self.nairobi_index is None: self.build_indices()
        
        query_engine_tools = []
        # Robust check for documents in the index
        lagos_has_docs = hasattr(self.lagos_index, 'docstore') and self.lagos_index.docstore.docs or \
                         (hasattr(self.lagos_index, 'index_struct') and hasattr(self.lagos_index.index_struct, 'doc_id_to_node_id') and self.lagos_index.index_struct.doc_id_to_node_id)

        nairobi_has_docs = hasattr(self.nairobi_index, 'docstore') and self.nairobi_index.docstore.docs or \
                           (hasattr(self.nairobi_index, 'index_struct') and hasattr(self.nairobi_index.index_struct, 'doc_id_to_node_id') and self.nairobi_index.index_struct.doc_id_to_node_id)


        if lagos_has_docs:
            lagos_engine = self.lagos_index.as_query_engine(similarity_top_k=3)
            query_engine_tools.append(QueryEngineTool(query_engine=lagos_engine, metadata=ToolMetadata(name="devfest_lagos_schedule_retriever",description="Provides DevFest Lagos 2024 schedule. Use for Lagos event queries.")))
        else: logger.warning("Lagos index empty, tool not added.")

        if nairobi_has_docs:
            nairobi_engine = self.nairobi_index.as_query_engine(similarity_top_k=3)
            query_engine_tools.append(QueryEngineTool(query_engine=nairobi_engine, metadata=ToolMetadata(name="devfest_nairobi_schedule_retriever",description="Provides DevFest Nairobi 2024 schedule. Use for Nairobi event queries.")))
        else: logger.warning("Nairobi index empty, tool not added.")

        if not query_engine_tools: logger.error("No tools for agent as all indices are empty."); return

        self.agent = ReActAgent.from_tools(query_engine_tools, llm=Settings.llm, verbose=True)
        logger.info("ReAct agent built successfully with available tools.")
        
    def query(self, query_text: str):
        if self.agent is None:
            logger.info("Agent not yet built. Building agent now...")
            self.build_agent()
            if self.agent is None: logger.error("Agent build failed."); return "Agent not available."
        
        logger.info(f"Querying ReAct agent: '{query_text}'")
        try:
            response = self.agent.chat(query_text)
            return str(response)
        except Exception as e:
            logger.error(f"Agent query error: {e}", exc_info=True)
            model_name_used = Settings.llm.metadata.model_name if hasattr(Settings.llm, 'metadata') else "the configured LLM"
            if "API key not valid" in str(e) or "permission" in str(e).lower() or ("could not be found" in str(e).lower() and "model" in str(e).lower()):
                 return (f"Sorry, there's an issue with accessing the AI model. "
                        f"Please check your GEMINI_API_KEY and model name ('{model_name_used}').")
            return f"Sorry, an error occurred with the agent: {type(e).__name__}"

# Main function
def main():
    logger.info("=== DevFest Schedule ReAct Assistant (Google GenAI API Key) ===")
    assistant = DevFestReActAssistant()
    logger.info("Building ReAct agent...")
    assistant.build_agent() 
    
    if assistant.agent is None:
        logger.error("Agent initialization failed. Exiting."); print("Assistant could not be initialized."); return
    
    logger.info("✅ Assistant ready!")
    print("\n✅ Assistant ready! Ask about DevFest Lagos or Nairobi schedules (using Google GenAI).")
    
    example_queries = [
        "Find me sessions about AI and machine learning in DevFest Nairobi",
        "What web development talks are available at DevFest Lagos?",
        "Compare the ML/AI sessions between Lagos and Nairobi DevFest events.",
        "What is DevFest?"
    ]
    for i, query in enumerate(example_queries):
        print(f"\n--- Example Query {i+1} ---")
        print(f"User: {query}")
        response = assistant.query(query)
        print(f"Agent Response: {response}")
        time.sleep(1.5) 
    
    print("\n--- Interactive Mode ---")
    while True:
        try:
            user_query = input("\nEnter your query (or 'exit' to quit): ")
            if user_query.lower() in ['exit', 'quit', 'q']: print("Exiting."); break
            if not user_query.strip(): continue
            response = assistant.query(user_query)
            print(f"Agent Response: {response}")
        except KeyboardInterrupt: print("\nExiting."); break
        except Exception as e:
            logger.error(f"Interactive loop error: {e}", exc_info=True)
            print(f"Error: {e}")

if __name__ == "__main__":
    main()