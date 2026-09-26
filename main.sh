
# 1. Compile the website using Python
python3 src/main.py "$1"

# 2. Step inside our public folder and spawn a local background testing web server
cd public && python3 -m http.server 8888
