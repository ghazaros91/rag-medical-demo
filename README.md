# Medical RAG Demo

This project is designed to demonstrate simple use case for RAG on domain specific data that are medical progress notes.


# Installation

```
git clone rag-demo
cd rag-demo
```

## Run Ollama
```
brew install ollama
ollama serve
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

## Open new terminal and set up virtual environemnt
```
python3.12 -m venv venv
source venv/bin/activate
```

## Install Dependencies
```
pip3.12 install -r requirements.txt
```

## Run CLI

```
python3.12 main.py
```

## Run Gradio UI (optional)
```
python3.12 app.py
```

open http://127.0.0.1:7860

## Run tests
```
pytest -q
```

