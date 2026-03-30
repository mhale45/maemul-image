from flask import Flask, render_template, request
from scraper import get_images
import re

app = Flask(__name__)

@app.route('/')
def home():
    item_id = request.args.get('id', '').strip()
    
    # 숫자만 남기기 (보안 및 불필요한 문자 제거)
    item_id = re.sub(r'\D', '', item_id)
    
    images = []
    if item_id:
        images = get_images(item_id)
        
    return render_template('index.html', item_id=item_id, images=images)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
