#!/bin/bash

echo "🔍 Searching for 'proxy_pass http://127.0.0.1:2368' in /etc/nginx..."
matches=$(grep -rl "proxy_pass http://127.0.0.1:2368" /etc/nginx 2>/dev/null)

if [ -z "$matches" ]; then
    echo "✅ No references to port 2368 found in NGINX config."
    exit 0
fi

echo "⚠️ Found the following file(s) pointing to port 2368:"
echo "$matches"

for file in $matches; do
    echo "🔧 Patching $file..."
    sudo sed -i 's|http://127.0.0.1:2368|http://127.0.0.1:8000|g' "$file"
done

echo "🔁 Testing NGINX configuration..."
sudo nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Config is valid. Reloading NGINX..."
    sudo systemctl reload nginx
    echo "🚀 NGINX reloaded. Backend now points to port 8000."
else
    echo "❌ NGINX config has issues. Restore changes and fix manually."
fi
