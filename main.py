import json
import datetime
import uuid
import argparse # For command-line arguments
import sys # To exit cleanly and get script name
import os # To get base script name

# --- Functions (get_user_choice, generate_filename, load_and_display_json) remain the same ---

def get_user_choice(prompt, options):
    """Gets validated user choice from multiple options."""
    print(f"\n{prompt}")
    for key, value in options.items():
        print(f"  {key}: {value}")

    while True:
        choice = input("Your choice: ").strip().upper()
        if choice in options:
            return choice, options[choice]
        else:
            print(f"Invalid choice. Please enter one of {list(options.keys())}")

def generate_filename():
    """Generates a filename like IT-career-advice-YYYYMMDD-HHMMSS.json"""
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    return f"IT-career-advice-{timestamp_str}.json"

def load_and_display_json(filepath):
    """Loads a JSON file and prints its content."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"\n--- Contents of {filepath} ---")
        print(json.dumps(data, indent=2))
        print("-" * (len(f"--- Contents of {filepath} ---"))) # Match separator length
        # Optional: Add validation against the schema here if needed
        # ... (schema validation code) ...

    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'. File might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred while loading {filepath}: {e}")

def run_it_career_expert_system():
    """Runs the IT career progression expert system Q&A and saves the log."""

    # --- Introduction ---
    # (Welcome message is now printed before this function is called in interactive mode)
    # print("--- Welcome to the Simple IT Career Progression Advisor ---")
    # ... rest of welcome message ...

    # 1. Confirm Decision Space
    initial_prompt = "What is your decision space input? (e.g., 'advice on IT career progression')"
    user_decision_space = input(f"{initial_prompt}\n> ")

    # --- Refined Check for Decision Space ---
    is_it_related = "it" in user_decision_space.lower() or \
                    "information technology" in user_decision_space.lower() or \
                    "tech" in user_decision_space.lower()
    is_career_related = "career" in user_decision_space.lower() or \
                        "job" in user_decision_space.lower() or \
                        "progress" in user_decision_space.lower()

    session_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {}

    if not (is_it_related and is_career_related):
        print("\n--------------------------------------------------")
        print("This expert system is specifically designed to provide advice on")
        print("**IT career progression**.")
        print(f"Your input ('{user_decision_space}') doesn't seem to match this focus.")
        print("Exiting session.")
        print("--------------------------------------------------")

        log_entry = {
            "session_id": session_id, "timestamp": timestamp,
            "initial_prompt": initial_prompt, "user_decision_space_input": user_decision_space,
            "outcome": "User input did not match the expected decision space (IT Career Progression).",
            "interactions": [], "final_advice": None
        }
        print("\n--- Interaction Log (JSON) ---")
        print(json.dumps(log_entry, indent=2))
        try:
            filename = generate_filename()
            with open(filename, "w") as f: json.dump(log_entry, f, indent=2)
            print(f"\nPartial interaction log saved to: {filename}")
        except Exception as e: print(f"\nError saving partial log to file: {e}")
        return

    # --- Proceed if input is relevant ---
    print("\nGreat! Let's explore some options for your IT career progression.")
    interactions = []
    answers = {}

    # --- Questions 1, 2, 3 (same as before) ---
    q1_text = "What is your current experience level?"
    q1_options = { "A": "Entry-level (0-2 years)", "B": "Mid-level (3-7 years)", "C": "Senior-level (8+ years)" }
    choice_key, choice_value = get_user_choice(q1_text, q1_options)
    interactions.append({ "step": 1, "question": q1_text, "options": q1_options, "user_answer_key": choice_key, "user_answer_value": choice_value })
    answers["experience"] = choice_key

    q2_text = "What is your primary career goal right now?"
    q2_options = { "A": "Deepen technical expertise...", "B": "Move into management...", "C": "Explore different specialization...", "D": "Increase compensation...", "E": "Improve work-life balance." } # Shortened for brevity
    choice_key, choice_value = get_user_choice(q2_text, q2_options)
    interactions.append({ "step": 2, "question": q2_text, "options": q2_options, "user_answer_key": choice_key, "user_answer_value": choice_value })
    answers["goal"] = choice_key

    q3_text = "What's your preferred method for acquiring new skills?"
    q3_options = { "A": "Formal Certifications...", "B": "Structured Courses...", "C": "Self-study & Practice...", "D": "On-the-job Training..." } # Shortened for brevity
    choice_key, choice_value = get_user_choice(q3_text, q3_options)
    interactions.append({ "step": 3, "question": q3_text, "options": q3_options, "user_answer_key": choice_key, "user_answer_value": choice_value })
    answers["learning"] = choice_key


    # --- Basic Advice Logic (same as before) ---
    advice = "Based on your answers, here is some general advice:\n"
    # (...rest of the advice generation logic...)
    if answers["experience"] == "A": advice += "- Focus on building foundational skills...\n"
    elif answers["experience"] == "B": advice += "- Look for opportunities to take on more responsibility...\n"
    else: advice += "- Focus on strategic impact...\n"

    if answers["goal"] == "D": advice += "- Research salary benchmarks...\n"
    if answers["goal"] == "E": advice += "- Identify sources of imbalance...\n"

    if answers["learning"] == "A": advice += f"- Prioritize certifications...\n"
    # (... rest of learning advice ...)
    advice += "\nRemember: Continuous learning, networking, and seeking feedback are crucial for IT career growth."


    print("\n--- Advice ---")
    print(advice)

    # --- Store final log ---
    log_entry = {
        "session_id": session_id, "timestamp": timestamp,
        "initial_prompt": initial_prompt, "user_decision_space_input": user_decision_space,
        "outcome": "Provided career advice.",
        "interactions": interactions, "final_advice": advice
    }

    print("\n--- Interaction Log (JSON) ---")
    json_output = json.dumps(log_entry, indent=2)
    print(json_output)

    # Save to a file
    try:
        filename = generate_filename()
        with open(filename, "w") as f: json.dump(log_entry, f, indent=2)
        print(f"\nInteraction log saved to: {filename}")
    except Exception as e: print(f"\nError saving log to file: {e}")


# --- Main execution block ---
if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(
        # Updated description to explain modes
        description="""Simple IT Career Advisor expert system.
Runs in one of two modes:
  1. Interactive Mode (default): Asks questions, provides advice, and saves a session log.
  2. Load Mode (--load-json): Loads and displays a previously saved JSON log file.""",
        # Use RawTextHelpFormatter to preserve newlines in description and help text
        formatter_class=argparse.RawTextHelpFormatter
        )
    parser.add_argument(
        "--load-json",
        metavar="FILENAME",
        type=str,
        # Updated help text with clearer example command structure
        help="Load and display a previously saved JSON log file instead of running interactively.\n"
             "Example Usage:\n"
             "  python %(prog)s --load-json IT-career-advice-YYYYMMDD-HHMMSS.json\n"
             "  python %(prog)s --load-json path/to/your/log_file.json"
    )

    # Parse arguments from command line
    args = parser.parse_args()

    # Get the base name of the script (e.g., main.py or it_advisor.py)
    script_name = os.path.basename(sys.argv[0])

    # Check if the --load-json argument was provided
    if args.load_json:
        print(f"--- Load JSON Mode ---")
        print(f"Attempting to load: '{args.load_json}'")
        load_and_display_json(args.load_json)
        sys.exit(0) # Exit after loading the file
    else:
        # --- Interactive Mode ---
        # Print welcome and instructions for interactive mode
        print("--- Welcome to the Simple IT Career Progression Advisor ---")
        print("This script will ask questions to provide basic IT career advice.")
        print("-" * 60)
        # --- Add the specific tip here ---
        print(f"(Tip: You can also view a previously saved session log.)")
        print(f"(To do so, run this script again using the --load-json option, like this:")
        print(f"   python {script_name} --load-json <filename.json> )")
        print("-" * 60)

        # Run the main interactive function
        run_it_career_expert_system()