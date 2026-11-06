# RDK X5 EdgeVision — شرح التنفيذ بالعربي

**الحالة الحالية:** جهزنا الكود، الدائرة، ملفات التوثيق، وفحوصات ما قبل التسليم. لم نشغّل اللوحة فعلياً ولم نصوّر أدلة، ولذلك ليست مشاركة مكتملة بعد.

## ما سنقدمه في المرحلة الأولى (Ignite)

1. تفليش النظام الرسمي على **RDK X5**، ثم توصيل الإنترنت وتصوير جلسة SSH حقيقية.
2. توصيل **كاميرا USB UVC** على منفذ USB-A في اللوحة، وحفظ صورة فعلية من الكاميرا كدليل عمل الحساس.
3. تشغيل مثال YOLO11m الرسمي على اللوحة نفسها باستخدام BPU ومشاهدة إطار الصورة مع كشف الأجسام.
4. تجهيز README ومخططات التوصيل ونموذج العرض؛ ثم رفع مستودع GitHub عام ونشر الروابط في خيط Discord وفتح Pull Request.

لا يوجد أي ادعاء أن الصور المولدة أو المخططات تثبت عمل الهاردوير. الدليل يجب أن يُلتقط من جهازك فعليًا.

## القطع المطلوبة

- لوحة RDK X5 (ضرورية)، مزود طاقة USB-C بقيمة **5V/5A** للمنفذ المخصص للطاقة، وكرت microSD عليه صورة النظام المناسبة إن لزم.
- كاميرا USB قياسية داعمة UVC (ضرورية لمسارنا)، كابل Ethernet أو Wi-Fi، شاشة HDMI أو SSH مع X11.
- **اختياري فقط:** LED أحمر + مقاومة 470 أوم + 2 سلك Jumper لعمل اختبار GPIO.

## التوصيل

1. الكاميرا إلى USB-A HOST على RDK X5.
2. Ethernet إلى الراوتر. لو تستخدم Wi-Fi فلا حاجة لهذا الكابل.
3. محول **5V/5A** إلى منفذ Power USB-C. لا تستخدم USB الكمبيوتر كمصدر للطاقة.
4. اختياري (بعد فصل الطاقة): رجل **BOARD 15** -> مقاومة **470Ω** -> أنود LED (الرجل الطويلة)، كاثود LED (القصيرة) -> رجل GND **BOARD 14**. راجع مستوى 3.3V وpinmux، ولا توصل LED مباشرةً بدون مقاومة.

راجع `hardware/rdk_x5_wiring.png` و`hardware/optional_led_schematic.png`.

## الأوامر المختصرة — تُنفَّذ على اللوحة بعد التفليش وSSH

```bash
cd RDK-X5-EdgeVision-Ignite-2026
bash scripts/01_preflight.sh
python3 scripts/02_camera_test.py --device 0 --output evidence/02_sensor_camera.png
bash scripts/03_setup_model.sh
# افتح Terminal داخل Desktop الخاص باللوحة أو SSH يدعم X11
bash scripts/04_run_yolo.sh 0
```

**للدائرة الإضافية فقط:**

```bash
sudo python3 scripts/05_led_test.py --pin 15 --seconds 10
```

بعد تصوير FLASH + SSH والنافذة التي تعرض YOLO11m على اللوحة، راجع `docs/SUBMISSION_CHECKLIST.md` وشغّل `python3 scripts/06_verify_submission.py`.

## قبل التسليم

- تأكد أن لديك تسجيل فعال و**خيط Discord شخصي**.
- التقط أدلة حقيقية (لا تستخدم صورة مولّدة بدلًا من تشغيل اللوحة).
- انشر الكود في GitHub الشخصي مع الروابط والأدلة بعد فحص الأسرار.
- افتح PR يحتوي **ملف عرض واحد** تحت `projects/` داخل المستودع الرسمي؛ لا تضع الكود كله في هذا المستودع.

**الموعد المعلن للمرحلة الأولى: 10 نوفمبر 2026.**

## الفيديو والتحقق النهائي

**Stage 1 لا يشترط فيديو**، ولكن يلزم لقطات تشغيل حقيقية + GitHub + Discord + PR. **Stage 3 يشترط فيديو** من 3–7 دقائق و30 ثانية تشغيل AI متواصل. [دليل الفيديو الكامل](docs/VIDEO_REQUIREMENTS_AND_SHOTLIST_AR.md).

بعد تشغيل اللوحة: `bash scripts/07_board_info.sh`، ثم املأ `submission/stage1_links.json` بروابطك الحقيقية، ثم `python3 scripts/08_verify_submission.py`. نجاح هذا الاختبار لا يثبت قبول المسابقة.

## الصور والمنشور

الصورة `assets/CONCEPT_ONLY_NOT_EVIDENCE.png` تصوير تخيّلي وليست توثيقًا عمليًا ولا مرجعًا للتوصيل الكهربائي. راجع `docs/REFERENCE_IMAGE_AUDIT.md` لمراجع القطع الأصلية، وملفي `submission/DISCORD_PROGRESS_POST.md` و`submission/DISCORD_COMPLETION_TEMPLATE.md` للمنشور الحالي والنهائي. نشر GitHub يحتاج إنشاء مستودع فارغ لأن هذه الجلسة لا تملك إجراء إنشاء المستودع؛ راجع `docs/GITHUB_PUBLICATION_GUIDE.md`.
