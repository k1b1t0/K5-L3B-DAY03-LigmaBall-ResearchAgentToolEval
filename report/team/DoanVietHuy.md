# Báo cáo cá nhân — Đoàn Viết Huy

## 1. Thông tin thành viên

- Họ tên: Đoàn Viết Huy
- MSSV: DoanVietHuy
- Email: viethuydoan06@gmail.com
- GitHub: HuyDoan
- Nhóm: LigmaBall (Lớp L3B)

## 2. Phần việc phụ trách

- Tối ưu hóa vòng lặp `system_prompt.md` và `tools.yaml` qua các phiên bản từ v0 đến v3 dựa trên phân tích lỗi thực tế từ log run.
- Thiết kế, cài đặt và kiểm thử công cụ mới `dedupe_sources` (khử trùng lặp URL và query parameters).
- Xây dựng bộ Unit Tests cho tool mới trong `starter_v0/tests/test_tools_todo.py`.
- Phát triển giao diện người dùng tương tác Live Chat bằng Streamlit (`starter_v0/app.py`).

## 3. Đóng góp cụ thể

- **Prompt & Tool Engineering**:
  - Loại bỏ các chỉ dẫn gây nhiễu và thiên kiến sai trong starter prompt.
  - Xây dựng bộ quy tắc ranh giới: bắt buộc hỏi lại (`clarify`) khi thiếu URL hoặc tên tài khoản; trả lời trực tiếp không gọi tool cho câu hỏi meta; yêu cầu xác nhận trước khi thực hiện hành động gửi tin (`send`).
  - Chuẩn hóa quy ước tham số: query chỉ chứa từ khóa cốt lõi (ví dụ "AI" thay vì "tin tức AI mới nhất").
- **Phát triển Tool mới `dedupe_sources`**:
  - Viết module `starter_v0/tools/dedupe_sources/tool.py` và tài liệu đặc tả `TOOL.md`.
  - Đăng ký tool vào hệ thống (`starter_v0/tools/__init__.py`) và khai báo JSON schema vào `starter_v0/artifacts/tools.yaml`.
  - Viết 3 unit tests bao phủ happy path, kiểm tra input xấu và URL lỗi, đảm bảo luôn trả dictionary lỗi và không raise exception.
- **Xây dựng UI Streamlit**:
  - Xây dựng `starter_v0/app.py` hỗ trợ hội thoại trực tiếp với LLM, hiển thị chi tiết các tool calls theo thời gian thực và tự động lưu transcript JSON chuẩn quy cách.

## 4. Bằng chứng

- **Files cấu hình & mã nguồn**:
  - `starter_v0/artifacts/system_prompt.md`
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/tools/dedupe_sources/tool.py` & `TOOL.md`
  - `starter_v0/tests/test_tools_todo.py`
  - `starter_v0/app.py`
- **Các run đánh giá v0–v3**:
  - `starter_v0/runs/v0_B_base_gemini_20261110T145411964411.json`
  - `starter_v0/runs/v1_B_base_gemini_20261110T150533950289.json`
  - `starter_v0/runs/v2_B_base_gemini_20261110T151133825813.json`
  - `starter_v0/runs/v3_B_base_gemini_20261110T152114003766.json`
- **Kiểm thử tự động**:
  - Chạy `pytest` đạt **84 passed, 0 failed, 0 skipped** (vượt qua toàn bộ contract tests và unit tests).
- **AI/công cụ đã dùng**: Trợ lý AI hỗ trợ rà soát schema JSON, sinh test case unit test và kiểm tra quy chuẩn contract.

## 5. Tự đánh giá

- Đóng góp: 100% hoàn thành các nhiệm vụ phụ trách theo phân công của nhóm.
- Mức độ hài lòng: Toàn bộ suite test xanh hoàn toàn, tool mới hoạt động ổn định và giao diện chat trực quan, hỗ trợ tốt cho việc nghiệm thu bài lab.

