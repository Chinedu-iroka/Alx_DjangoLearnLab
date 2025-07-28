In a production environment, I would configure my web server (like Nginx) to use HTTPS with Let’s Encrypt. Here is an example configuration:

server {
listen 80;
server_name yourdomain.com www.yourdomain.com;
# Redirect all HTTP to HTTPS
return 301 https://$host$request_uri;
}

server {
listen 443 ssl;
server_name yourdomain.com www.yourdomain.com;

ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

include ssl-params.conf;

location / {
    proxy_pass http://127.0.0.1:8000;
    include proxy_params;
}
}

yaml
Copy code

---

### ✅ 3. If you want to include it inside `settings.py` as a comment:

At the bottom of your `settings.py`, just add this as a block comment:

```python
# Deployment Configuration (for assignment)

"""
In production, I would configure Nginx with HTTPS using Let's Encrypt.

Example:

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    include ssl-params.conf;

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
    }
}
"""