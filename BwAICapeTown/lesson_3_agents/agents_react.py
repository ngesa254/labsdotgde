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
from IPython.display import JSON, display

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import LlamaIndex and VertexAI dependencies
try:
    from llama_index.core import Document, VectorStoreIndex, Settings
    from llama_index.core.agent import ReActAgent
    from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.vertex import Vertex
    
    # Project settings
    PROJECT_ID = "angelic-bee-193823"
    LOCATION = "us-central1"
    
    try:
        import vertexai
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        logger.info(f"✅ Initialized Vertex AI with Project: {PROJECT_ID}, Location: {LOCATION}")
    except Exception as e:
        logger.error(f"Error initializing Vertex AI: {e}")
        raise
        
except ImportError as e:
    logger.error(f"Error importing LlamaIndex or Vertex AI dependencies: {e}")
    logger.error("Please install the required packages using: pip install llama-index llama-index-llms-vertex")
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

# Initialize models - embed_model and llm
try:
    # Initialize embedding model
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    logger.info("✅ Initialized HuggingFace embedding model successfully")
    
    # Initialize LLM with fallback options
    try:
        # Try the newer model first
        llm = Vertex("gemini-2.5-pro-preview-03-25")
        logger.info("✅ Initialized Vertex LLM with gemini-2.5-pro-preview-03-25")
    except Exception as e:
        logger.warning(f"Failed to initialize gemini-2.5-pro-preview-03-25: {e}")
        try:
            # First fallback option
            llm = Vertex("gemini-1.5-pro")
            logger.info("✅ Initialized Vertex LLM with gemini-1.5-pro")
        except Exception as e:
            logger.warning(f"Failed to initialize gemini-1.5-pro: {e}")
            # Second fallback option
            llm = Vertex("gemini-pro")
            logger.info("✅ Initialized Vertex LLM with gemini-pro")
            
    # Update global settings
    Settings.embed_model = embed_model
    Settings.llm = llm
    
except Exception as e:
    logger.error(f"Error initializing models: {e}")
    raise

# ================================
# LAGOS SCRAPER FUNCTIONS
# ================================

def get_devfest_lagos_schedule() -> Dict[str, List[Dict]]:
    """
    Scrape and return the DevFest Lagos schedule as JSON data.
    Returns a dictionary with days as keys and lists of session information as values.
    """
    # Initialize schedule structure
    schedule = {
        'day1': [],
        'day2': []
    }
    
    try:
        # Set up session and get page content
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })
        
        # Get HTML content
        response = session.get("https://devfestlagos.com/schedule")
        response.raise_for_status()
        
        # Save HTML for debugging if needed
        with open('lagos_page_source.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find schedule container
        schedule_container = soup.find('div', class_='schedule_scheduleItemsContainer__wkWNt')
        
        if schedule_container:
            # Extract general sessions
            general_events = schedule_container.find_all('div', class_='EventBlock_event__UsJua')
            for event in general_events:
                session_data = {
                    'title': event.find('h3').text.strip(),
                    'time': event.find('div', class_='EventBlock_time__RQGQz').text.strip() if event.find('div', class_='EventBlock_time__RQGQz') else "Time not specified",
                    'room': event.find('div', class_='EventBlock_venue__wjpVu').find('span').text.strip() if event.find('div', class_='EventBlock_venue__wjpVu') and event.find('div', class_='EventBlock_venue__wjpVu').find('span') else "Main Hall",
                    'speaker': "N/A",
                    'track': "General",
                    'session_type': "General",
                    'day': "Day 1"
                }
                schedule['day1'].append(session_data)
            
            # Extract breakout sessions
            breakout_container = schedule_container.find('div', class_='EventCategory_eventSchedule__events__cCu22')
            if breakout_container:
                breakout_events = breakout_container.find_all('div', class_='EventCategory_eventSchedule__event__AhbY3')
                for event in breakout_events:
                    session_data = {
                        'title': event.find('h3', class_='EventCategory_eventSchedule__event-title__F2air').text.strip() if event.find('h3', class_='EventCategory_eventSchedule__event-title__F2air') else "No Title",
                        'speaker': event.find('p', class_='EventCategory_eventSchedule__event-facilitator__nWvuU').text.strip() if event.find('p', class_='EventCategory_eventSchedule__event-facilitator__nWvuU') else "Not specified",
                        'time': event.find('div', class_='EventCategory_eventSchedule__event-time__f_zfq').find('span', class_='text-sm').text.strip() if event.find('div', class_='EventCategory_eventSchedule__event-time__f_zfq') else "Time not specified",
                        'room': "Breakout Room",
                        'track': "Breakout",
                        'session_type': "Breakout",
                        'day': "Day 1"
                    }
                    schedule['day1'].append(session_data)
    
    except Exception as e:
        logger.error(f"Error scraping Lagos schedule: {str(e)}")
        
    return schedule

# ================================
# NAIROBI SCRAPER FUNCTIONS
# ================================

def get_devfest_nairobi_schedule() -> Dict[str, List[Dict]]:
    """
    Manual creation of DevFest Nairobi schedule since the scraping approach is failing.
    This is a fallback approach to ensure we have data for Nairobi queries.
    """
    # Initialize schedule structure with predefined sessions
    schedule = {
        'day1': []
    }
    
    # Add sessions manually based on the data from the paste
    nairobi_sessions = [
        {
            'title': 'Arrival And Registration',
            'time': '8:00 AM',
            'room': 'Main Entrance',
            'speaker': 'N/A',
            'track': 'General',
            'session_type': 'Admin',
            'day': 'Day 1',
            'description': 'Registration and check-in for all attendees',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Welcome Address (GDG Nairobi)',
            'time': '9:00 AM',
            'room': 'Main Hall',
            'speaker': 'Kai Mwanyumba & Cynthia Kamau',
            'track': 'General',
            'session_type': 'Keynote',
            'day': 'Day 1',
            'description': 'Opening remarks and welcome address from GDG Nairobi organizers',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Google Keynote Address',
            'time': '9:20 AM',
            'room': 'Main Hall',
            'speaker': 'John Kimani - Senior Program Manager, Google\'s Developer Ecosystem',
            'track': 'General',
            'session_type': 'Keynote',
            'day': 'Day 1',
            'description': 'Keynote address from Google representative',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'How you Build Apps with Google',
            'time': '9:30 AM',
            'room': 'Main Hall',
            'speaker': 'Seba Gnagnarella, Director of Engineering, Google, Firebase',
            'track': 'General',
            'session_type': 'Keynote',
            'day': 'Day 1',
            'description': 'Learn about the latest Google efforts to shape how You Build Apps',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Build and Deploy an AI-Powered Blood Pressure Tracker on Google Cloud Run',
            'time': '10:10 AM',
            'room': 'Main Hall',
            'speaker': 'Femi Taiwo (GDE Cloud)',
            'track': 'AI & Cloud',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Practical demonstration of building and deploying an AI-powered application',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Algorithm, DSA & Problem-solving Session',
            'time': '10:10 AM',
            'room': 'Malewa Hall',
            'speaker': 'Google Kenya Engineering Team',
            'track': 'Computer Science',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Deep dive into algorithms, data structures and problem-solving techniques',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'What is new on the web? The latest advancements in web apis, web assembly and web capabilities',
            'time': '10:10 AM',
            'room': 'Rooftop Hall',
            'speaker': 'Michelle Buchi (GDE Web)',
            'track': 'Web',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Overview of the latest web technologies and capabilities',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Bridging Languages: Building AI-Powered Multilingual Chat Applications with Android and Gemini',
            'time': '11:15 AM',
            'room': 'Main Hall',
            'speaker': 'Marvin Ngesa and Jessica Randall',
            'track': 'AI & Mobile',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Creating multilingual applications using Gemini on Android',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Firebase Fundamentals: Structuring your Nosql Data For scalability and reporting',
            'time': '11:15 AM',
            'room': 'Turkwell Hall',
            'speaker': 'Jason Berryman - Google Cloud Architect & Google Developer Expert',
            'track': 'Cloud',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Best practices for NoSQL data structure in Firebase',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Not a Senior Dev Yet: Modular Software Development And Release',
            'time': '11:15 AM',
            'room': 'Rooftop Hall',
            'speaker': 'Marvin Hosea - Managing Partner · Apps:Lab Limited',
            'track': 'Software Engineering',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Techniques for modular software development and efficient release processes',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'The Angular Renaissance - Adopting the New Angular Way',
            'time': '1:20 PM',
            'room': 'Main Hall',
            'speaker': 'Wycliff Maina - Frontend Engineer - TypeScript Aficionado && GDE Web',
            'track': 'Web',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Exploring new Angular features and best practices',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[Gemma] AI hands-on Workshop',
            'time': '1:20 PM',
            'room': 'Turkwell Hall',
            'speaker': 'Oscar Wahltinez - Developer Relations @Google',
            'track': 'AI',
            'session_type': 'Workshop',
            'day': 'Day 1',
            'description': 'Hands-on workshop with Google\'s Gemma AI model',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[AI] Exploring Autonomous AI: Aligning Ethics, Technology, Society and Law Through TensorFlow',
            'time': '1:25 PM',
            'room': 'Rooftop Hall',
            'speaker': 'Risper Joy - Data Scientist',
            'track': 'AI',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Ethical considerations in autonomous AI development using TensorFlow',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[Google Cloud] Optimizing Cloud Infrastructure Management with Terraform',
            'time': '1:25 PM',
            'room': 'Malewa Hall',
            'speaker': 'Rebecca Mirembe - Professional Security Analyst | Cloud Engineer',
            'track': 'Cloud',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Using Terraform for efficient cloud infrastructure management',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Angular\'s New Control Flow Syntax',
            'time': '2:30 PM',
            'room': 'Main Hall',
            'speaker': 'Wayne Gakuo - Google Developer Expert for Angular | Frontend Engineer | Lead @ Angular Kenya',
            'track': 'Web',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Deep dive into Angular\'s new control flow syntax features',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[AI] Building Responsible AI with Generative Models',
            'time': '2:30 PM',
            'room': 'Rooftop Hall',
            'speaker': 'Wesley Kambale - Machine learning engineer and Data scientist',
            'track': 'AI',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Principles of responsible AI development with generative models',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[Flutter] Building AI-Enhanced E-commerce Apps with Flutter and Firebase Genkit',
            'time': '2:30 PM',
            'room': 'Malewa Hall',
            'speaker': 'Bright Sunu - Software Engineer. Google Developer Expert',
            'track': 'Mobile & AI',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Creating AI-enhanced e-commerce applications with Flutter and Firebase',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[ML] Building Responsible AI Through Explainability with Keras',
            'time': '3:15 PM',
            'room': 'Main Hall',
            'speaker': 'Brayan Kai - Data Scientist and Technical Writer',
            'track': 'AI',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Implementing AI explainability with Keras for more responsible machine learning',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': '[AI] Transfer Learning Turbo: Detecting Pneumonia with Keras, TensorFlow & Style!',
            'time': '3:15 PM',
            'room': 'Rooftop Hall',
            'speaker': 'Kayongo Johnson Brian - Team Lead - InversePay',
            'track': 'AI & Healthcare',
            'session_type': 'Technical',
            'day': 'Day 1',
            'description': 'Using transfer learning techniques for medical image analysis',
            'audience_type': 'IN_PERSON'
        },
        {
            'title': 'Closing Remarks by GDG Nairobi',
            'time': '3:55 PM',
            'room': 'Main Hall',
            'speaker': 'GDG Nairobi Team',
            'track': 'General',
            'session_type': 'Closing',
            'day': 'Day 1',
            'description': 'Closing remarks and summary of the event',
            'audience_type': 'IN_PERSON'
        }
    ]
    
    # Add all sessions to the schedule
    schedule['day1'].extend(nairobi_sessions)
    
    logger.info(f"Created manual Nairobi schedule with {len(nairobi_sessions)} sessions")
    return schedule

def convert_to_documents(schedule_data: Dict[str, List[Dict]], event_name: str) -> List[Document]:
    """
    Convert schedule data into LlamaIndex Document objects with proper metadata
    """
    documents = []
    
    for day, sessions in schedule_data.items():
        for session in sessions:
            # Create formatted content with safe access to fields
            content = f"""
            Title: {session['title']}
            Time: {session['time']}
            Room: {session.get('room', 'Not specified')}
            Speaker: {session.get('speaker', 'Not specified')}
            Track: {session.get('track', 'General')}
            Session Type: {session.get('session_type', 'Session')}
            Description: {session.get('description', '')}
            Audience Type: {session.get('audience_type', 'IN_PERSON')}
            Day: {day.replace('day', 'Day ')}
            Event: {event_name}
            """
            
            # Create metadata for better querying
            metadata = {
                "title": session['title'],
                "time": session['time'],
                "room": session.get('room', 'Not specified'),
                "speaker": session.get('speaker', 'Not specified'),
                "track": session.get('track', 'General'),
                "session_type": session.get('session_type', 'Session'),
                "description": session.get('description', ''),
                "audience_type": session.get('audience_type', 'IN_PERSON'),
                "day": day.replace('day', 'Day '),
                "event": event_name
            }
            
            # Create Document object
            doc = Document(
                text=content,
                metadata=metadata
            )
            documents.append(doc)
    
    return documents

class DevFestScheduleTool:
    """Tool for handling DevFest schedule data"""
    
    def __init__(self, event_location="Lagos"):
        self.schedule_data = None
        self.documents = None
        self.event_location = event_location
        self.event_name = f"DevFest {event_location} 2024"
    
    def get_schedule(self) -> Dict[str, List[Dict]]:
        """Get schedule data"""
        if not self.schedule_data:
            if self.event_location.lower() == "lagos":
                self.schedule_data = get_devfest_lagos_schedule()
                logger.info(f"Retrieved Lagos schedule with {len(self.schedule_data.get('day1', []))} sessions")
            elif self.event_location.lower() == "nairobi":
                self.schedule_data = get_devfest_nairobi_schedule()
                logger.info(f"Retrieved Nairobi schedule with {len(self.schedule_data.get('day1', []))} sessions")
            else:
                logger.error(f"Unknown event location: {self.event_location}")
                self.schedule_data = {"day1": []}
                
        return self.schedule_data
    
    def get_documents(self) -> List[Document]:
        """Get schedule as Document objects"""
        if not self.documents:
            schedule_data = self.get_schedule()
            self.documents = convert_to_documents(schedule_data, self.event_name)
            logger.info(f"Created {len(self.documents)} documents for {self.event_name}")
        return self.documents
    
    def save_schedule(self, filename: str = None):
        """Save schedule to JSON file"""
        if filename is None:
            filename = f"devfest_{self.event_location.lower()}_schedule.json"
            
        schedule_data = self.get_schedule()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Schedule saved to {filename}")
    
    def display_schedule(self, show_details: bool = False):
        """Display schedule in readable format"""
        print(f"\n=== {self.event_name} Schedule ===\n")
        schedule_data = self.get_schedule()
        display_schedule(schedule_data, show_details)

def display_schedule(schedule_data: Dict[str, List[Dict]], show_details: bool = True):
    """Display the schedule in a readable format"""
    if not schedule_data or not schedule_data.get('day1'):
        print("\nNo schedule data available. Please check the logs for errors.")
        return
        
    sessions = schedule_data['day1']
    if not sessions:
        print("\nNo sessions found in the schedule.")
        return
        
    print("\n=== DevFest Schedule ===\n")
    
    # Sort sessions by time
    for session in sorted(sessions, key=lambda x: x.get('time', '')):
        print(f"Time: {session['time']}")
        print(f"Title: {session['title']}")
        if session.get('room'):
            print(f"Room: {session['room']}")
        if session.get('speaker'):
            print(f"Speaker: {session['speaker']}")
        if show_details and session.get('description'):
            print(f"Description: {session['description']}")
        print("-" * 50)

# Create Function Tools for both locations
lagos_schedule_tool = FunctionTool.from_defaults(
    fn=get_devfest_lagos_schedule,
    name="get_devfest_lagos_schedule",
    description="Get the complete DevFest Lagos 2024 schedule as JSON data"
)

nairobi_schedule_tool = FunctionTool.from_defaults(
    fn=get_devfest_nairobi_schedule,
    name="get_devfest_nairobi_schedule",
    description="Get the complete DevFest Nairobi 2024 schedule as JSON data"
)

class DevFestAssistant:
    """DevFest schedule assistant that can handle queries for multiple events"""
    
    def __init__(self):
        # Initialize tools
        self.lagos_tool = DevFestScheduleTool(event_location="Lagos")
        self.nairobi_tool = DevFestScheduleTool(event_location="Nairobi")
        
        # Build indices
        self.lagos_index = None
        self.nairobi_index = None
        
        # Agent
        self.agent = None
        
    def build_indices(self):
        """Build indices for both events"""
        logger.info("Building indices for DevFest events...")
        
        # Get documents
        lagos_documents = self.lagos_tool.get_documents()
        nairobi_documents = self.nairobi_tool.get_documents()
        
        # Build indices
        self.lagos_index = VectorStoreIndex.from_documents(lagos_documents)
        self.nairobi_index = VectorStoreIndex.from_documents(nairobi_documents)
        
        logger.info("Indices built successfully")
        
        # Save indices
        os.makedirs("./storage", exist_ok=True)
        os.makedirs("./storage/devfest_lagos", exist_ok=True)
        os.makedirs("./storage/devfest_nairobi", exist_ok=True)
        
        self.lagos_index.storage_context.persist(persist_dir="./storage/devfest_lagos")
        self.nairobi_index.storage_context.persist(persist_dir="./storage/devfest_nairobi")
        
        logger.info("Indices saved to storage directory")
        
    def build_agent(self):
        """Build ReAct agent with both query engines"""
        if self.lagos_index is None or self.nairobi_index is None:
            self.build_indices()
            
        # Create query engines
        lagos_engine = self.lagos_index.as_query_engine(similarity_top_k=3)
        nairobi_engine = self.nairobi_index.as_query_engine(similarity_top_k=3)
        
        # Create query engine tools
        query_engine_tools = [
            QueryEngineTool(
                query_engine=nairobi_engine,
                metadata=ToolMetadata(
                    name="devfest_nairobi",
                    description=(
                        "Provides information about DevFest Nairobi 2024 schedule, "
                        "including sessions, speakers, tracks, and timings. "
                        "Use for queries specifically about the Nairobi event."
                    ),
                ),
            ),
            QueryEngineTool(
                query_engine=lagos_engine,
                metadata=ToolMetadata(
                    name="devfest_lagos",
                    description=(
                        "Provides information about DevFest Lagos 2024 schedule, "
                        "including sessions, speakers, tracks, and timings. "
                        "Use for queries specifically about the Lagos event."
                    ),
                ),
            ),
        ]
        
        # Build agent
        self.agent = ReActAgent.from_tools(
            query_engine_tools,
            llm=llm,
            verbose=True,
        )
        
        logger.info("ReAct agent built successfully")
        
    def query(self, query_text):
        """Query the schedule using the appropriate method"""
        if "lagos" in query_text.lower() and "nairobi" in query_text.lower():
            # If query mentions both events, use the agent
            if self.agent is None:
                self.build_agent()
            return self.agent.chat(query_text)
        elif "lagos" in query_text.lower():
            # Lagos-specific query
            if self.lagos_index is None:
                self.build_indices()
            return self.lagos_index.as_query_engine().query(query_text)
        elif "nairobi" in query_text.lower():
            # Nairobi-specific query
            if self.nairobi_index is None:
                self.build_indices()
            return self.nairobi_index.as_query_engine().query(query_text)
        else:
            # Generic query - let's use the agent to decide
            if self.agent is None:
                self.build_agent()
            return self.agent.chat(query_text)

# Main function for running as a script
def main():
    """Main function to demonstrate functionality"""
    print("\n=== DevFest Schedule Assistant ===")
    print("Initializing assistant...")
    
    assistant = DevFestAssistant()
    
    # Example queries to demonstrate functionality
    example_queries = [
        "Find me sessions about AI and machine learning in DevFest Nairobi",
        "What web development talks are available at DevFest Lagos?",
        "Compare the ML/AI sessions between Lagos and Nairobi DevFest events",
        "When are the keynote sessions at both events?"
    ]
    
    print("\nBuilding indices and agent...")
    assistant.build_agent()
    
    print("\nReady to answer questions!")
    
    # Process a few example queries
    for i, query in enumerate(example_queries[:2]):  # Just do 2 examples to save time
        print(f"\nQuery {i+1}: {query}")
        response = assistant.query(query)
        print(f"Response: {response}")
    
    # Interactive mode
    while True:
        user_query = input("\nEnter your query (or 'exit' to quit): ")
        if user_query.lower() in ['exit', 'quit', 'q']:
            break
        
        response = assistant.query(user_query)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()