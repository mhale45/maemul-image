from flask import Flask, render_template, request
from scraper import get_item_data
import re

app = Flask(__name__)

@app.route('/')
def home():
    item_id = request.args.get('id', '').strip()
    
    # 숫자만 남기기 (보안 및 불필요한 문자 제거)
    item_id = re.sub(r'\D', '', item_id)
    
    item_data = None
    if item_id:
        item_data = get_item_data(item_id)
        
    return render_template('index.html', item_id=item_id, item_data=item_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
