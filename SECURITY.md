# Security Policy / سياسة الأمان

Dashboard Generator is a local report generator. It does not intentionally make network requests, execute input data, or collect telemetry.

## Supported version
Security fixes target the latest version on `main`.

## Reporting
Please report suspected vulnerabilities privately through GitHub's security reporting features when available rather than publishing exploit details in a public issue.

## Data handling
Generated HTML contains values from the supplied dataset. Treat the report with the same sensitivity as its input. The renderer escapes HTML and safely serializes embedded data, but users should still avoid opening untrusted modified report files as though they were trusted application artifacts.

## العربية

الأداة محلية ولا تنفذ بيانات الإدخال ولا تجمع telemetry ولا تجري اتصالات شبكة مقصودة. يستهدف الدعم الأمني أحدث نسخة على `main`. يفضل الإبلاغ عن الثغرات بصورة خاصة عبر أدوات GitHub الأمنية المتاحة. يحتوي ملف HTML الناتج على بيانات المصدر، لذلك يجب التعامل معه بنفس مستوى حساسية البيانات الأصلية. يقوم المولد بتهريب HTML وتسلسل البيانات المضمنة بأمان، لكن لا ينبغي اعتبار ملفات التقارير المعدلة من جهات غير موثوقة ملفات موثوقة.
