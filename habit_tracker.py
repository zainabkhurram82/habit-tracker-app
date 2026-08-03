import json
import datetime
import os
import matplotlib.pyplot as plt

FILE = "habits.json"
REMINDER_FILE = "reminder.txt"

def load_habits():
    """Load habits from file. If no file, return empty dict"""
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_habits(habits):
    """Save habits dict to file"""
    with open(FILE, "w") as f:
        json.dump(habits, f, indent=4)

def mark_habit(habit_name):
    """Mark a habit as done for today"""
    habits = load_habits()
    today = str(datetime.date.today())

    if habit_name not in habits:
        habits[habit_name] = [] # create new habit list

    if today not in habits[habit_name]:
        habits[habit_name].append(today)
        print(f"✅ Done! Marked '{habit_name}' for {today}")
    else:
        print(f"You already marked '{habit_name}' today")

    save_habits(habits)

def show_habits():
    """Show all habits and total days"""
    habits = load_habits()
    if not habits:
        print("No habits yet. Add one!")
        return

    print("\n--- Your Progress ---")
    for habit, dates in habits.items():
        print(f"{habit}: {len(dates)} days | Last done: {dates[-1]}")
    print("---------------------\n")

def show_chart():
    """Show streak graph for last 7 days using matplotlib"""
    habits = load_habits()
    if not habits:
        print("No data to show chart")
        return

    # Get last 7 days
    today = datetime.date.today()
    last_7_days = [(today - datetime.timedelta(days=i)).isoformat() for i in range(6, -1, -1)]

    names = list(habits.keys())
    data = []
    for habit in names:
        count = sum(1 for d in habits[habit] if d in last_7_days)
        data.append(count)

    plt.figure(figsize=(8, 4))
    plt.bar(names, data, color='skyblue')
    plt.title("Habit Streaks - Last 7 Days")
    plt.xlabel("Habits")
    plt.ylabel("Days Completed")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

def set_reminder():
    """Set reminder time. For MVP we save it. Full version = WhatsApp API"""
    time = input("Enter reminder time [e.g. 8:00 PM]: ")
    with open(REMINDER_FILE, "w") as f:
        f.write(time)
    print(f"⏰ Reminder set for {time} daily!")
    print("NOTE: Next version will connect to WhatsApp API to send reminders")

# --- MAIN LOOP ---
while True:
    print("\n1. Mark Habit 2. Show Progress 3. Show Chart 4. Set Reminder 5. Exit")
    choice = input("Choose option: ")

    if choice == "1":
        name = input("Enter habit name: ")
        mark_habit(name)
    elif choice == "2":
        show_habits()
    elif choice == "3":
        show_chart()
    elif choice == "4":
        set_reminder()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice")
