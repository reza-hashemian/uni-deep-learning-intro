<div dir="rtl">

# یادگیری عمیق: مبانی پایتون، NumPy/Matplotlib و PyTorch

مجموعه‌ی سه جلسه‌ای برای آشنایی با پایه‌های برنامه‌نویسی و ابزارهای یادگیری عمیق. دو جلسه‌ی اول روی **پایتون، NumPy و Matplotlib** تمرکز دارند و جلسه‌ی سوم به **PyTorch و شبکه‌ی عصبی کانولوشنی (CNN)** می‌پردازد.

هدف این است که وقتی به کد PyTorch می‌رسیم، هیچ خطی برایتان عجیب نباشد. هر مفهوم با مثال، نمودار و تمرین همراه است.

## ساختار ریپو

| فایل / پوشه | توضیح |
|---|---|
| `session1_python_basics.ipynb` | **جلسه ۱:** مبانی پایتون: متغیر، نوع داده، لیست/tuple/dict، شرط و حلقه، تابع، مفهوم «اسم» در برابر «جعبه»، کپی shallow/deep، خطاها و شیءگرایی |
| `session2_numpy_matplotlib.ipynb` | **جلسه ۲:** Data Model پایتون (dunder)، iterator و generator، `Dataset`/`DataLoader`، `with` و دکوراتور، NumPy (آرایه، برش، broadcasting، `axis`، ضرب ماتریسی)، Matplotlib و پرسپترون از صفر (با نشان‌دادن شکست روی XOR) |
| `session3_pytorch_cnn.ipynb` | **جلسه ۳:** تنسور، autograd، رگرسیون خطی، `nn.Module`، MLP برای XOR و MNIST، CNN و کانولوشن، ذخیره‌سازی مدل و GPU |
| `figures/` | نمودارهای آموزشی و اسکریپت تولید آن‌ها (`make_figures.py`) |

## پیش‌نیازها

- Python 3.9 یا جدیدتر
- کتابخانه‌ها:

```bash
pip install numpy matplotlib torch torchvision jupyter
```

## اجرا

```bash
git clone https://github.com/reza-hashemian/uni-deep-learning-intro.git
cd uni-deep-learning-intro
jupyter lab
```

سپس notebookها را به ترتیب شماره اجرا کنید.

> **نکته:** دیتاست MNIST در جلسه‌ی ۳ به‌صورت خودکار دانلود می‌شود و در پوشه‌ی `data/` ذخیره می‌شود. این پوشه عمداً در ریپو قرار نگرفته است.

## بازسازی نمودارها

```bash
python figures/make_figures.py
```

## مجوز

<!-- مجوز را اینجا تعیین کنید، مثلاً MIT یا CC BY-NC 4.0 -->
</div>
