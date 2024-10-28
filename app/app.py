from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import re
from bs4 import BeautifulSoup
import json
import subprocess
import os
from pathlib import Path

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

@app.route('/scoreboards')
def scoreboards():
    scoreboards = Scoreboard.query.all()
    return render_template('all_scoreboards.html', scoreboards=scoreboards)

@app.route('/scoreboard/<int:scoreboard_id>')
def view_scoreboard(scoreboard_id):
    scoreboard = Scoreboard.query.get_or_404(scoreboard_id)
    return render_template('scoreboard.html', scoreboard=scoreboard.data, title=scoreboard.title)

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

@app.route('/rctf')
def rctf():
    flash("rCTF is not yet supported.")
    return redirect(url_for('index'))

@app.route('/create_gif_ctf', methods=['POST'])
def create_gif_ctf():
    if request.method == 'POST':
        ctf_url = request.form['ctf_url']
        title = get_title_from_url(ctf_url)

        if title is None:
            flash('Không thể lấy tiêu đề từ URL.')
            return redirect(url_for('create_gif_ctf'))

        # Xử lý tên thư mục để loại bỏ ký tự không hợp lệ
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title).strip()
        gifs_directory = Path("static/gifs") / safe_title

        # Đảm bảo thư mục theo tiêu đề tồn tại
        gifs_directory.mkdir(parents=True, exist_ok=True)

        # Tạo tên file GIF và đường dẫn lưu
        gif_filename = f"gif_{safe_title}_full.gif"
        gif_path = gifs_directory / gif_filename

        # Đường dẫn đầy đủ đến script tạo GIF
        script_path = os.path.join(os.path.dirname(__file__), 'create_gif.py')

        # Gọi script Python để chạy trong nền
        with open("error_log.txt", "w") as error_file:
            subprocess.Popen(
                ['python', script_path, ctf_url, request.form['total_duration'], str(gif_path), safe_title],
                stdout=subprocess.PIPE,
                stderr=error_file,
                shell=True
            )

        flash('GIF đang được tạo, vui lòng kiểm tra lại sau.')
        return redirect(url_for('gif_status', gif_filename=gif_filename, title=safe_title))

    return render_template('create_gif_ctf.html')

@app.route('/gif_status/<title>/<gif_filename>')
def gif_status(gif_filename, title):
    gifs_directory = Path("static/gifs")
    gif_path = gifs_directory / title / gif_filename

    if gif_path.exists():
        return render_template('gif_status.html', gif_path=url_for('static', filename=f'gifs/{title}/{gif_filename}'))
    else:
        return render_template('gif_status.html', message="GIF chưa sẵn sàng. Vui lòng thử lại sau.")

@app.route('/all_gifs')
def all_gifs():
    gifs_directory = Path("static/gifs")
    gifs = []

    # Duyệt qua tất cả thư mục con để tìm các file GIF
    for subdir in gifs_directory.iterdir():
        if subdir.is_dir():
            for gif_file in subdir.glob('*.gif'):
                gifs.append({
                    'path': str(gif_file.relative_to(gifs_directory)),  # Đường dẫn tương đối dưới dạng chuỗi
                    'name': gif_file.name,
                    'subdir': subdir.name  # Lưu tên thư mục con
                })

    return render_template('all_gifs.html', gifs=gifs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
