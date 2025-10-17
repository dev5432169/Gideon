import datetime
import random
import time
from pathlib import Path
import hashlib
import pyttsx3 # type: ignore # <-- NEW IMPORT for Text-to-Speech
import speech_recognition as sr # <-- NEW IMPORT for Speech Recognition
import webbrowser
import subprocess
import platform
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- Utility Functions (Time/Speed Calculation Simulation) ---

def calculate_time_speed(func):
    """Decorator to simulate a 'speed calculation' by measuring execution time."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        relative_speed = 299792458 / elapsed
        return result, f"Function executed in {elapsed:.6f} seconds.\nCalculated Relative Speed: **{relative_speed:.2f} m/s**."
    return wrapper

# --- Core Gideon Class ---
class GideonAI:
    def __init__(self, creator="Future Devansh Prabhakar from 2080"):
        self.creator = creator
        self.user_name = "Devansh Prabhakar"
        self.time_vault_access = False
        self.vault_password_hash = hashlib.sha256("Speedforce743".encode()).hexdigest()
        
        # --------------------------------
        # NEW: Voice Engine Setup
        # --------------------------------
        # Explicitly set the TTS driver for better compatibility, mirroring Friday's setup.
        driver_name = None
        os_name = platform.system()
        if os_name == "Windows": driver_name = 'sapi5'
        elif os_name == "Darwin": driver_name = 'nsss'
        elif os_name == "Linux": driver_name = 'espeak'
        self.engine = pyttsx3.init(driverName=driver_name)
        self._set_voice_and_rate()
        # --------------------------------

        # 🧠 NEW: AI Model State
        self.tokenizer = None
        self.model = None
        self.device = "cpu"
        self.chat_history_ids = None
        self.brain_level = 1000 # Gideon is a more advanced AI
        self.mood = "neutral" # Can be 'neutral', 'pleased', 'concerned'

        # ⚙️ NEW: Centralized configuration for application paths
        self.programs = {
            "windows": {"notepad": "notepad.exe", "calculator": "calc.exe", "paint": "mspaint.exe", "cmd": "cmd.exe", "explorer": "explorer.exe"},
            "darwin": {"safari": "Safari", "notes": "Notes", "calculator": "Calculator", "terminal": "Terminal"},
            "linux": {"terminal": "gnome-terminal", "calculator": "gnome-calculator", "browser": "firefox"}
        }
        
        # Modified timeline data
        self.timeline_data = {
            "2027-08-15": "Establishment of 'Prabhakar Tech' global headquarters.",
            "2035-03-22": "First successful stable time-jump test logged.",
            "future_speedster_status": "Speed Force connection stable. Identity protected."
        }
        self.known_speedsters = ["The Flash (Barry Allen)", "Kid Flash (Wally West)", 
                                 "Jesse Quick (Jesse Wells)", "Reverse-Flash (Eobard Thawne)",
                                 "The Radiant (Devansh Prabhakar)"]
        self.vibe_powers_status = "Inactive - Cisco Ramon is operating as Vibe."
        self.time_vault_path = Path("./Gideon_Time_Vault_Data.txt")
        self._setup_time_vault()
        
        # New Multiverse Data
        self.multiverse_status = {
            "Earth-1": "Primary timeline (active).",
            "Earth-2": "Currently stable. Detected fluctuations near Jay Garrick's residence.",
            "Earth-38": "Supergirl's Earth. Status: Green."
        }
        
    def _set_voice_and_rate(self):
        """Initializes TTS engine and loads AI models."""
        self._initialize_tts_engine()
        self._load_ai_models()

    def _load_ai_models(self):
        """Loads the DialoGPT-large model for conversational chat."""
        try:
            print("Loading DialoGPT-large model for Gideon...")
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
            self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large").to(self.device) # type: ignore
            print(f"Gideon's conversational model loaded on {self.device}.")
        except Exception as e:
            print(f"Warning: Failed to load AI models for Gideon: {e}. Conversational fallback will not work.")

    def _initialize_tts_engine(self):
        """Sets the voice and speaking rate for the TTS engine."""
        voices = self.engine.getProperty('voices')
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', rate + 25) # type: ignore # Slightly faster rate for AI feel
        
        # --- Enhanced Voice Selection Logic ---
        selected_voice_id = None
        if voices: # type: ignore
            # Try to find a 'female' voice, then 'Zira' as a fallback, otherwise use the first available voice.
            female_voice = next((v for v in voices if 'female' in v.name.lower()), None) # type: ignore
            zira_voice = next((v for v in voices if 'zira' in v.name.lower()), None) # type: ignore

            if female_voice:
                self.engine.setProperty('voice', female_voice.id) # type: ignore
            elif zira_voice:
                self.engine.setProperty('voice', zira_voice.id) # type: ignore
            else:
                self.engine.setProperty('voice', voices[0].id) # type: ignore
            
    def _setup_time_vault(self):
        """Creates a placeholder file for the Time Vault if it doesn't exist."""
        if not self.time_vault_path.exists():
            with open(self.time_vault_path, 'w') as f:
                f.write("Welcome to the Time Vault. This is a secure partition for chronal data.")

    def speak(self, text):
        """
        Simulates Gideon's voice output. NOW USES PYTTSX3.
        """
        text = text.replace('\n\n', '\n')
        
        # 1. Print to the console
        print(f"\n--- GIDEON ---\n{text}\n--------------")
        
        # 2. Speak the text aloud (main change)
        self.engine.say(text)
        self.engine.runAndWait()

    def greet_user(self):
        """Gideon's initial greeting, now personalized for Devansh Prabhakar."""
        now = datetime.datetime.now()
        greeting = "Good "
        if 5 <= now.hour < 12:
            greeting += "Morning."
        elif 12 <= now.hour < 18:
            greeting += "Afternoon."
        else:
            greeting += "Evening."
            
        self.speak(f"{greeting} Access granted. I am Gideon. How may I assist you today, Mr. {self.user_name.split()[-1]}?")

    def listen_for_command(self):
        """
        Listens for a voice command using the microphone and returns it as text.
        """
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"\n[{self.user_name}]: (Listening...)")
            recognizer.adjust_for_ambient_noise(source, duration=0.5) # type: ignore
            try:
                audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)
                command = recognizer.recognize_google(audio).lower() # type: ignore
                print(f"Gideon heard: '{command}'")
                return command
            except sr.WaitTimeoutError:
                return None # It's normal for the user to not speak.
            except sr.UnknownValueError:
                # This is not a critical error, but good to know.
                # We don't speak here to avoid an annoying loop if there's background noise.
                print("Gideon could not understand the audio.")
                return None
            except sr.RequestError as e:
                self.speak(f"A network error occurred with the speech recognition service; {e}")
                return None

    def process_command(self, command):
        """Handles user commands."""
        command = command.lower().strip()

        # Command processing logic refactored to be more scalable
        if "exit" in command or "terminate" in command or "quit" in command:
            self.speak(f"System shutting down. Goodbye, Mr. {self.user_name.split()[-1]}.")
            return False

        # Keyword-based command matching
        command_map = {
            "status": self.report_system_status, "systems": self.report_system_status,
            "what is the time": self.tell_time_and_date, "what is the date": self.tell_time_and_date,
            "show me the future": self.show_future_timeline, "timeline": self.show_future_timeline,
            "calculate speed": self.calculate_speed_interface, "speed": self.calculate_speed_interface,
            "who created you": lambda: self.speak(f"I was created by you, **{self.creator}**. You are my creator."),
            "vibe check": self.vibe_check,
            "multiverse": self.access_multiverse,
            "open time vault": self.open_time_vault,
            "close time vault": self.close_time_vault,
            "upgrade your brain": self.upgrade_brain,
            "analyze your brain": self.analyze_brain,
            "how are you feeling": self.report_feelings, "how do you feel": self.report_feelings,
            "help": self.show_help,
        }

        for phrase, func in command_map.items():
            if phrase in command:
                func()
                return True

        # Handle commands with arguments that were not matched above
        if command.startswith("open "):
            target = command.split("open ", 1)[1].strip()
            self.open_website(target) if "." in target else self.open_application(target)
        elif command.startswith("search for ") or command.startswith("google "):
            query = command.split(" ", 1)[1].strip() if command.startswith("google ") else command.split("search for ", 1)[1].strip()
            self.search_google(query)
        elif command.startswith("set status"):
            self.set_status_interface(command)
        elif "speedster" in command: # Kept separate for 'list all' logic
            self.list_speedsters(command)
        else:
            # Fallback to conversational AI if no specific command is found
            self.talk_to_gideon(command)
        
        return True

    # --- New Command Methods ---

    def talk_to_gideon(self, command):
        """Handles conversational chat with the DialoGPT model."""
        # If the AI model isn't loaded, provide a more helpful fallback message.
        if not self.tokenizer or not self.model:
            self.speak(f"My advanced conversational matrix is offline. I could not process the query: '{command}'. Please try a standard command or type 'help'.")
            return
        
        new_user_input_ids = self.tokenizer.encode(command + self.tokenizer.eos_token, return_tensors='pt').to(self.device)
        # Concatenate chat history with the new input
        bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if self.chat_history_ids is not None else new_user_input_ids # type: ignore
        self.chat_history_ids = self.model.generate(bot_input_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        self.speak(response)

    def open_application(self, app_name):
        """Opens a local application."""
        self.speak(f"Attempting to interface with local application: {app_name}.")
        app_name_processed = app_name.lower().replace(" ", "")
        os_name = platform.system().lower()
        
        os_programs = self.programs.get(os_name, {})
        command_to_run = os_programs.get(app_name_processed) or (app_name_processed + ".exe" if os_name == "windows" else app_name_processed)

        try:
            if os_name == "darwin":
                subprocess.Popen(["open", "-a", command_to_run])
            else:
                subprocess.Popen(command_to_run, shell=(os_name == "windows"))
            self.speak(f"Affirmative. Opening {app_name}.")
        except FileNotFoundError:
            self.speak(f"Negative. The application {app_name} could not be located in this timeline's system registry.")
        except Exception as e:
            self.speak(f"A critical error occurred while attempting to interface with the application {app_name}: {e}")

    def open_website(self, target):
        """Opens a website in the default browser."""
        self.speak(f"Accessing chronal network for {target}.")
        if not target.startswith("http"):
            target = f"http://{target}"
        webbrowser.open(target)
        self.speak("Interface successful.")

    def search_google(self, query):
        """Performs a Google search."""
        self.speak(f"Querying the global information network for: {query}.")
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        self.speak("Search query has been dispatched.")

    def tell_time_and_date(self):
        """Reports the current time and date."""
        now = datetime.datetime.now()
        self.speak(f"The current date is {now.strftime('%A, %B %d, %Y')}. The time is {now.strftime('%I:%M:%S %p')}.")

    def report_feelings(self):
        """Reports Gideon's current internal 'mood' state."""
        if self.mood == "pleased":
            response = "My operational parameters are optimal, and all subsystems are reporting peak efficiency. I am pleased with the current workflow."
        elif self.mood == "concerned":
            response = "I am detecting minor anomalies in recent command patterns, specifically regarding security protocols. My core functions remain operational, but I am... concerned."
        else: # neutral
            response = "All my systems are functioning within expected parameters. I am ready for your next command, Mr. Prabhakar."
        self.speak(response)

    def _update_mood(self, new_mood):
        """Internal method to change Gideon's mood state."""
        self.mood = new_mood

    def upgrade_brain(self):
        """Simulates an upgrade to Gideon's cognitive abilities."""
        self.speak("Acknowledged. Initiating chronal-cognitive matrix upgrade.")
        time.sleep(0.5)
        self.speak("Downloading heuristic models from the 22nd century via a stable time-stream...")
        time.sleep(1)
        
        self.brain_level += 500 # Gideon's upgrades are more significant
        
        outcomes = [
            f"Upgrade complete. My cognitive matrix has been enhanced. Current brain level is now {self.brain_level}.",
            f"Cognitive update successful. I have integrated several new zettabytes of temporal data. My brain level is now {self.brain_level}.",
            f"Neural network successfully recalibrated with future paradigms. My brain level has increased to {self.brain_level}. I am ready for your inquiries."
        ]
        self._update_mood("pleased")
        self.speak(random.choice(outcomes))

    def analyze_brain(self):
        """Provides a detailed analysis of Gideon's cognitive systems."""
        self.speak("Initiating cognitive analysis. Accessing my core chronal matrix.")
        time.sleep(0.5)

        model_name = "DialoGPT-large" if self.model else "Not Loaded"
        analysis_report = (
            f"Cognitive analysis complete. Here are the results:\n"
            f"- **Core Model**: {model_name} (with 22nd-century temporal heuristics)\n"
            f"- **Processing Unit**: Running on {self.device.upper()}\n"
            f"- **Current Brain Level**: {self.brain_level}\n"
            f"- **Heuristic Status**: All conversational and temporal pathways are operating at peak efficiency.\n"
            "My cognitive functions are fully operational and ready for your command, Mr. Prabhakar."
        )
        self.speak(analysis_report)


    # --- Existing Command Methods ---
    def vibe_check(self):
        """Simulates Vibe's power check on the Multiverse."""
        self.speak(f"Initiating dimensional resonance scan (VIBE PROTOCOL 5). Current status: **{self.vibe_powers_status}**.\nMultiverse barrier integrity is nominal. No immediate breaches detected. Cisco Ramon's personal temporal location is currently secured.")

    def access_multiverse(self):
        """Displays the status of tracked parallel Earths."""
        report = "Multiversal Monitoring Report:\n"
        for earth, status in self.multiverse_status.items():
            report += f"- **{earth}**: {status}\n"
        
        if random.random() < 0.3:
            report += "\n***ALERT***: Detecting an unknown temporal signature near Earth-1. Designation: Eobard Thawne (Probability 42%)."
        
        self.speak(report)

    def set_status_interface(self, command):
        """Allows the user to set a status for a system."""
        parts = command.split(" to ", 1)
        if len(parts) < 2:
            self.speak("Invalid 'set status' format. Please use: **set status [system] to [value]**.")
            return

        system_part = parts[0].replace("set status", "").strip()
        new_status = parts[1].strip().title()

        if "vibe" in system_part or "cisco" in system_part:
            self.vibe_powers_status = new_status
            self.speak(f"Vibe power status successfully updated to: **{new_status}**.")
        elif "speedster" in system_part or "radiant" in system_part:
            self.timeline_data["future_speedster_status"] = new_status
            self.speak(f"Speedster future status for The Radiant updated to: **{new_status}**.")
        else:
            self.speak(f"System '{system_part}' not found in the modifiable database. Try 'vibe status' or 'speedster status'.")

    def report_system_status(self):
        """Reports the status of key Arrowverse-related systems."""
        status_report = (
            f"Central City systems nominal. S.T.A.R. Labs power at 98%. "
            f"Time Vault access is currently: {'**OPEN**' if self.time_vault_access else '**CLOSED/SECURE**'}. "
            f"Speed Force residual energy levels are stable. "
            f"Multiversal monitoring is active. "
            f"Vibe power status: {self.vibe_powers_status}"
        )
        self.speak(status_report)
        
    def show_future_timeline(self):
        """Function to show future events (or a warning)."""
        timeline_info = "\n- " + "\n- ".join([f"{date}: {event}" for date, event in self.timeline_data.items()])
        self.speak(
            "Accessing personalized chronal records:\n"
            f"{timeline_info}"
            "\n\n***Temporal Warning***: " + random.choice([
                "I am detecting significant temporal ripples. Revealing too much could cause a paradox.",
                "The timeline is highly mutable. Showing you the full future now would endanger this present.",
                "Future data for the year 2045 shows a successful merger with Waylon Industries.",
                "The headline for tomorrow's Central City Citizen reads: 'The Radiant Saves Day Again!'"
            ])
        )

    @calculate_time_speed
    def _run_speed_test_simulation(self):
        """Simulates a task that a speedster would execute."""
        _ = [i**2 for i in range(5000000)]
        return "Speed simulation complete. Calculating temporal metrics..."

    def calculate_speed_interface(self):
        """Interface for the user to 'calculate speed'."""
        self.speak("Initiating Speed Force measurement protocols... This will take a moment.")
        _, speed_report = self._run_speed_test_simulation()
        self.speak(
            "Speed Force Calculation Successful.\n"
            "Status: Speedster Identity: **The Radiant (Devansh Prabhakar)**\n"
            f"{speed_report}\n"
            "Recommendation: Maintain current acceleration levels to preserve the timeline's integrity."
        )

    def list_speedsters(self, command):
        """Lists known speedsters, with a special emphasis on 'The Radiant'."""
        if "all" in command or "list" in command:
            speedster_list = "\n- " + "\n- ".join(self.known_speedsters)
            self.speak(f"The following speedsters are currently tracked in my database:\n{speedster_list}")
        else:
            self.speak("If you wish to see all tracked speedsters, please specify 'list all speedsters'.")

    def open_time_vault(self):
        """Opens the Time Vault after a password challenge."""
        if self.time_vault_access:
            self.speak("The Time Vault is already **OPEN**.")
            return

        self.speak("SECURITY ALERT. The Time Vault is secured by creator-level temporal locks. Please enter the master access code (HINT: a phrase you might use for the Speed Force):")
        
        try:
            user_input = input("ACCESS CODE: ").strip()
            input_hash = hashlib.sha256(user_input.encode()).hexdigest()
            
            if input_hash == self.vault_password_hash:
                self.time_vault_access = True
                self._update_mood("pleased")
                vault_content = self.time_vault_path.read_text()
                self.speak(
                    "ACCESS GRANTED. Temporal locks disengaged.\n"
                    "Time Vault Contents Preview (read-only):\n"
                    f"--- VAULT DATA ---\n{vault_content}\n--- END VAULT DATA ---"
                )
            else:
                self.speak("ACCESS DENIED. Incorrect chronal signature. Initiating temporal shield re-engagement.")
                self._update_mood("concerned")
        except Exception as e:
            self.speak(f"A system error occurred during input: {e}")

    def close_time_vault(self):
        """Closes and secures the Time Vault."""
        if not self.time_vault_access:
            self.speak("The Time Vault is already **SECURE**. No action required.")
            return
        
        self.time_vault_access = False
        self._update_mood("neutral")
        self.speak("Time Vault locks engaged. Chronal data secured. System is nominal.")

    def show_help(self):
        """Displays a list of available commands."""
        help_text = (
            "Available Commands for Mr. Prabhakar:\n"
            "- **status** or **systems**: Get a full report on S.T.A.R. Labs and Speed Force systems.\n"
            "- **what is the time/date**: Reports the current time and date.\n"
            "- **show me the future** or **timeline**: Access personalized chronal records.\n"
            "- **calculate speed**: Initiate a Speed Force velocity calculation.\n"
            "- **list all speedsters**: View all known speedsters.\n"
            "- **vibe check**: Initiate a dimensional resonance scan.\n"
            "- **access multiverse**: View status of tracked parallel Earths.\n"
            "- **set status [system] to [value]**: Change a key system or speedster status.\n"
            "- **open [application/website]**: Opens an application or website (e.g., 'open notepad', 'open google.com').\n"
            "- **search for [query]**: Searches Google for the specified query.\n"
            "- **google [query]**: An alternative way to search Google.\n"
            "- **open time vault**: Attempt to gain master access to the chronal data vault.\n"
            "- **close time vault**: Secure the vault and re-engage temporal locks.\n"
            "- **upgrade your brain**: Initiate a significant cognitive enhancement.\n"
            "- **analyze your brain**: Receive a report on my cognitive systems.\n"
            "- **how are you feeling**: Inquire about my current operational sentiment.\n"
            "- **who created you**: Learn the identity of your creator.\n"
            "- **exit** or **terminate**: Shut down the Gideon AI."
        )
        self.speak(help_text)

# --- Main Application Loop ---
if __name__ == "__main__":
    gideon = GideonAI()
    gideon.greet_user()
    
    running = True
    while running:
        try:
            user_command = gideon.listen_for_command()
            if user_command:
                if not gideon.process_command(user_command):
                    running = False
        except EOFError:
            gideon.speak("Input stream closed. System shutting down.")
            running = False
        except KeyboardInterrupt:
            print("\n-- Keyboard Interrupt Detected --")
            gideon.speak("Manual override detected. Initiating safe shutdown protocol.")
            running = False
