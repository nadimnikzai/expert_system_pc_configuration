from experta import Fact, Field

# --- ورودی کاربر ---
class UserInput(Fact):
    usage = Field(str)       # Gaming, Office, ...
    # این فیلدها را فعلاً تعریف می‌کنیم تا بعداً پر شوند
    budget = Field(int)
    cpu_pref = Field(str)
    gpu_pref = Field(str)
    case_size = Field(str)
    ram_pref = Field(int)  # مقدار دستی رم (مثلا 32) یا 0 برای اتوماتیک
    storage_pref=Field(str)

# --- خروجی جدول ۱: نیازهای سیستم (System Usage) ---
class BaseRequirements(Fact):
    gpu_required = Field(str)          # T, F, Optional
    min_gpu_tier = Field(str)          # Low, Medium, High...
    cpu_importance = Field(str)        # Low, Medium, High
    ram_base_requirement = Field(int)  # 8, 16, 32
    storage_base = Field(str)          # 256GB, 1TB...

    # ... کدهای قبلی ...

# --- خروجی جدول ۲: محدودیت‌های بودجه (Budget Constraints) ---
class BudgetConstraints(Fact):
    budget_tier = Field(str)     # مثلا Entry, Mid, High
    max_gpu_tier = Field(str)    # سقف قدرت گرافیک
    max_cpu_tier = Field(str)    # سقف قدرت پردازنده
    ram_limit = Field(int)       # سقف رم (مثلا 32)
    storage_limit = Field(str)   # سقف حافظه



# ... کدهای قبلی ...

# --- خروجی مرحله ۳: پردازنده انتخاب شده (Selected CPU) ---
class SelectedCPU(Fact):
    tier = Field(str)    # سطح قدرت (Low, Medium, High, Ultra)
    brand = Field(str)   # Intel, AMD
    model = Field(str)   # مثلا Core i5-12400F
    socket = Field(str)  # LGA1700 یا AM4 یا AM5 (برای مادربورد لازمه)


# ... کدهای قبلی ...

# --- خروجی مرحله ۴: گرافیک (طبق جدول شما فقط همین ۳ تا) ---
class SelectedGPU(Fact):
    tier = Field(str)     # Low, Medium, High
    brand = Field(str)    # NVIDIA, AMD, Integrated
    model = Field(str)    # نام مدل



# ... کدهای قبلی ...

# --- خروجی مرحله ۵: مادربورد انتخاب شده ---
class SelectedMotherboard(Fact):
    model = Field(str)    # نام مدل (مثلا ASUS Prime B760)
    chipset = Field(str)  # چیپست (B760, Z790, B650...)
    size = Field(str)     # سایز (ATX, mATX, ITX)

# --- خروجی مرحله ۵: کیس انتخاب شده ---
class SelectedCase(Fact):
    model = Field(str)    # نام مدل (مثلا Master Tech T500)
    form_factor = Field(str) # سایز کیس (Mid Tower, Full Tower...)


class SelectedRAM(Fact):
    capacity = Field(int)  # حجم (مثلا 16)
    speed = Field(str)     # سرعت و نسل (مثلا DDR4 3200MHz)
    model = Field(str)     # مدل و دلیل (مثلا Corsair ... (Reason))


class SelectedStorage(Fact):
    capacity = Field(str) # مثلا 1 TB
    model = Field(str)    # مثلا Samsung 980
    type = Field(str)     # مثلا NVMe Gen4