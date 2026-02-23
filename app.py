from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
import io
import uvicorn
from typing import Optional

## This is a test to check deployments to EC2

# Initialize FastAPI app
app = FastAPI(
    title="Image Captioning API",
    description="API for generating captions for images using BLIP model",
    version="1.0.0"
)

# Mount static files (for serving images, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

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


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint with frontend interface"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None and processor is not None
    }


@app.post("/caption", response_class=HTMLResponse)
async def generate_caption(
    request: Request,
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
        if file.content_type and not file.content_type.startswith("image/"):
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

        # Save the uploaded image to a static directory (optional)
        image_path = f"static/uploads/{file.filename}"
        image.save(image_path)  

        # Render the template with the image and caption
        return templates.TemplateResponse(
            "caption.html",
            {
                "request": request,
                "image_url": f"/{image_path}",
                "caption": caption,
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

