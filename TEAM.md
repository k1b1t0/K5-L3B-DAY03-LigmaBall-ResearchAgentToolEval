# Team

## Thông tin nhóm

- Tên nhóm: LigmaBall
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-LigmaBall-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: Nhánh `NguyenMinhDuc`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Minh Đức | 2A202603960 |  |  | Đánh giá eval group, thu thập live chat transcripts, báo cáo cá nhân |
|   2 | Đoàn Viết Huy |  | viethuydoan06@gmail.com | HuyDoan | Tối ưu prompt/tools, tool mới, giao diện UI (phụ trách nhánh riêng) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

## NguyenMinhDuc-2A202603960

### Phần việc phụ trách

- Thực thi đánh giá bộ 11 test cases của nhóm (`starter_v0/data/eval_group.json`) trên mô hình Gemini.
- Chạy tương tác Live Chat thực tế (`starter_v0/chat.py`), tạo và xác thực file transcript hội thoại với 3 kịch bản: tra cứu tin tức, hỏi lại URL thiếu (`clarify`) và xin xác nhận trước khi gửi (`send`).
- Tổng hợp bảng B3, B4 trong báo cáo nhóm và lập báo cáo cá nhân `report/team/2A202603960_NguyenMinhDuc.md`.

### Đóng góp cụ thể

- Sinh log kết quả `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json` (Case accuracy: 77.8%, Routing accuracy: 88.9%, Multiturn accuracy: 75.0%).
- Sinh log hội thoại `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json` chứng minh agent tuân thủ ranh giới an toàn.
- Hoàn thiện báo cáo cá nhân `report/team/2A202603960_NguyenMinhDuc.md` và đóng góp các mục B3, B4 vào `report/team/group_report.md`.

### Bằng chứng

- Run file: `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json`
- Transcript file: `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json`
- Test cases: `starter_v0/data/eval_group.json`

## DoanVietHuy

*(Phần việc và đóng góp của thành viên Đoàn Viết Huy sẽ được cập nhật từ nhánh làm việc của Huy)*
