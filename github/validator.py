from urllib.parse import urlparse

def validate_github_url(url: str) -> bool:
    """
    validate whether the given url is a valid github repository url.
    """
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in ("http","https"):
            return False
        if parsed.netloc != "github.com":
            return False
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) <2:
            return False
        return True
    except Exception:
        return False