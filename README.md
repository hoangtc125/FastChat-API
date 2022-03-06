# FastChat application backend
**FastChat** phát triển một ứng dụng nhắn tin *nhanh* và *sạch sẽ*
## Tính năng
1. Người dùng có thể tham gia **FastChat** với 1 *nickname* bất kì
2. Chat nhanh với người dùng khác
3. Sau khi thoát ứng dụng sẽ không lưu lại thông tin gì về *nickname* hay các *conversations*
## Hướng dẫn cài đặt
**FastChat** được viết bằng ngôn ngữ *Python* và *FastAPI*
### Truy cập online tại:
![https://fastchatapi.deta.dev/](https://fastchatapi.deta.dev/)
### Các bước để chạy **FastChat** bằng CMD:
1. git init
2. git clone https://github.com/hoangtc125/FastChat.git
3. cd FastChat
4. pip install -r requirements.txt
5. uvicorn main:app --reload
## Các API
### Thao tác User
1. GET
    - Lấy danh sách các người dùng đang *online* trong hệ thống
    - *Front end* sẽ gọi liên tục để cập nhật danh sách liên lạc cho người dùng
2. POST
    - Tạo *nickname* cho người dùng mới, trả về thông tin của người dùng vừa tạo
    - *nickname* cần phải khác với danh sách *nickname* đang *online* trong hệ thống
    (*nickname* có thể được sử dụng nhiều lần, mỗi lần người dùng có thể chọn tùy ý)
3. PUT
    - Được *Front end* gửi định kỳ lên *server* để gia hạn sử dụng *nickname* cho người dùng
    - Nếu quá hạn, *server* sẽ tự động kiểm tra và xóa *nickname* và *conversations* tương ứng
    (Thời gian gia hạn mặc định đang là 60s kể từ thời điểm gửi *request*)
### Thao tác Conversation
1. GET
    - Lấy danh sách các *conversation* có tin nhắn mà người dùng chưa xem 
    - Dùng để thông báo cho người dùng về các *conversation* có tin nhắn mới
2. POST
    - Dùng để tạo một *conversation* mới giữa hai *nickname*
    - Hoặc dùng để load nội dung của một *conversation* mà người dùng có tham gia
3. PUT
    - Dùng để gửi một *message* (tin nhắn) mới vào một *conversation* của người dùng