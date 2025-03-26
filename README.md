# piper_podcast

Podcast generator with 2 hosts using [Ollama](https://ollama.com/) and [Piper](https://github.com/rhasspy/piper). Inspired by NotebookLM, but is generally of much lower quality. 

## Requirements
* Tested on Python 3.13
* Install the requirments with pip: `pip install -r requirements.txt`
* Piper installed and in PATH (executable with `piper-tts`)
* Download Piper voice models to the `voices` folder: https://rhasspy.github.io/piper-samples/
* Ollama installed and serving
* [llama3.2](https://ollama.com/library/llama3.2)

## Usage
1. Create a text file where you insert the text you want the AI to discuss.
2. Execute the script with this syntax:
```bash
python podcast.py <speaker 1>.onnx <speaker 2>.onnx <text>.txt 
```
3. Check the script, press Enter, and your podcast will be generated to `./audio/generated/<current time>.ogg`

## Demo
Based on text from this article: https://en.wikipedia.org/wiki/IP_over_Avian_Carriers