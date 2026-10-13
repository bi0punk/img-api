import io
from typing import IO

from PIL import Image, ImageFilter

# Mapeo explícito de filtros permitidos -> filtro PIL.
# Evita el uso de eval() con entrada del usuario.
FILTERS = {
    "blur": ImageFilter.BLUR,
    "contour": ImageFilter.CONTOUR,
    "detail": ImageFilter.DETAIL,
    "edge_enhance": ImageFilter.EDGE_ENHANCE,
    "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
    "emboss": ImageFilter.EMBOSS,
    "find_edges": ImageFilter.FIND_EDGES,
    "sharpen": ImageFilter.SHARPEN,
    "smooth": ImageFilter.SMOOTH,
    "smooth_more": ImageFilter.SMOOTH_MORE,
}


def get_filter(name: str):
    """Devuelve el filtro PIL correspondiente o lanza ValueError si no existe."""
    try:
        return FILTERS[name.lower()]
    except KeyError as exc:
        raise ValueError(f"Filtro no permitido: {name}") from exc


def apply_filter(file: IO[bytes], filter: str) -> IO[bytes]:
    """
    1. Accept the image as file object, and the filter type as string
    2. Open the as an PIL Image object
    3. Apply the filter
    4. Convert the PIL Image object to file object
    5. Return the file object
    """
    image: Image.Image = Image.open(file)
    image = image.filter(get_filter(filter))

    out = io.BytesIO()
    image.save(out, "JPEG")
    out.seek(0)

    return out
