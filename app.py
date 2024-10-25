from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import re
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Scoreboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(300), unique=True, nullable=False)
    data = db.Column(db.JSON, nullable=False)

def is_valid_url(url):
    """Xác thực URL xem có đúng định dạng không"""
    pattern = re.compile(
        r'^(https?:\/\/)?'  # http:// hoặc https://
        r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,})'  # domain
        r'(\/.*)?$', re.IGNORECASE
    )
    return re.match(pattern, url) is not None

def get_title_from_url(url):
    """Trích xuất tiêu đề từ URL"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'Untitled'
        return title.strip()
    return "Unknown Title"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ctfd', methods=['POST'])
def ctfd():
    url = request.form.get('ctfd_url')
    if not is_valid_url(url):
        flash("Invalid URL format. Please enter a valid URL.")
        return redirect(url_for('index'))

    full_url = url + '/api/v1/scoreboard'
    response = requests.get(full_url)
    if response.status_code == 200:
        data = response.json()
        title = get_title_from_url(url)
        
        # Kiểm tra xem URL đã tồn tại chưa
        existing_scoreboard = Scoreboard.query.filter_by(url=url).first()
        if existing_scoreboard:
            # Cập nhật dữ liệu mới nếu URL đã tồn tại
            existing_scoreboard.data = data
            existing_scoreboard.title = title
            db.session.commit()
            flash("Updated existing scoreboard with the latest data.")
            return redirect(url_for('view_scoreboard', scoreboard_id=existing_scoreboard.id))
        else:
            # Tạo bảng điểm mới nếu URL chưa tồn tại
            new_scoreboard = Scoreboard(title=title, url=url, data=data)
            db.session.add(new_scoreboard)
            db.session.commit()
            return redirect(url_for('view_scoreboard', scoreboard_id=new_scoreboard.id))
    else:
        flash("Failed to retrieve data from the provided URL.")
        return redirect(url_for('index'))

@app.route('/api/v1/scoreboard/upload', methods=['POST'])
def upload_scoreboard():
    uploaded_file = request.files.get('file')
    if not uploaded_file or not uploaded_file.filename.endswith('.json'):
        flash("Please upload a valid JSON file.")
        return redirect(url_for('index'))
    
    try:
        data = json.load(uploaded_file)
    except json.JSONDecodeError:
        flash("Invalid JSON format in uploaded file.")
        return redirect(url_for('index'))

    if "url" not in data or "data" not in data:
        flash("JSON file must contain 'url' and 'data' fields.")
        return redirect(url_for('index'))
    
    url = data['url']
    title = get_title_from_url(url)
    
    existing_scoreboard = Scoreboard.query.filter_by(url=url).first()
    if existing_scoreboard:
        # Cập nhật dữ liệu nếu URL đã tồn tại
        existing_scoreboard.data = data['data']
        existing_scoreboard.title = title
        db.session.commit()
        flash("Scoreboard updated successfully.")
    else:
        # Thêm mới nếu URL chưa tồn tại
        new_scoreboard = Scoreboard(title=title, url=url, data=data['data'])
        db.session.add(new_scoreboard)
        db.session.commit()
        flash("Scoreboard added successfully.")
    
    return redirect(url_for('scoreboards'))

@app.route('/scoreboards')
def scoreboards():
    scoreboards = Scoreboard.query.all()
    return render_template('all_scoreboards.html', scoreboards=scoreboards)

@app.route('/scoreboard/<int:scoreboard_id>')
def view_scoreboard(scoreboard_id):
    scoreboard = Scoreboard.query.get_or_404(scoreboard_id)
    return render_template('scoreboard.html', scoreboard=scoreboard.data, title=scoreboard.title)

@app.route('/rctf')
def rctf():
    return "Chưa hỗ trợ rCTF"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
