from ultralytics import YOLO
import openai
from gtts import gTTS
from io import BytesIO
import pygame
import tempfile
import time

model= YOLO('E:\\Projects\\object_detection\\data\\yolov8\\best.pt')
model.predict(source='E:\\Projects\\object_detection\\data\\uploads', save=True)

# Run inference on the source
all_coords = []  # Initialize an empty list to store coordinates

results = model(source='E:\\Projects\\object_detection\\data\\uploads')
for result in results:
    boxes = result.boxes.xyxy
    coord = boxes.tolist()

    # Convert the tensor to a Python list
    all_coords.append(coord)  # Append coord to the list

# Now, 'all_coords' contains all the coordinates as Python lists from each iteration
print(all_coords)

#chatgpt



# Set your OpenAI API key

openai.api_key = "your-secret-api-key"


messages = [{"role": "system", "content": "You are an intelligent assistant."}]

message = """
explain this yolo object detection output to alert the blind person
tell them where the vehicle is with the help of coordinates
do not tell them coordinates, tell them the location like it is located
like left or right in two or three lines, guide them.
Don't put bulletins:image 1/1 E:\Projects\object_detection\data\predict\download.jpeg: 448x640 1 bike, 1713.3ms
Speed: 5.0ms preprocess, 1713.3ms inference, 1.0ms postprocess per image at shape (1, 3, 448, 640)
[[[64.16331481933594, 27.104263305664062, 211.88125610351562, 154.1317138671875]]]
"""

if message:
    messages.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    reply = chat.choices[0].message.content

    # Save the ChatGPT response to a text file
    with open("chatgpt_response.txt", "w") as file:
        file.write(reply)

    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})

# Function to convert text to speech
def speak(text, language='en'):
    mp3_fo = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(mp3_fo)
    return mp3_fo

pygame.init()
pygame.mixer.init()

# Read text from a file
with open('chatgpt_response.txt', 'r') as file:
    text_to_speak = file.read()

# Generate speech and save it to a temporary file
sound = speak(text_to_speak)

temp_mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
temp_mp3_file.write(sound.getvalue())
temp_mp3_file.close()

# Load and play the temporary MP3 file
pygame.mixer.music.load(temp_mp3_file.name)
pygame.mixer.music.play()

# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.delay(100)

# Clean up the temporary file
temp_mp3_file.unlink(temp_mp3_file.name)





