# Báo cáo cá nhân — NguyenMinhDuc-2A202603960

## 1. Thông tin thành viên

- Họ tên: Nguyễn Minh Đức
- MSSV: 2A202603960
- Nhóm: LigmaBall (K5-L3A)

## 2. Phần việc phụ trách

- Thực thi đánh giá bộ 11 test cases của nhóm (`starter_v0/data/eval_group.json`) trên mô hình Gemini.
- Chạy tương tác Live Chat thực tế (`starter_v0/chat.py`), tạo và xác thực file transcript hội thoại với 3 kịch bản: tra cứu tin tức thời sự, hỏi lại URL thiếu (`clarify`) và xin xác nhận trước khi gửi (`send`).
- Tổng hợp bảng B3, B4 và hoàn thiện báo cáo nhóm `report/team/group_report.md` cũng như đồng bộ cấu trúc mới của bài lab.

## 3. Đóng góp cụ thể

- Đóng góp file run đánh giá nhóm: `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json` (Case accuracy: 77.8%, Routing accuracy: 88.9%, Multiturn accuracy: 75.0%).
- Đóng góp file log hội thoại trực tiếp: `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json`.
- Ghi nhận đầy đủ thông tin thực nghiệm vào `starter_v0/artifacts/version_log.csv` và `report/team/group_report.md`.

## 4. Bằng chứng

- File run eval group: `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json`
- File transcript: `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json`
- AI/công cụ đã dùng: Trợ lý AI hỗ trợ rà soát schema, phân tích failure types và tự kiểm tra bằng `pytest tests/test_tool_contract.py` (84 tests passed).

## 5. Tự đánh giá

- Đóng góp: 100% hoàn thành các nhiệm vụ phụ trách theo phân công của nhóm.
- Mức độ hài lòng: Agent xử lý tốt các tình huống thiếu thông tin và tuân thủ ranh giới Human-in-the-Loop trước khi kích hoạt Action Tool.

