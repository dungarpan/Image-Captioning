"""
Test script for the Image Captioning API
Run this after starting the FastAPI server
"""
import requests
import sys
from pathlib import Path


def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_root():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get("http://localhost:8000/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200


def test_caption(image_path):
    """Test the caption endpoint with an image"""
    print(f"Testing caption endpoint with image: {image_path}")
    
    if not Path(image_path).exists():
        print(f"Error: Image file not found at {image_path}")
        return False
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post("http://localhost:8000/caption", files=files)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Caption: {result['caption']}")
        print(f"Filename: {result['filename']}\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False


def test_caption_with_max_length(image_path, max_length):
    """Test the caption endpoint with custom max_length"""
    print(f"Testing caption with max_length={max_length}...")
    
    if not Path(image_path).exists():
        print(f"Error: Image file not found at {image_path}")
        return False
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        params = {"max_length": max_length}
        response = requests.post(
            "http://localhost:8000/caption",
            files=files,
            params=params
        )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Caption: {result['caption']}\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Image Captioning API Test Suite")
    print("=" * 60 + "\n")
    
    # Test health and root endpoints
    health_ok = test_health()
    root_ok = test_root()
    
    if not health_ok:
        print("⚠️  Health check failed. Is the server running?")
        print("Start the server with: python app.py")
        return
    
    # Test caption endpoint if image path is provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        caption_ok = test_caption(image_path)
        
        if caption_ok:
            # Test with different max_length
            test_caption_with_max_length(image_path, 30)
            test_caption_with_max_length(image_path, 100)
    else:
        print("ℹ️  To test the caption endpoint, run:")
        print("   python test_api.py path/to/your/image.jpg")
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

