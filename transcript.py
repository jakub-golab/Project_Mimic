import time
import pyaudio
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.pause_threshold = 8.0

def recognize_speech(audio):
    try:
        text = recognizer.recognize_google(audio)
        timestamp = time.strftime("[%H:%M:%S]", time.localtime())
        return text, timestamp

    except sr.UnknownValueError:
        print("")

    except sr.RequestError as req:
        print(f"Service error: {req}")
    
    return None


def save(speech_data):
    if speech_data:
        text, timestamp = speech_data
        with open("speech_transcript.txt", 'a') as file:
            file.write(f"{timestamp} {text}\n")


def speech_to_text():

    with sr.Microphone() as source:

        print("Starting calibration. Don't talk for now...")
        recognizer.adjust_for_ambient_noise(source, duration = 1)
        time.sleep(1)
        print("Calibration finished. You can start speaking now...")

        start_time = time.time()

        try:
            audio = recognizer.listen(source, timeout = 10, phrase_time_limit = None)
            speech_data =recognize_speech(audio)
            save(speech_data)
        
        except sr.WaitTimeoutError:
            print("Maximum time without speech reached")

        except Exception as e:
            print(e)


def main():
    speech_to_text()
    print("Transcript finished!")


if __name__ == '__main__':
    main()
