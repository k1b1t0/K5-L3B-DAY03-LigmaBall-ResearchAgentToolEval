# Team

## Thông tin nhóm

- Tên nhóm: LigmaBall
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-LigmaBall-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: Nhánh `NguyenMinhDuc`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Minh Đức | 2A202603960 | | | Đánh giá eval group, thu thập live chat transcripts, báo cáo cá nhân |
|   2 | Đoàn Viết Huy | DoanVietHuy | viethuydoan06@gmail.com | HuyDoan | Tối ưu prompt/tools, tool mới, unit tests, giao diện UI |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```
- `report/team/2A202603960_NguyenMinhDuc.md`
- `report/team/DoanVietHuy.md`

## NguyenMinhDuc-2A202603960

### Phần việc phụ trách

- Thực thi đánh giá bộ 11 test cases của nhóm (`starter_v0/data/eval_group.json`) trên mô hình Gemini.
- Chạy tương tác Live Chat thực tế (`starter_v0/chat.py`), tạo và xác thực file transcript hội thoại với 3 kịch bản: tra cứu tin tức thời sự, hỏi lại URL thiếu (`clarify`) và xin xác nhận trước khi gửi (`send`).
- Tổng hợp bảng B3, B4 trong báo cáo nhóm và lập báo cáo cá nhân `report/team/2A202603960_NguyenMinhDuc.md`.

### Đóng góp cụ thể

- Sinh log kết quả `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json` (Case accuracy: 77.8%, Routing accuracy: 88.9%, Multiturn accuracy: 75.0%).
- Sinh log hội thoại `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json` chứng minh agent tuân thủ ranh giới an toàn.
- Hoàn thiện báo cáo cá nhân `report/team/2A202603960_NguyenMinhDuc.md` và đóng góp các mục B3, B4 vào `report/team/group_report.md`.

### Bằng chứng

- Run file: `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json`
- Transcript file: `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json`
- Test cases: `starter_v0/data/eval_group.json`
- Báo cáo: `report/team/2A202603960_NguyenMinhDuc.md`

## DoanVietHuy

### Phần việc phụ trách

- Tối ưu hóa vòng lặp `system_prompt.md` và `tools.yaml` qua các phiên bản từ v0 đến v3 dựa trên phân tích lỗi thực tế từ log run.
- Thiết kế, cài đặt và kiểm thử công cụ mới `dedupe_sources` (khử trùng lặp URL và query parameters).
- Xây dựng bộ Unit Tests cho tool mới trong `starter_v0/tests/test_tools_todo.py`.
- Phát triển giao diện người dùng tương tác Live Chat bằng Streamlit (`starter_v0/app.py`).

### Đóng góp cụ thể

- Xây dựng module `starter_v0/tools/dedupe_sources/tool.py` và `TOOL.md`, đăng ký trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml`.
- Viết 3 unit tests độc lập không gọi mạng, kiểm tra happy path, input xấu và URL lỗi, đảm bảo luôn trả dictionary lỗi và không làm crash agent.
- Đạt 84/84 tests passed khi chạy `pytest` toàn diện hệ thống.
- Xây dựng `starter_v0/app.py` với giao diện Streamlit hỗ trợ hội thoại trực tiếp và tự động ghi log transcript JSON.

### Bằng chứng

- Files cấu hình & mã nguồn: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/tools/dedupe_sources/`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/app.py`.
- Run files: `starter_v0/runs/v0_B_base_gemini_20261110T145411964411.json`, `starter_v0/runs/v1_B_base_gemini_20261110T150533950289.json`, `starter_v0/runs/v2_B_base_gemini_20261110T151133825813.json`, `starter_v0/runs/v3_B_base_gemini_20261110T152114003766.json`.
- Báo cáo: `report/team/DoanVietHuy.md`
