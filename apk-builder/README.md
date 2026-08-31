# 📱 ساخت APK اندروید - ربات روبیکا

## ✅ روش ۱: GitHub Actions (رایگان و ساده)

### مراحل:

**۱. کد رو به GitHub بفرستید:**
```bash
cd apk-builder
git init
git add .
git commit -m "init"
git remote add origin https://github.com/YOUR_USERNAME/rubika-bot.git
git push -u origin main
```

**۲. GitHub Actions خودکار APK می‌سازه!**
- برو به تب **Actions** در ریپازیتوری
- منتظر بمانید تا Build تموم بشه
- از تب **Artifacts** فایل APK رو دانلود کنید

**۳. APK رو روی گوشی نصب کنید!**

---

## ✅ روش ۲: ساخت با Buildozer (روی کامپیوتر)

### پیش‌نیازها (لینوکس یا WSL):
```bash
# نصب Buildozer
pip install buildozer

# رفتن به پوشه پروژه
cd apk-builder

# ساخت APK
buildozer android debug
```

APK در پوشه `bin/` ساخته می‌شه.

---

## ✅ روش ۳: Colab (بدون نصب)

### مراحل:
1. برو به [Google Colab](https://colab.research.google.com)
2. این کدها رو اجرا کن:

```python
!pip install buildozer cython
!apt-get install -y build-essential git python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# کپی فایل‌ها
!mkdir -p apk-builder
# ... (فایل‌ها رو آپلود کنید)

!cd apk-builder && buildozer android debug
```

---

## 📱 نصب APK:

1. فایل APK رو به گوشی منتقل کنید
2. در گوشی، فایل رو باز کنید
3. اگر پیام "از منابع ناشناخته" اومد، تایید کنید
4. نصب کنید
5. اپ رو باز کنید!

---

## 🎮 امکانات اپ:

- ✅ لاگین با شماره تلفن
- ✅ ارسال پیام به گروه‌ها
- ✅ تنظیم متن پیام
- ✅ ارسال خودکار
- ✅ نمایش گروه‌ها
- ✅ ذخیره تنظیمات

---

## ⚠️ نکات مهم:

- اپ به **اینترنت** نیاز داره
- از **شماره واقعی** روبیکا استفاده کنید
- **Session** ذخیره می‌شه، دفعه بعد نیاز به لاگین نیست
- حتماً **rubpy** نسخه آخر رو نصب کنید
