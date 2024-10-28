import os
import sys
import requests
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import imageio
from pathlib import Path

# Đường dẫn API và các tham số
url = sys.argv[1] + '/api/v1/scoreboard'
total_duration = int(sys.argv[2])
output_path = sys.argv[3]
title = sys.argv[4]

num_parts = 20  # Cố định số lượng phần
fetch_interval = total_duration / 500  # Tần suất fetch cố định (1/500 thời lượng)
part_duration = total_duration / num_parts  # Thời gian mỗi phần
score_data_parts = [[] for _ in range(num_parts)]  # Mảng lưu dữ liệu từng phần

# print("Bắt đầu thu thập dữ liệu...")
start_time = time.time()
current_part = 0  # Theo dõi phần hiện tại
while time.time() - start_time < total_duration:
    success = False
    retries = 0
    max_retries = 3  # Số lần thử lại tối đa

    while not success and retries < max_retries:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                part_index = int((time.time() - start_time) / part_duration)

                # Đảm bảo part_index không vượt quá giới hạn của score_data_parts
                if part_index < num_parts:
                    score_data_parts[part_index].append(data)
                    # print(f'Fetched data at {time.time() - start_time:.1f}s for part {part_index + 1}')
                # else:
                    # print("Warning: Đã vượt quá số phần chia dự kiến.")
                
                success = True  # Dừng vòng lặp nếu thành công
            else:
                # print(f'Failed to fetch data: {response.status_code}')
                retries += 1
                time.sleep(2)  # Đợi 2 giây trước khi thử lại
        except requests.exceptions.RequestException as e:
            # print(f"Fetch failed with exception: {e}")
            retries += 1
            time.sleep(2)  # Đợi 2 giây trước khi thử lại
    
    # Kiểm tra nếu đạt số lần thử lại tối đa và không thành công
    # if not success:
        # print("Failed to fetch data after multiple retries. Moving to next interval.")
    
    # Đợi tiếp cho đến lần fetch tiếp theo
    time.sleep(fetch_interval)
    
    # Kiểm tra nếu kết thúc một phần
    if time.time() - start_time >= (current_part + 1) * part_duration:
        # Kiểm tra nếu phần hiện tại có dữ liệu
        if not score_data_parts[current_part]:  # Nếu không có dữ liệu trong phần này
            # print(f"Phần {current_part + 1} không có dữ liệu, bỏ qua tạo GIF.")
            current_part += 1
            continue

        # Tạo GIF cho phần hiện tại nếu có dữ liệu
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, max([max([team['score'] for team in data['data']]) for data in score_data_parts[current_part]]) + 1000)
        ax.set_xlabel('Scores')
        ax.set_ylabel('Teams')
        ax.set_title(f'Top 20 Teams Score Progression - Part {current_part + 1}')

        def get_top_20_teams(data):
            team_scores = {team['name']: team['score'] for team in data['data']}
            sorted_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)[:20]
            top_team_names = [team[0] if len(team[0]) <= 15 else team[0][:15] + "..." for team in sorted_teams]  # Cắt ngắn tên
            top_scores = [team[1] for team in sorted_teams]
            return top_team_names[::-1], top_scores[::-1]

        def update(frame):
            top_team_names, top_scores = get_top_20_teams(score_data_parts[current_part][frame])
            ax.clear()
            bars = ax.barh(top_team_names, top_scores, color='skyblue')
            ax.set_xlim(0, max(top_scores) + 1000)
            ax.set_xlabel('Scores')
            ax.set_ylabel('Teams')
            ax.set_title(f'Top 20 Teams at Frame {title}')
            ax.tick_params(axis='y', labelsize=8)  # Giảm kích thước phông chữ cho trục y
            return bars

        gif_filename = f'static/gifs/{title}/gif_part_{title}_{current_part + 1}.gif'
        ani = animation.FuncAnimation(fig, update, frames=len(score_data_parts[current_part]), blit=False)
        ani.save(gif_filename, writer='pillow', fps=2)
        plt.close(fig)
        # print(f"Đã tạo file GIF cho phần {current_part + 1}: {gif_filename}")
        
        # Chuyển sang phần tiếp theo
        current_part += 1

# print("Hoàn thành thu thập dữ liệu và tạo GIF cho từng phần.")

# Ghép các file GIF nhỏ lại thành một file GIF lớn
gif_files = [f'static/gifs/{title}/gif_part_{title}_{i + 1}.gif' for i in range(num_parts) if score_data_parts[i]]
with imageio.get_writer(f'static/gifs/{title}/gif_{title}_full.gif', mode='I', duration=0.5) as writer:
    for gif_file in gif_files:
        gif_frames = imageio.mimread(gif_file)
        for frame in gif_frames:
            writer.append_data(frame)

# print("Đã tạo file GIF lớn: f'gif_{sys.argv[1]}_full.gif'")
for gif_file in gif_files:
    if os.path.exists(gif_file) and gif_file != f'static/gifs/{title}/gif_{title}_full.gif':
        os.remove(gif_file)