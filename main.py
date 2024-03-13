from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from bin.filters import apply_filter
import io

app = FastAPI()

# Directory for templates
templates = Jinja2Templates(directory="templates")

# Serving static files (for Bootstrap CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

filters_available = [
    "blur", "contour", "detail", "edge_enhance", "edge_enhance_more",
    "emboss", "find_edges", "sharpen", "smooth", "smooth_more",
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the HTML form for uploading an image and selecting a filter.
    """
    return templates.TemplateResponse("index.html", {"request": request, "filters": filters_available})
@app.post("/apply-filter", response_class=StreamingResponse)
async def apply_image_filter(request: Request, filter: str = Form(...), img: UploadFile = File(...)):
    """
    Apply the selected filter to the uploaded image and return the result.
    """
    if filter not in filters_available:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Incorrect filter selected"})

    # Apply the filter and get the result as a BytesIO object
    filtered_image_io = apply_filter(img.file, filter)

    # Assuming filtered_image_io is a BytesIO object containing the image data.
    # No need to call .save() on it; just reset the pointer to the beginning of the BytesIO stream.
    filtered_image_io.seek(0)

    # Return the filtered image directly
    return StreamingResponse(filtered_image_io, media_type="image/jpeg")
