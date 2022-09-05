# Video-CLIP-Indexer
A GUI short-video 'clip' indexer in 60 lines.

## Basic Usage
### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Run the streamlit GUI
```bash
streamlit run app.py
```

## Parameters
### Text Prompt
You can use a prompt to describe the scene you want to search for. The indexer will return several clips related to it.
### Top N
The number of video clips you want to be returned.
### Cut Sim
Approximately from 0.44 to 0.6. The smaller the number, the longer the video clips(with lower precise).
### CLIP-as-service Server
The url of CLIP-as-service Server. The default value is a demo server loaded with ViT-L/14-336px provided by Jina.ai. You can also run your own [CLIP-as-service](https://github.com/jina-ai/clip-as-service) server.
