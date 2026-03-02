import speech_recognition as sr
import time

def get_voice_text():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            start_time = time.time()

            audio = r.listen(
                source,
                timeout=5,              # wait max 5 sec for speech
                phrase_time_limit=10    # stop after 10 sec speaking
            )

            end_time = time.time()

        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return "", 0

    duration = round(end_time - start_time, 2)

    try:
        text = r.recognize_google(audio, language="en-IN")
        print("Recognized:", text)
        return text, duration

    except sr.UnknownValueError:
        print("Google could not understand audio")
        return "", duration

    except sr.RequestError as e:
        print("API request failed:", e)
        return "", duration

