from flask import Flask, jsonify
import random
import datetime

app = Flask(__name__)

# List of people and duties
people = ["Love", "Arpan", "Keshav", "Jyoti", "Prabh"]
duties = ["Upper Washroom", "Lower Washroom", "Mop and Broom", "Vacuum Cleaning", "Kitchen"]

# Load the previous week's schedule
def load_previous_schedule():
    try:
        with open("previous_schedule.txt", "r") as file:
            lines = file.readlines()
            return {line.split(":")[0]: line.split(":")[1].strip() for line in lines}
    except FileNotFoundError:
        # Return None if no previous schedule exists
        return None

# Save the current schedule to a file
def save_schedule(schedule):
    with open("previous_schedule.txt", "w") as file:
        for person, duty in schedule.items():
            file.write(f"{person}: {duty}\n")

# Generate the next week’s schedule based on the previous one
def generate_next_schedule(previous_schedule):
    if not previous_schedule:
        random.shuffle(duties)
        return {person: duties[i] for i, person in enumerate(people)}
    else:
        previous_duties = [previous_schedule[person] for person in people]
        rotated_duties = previous_duties[1:] + previous_duties[:1]
        return {person: rotated_duties[i] for i, person in enumerate(people)}

# Format the schedule into a message
def format_schedule_message(schedule):
    today = datetime.date.today().strftime("%a, %b %d %Y")
    message = f"Duty Assignments for the Week Starting {today}:\n\n"
    for person, duty in schedule.items():
        message += f"- {person}: {duty}\n"
    return message

@app.route('/duty', methods=['GET'])
def duty():
    # Load the previous schedule
    previous_schedule = load_previous_schedule()

    # Generate the next schedule
    current_schedule = generate_next_schedule(previous_schedule)

    # Save the current schedule
    save_schedule(current_schedule)

    # Format the message
    message = format_schedule_message(current_schedule)

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)
