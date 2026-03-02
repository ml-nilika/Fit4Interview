def analyze_voice(text, duration):
    if duration == 0 or text.strip() == "":
        return 0, "No voice detected."

    words = len(text.split())
    wpm = int((words / duration) * 60)

    if wpm < 90:
        feedback = "You are speaking too slowly. Try to sound more confident."
        score = 40
    elif wpm > 160:
        feedback = "You are speaking too fast. Slow down for clarity."
        score = 50
    else:
        feedback = "Good speaking pace. Sounds confident."
        score = 80

    return score, feedback
