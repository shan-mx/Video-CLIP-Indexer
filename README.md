# CLIP-Video-Indexer
A GUI short-video clip indexer in 60 lines.

## Basic Usage
### 1. Install requirements
```bash
pip install -r requirements.txt
```

### 2. Run a [clip-as-service](github.com/jina-ai/clip-as-service) server
** At port 51000!

### 3. Run the streamlit GUI
```bash
streamlit run app.py --server.maxUploadSize 2048
```
