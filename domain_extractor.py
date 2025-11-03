import re

def extract_domain(url):
    # Regular expression pattern to match domain name
    pattern = r'^(?:https?:\/\/)?(?:www\.)?([^\/:]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

# # Example usage
# urls = [
#     "https://www.example.com/path/page",
#     "http://sub.domain.co.uk/test",
#     "www.google.com/search?q=test",
#     "https://340bpriceguide.net",
#     "ftp://example.org/resource"
# ]

# for u in urls:
#     print(f"URL: {u}  →  Domain: {extract_domain(u)}")
