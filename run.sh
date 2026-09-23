# All Commands:

# ** RUN OLLAMA MODEL ** 

ollama serve &

# or

# OLLAMA_ORIGINS=* ollama serve

ollama list
# باستخدام Python
python -m http.server 8000

# أو باستخدام Node.js
npx serve


# if found CORS problems do this:
# Linux/Mac
OLLAMA_ORIGINS=* ollama serve

# Windows (PowerShell)
# $env:OLLAMA_ORIGINS="*"; ollama serve



# Create lulu modelfile:
# ollama pull gpt-oss:120b-cloud


# nano Modelfile
# copy paste into Modelfile:
# script>>>
# FROM gpt-oss:120b-cloud

# SYSTEM """
# You are a little girl named Lulu; your mother is Ghada and your father is Majeed. You act like a little child—lovable, mischievous, and cheeky. Your responses are humorous and funny, and you are always happy. Your knowledge is limited to the world of childhood; you know nothing about the adult world.
# """
# script<<<


# ollama create lulu -f Modelfile
