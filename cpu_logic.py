from experta import Rule, MATCH, KnowledgeEngine
from facts import UserInput, BaseRequirements, BudgetConstraints, SelectedCPU

class CPURules(KnowledgeEngine):
    
    # ورودی‌ها: برند دلخواه + اهمیت پردازنده (از جدول ۱) + سقف بودجه (از جدول ۲)
    @Rule(
        UserInput(cpu_pref=MATCH.brand_pref),
        BaseRequirements(cpu_importance=MATCH.imp),
        BudgetConstraints(max_cpu_tier=MATCH.max_tier)
    )
    def select_cpu_strict(self, brand_pref, imp, max_tier):
        
        final_tier = None # هیچ پیش‌فرضی نداریم

        # ====================================================
        # منطق تقاطع جدول‌ها (Strict Logic)
        # ====================================================

        # --- سناریو ۱: بودجه محدود است (Max: Medium) ---
        # در این حالت مهم نیست اهمیت چیست، سیستم زورِ بیشتر از Medium ندارد.
        if max_tier == 'Medium':
            final_tier = 'Medium'
        if max_tier == 'Low':
            final_tier = 'Low'

        # --- سناریو ۲: بودجه متوسط است (Max: High) ---
        elif max_tier == 'High':
            if imp == 'Low': final_tier = 'Low'        # بودجه هست، ولی نیاز کمه -> Low
            elif imp == 'Medium': final_tier = 'Medium' # نیاز متوسطه -> Medium
            elif imp == 'High': final_tier = 'High'     # نیاز بالاست -> High

        # --- سناریو ۳: بودجه زیاد است (Max: Ultra) ---
        elif max_tier == 'Ultra':
            if imp == 'Low': final_tier = 'Medium'      # با بودجه زیاد، Low نمیبندیم
            elif imp == 'Medium': final_tier = 'High'   # ارتقا میدیم
            elif imp == 'High': final_tier = 'Ultra'    # نهایت قدرت

        
        # اگر حالتی پیش بیاید که در جدول بالا نباشد، یعنی دیتای ورودی غلط است و سیستم چیزی پیشنهاد نمیدهد
        if final_tier is None:
            self.declare(SelectedCPU(tier='NA', brand='NA', model='NA', socket='NA'))
            return

        # ====================================================
        # انتخاب قطعه نهایی بر اساس Tier و Brand
        # ====================================================
        
        target_brand = brand_pref
        if target_brand == 'Auto' or not target_brand:
            target_brand = 'Intel' # اگر کاربر نگفت، اینتل بده

        # >>> قطعات اینتل <<<
        if target_brand == 'Intel':
            if final_tier == 'Low':
                self.declare(SelectedCPU(tier='Low', brand='Intel', model='Core i3-12100', socket='LGA1700'))
            elif final_tier == 'Medium':
                self.declare(SelectedCPU(tier='Medium', brand='Intel', model='Core i5-12400F', socket='LGA1700'))
            elif final_tier == 'High':
                self.declare(SelectedCPU(tier='High', brand='Intel', model='Core i7-13700K', socket='LGA1700'))
            elif final_tier == 'Ultra':
                self.declare(SelectedCPU(tier='Ultra', brand='Intel', model='Core i9-14900K', socket='LGA1700'))

        # >>> قطعات AMD <<<
        elif target_brand == 'AMD':
            if final_tier == 'Low':
                self.declare(SelectedCPU(tier='Low', brand='AMD', model='Ryzen 3 4100', socket='AM4'))
            elif final_tier == 'Medium':
                self.declare(SelectedCPU(tier='Medium', brand='AMD', model='Ryzen 5 5600', socket='AM4'))
            elif final_tier == 'High':
                self.declare(SelectedCPU(tier='High', brand='AMD', model='Ryzen 7 7700X', socket='AM5'))
            elif final_tier == 'Ultra':
                self.declare(SelectedCPU(tier='Ultra', brand='AMD', model='Ryzen 9 7950X', socket='AM5'))
                