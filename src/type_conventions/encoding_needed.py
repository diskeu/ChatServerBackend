# indicates wheter or not the specific formats have to be encoded

mimetype_encoding_needed = {
    # Textformats
    "text/plain": True,
    "text/html": True,
    "text/css": True,
    "application/javascript": True,
    "application/json": True,
    "application/xml": True,
    
    # Binary formats
    "image/png": False,
    "image/jpeg": False,
    "image/gif": False,
    "image/webp": False,
    "image/svg+xml": True,
    "application/pdf": False,
    "application/zip": False,
    "application/gzip": False,
    "audio/mpeg": False,
    "audio/wav": False,
    "video/mp4": False,
    "video/webm": False,
}