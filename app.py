from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import io
import uvicorn
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Image Captioning API",
    description="API for generating captions for images using BLIP model",
    version="1.0.0"
)

# Global variables to store model and processor
processor = None
model = None


@app.on_event("startup")
async def load_model():
    """Load the model and processor on startup"""
    global processor, model
    print("Loading BLIP model and processor...")
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    print("Model loaded successfully!")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Image Captioning API",
        "endpoints": {
            "/caption": "POST - Upload an image to get a caption",
            "/health": "GET - Check API health status"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None and processor is not None
    }


@app.post("/caption")
async def generate_caption(
    file: UploadFile = File(...),
    max_length: Optional[int] = 50
):
    """
    Generate a caption for an uploaded image
    
    Args:
        file: Image file (JPEG, PNG, etc.)
        max_length: Maximum length of the generated caption (default: 50)
    
    Returns:
        JSON response with the generated caption
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read and process the image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Process image and generate caption
        inputs = processor(images=image, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=max_length)
        
        # Decode the generated tokens to text
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        return JSONResponse(
            content={
                "success": True,
                "caption": caption,
                "filename": file.filename
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

