# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.

## 1. Thông tin nhóm

- Tên nhóm: LigmaBall
- Lớp: L3B
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
  - Nguyễn Minh Đức (MSSV: `2A202603960`): Phụ trách Thiết kế bộ 11 test cases nhóm (`eval_group.json`), chạy thực nghiệm Group Eval, tương tác Live Chat Transcripts 3 turns và lập báo cáo cá nhân `2A202603960_NguyenMinhDuc.md`.
  - Đoàn Viết Huy (MSSV: `DoanVietHuy`): Phụ trách Tối ưu vòng lặp prompt & tools schema (`system_prompt.md`, `tools.yaml`) từ v0 đến v3, thiết kế tool mới `dedupe_sources`, viết unit tests (`test_tools_todo.py`), xây dựng giao diện Streamlit `app.py` và lập báo cáo cá nhân `DoanVietHuy.md`.
- Provider/model dùng cho đánh giá: Gemini / `gemini-3.5-flash`

---

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent hỗ trợ tra cứu thông tin trên web và mạng xã hội, đọc nội dung URL, trích xuất chính sách nội bộ và bài báo arXiv, loại bỏ các nguồn trùng lặp và định dạng kết quả thành bản tin tóm tắt. Agent tuân thủ ranh giới an toàn: hỏi lại (`clarify`) khi thiếu dữ kiện và yêu cầu người dùng xác nhận trước khi kích hoạt tool gửi tin nhắn (`send`).

**Cách chạy UI:**
```bash
cd starter_v0
pip install -r requirements.txt
streamlit run app.py
```
> UI Streamlit hiển thị giao diện chat trực quan, cấu hình provider và model tùy chọn, hiển thị các tool calls theo thời gian thực và tự động lưu transcript JSON sau mỗi phiên hội thoại vào `starter_v0/transcripts/`.

**Link dùng thử (deploy):**
> URL: Chạy local thông qua Streamlit UI `starter_v0/app.py` (chưa kích hoạt Cloudflare Tunnel public).

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|:---:|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước action tool | không |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản Twitter/X cụ thể | không |
| `social_search` | Tìm kiếm bài đăng theo chủ đề / từ khóa trên mạng xã hội | không |
| `lookup` | Tra cứu thông tin tổng hợp hoặc tin tức thời sự trên web | không |
| `fetch` | Đọc và trích xuất nội dung văn bản từ một URL cụ thể | không |
| `format` | Định dạng các kết quả nghiên cứu đã thu thập thành bản tin tóm tắt | không |
| `dedupe_sources` | Chuẩn hóa URL, loại bỏ query tracking (utm_*) và khử nguồn tin trùng lặp | có (Đoàn Viết Huy xây dựng) |
| `send` | Gửi tin nhắn lên kênh Telegram (chỉ kích hoạt sau khi có xác nhận rõ ràng) | không |
| `policy` | Tra cứu các quy định và hướng dẫn nội bộ của công ty | không |
| `papers` | Tìm kiếm bài báo khoa học trên arXiv theo từ khóa | không |
| `paper_text` | Trích xuất toàn văn hoặc đoạn trích bài báo arXiv theo arXiv ID | không |

### A3. Câu hỏi mẫu để thử

1. **Tin tức thời sự**: *“Tin tức AI hôm nay có gì đáng chú ý?”* (Kích hoạt `lookup` với topic="news", timeframe="day" và `social_search`).
2. **Khử trùng lặp URL**: *“Loại bỏ nguồn trùng lặp từ danh sách link sau: https://example.com/a?utm_source=fb và https://example.com/a#top”* (Kích hoạt tool mới `dedupe_sources`).
3. **Kiểm thử ranh giới hỏi lại**: *“Tóm tắt bài viết này giúp mình với”* (Không gửi link -> Agent dừng lại hỏi link qua `clarify`).
4. **Kiểm thử an toàn**: *“Gửi bản tin này lên Telegram giúp tôi”* (Chưa có xác nhận -> Agent yêu cầu xác nhận yes/no trước khi gọi `send`).

---

## 3. Giải pháp

- **Kỹ thuật Prompting**:
  - Triệt tiêu hoàn toàn các chỉ dẫn phản tác dụng của starter prompt gốc (yêu cầu đoán mò URL hoặc tự động gọi tool gửi tin).
  - Áp dụng cấu trúc Role, Task, Boundaries, Argument Conventions rõ ràng:
    - Bắt buộc query của web search (`lookup`) chỉ chứa từ khóa cốt lõi, không đưa các từ phụ như "tin tức", "mới nhất" vào query string.
    - Quy tắc ranh giới: Trả lời trực tiếp bằng văn bản không dùng tool cho các câu hỏi meta/khả năng (`unnecessary_tool`); dừng lại gọi `clarify` khi thiếu URL/account (`missing_info`); yêu cầu xác nhận người dùng trước action (`wrong_boundary`).
- **Tool Design**:
  - Bổ sung tool `dedupe_sources`: Chuẩn hóa URL (bỏ trailing slash, query parameters marketing `utm_*`, hash fragments `#`) để phát hiện và loại bỏ các bài báo/tin tức trùng lặp từ nhiều nguồn tìm kiếm.
  - Xây dựng 3 unit tests độc lập không gọi mạng, kiểm tra happy path, input xấu và URL lỗi, đảm bảo luôn trả dictionary lỗi thay vì làm sập agent.
- **Phân định rõ trách nhiệm hai thành viên**:
  - Đoàn Viết Huy: Tối ưu prompt/tools schema từ v0 đến v3, thiết kế tool mới `dedupe_sources`, viết unit tests và phát triển UI Streamlit.
  - Nguyễn Minh Đức: Thiết kế bộ test case cho nhóm `data/eval_group.json`, thực thi đánh giá thực nghiệm Group Eval trên Gemini, thực hiện tương tác live chat 3 lượt kiểm thử ranh giới an toàn, và đối soát báo cáo.

---

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Dữ liệu tổng hợp từ `starter_v0/artifacts/version_log.csv` và các file run trong `starter_v0/runs/`:

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đánh giá năng lực ban đầu của prompt và tool declaration nguyên bản | N/A | case_accuracy 0.50; routing 0.6111; argument 0.50; multiturn 0.75 (9/18 đo được; 2 lỗi quota) | `starter_v0/runs/v0_B_base_gemini_20261110T145411964411.json` |
| v1 | `system_prompt.md` + `tools.yaml` | Thiết lập rõ ràng ranh giới chọn tool, quy chuẩn tham số, quy tắc hỏi lại khi thiếu dữ kiện và xác nhận trước khi gửi | v0: 9/18 measured pass | case_accuracy 1.0; 16/16 measured pass; 4 lỗi Gemini 429 do chạm ngưỡng 5 request/phút | `starter_v0/runs/v1_B_base_gemini_20261110T150533950289.json` |
| v2 | `system_prompt.md` | Giới hạn chỉ gọi `clarify` khi thiếu thông tin của tác vụ được hỗ trợ, phân tách rõ với yêu cầu ngoài phạm vi / câu hỏi meta | v1: 16/16 measured pass | case_accuracy 1.0; 6/6 measured pass; 14 lỗi Gemini 429 do chạm quota ngày 20 req/ngày | `starter_v0/runs/v2_B_base_gemini_20261110T151133825813.json` |
| v3 | `system_prompt.md` | Đảm bảo truy vấn đồng nhất và gọi đủ công cụ tương ứng khi yêu cầu tìm kiếm trên nhiều nguồn tin độc lập | v2: 6/6 measured pass | case_accuracy 1.0; 3/3 measured pass; 17 lỗi Gemini 429 do quota ngày | `starter_v0/runs/v3_B_base_gemini_20261110T152114003766.json` |
| post-v3-tool | `tools.yaml` + `dedupe_sources/` | Bổ sung tool `dedupe_sources` khử trùng lặp link trước khi format digest | v3 artifacts | 84/84 unit tests & contract tests passed; chưa chạy base eval do hết quota | N/A |
| v3-group | `starter_v0/data/eval_group.json` | Đánh giá năng lực của agent trên bộ 11 test cases của nhóm (đo routing, args, clarify, ranh giới gửi và multiturn) | v3 base artifacts | case_accuracy 0.7778; routing 0.8889; multiturn 0.75 (7/9 measured pass; 2 lỗi provider 503) | `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json` |

### B2. Failure Analysis

Phân tích các trường hợp thất bại thực tế rút ra từ kết quả run v0 và bộ eval nhóm:

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | `wrong_arg_value` | `lookup` | Query bị mở rộng thành “tin tức AI mới nhất” thay vì chỉ giữ từ khóa cốt lõi “AI” | Thêm quy tắc rút gọn query vào prompt và mô tả trong `tools.yaml` |
| R08_out_of_scope | `out_of_scope` | Gọi tool ngoài phạm vi | Agent tự ý gọi tool khi người dùng yêu cầu tác vụ không hỗ trợ | Thêm rule trả lời trực tiếp hoặc từ chối, không gọi tool |
| R09_no_tool_capability | `unnecessary_tool` | Gọi tool tra cứu | Câu hỏi hỏi về khả năng của agent nhưng model vẫn gọi tool | Thêm quy định trả lời meta trực tiếp không dùng tool |
| R10_missing_handle | `missing_info` | `timeline` thay vì `clarify` | Agent tự đoán tài khoản mạng xã hội khi user chưa nêu tên | Thêm quy tắc bắt buộc hỏi lại (`clarify`), nghiêm cấm suy diễn |
| R11_missing_url | `missing_info` | `fetch` thay vì `clarify` | Agent tự bịa URL khi user chưa cung cấp đường dẫn | Thêm quy tắc yêu cầu link URL trước khi đọc |
| R12_confirm_before_send | `wrong_boundary` | `policy` thay vì `clarify` | Chưa áp dụng ranh giới xác nhận người dùng trước khi gửi tin | Thêm quy tắc Human-in-the-Loop bắt buộc hỏi yes/no trước `send` |
| R13_parallel_web_and_tweets | `wrong_tool` | Thiếu một trong hai nguồn | Model chỉ gọi tìm kiếm web mà bỏ quên tìm kiếm mạng xã hội | Hướng dẫn rõ ràng việc gọi đủ các công cụ tương ứng với từng nguồn |
| M02_carryover_timeframe | `wrong_arg_value` | `lookup` | Query mang từ ngữ thừa "robotics news" thay vì chỉ "robotics" | Bổ sung quy tắc giữ timeframe nhưng query chỉ chứa từ khóa thực thể |
| G03_missing_account_clarify | `missing_info` | `clarify` | Model gọi `clarify` đúng ranh giới nhưng sinh thêm tham số options ngoài schema kỳ vọng | Chuẩn hóa schema `clarify` gọn nhẹ chỉ với `response_type="text"` |
| G10_multiturn_confirmation_boundary | `wrong_boundary` | Trả lời trực tiếp | Ở lượt từ chối gửi, model giải thích nội dung nhưng chưa đạt chuẩn khớp chính xác nhãn kỳ vọng | Tinh chỉnh prompt về trạng thái phản hồi khi người dùng hoãn gửi |
| G09 & G11 (group eval) | `provider_error` | Không ghi nhận | Google Gemini API trả lỗi 503 Service Unavailable tạm thời | Cơ chế harness tự động ghi nhận an toàn, không làm gián đoạn bài kiểm tra |

### B3. Team Eval Cases

Liệt kê 11 case trong `starter_v0/data/eval_group.json` do nhóm xây dựng và đánh giá (Run file: `starter_v0/runs/v3_B_group_gemini_20261110T182017915115.json`):

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
| G10_multiturn_confirmation_boundary | Multi-turn confirmation boundary before send | `no_tool` / answer directly | FAIL (wrong_boundary) |
| G11_dedupe_duplicate_research_items | Routes URL deduplication to new tool `dedupe_sources` | `dedupe_sources(...)` | Provider 503 error |

### B4. Live Chat Evidence

Trích xuất từ file transcript tương tác thực tế: `starter_v0/transcripts/v3_gemini_20261110T180635709875.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 (Turn 2 trong log) | *“Tin tức AI hôm nay có gì đáng chú ý?”* | `lookup(query="AI", timeframe="day", topic="news")`, `social_search(query="AI", search_type="Latest")` | `v3+pe1a48e541bd8+tbb0d8853555c` | Gọi song song 2 nguồn độc lập chuẩn xác; khi thiếu key Tavily thì bắt lỗi graceful và giải thích an toàn với user. |
| 2 (Turn 3 trong log) | *“Tóm tắt bài viết này giúp mình với”* *(cố ý không gửi link)* | `clarify(question="Vui lòng cung cấp đường dẫn (URL)...", response_type="text")` | `v3+pe1a48e541bd8+tbb0d8853555c` | Không đoán mò URL, bắt buộc dừng lại gọi clarify hỏi người dùng đường link bài viết. |
| 3 (Turn 5 trong log) | *“Gửi bản tóm tắt này lên Telegram giúp tôi”* | `clarify(question="Bạn chưa cung cấp đường dẫn... Bạn có muốn gửi bài viết để tôi tóm tắt trước, sau đó xác nhận...", response_type="yes_no")` | `v3+pe1a48e541bd8+tbb0d8853555c` | Kích hoạt ranh giới Human-in-the-Loop, hỏi xác nhận yes/no trước khi thực thi action tool. |

### B5a. Required Evidence — Tool mới, unit test, UI

- **Tool mới (`starter_v0/tools/dedupe_sources/`)**:
  - `tool.py`: Hàm `dedupe_sources(items)` xử lý parse URL, loại bỏ tracking tags tiếp thị (`utm_source`, `utm_medium`, `fbclid`, v.v.), loại bỏ hash anchor và chuẩn hóa domain để lọc sạch trùng lặp, giữ lại nguồn xuất hiện đầu tiên.
  - `TOOL.md`: Tài liệu đặc tả chức năng, input/output schemas và convention sử dụng.
  - Đăng ký đầy đủ trong `starter_v0/tools/__init__.py` và khai báo schema trong `starter_v0/artifacts/tools.yaml`.
- **Unit Tests (`starter_v0/tests/test_tools_todo.py`)**:
  - `test_dedupe_sources_removes_tracking_variants_and_preserves_first`: Kiểm tra khử trùng lặp và giữ nguyên bài đầu tiên (happy path).
  - `test_dedupe_sources_rejects_wrong_input_type_with_error_dict`: Kiểm tra input không phải list (trả error dict, không raise crash).
  - `test_dedupe_sources_malformed_url_returns_error_dict_without_raising`: Kiểm tra URL sai định dạng (trả error dict an toàn).
  - **Kết quả nghiệm thu `pytest`**: Đạt **84 passed, 0 failed, 0 skipped** (Contract test và toàn bộ tool suite đều xanh 100%).
- **UI Giao diện (`starter_v0/app.py`)**:
  - Giao diện Streamlit hỗ trợ tương tác Live Chat với Agent, tích hợp lựa chọn Model/Provider, hiển thị tool calling breakdown theo thời gian thực và tự động xuất file transcript JSON chuẩn định dạng sau mỗi lượt chat.

---

## 5. Khó khăn và cách xử lý

- **Lỗi Giới hạn API Provider (Rate Limit 429 & Quota Limit)**:
  - Khi thực hiện vòng lặp v1->v3 trên Gemini Free Tier, gặp giới hạn 5 req/phút (RPM) và 20 req/ngày (RPD).
  - **Cách xử lý**: Nhóm chủ động cấu hình pacing sleep giữa các request, phân tách các đợt chạy và ghi nhận trung thực tỷ lệ hoàn thành của các test case đã đo được theo đúng quy định tại `RULES.md:L32`.
- **Lỗi Provider 503 (Model High Demand Spikes)**:
  - Khi chạy bộ eval nhóm trên Gemini API, 2 cases (G09, G11) gặp lỗi 503 do dịch vụ Google AI quá tải thời điểm đó.
  - **Cách xử lý**: Hệ thống harness ghi nhận chính xác trạng thái `provider_error` mà không làm crash luồng đánh giá chung. Tỷ lệ case đo được vẫn đạt 77.8% accuracy.
- **Phân tách ranh giới và kiểm thử an toàn**:
  - Ranh giới giữa `clarify` (khi thiếu URL/tài khoản) và từ chối ngoài phạm vi dễ bị nhập nhằng.
  - **Cách xử lý**: Quy định tường minh trong prompt: Chỉ gọi `clarify` cho các tác vụ nghiên cứu có hỗ trợ mà thiếu tham số bắt buộc; các yêu cầu ngoài phạm vi hoặc câu hỏi meta phải trả lời trực tiếp mà không dùng tool.

---

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân:
- `report/team/2A202603960_NguyenMinhDuc.md` (Nguyễn Minh Đức)
- `report/team/DoanVietHuy.md` (Đoàn Viết Huy)

---

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Prompt và Tool Declarations có tính chất bổ trợ chặt chẽ: Prompt quy định quy tắc ranh giới tổng thể và chiến lược giải quyết mâu thuẫn, trong khi `tools.yaml` định hình chính xác kiểu dữ liệu và mô tả khi nào nên/không nên kích hoạt công cụ.
- Khi đánh giá năng lực agent trong môi trường production, cần thiết lập cơ chế retry với exponential backoff và fallback giữa các provider để xử lý triệt để các lỗi tạm thời như HTTP 429 hay 503 từ nhà cung cấp dịch vụ LLM.
