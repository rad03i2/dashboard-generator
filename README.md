# Dashboard Generator

A local-first Python tool that turns JSON or CSV data into a polished, self-contained HTML dashboard. No web server, JavaScript framework, account, telemetry, or runtime dependency is required.

> The repository is being initialized with a complete implementation in this run; see the files in `src/`, `tests/`, and `examples/`.

## English

### Overview
Dashboard Generator converts structured data into a portable HTML report with summary cards, a searchable data table, automatic numeric statistics, responsive layout, light/dark theme support, and safe HTML escaping.

### Why it exists
Quick data inspection should not require deploying a BI service. This project provides a small deterministic CLI for creating reports that can be opened locally or attached to an email/artifact.

### Key features
- JSON arrays and CSV input.
- Automatic column discovery and numeric summaries.
- Responsive self-contained HTML; no CDN assets.
- Searchable/sortable table implemented with embedded vanilla JavaScript.
- Light/dark/system theme selection.
- Optional title/subtitle and row limit.
- JSON build summary for automation.
- HTML escaping and safe JSON embedding.
- Python API plus `dashboard-generator` CLI.

### Preview
Generate `dashboard.html` from `examples/sales.csv`, then open it in any modern browser. Screenshots are intentionally not committed because the rendered report is reproducible from the included sample.

### Requirements & installation
Python 3.10+.

```bash
python -m pip install -e .
dashboard-generator examples/sales.csv -o dashboard.html --title "Sales overview"
```

No environment variables are required.

### Usage
```bash
# CSV
dashboard-generator data.csv -o report.html

# JSON array
dashboard-generator data.json -o report.html --theme dark --max-rows 500

# machine-readable build result
dashboard-generator data.csv -o report.html --json

# module entry point
python -m dashboard_generator examples/sales.csv -o dashboard.html
```

Input JSON must be an array of objects. CSV must contain a header row. `--max-rows` limits rendered table rows, while summary statistics are calculated from the full input.

### Python API
```python
from pathlib import Path
from dashboard_generator import build_dashboard, load_records

records = load_records(Path("examples/sales.csv"))
result = build_dashboard(records, Path("dashboard.html"), title="Sales")
print(result.rows, result.columns)
```

### Project structure
```text
src/dashboard_generator/   package, loader, renderer and CLI
tests/                     unit and CLI tests
examples/sales.csv         synthetic sample input
.github/workflows/ci.yml   cross-platform CI
```

### Testing
```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```
CI runs the suite on Python 3.10, 3.12 and 3.13 across Ubuntu, Windows and macOS.

### Security & privacy
All processing is local. The application performs no network requests and includes no telemetry. Values and labels are HTML-escaped, and embedded table data is serialized safely. Generated reports contain the source values you provide, so review them before sharing if the input is sensitive.

### Limitations
- JSON input is limited to a top-level array of flat objects; nested values are displayed as compact JSON strings.
- CSV encoding is UTF-8/UTF-8-BOM.
- Numeric summaries use values that can be parsed as finite numbers; this is not a schema/type inference engine.
- Charts are intentionally omitted to keep reports dependency-free and deterministic.
- Very large inputs should use `--max-rows` because the output is a single HTML file.

### Optional roadmap
Potential future additions include explicit schemas, chart components, and streaming readers. These are not required for current functionality.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Security guidance is in [SECURITY.md](SECURITY.md).

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
Dashboard Generator أداة محلية بلغة بايثون تحول بيانات JSON أو CSV إلى لوحة HTML مستقلة قابلة للفتح مباشرة في المتصفح، مع بطاقات ملخص وجدول قابل للبحث والترتيب وإحصاءات رقمية تلقائية وتصميم متجاوب.

### لماذا هذا المشروع؟
ليس من الضروري نشر منصة ذكاء أعمال كاملة لمعاينة مجموعة بيانات أو مشاركة تقرير بسيط. توفر الأداة مسارًا صغيرًا وحتميًا لإنشاء تقرير محلي محمول بلا خادم أو حساب خارجي.

### الميزات
- قراءة JSON وCSV.
- اكتشاف الأعمدة وإحصاءات رقمية تلقائية.
- ملف HTML واحد بلا CDN أو أطر JavaScript.
- بحث وترتيب للجدول.
- ثيم فاتح أو داكن أو حسب النظام.
- عنوان وعنوان فرعي وحد أقصى اختياري للصفوف المعروضة.
- نتيجة JSON مناسبة للأتمتة.
- تهريب آمن لمحتوى HTML.
- واجهة Python إضافة إلى CLI.

### المعاينة
أنشئ `dashboard.html` من `examples/sales.csv` وافتحه بمتصفح حديث. لم نضف لقطة ثابتة لأن التقرير يمكن إعادة توليده من المثال المرفق.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث.

```bash
python -m pip install -e .
dashboard-generator examples/sales.csv -o dashboard.html --title "Sales overview"
```

لا يحتاج المشروع إلى متغيرات بيئة.

### الاستخدام
```bash
dashboard-generator data.csv -o report.html
dashboard-generator data.json -o report.html --theme dark --max-rows 500
dashboard-generator data.csv -o report.html --json
python -m dashboard_generator examples/sales.csv -o dashboard.html
```

يجب أن يكون JSON مصفوفة من الكائنات، ويجب أن يحتوي CSV على صف عناوين. يحد `--max-rows` عدد الصفوف داخل الجدول فقط، بينما تحسب الإحصاءات من كامل البيانات.

### واجهة Python
```python
from pathlib import Path
from dashboard_generator import build_dashboard, load_records
records = load_records(Path("examples/sales.csv"))
result = build_dashboard(records, Path("dashboard.html"), title="Sales")
```

### بنية المشروع
المصدر داخل `src/dashboard_generator/`، والاختبارات داخل `tests/`، ومثال البيانات داخل `examples/`، وCI داخل `.github/workflows/ci.yml`.

### الاختبارات
```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```
ويشغّل CI الاختبارات على Python 3.10 و3.12 و3.13 في Ubuntu وWindows وmacOS.

### الأمان والخصوصية
كل المعالجة محلية، ولا توجد طلبات شبكة أو telemetry. يتم تهريب القيم والعناوين قبل إدراجها في HTML. التقرير الناتج يحتوي بيانات المصدر نفسها، لذلك يجب مراجعته قبل المشاركة إذا كانت البيانات حساسة.

### القيود
- يدعم JSON مصفوفة علوية من كائنات؛ القيم المتداخلة تظهر كنص JSON مختصر.
- CSV مدعوم بترميز UTF-8 أو UTF-8-BOM.
- الإحصاءات الرقمية تعتمد القيم المحدودة القابلة للتحويل إلى أرقام ولا تمثل نظام استنتاج مخطط كاملًا.
- لا توجد رسوم بيانية حاليًا للحفاظ على الاستقلالية والحتمية.
- للملفات الكبيرة يفضل استخدام `--max-rows` لأن الناتج ملف HTML واحد.

### تطوير اختياري
يمكن مستقبلًا إضافة مخططات صريحة ورسوم بيانية وقراءة تدفقية، لكنها ليست مطلوبة لعمل الإصدار الحالي.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md)، وإرشادات الأمان في [SECURITY.md](SECURITY.md).

### الترخيص
MIT — راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
