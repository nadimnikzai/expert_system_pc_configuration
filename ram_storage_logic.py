from experta import Rule, MATCH, KnowledgeEngine
from facts import BaseRequirements, BudgetConstraints, SelectedCPU, SelectedRAM, SelectedStorage

class RamStorageRules(KnowledgeEngine):
    
    @Rule(
        BaseRequirements(ram_base_requirement=MATCH.req_ram, storage_base=MATCH.req_store), # نیاز جدول ۱
        BudgetConstraints(ram_limit=MATCH.max_ram, storage_limit=MATCH.max_store),          # سقف جدول ۲
        SelectedCPU(socket=MATCH.sock), # برای تشخیص DDR4/DDR5
        BudgetConstraints(budget_tier=MATCH.tier) # برای تشخیص نسل هارد
    )
    def select_ram_storage_strict(self, req_ram, req_store, max_ram, max_store, sock, tier):
        
        # ==========================================
        # بخش ۱: منطق رم (RAM)
        # ==========================================
        
        # --- الف) تعیین حجم (Intersection) ---
        final_ram = req_ram # پیش‌فرض: همون چیزی که نیازه

        # اگر نیاز بیشتر از زورِ بودجه باشد، محدودش میکنیم به سقف بودجه
        if req_ram > max_ram:
            final_ram = max_ram
        
        # نکته: اگر نیاز کمتر از بودجه باشد (مثلا آفیس ۸ گیگ، بودجه ۳۲ گیگ)، 
        # همون ۸ گیگ میمونه چون جدول Usage گفته ۸ کافیه.

        # --- ب) تعیین نوع (DDR4 vs DDR5) ---
        # این بخش فنی است و باید با پردازنده مچ شود
        ram_tech = "DDR4"

        if sock == "AM5":
            # رایزن‌های جدید فقط DDR5 هستند
            ram_tech = "DDR5"
        elif sock == "LGA1700": # اینتل نسل ۱۲/۱۳/۱۴
            # بستگی به بودجه داره
            if tier in ['Low', 'Entry']:
                ram_tech = "DDR4" # مادربوردهای H610/B760 ارزون معمولا DDR4 هستن
            else:
                ram_tech = "DDR5" # بودجه‌های Mid به بالا DDR5 میبندیم
        elif sock == "AM4":
            ram_tech = "DDR4"

        # ثبت رم
        self.declare(SelectedRAM(
            capacity=final_ram,
            type=ram_tech
        ))

        # ==========================================
        # بخش ۲: منطق هارد (Storage)
        # ==========================================
        
        # --- الف) تعیین حجم ---
        # نگاشت متن به عدد برای مقایسه (چون رشته هستند)
        # 256GB -> 1, 512GB -> 2, 1TB -> 3, 2TB -> 4, 4TB -> 5
        def size_rank(s):
            if "256" in s: return 1
            if "512" in s: return 2
            if "1" in s and "TB" in s: return 3
            if "2" in s and "TB" in s: return 4
            if "4" in s and "TB" in s: return 5
            return 0

        req_rank = size_rank(req_store)
        max_rank = size_rank(max_store)

        final_storage = req_store # پیش‌فرض

        # اگر نیاز بیشتر از سقف بودجه باشد
        if req_rank > max_rank:
            final_storage = max_store # کاهش به سقف بودجه
        
        # --- ب) تعیین سرعت (Gen3 vs Gen4) ---
        storage_tech = "NVMe Gen3"
        
        if tier in ['Very Low', 'Entry']:
            storage_tech = "NVMe Gen3"
        else:
            # Mid, High, Enthusiast -> Gen4
            storage_tech = "NVMe Gen4"

        # ثبت هارد
        self.declare(SelectedStorage(
            capacity=final_storage,
            type=storage_tech
        ))