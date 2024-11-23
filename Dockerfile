# Sử dụng Python chính thức làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy toàn bộ source code và cấu hình vào container
COPY ./src /app/src
COPY requirements.txt /app/

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade llama-index

# Mở cổng cho Flask
EXPOSE 5000

# Thiết lập lệnh chạy ứng dụng
CMD ["python", "src/app.py"]
