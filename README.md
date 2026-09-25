# Spec-Driven Product Toolkit

[English version](README.en.md)

Một bộ skill và installer giúp phát triển sản phẩm bằng AI coding agent theo quy trình:

```text
Đặc tả → Thiết kế → Lập kế hoạch → Triển khai → Kiểm thử → Audit → Review → Release
```

Toolkit được thiết kế cho vibe coding có kiểm soát: agent vẫn làm việc nhanh, nhưng mọi thay đổi quan trọng đều có tiêu chí chấp nhận, lệnh kiểm chứng và báo cáo audit.

> Đây là một bộ tích hợp độc lập, không phải bản phân phối chính thức của bất kỳ dự án upstream nào. Toolkit kế thừa/cảm hứng từ các dự án được ghi rõ trong [catalog nguồn](references/catalog.md).

## Có gì trong repo?

| Thành phần | Chức năng |
|---|---|
| [`SKILL.md`](SKILL.md) | Điểm vào của skill trong Codex |
| [`references/profiles.md`](references/profiles.md) | Tiêu chí chọn profile và các giai đoạn workflow |
| [`references/catalog.md`](references/catalog.md) | Chức năng, repo nguồn và thông tin truy nguyên |
| [`scripts/install_profile.py`](scripts/install_profile.py) | Preflight, chọn profile và tạo manifest cài đặt |
| [`agents/openai.yaml`](agents/openai.yaml) | Tên hiển thị và prompt mặc định trong Codex |

## Ba profile

| Profile | Phù hợp với | Phương pháp | Các giai đoạn |
|---|---|---|---|
| `prototype` | Prototype, MVP nhỏ, dự án ít rủi ro | Matt Pocock workflow, feedback nhanh | Grill → plan → implement → smoke test → review |
| `balanced` | Ứng dụng thật, nhóm nhỏ/vừa | Matt Pocock + quality gates thực thi | Discover → design → plan → implement → test → audit → PR review |
| `production` | Sản phẩm đã triển khai, dữ liệu nhạy cảm, nhiều contributor | Balanced + Spec Kit + security/release gates | Spec → design → plan → implement → full audit → protected PR → release/retro |

### Nên chọn profile nào?

- Chọn `prototype` nếu bạn cần kiểm chứng ý tưởng nhanh và không xử lý dữ liệu nhạy cảm.
- Chọn `balanced` nếu đây là sản phẩm thật có UI/API/database và bạn muốn kiểm tra code, UI, dependency, secret và security cơ bản.
- Chọn `production` nếu có authentication, payment, PII, migration quan trọng, CI/CD production, nhiều contributor hoặc yêu cầu audit.

## Công cụ theo profile

### Prototype

- Matt Pocock Skills: làm rõ yêu cầu, lập kế hoạch, triển khai, review.
- Playwright: smoke test UI nếu dự án có web app.
- Formatter, linter, typecheck và test native của project.

### Balanced

- Tất cả thành phần của Prototype.
- `pre-commit`: quality hooks tại local.
- `Semgrep`: SAST và code pattern audit.
- `Gitleaks`: phát hiện secret.
- `OSV-Scanner`: kiểm tra dependency vulnerability.
- `SQLFluff`: lint SQL khi dự án có SQL.
- `Reviewdog`: đưa kết quả audit vào pull request.
- `axe-core` và `Lighthouse`: accessibility, performance, SEO và best practices.

### Production

- Tất cả thành phần của Balanced.
- `Spec Kit`: đặc tả bền vững cho feature lớn.
- `Trivy`: container, filesystem và IaC scanning.
- `CodeQL`: semantic security analysis sâu hơn.
- `Zizmor`: audit GitHub Actions.
- `Atlas` hoặc migration authority hiện có của ORM: schema diff và migration plan.
- Visual regression và artifact bắt buộc trong CI.

## Cài đặt

### Chạy installer và để toolkit hỏi lựa chọn

```powershell
python scripts/install_profile.py --target D:\path\to\your-project
```

### Xem profile trước khi cài

```powershell
python scripts/install_profile.py --target D:\path\to\your-project --list-profiles
```

### Kiểm tra tool mà không thay đổi project

```powershell
python scripts/install_profile.py --target D:\path\to\your-project --profile balanced --check-only
```

### Cài profile đã chọn

```powershell
python scripts/install_profile.py --target D:\path\to\your-project --profile balanced
```

Installer tạo thư mục `.spec-product/` trong target project, bao gồm:

- `manifest.json`: profile và component đã chọn.
- `README.md`: phạm vi, phương pháp và giai đoạn.
- `source-catalog.md`: nguồn upstream của các component.

Tool thiếu không bị bỏ qua âm thầm. Installer trả về trạng thái chưa hoàn tất để bạn cài bổ sung trước khi coi workflow là verified.

## Nguyên tắc tránh xung đột

- Chỉ dùng Matt Pocock làm workflow orchestrator chính.
- Spec Kit chỉ bổ sung cho feature lớn trong profile `production`.
- Playwright là browser runner duy nhất mặc định.
- axe-core là accessibility engine; Lighthouse là performance/SEO auditor.
- Semgrep, Gitleaks, OSV-Scanner, Trivy và CodeQL có vai trò khác nhau, không thay thế lẫn nhau.
- Atlas không được trở thành schema authority thứ hai nếu project đã dùng Prisma, Drizzle hoặc migration system khác.

## Attribution và provenance

Toolkit này là một composition layer do tác giả repo này xây dựng, lấy cảm hứng và chọn lọc vai trò từ nhiều dự án mã nguồn mở. Không nên hiểu đây là endorsement hay bản fork chính thức. Danh sách đầy đủ repo nguồn, chức năng và liên kết truy nguyên nằm tại [references/catalog.md](references/catalog.md).

Khi tái sử dụng hoặc phân phối lại, hãy kiểm tra license và điều khoản của từng upstream project.

## License

Toolkit hiện cung cấp cấu hình và tài liệu tích hợp. License của từng công cụ upstream vẫn áp dụng riêng theo repo nguồn tương ứng.
