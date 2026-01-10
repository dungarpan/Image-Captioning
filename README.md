# Image Captioning API

A FastAPI-based REST API for generating captions for images using the BLIP (Bootstrapping Language-Image Pre-training) model from Salesforce.

## Features

- 🖼️ Upload images and get AI-generated captions
- 🚀 Fast and efficient inference
- 📝 RESTful API endpoints
- 🔍 Health check endpoint
- 📊 Automatic API documentation

## Installation

1. Make sure you have Python 3.8+ installed

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

### Start the server:

```bash
cd Image-captioning
python app.py
```

Or use uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Get API information and available endpoints

### 2. Health Check
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Check if the API is running and model is loaded

### 3. Generate Caption
- **URL**: `/caption`
- **Method**: `POST`
- **Description**: Upload an image and receive a generated caption
- **Parameters**:
  - `file`: Image file (required)
  - `max_length`: Maximum caption length (optional, default: 50)

## Usage Examples

### Using cURL:

```bash
# Generate caption for an image
curl -X POST "http://localhost:8000/caption" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"

# With custom max_length
curl -X POST "http://localhost:8000/caption?max_length=100" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"

# Health check
curl http://localhost:8000/health
```

### Using Python requests:

```python
import requests

# Generate caption
url = "http://localhost:8000/caption"
with open("image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    print(response.json())
```

### Using the interactive API documentation:

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Response Format

### Successful Response:
```json
{
  "success": true,
  "caption": "a picture of a room with a bed and a window",
  "filename": "room.jpeg"
}
```

### Error Response:
```json
{
  "detail": "Error processing image: [error message]"
}
```

## Original Script

The original image captioning script (`image_cap.py`) is still available for local testing and can be run independently.

## Model Information

This API uses the **BLIP (Bootstrapping Language-Image Pre-training)** model:
- Model: `Salesforce/blip-image-captioning-base`
- Task: Image-to-Text (Image Captioning)
- Framework: Transformers by Hugging Face

## Notes

- The model is loaded on startup, which may take a few seconds
- Supported image formats: JPEG, PNG, and other PIL-supported formats
- Images are automatically converted to RGB format
- Maximum caption length can be adjusted per request (default: 50 tokens)

