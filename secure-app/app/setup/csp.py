local_host = 'https://127.0.0.1:9001'

csp = {
    'default-src': ["'self'", local_host],
    'img-src': ["'self'", local_host],
    'script-src': [
        "'self'", 
        local_host, 
        "https://www.google.com", 
        "https://www.gstatic.com"
    ],
    'style-src': [
        "'self'", 
        local_host, 
        'data'
    ],
    'frame-src': [
        local_host,
        'https://www.google.com', 
        'https://www.gstatic.com'
    ],
    'frame-ancestors': [
        "'self'", 
    ],
    'form-action': [
        "'self'", 
    ],
}
