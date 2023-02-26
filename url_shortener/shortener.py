class NotFoundUrl(Exception):
    """Raised when an URL is not found"""
    pass

urls = {}

def shorten_url(url: str):
    short_url = hash(url) % 1000000
    urls[short_url] = url
    return {"short_url": f"http://localhost:8000/{short_url}"}

def redirect(short_url: int):
    if short_url not in urls:
        raise NotFoundUrl("Short URL not found")
    return {"redirect_url": urls[short_url]}

