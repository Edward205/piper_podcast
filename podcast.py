import re
import requests
import subprocess
import time
from pydub import AudioSegment
import sys

def piper_generate(text, model, output):
  command = ["piper-tts", "--model", str(model), "--output_file", str(output)]

  process = subprocess.Popen(command, stdin=subprocess.PIPE)
  process.communicate(input=text.encode("utf-8"))


def replace_name(input_text):
    lines = input_text.splitlines()
    
    processed_lines = []

    for line in lines:
        match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (.*)', line)
        if match:
            date_part = match.group(1)  
            rest_of_line = match.group(2) 
            processed_lines.append(f"{date_part} {rest_of_line}")
        else:
            processed_lines.append(line)
    
    return "\n".join(processed_lines)

def clean_text(input_text):
    pattern = r'\*.*?\*|\[.*?\]|\(.*?\)|<.*?>'
    result = re.sub(pattern, '', input_text)
    return result.strip()

def stitch_audio(files, output_file):
  combined_audio = AudioSegment.empty()

  for file in files:
      try:
          audio = AudioSegment.from_file(file)
          combined_audio += audio
      except Exception as e:
          print(f"Error processing {file}: {e}")
  
  try:
      combined_audio.export(output_file, format="ogg")
      print(f"Combined audio saved to {output_file}")
  except Exception as e:
      print(f"Error saving combined audio: {e}")

file = open(sys.argv[3], "r") 
messages = file.read()
messages = replace_name(messages)

request = {
  "model": "llama3.2",
  "messages": [
    {
      "role": "system",
      "content": "Summarise messages from a chat room in the form of a two-speaker podcast, precisely following the given instructions. Your job is to embody and generate a podcast from two hypothetical hosts. Do not include any action descriptions (such as \"[laughs]\", \"(pauses)\")."
    },
    {
        "role": "user",
        "content": messages + "\n-------------------\nInstructions: Create a podcast style summarising all topics discussed above with two speakers. Use \"<speaker1>\" and \"<speaker2>\" tags to denote the speakers (example: \"<speaker1> This was interesting <speaker2> I agree\"). Do not include any action descriptions (e.g. \"[laughs]\", \"(pauses)\"). The tone should be informal, rambling, and somewhat nonsensical. ONLY write in the perspective of the two hypothetical hosts."
    },
  ],
    "stream": False
}
url = "http://localhost:11434/api/chat"

response = requests.post(url, json=request)
print(response.status_code)
response = response.json()
response_content = ""
if response != None:
  response_content = response['message']['content'].replace("\n", "")
else:
  print("LLM generation failed")
  exit()

result = re.split(r"</?[Ss]peaker[12]>|\[[Ss]peaker[12]\]", response_content)
print("\n".join(map(str, result)))
if len(response) < 2:
  print("Generation probably failed")
  exit()

print("Press ENTER if this is okay.")
input()

files = []
voices = [sys.argv[1], sys.argv[2]]
count = 0
for line in result:
  voice_index = 0
  if count % 2 != 0:
    voice_index = 1
  print("Generating [" + str(count) + "/" + str(len(result)) + "]")

  file = "./audio/cache/"+str(count)
  piper_generate(clean_text(line), "./voices/"+voices[voice_index], file)
  files.append(file)

  count = count + 1
  
stitch_audio(files, "./audio/generated/"+str(time.time())+".ogg")
