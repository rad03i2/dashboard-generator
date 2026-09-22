# Contributing / المساهمة

Thanks for improving Dashboard Generator. Keep changes focused, dependency-light, and backward compatible where practical.

1. Use Python 3.10+ and create a virtual environment.
2. Install with `python -m pip install -e .`.
3. Add tests for behavior changes.
4. Run `python -m unittest discover -s tests -v` and `python -m compileall -q src tests`.
5. Keep generated dashboards, private datasets, secrets, and credentials out of commits.
6. Open a focused pull request explaining the user-visible change and validation performed.

For bugs, include a minimal synthetic input when possible. Never attach sensitive production data.

## العربية

نرحب بالمساهمات المركزة التي تحافظ على بساطة المشروع وتوافقه. استخدم Python 3.10+، وأضف اختبارات لأي تغيير سلوكي، وشغّل مجموعة الاختبارات و`compileall` قبل فتح Pull Request. لا ترفع بيانات خاصة أو تقارير مولدة أو أسرارًا أو مفاتيح وصول. عند الإبلاغ عن خلل، استخدم عينة اصطناعية صغيرة كلما أمكن.
