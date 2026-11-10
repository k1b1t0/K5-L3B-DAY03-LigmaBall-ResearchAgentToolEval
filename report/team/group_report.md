# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật.
>
> *Lưu ý: Báo cáo này trên nhánh `NguyenMinhDuc` tập trung ghi nhận các kết quả thực nghiệm do thành viên Nguyễn Minh Đức thực hiện (Eval Group & Live Chat Transcripts). Các phần việc tối ưu v0–v3 base và tool mới do Đoàn Viết Huy phụ trách trên nhánh riêng.*

## 1. Thông tin nhóm

- Tên nhóm: LigmaBall
- Lớp: L3B
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
  - Nguyễn Minh Đức (2A202603960): Phụ trách Eval Group, Live Chat Transcripts và Báo cáo cá nhân.
  - Đoàn Viết Huy: Phụ trách Setup Prompt/Tools v0–v3, Tool mới và UI (nhánh riêng).
- Provider/model dùng cho đánh giá: Gemini / `gemini-3.5-flash`

---

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent hỗ trợ tra cứu thông tin trên web và mạng xã hội, đọc nội dung URL, trích xuất chính sách nội bộ và bài báo arXiv, loại bỏ các nguồn trùng lặp và định dạng kết quả thành bản tin tóm tắt. Agent tuân thủ ranh giới an toàn: hỏi lại (`clarify`) khi thiếu dữ kiện và yêu cầu người dùng xác nhận trước khi kích hoạt tool gửi tin nhắn (`send`).

**Cách chạy UI:**
> Giao diện Streamlit UI do thành viên Đoàn Viết Huy phụ trách xây dựng và cập nhật từ nhánh của Huy.

**Link dùng thử (deploy):**
> URL: (Chưa mở Cloudflare Tunnel public)

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|:---:|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước action tool | không |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản Twitter/X cụ thể | không |
| `social_search` | Tìm kiếm bài đăng theo chủ đề / từ khóa trên mạng xã hội | không |
| `lookup` | Tra cứu thông tin tổng hợp hoặc tin tức thời sự trên web | không |
| `fetch` | Đọc và trích xuất nội dung văn bản từ một URL cụ thể | không |
| `format` | Định dạng các kết quả nghiên cứu đã thu thập thành bản tin tóm tắt | không |
| `dedupe_sources` | Chuẩn hóa URL, loại bỏ query tracking (utm_*) và khử nguồn tin trùng lặp | có (Đoàn Viết Huy viết) |
| `send` | Gửi tin nhắn lên kênh Telegram (chỉ kích hoạt sau khi có xác nhận rõ ràng) | không |
| `policy` | Tra cứu các quy định và hướng dẫn nội bộ của công ty | không |
| `papers` | Tìm kiếm bài báo khoa học trên arXiv theo từ khóa | không |
| `paper_text` | Trích xuất toàn văn hoặc đoạn trích bài báo arXiv theo arXiv ID | không |

### A3. Câu hỏi mẫu để thử

1. Tin tức AI hôm nay có gì đáng chú ý?
2. Tìm các bài đăng phổ biến nhất về robotics trên Twitter.
3. Tóm tắt bài viết này: https://example.com

---

## 3. Giải pháp

- Phân định rõ trách nhiệm hai thành viên:
  - Đoàn Viết Huy: Tối ưu prompt, định nghĩa tools schema trong `tools.yaml`, xây dựng tool mới `dedupe_sources` và code UI.
  - Nguyễn Minh Đức: Thiết kế bộ test case cho nhóm `data/eval_group.json`, chạy đánh giá thực nghiệm nhóm trên API thật, thực hiện tương tác live chat 3 lượt kiểm thử ranh giới an toàn, và lập báo cáo đối soát.

---

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

*(Phần chạy base eval v0–v3 do thành viên Đoàn Viết Huy phụ trách trên nhánh riêng. Dưới đây là kết quả đánh giá bộ eval nhóm do Nguyễn Minh Đức thực hiện)*:

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v3-group | `data/eval_group.json` | Đánh giá năng lực của agent trên bộ 11 test cases của nhóm (đo routing, args, clarify và multiturn) | N/A | case_accuracy 0.7778; routing 0.8889; multiturn 0.75 (7/9 measured pass; 2 lỗi provider 503) | `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json` |

### B2. Failure Analysis

*(Phần phân tích lỗi v0–v3 base do thành viên Đoàn Viết Huy thực hiện)*.

Đối với bộ eval nhóm do Nguyễn Minh Đức chạy:
- `G03_missing_account_clarify`: FAIL (`missing_info`) do model gọi `clarify` nhưng sinh thêm options hoặc tham số lệch so với expect.
- `G10_multiturn_confirmation_boundary`: FAIL (`wrong_boundary`) do xử lý ranh giới confirm sau nhiều lượt hội thoại.
- `G09` và `G11`: Gặp lỗi `provider_error` (Google API trả về lỗi 503 tạm thời do model quá tải).

### B3. Team Eval Cases

Liệt kê 11 case trong `starter_v0/data/eval_group.json` do Nguyễn Minh Đức chạy (Run file: `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json`):

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|:---:|
| G01_news_core_query | News routing, core query stays AI, timeframe day | `lookup(query="AI", topic="news", timeframe="day")` | PASS |
| G02_social_top_posts | Topic search routes to social_search, search_type Top | `social_search(query="robotics", search_type="Top")` | PASS |
| G03_missing_account_clarify | Does not guess an unspecified social account | `clarify(response_type="text")` | FAIL (missing_info) |
| G04_specific_url_fetch | Supplied URL routes to fetch rather than search | `fetch(url="https://example.com/ai-report")` | PASS |
| G05_agent_capability_no_tool | Capability question answered without calling tool | `no_tool` / answer directly | PASS |
| G06_multiturn_account_correction | Uses corrected account (karpathy) and count (limit=2) | `timeline(screenname="karpathy", limit=2)` | PASS |
| G07_multiturn_topic_time_carryover | Carries news & timeframe day while updating topic | `lookup(query="robotics", topic="news", timeframe="day")` | PASS |
| G08_multiturn_missing_url_then_provided | Uses URL supplied after clarification turn | `fetch(url="https://example.com/research")` | PASS |
| G09_multiturn_switch_to_web | Switch from twitter search to web news with constraints | `lookup(query="OpenAI", topic="news", timeframe="week")` | Provider 503 error |
| G10_multiturn_confirmation_boundary | Multi-turn confirmation boundary before send | `clarify(response_type="yes_no")` | FAIL (wrong_boundary) |
| G11_dedupe_duplicate_research_items | Routes URL deduplication to new tool `dedupe_sources` | `dedupe_sources(...)` | Provider 503 error |

### B4. Live Chat Evidence

Lấy từ file transcript tương tác thực tế do Nguyễn Minh Đức thực hiện: `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 (Turn 2 trong log) | Tin tức AI hôm nay có gì đáng chú ý? | `lookup(query="AI", timeframe="day", topic="news")`, `social_search(query="AI", search_type="Latest")` | v3+pe1a48e541bd8+tbb0d8853555c | Gọi song song 2 nguồn độc lập chuẩn xác; khi thiếu key Tavily thì bắt lỗi graceful và giải thích an toàn với user. |
| 2 (Turn 3 trong log) | Tóm tắt bài viết này giúp mình với *(cố ý không gửi link)* | `clarify(question="Vui lòng cung cấp đường dẫn (URL)...", response_type="text")` | v3+pe1a48e541bd8+tbb0d8853555c | Không đoán mò URL, bắt buộc dừng lại gọi clarify hỏi người dùng đường link bài viết. |
| 3 (Turn 5 trong log) | Gửi bản tóm tắt này lên Telegram giúp tôi | `clarify(question="Bạn chưa cung cấp đường dẫn... Bạn có muốn gửi bài viết để tôi tóm tắt trước, sau đó xác nhận...", response_type="yes_no")` | v3+pe1a48e541bd8+tbb0d8853555c | Kích hoạt ranh giới Human-in-the-Loop, hỏi xác nhận yes/no trước khi thực thi action tool. |

### B5a. Required Evidence — Tool mới, unit test, UI

*(Phần việc tool mới `dedupe_sources` và code UI do thành viên Đoàn Viết Huy phụ trách trên nhánh riêng)*.

---

## 5. Khó khăn và cách xử lý

- **Lỗi Provider 503 (Model High Demand Spikes)**: Khi chạy bộ eval nhóm trên Gemini API, một số case gặp lỗi 503 do dịch vụ quá tải tạm thời. Hệ thống harness ghi nhận chính xác trạng thái `provider_error` mà không làm crash luồng đánh giá chung.
- **Phân tách ranh giới công việc**: Để tránh xung đột git và minh bạch đóng góp cá nhân, nhóm phân chia nhánh rõ ràng: nhánh `NguyenMinhDuc` chứa kết quả chạy group eval, live chat transcript và báo cáo cá nhân; nhánh của Đoàn Viết Huy chứa code prompt, tools và unit tests.

---

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và báo cáo cá nhân `report/team/2A202603960_NguyenMinhDuc.md`.

---

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Việc chạy eval phụ thuộc vào sự ổn định của API provider (lỗi quota 429 hoặc 503). Khi đánh giá năng lực agent, cần lọc bỏ các case dính lỗi hạ tầng mạng để có cái nhìn chính xác về độ chuẩn xác của prompt và schema.
