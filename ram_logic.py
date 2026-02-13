from experta import Rule, MATCH, KnowledgeEngine
from facts import UserInput, BudgetConstraints, SelectedRAM

class RamRules(KnowledgeEngine):
    
    @Rule(
        UserInput(usage=MATCH.task, ram_pref=MATCH.user_ram), # دریافت ورودی کاربر
        BudgetConstraints(budget_tier=MATCH.tier)             # دریافت سطح بودجه
    )
    def select_ram_strict_30rows(self, task, user_ram, tier):
        
        # متغیرهای موقت برای نگهداری مقادیر جدول
        table_cap = 0
        table_speed = ""
        table_reason = ""

        # ============================================================
        # بررسی دقیق ۳۰ ردیف جدول (بدون کم و کاست)
        # ============================================================
        
        # --- دسته ۱: Very Low (ردیف ۱ تا ۶) ---
        if tier == "Low":
            if task == "Office":          
                table_cap, table_speed, table_reason = 8, "DDR4 3200MHz", "حداقل استاندارد اداری"
            elif task == "Economic":      
                table_cap, table_speed, table_reason = 8, "DDR4 3200MHz", "بودجه محدود"
            elif task == "Trading":       
                table_cap, table_speed, table_reason = 8, "DDR4 3200MHz", "کافی برای ترید سبک"
            elif task == "Engineering":   
                table_cap, table_speed, table_reason = 16, "DDR4 3200MHz", "نیاز پایه مهندسی"
            elif task == "Gaming":        
                table_cap, table_speed, table_reason = 16, "DDR4 3200MHz", "حداقل رم گیمینگ"
            elif task == "Rendering":     
                table_cap, table_speed, table_reason = 16, "DDR4 3200MHz", "حداقل برای شروع رندر"

        # --- دسته ۲: Entry (ردیف ۷ تا ۱۲) ---
        elif tier == "Entry":
            if task == "Office":          
                table_cap, table_speed, table_reason = 16, "DDR4 3200MHz", "سرعت بالا در مالتی‌تسک"
            elif task == "Economic":      
                table_cap, table_speed, table_reason = 16, "DDR4 3200MHz", "استاندارد سیستم خانگی"
            elif task == "Trading":       
                table_cap, table_speed, table_reason = 16, "DDR4 3200MHz", "استاندارد ترید"
            elif task == "Engineering":   
                table_cap, table_speed, table_reason = 16, "DDR4 3600MHz", "سرعت بالاتر برای محاسبات"
            elif task == "Gaming":        
                table_cap, table_speed, table_reason = 16, "DDR4 3600MHz", "استاندارد گیمینگ اقتصادی"
            elif task == "Rendering":     
                table_cap, table_speed, table_reason = 32, "DDR4 3200MHz", "ارتقای حجم برای رندر"

        # --- دسته ۳: Mid (ردیف ۱۳ تا ۱۸) ---
        elif tier == "Mid":
            if task == "Office":          
                table_cap, table_speed, table_reason = 16, "DDR5 4800MHz", "ورود به نسل جدید"
            elif task == "Economic":      
                table_cap, table_speed, table_reason = 16, "DDR5 5200MHz", "سرعت و پهنای باند بالا"
            elif task == "Trading":       
                table_cap, table_speed, table_reason = 32, "DDR5 5200MHz", "حجم بالا برای چارت‌ها"
            elif task == "Engineering":   
                table_cap, table_speed, table_reason = 32, "DDR5 5600MHz", "استاندارد مهندسی حرفه‌ای"
            elif task == "Gaming":        
                table_cap, table_speed, table_reason = 32, "DDR5 6000MHz", "رم مناسب گیمینگ"
            elif task == "Rendering":     
                table_cap, table_speed, table_reason = 32, "DDR5 6000MHz", "سرعت بالا برای پردازش"

        # --- دسته ۴: High (ردیف ۱۹ تا ۲۴) ---
        elif tier == "High":
            if task == "Office":          
                table_cap, table_speed, table_reason = 32, "DDR5 5200MHz", "سیستم اداری قدرتمند"
            elif task == "Economic":      
                table_cap, table_speed, table_reason = 32, "DDR5 5600MHz", "آینده‌نگرانه"
            elif task == "Trading":       
                table_cap, table_speed, table_reason = 64, "DDR5 5600MHz", "بدون لگ در چارت‌ها"
            elif task == "Engineering":   
                table_cap, table_speed, table_reason = 64, "DDR5 6000MHz", "شبیه‌سازی‌های سنگین"
            elif task == "Gaming":        
                table_cap, table_speed, table_reason = 32, "DDR5 6400MHz", "تمرکز روی سرعت"
            elif task == "Rendering":     
                table_cap, table_speed, table_reason = 64, "DDR5 6000MHz", "حجم بالا برای صحنه‌ها"

        # --- دسته ۵: Enthusiast (ردیف ۲۵ تا ۳۰) ---
        elif tier == "Enthusiast":
            if task == "Office":          
                table_cap, table_speed, table_reason = 64, "DDR5 5600MHz", "لوکس"
            elif task == "Economic":      
                table_cap, table_speed, table_reason = 64, "DDR5 6000MHz", "لوکس"
            elif task == "Trading":       
                table_cap, table_speed, table_reason = 128, "DDR5 6000MHz", "ورک‌استیشن ترید"
            elif task == "Engineering":   
                table_cap, table_speed, table_reason = 128, "DDR5 6400MHz", "ورک‌استیشن صنعتی"
            elif task == "Gaming":        
                table_cap, table_speed, table_reason = 64, "DDR5 7200MHz+", "نهایت سرعت و حجم"
            elif task == "Rendering":     
                table_cap, table_speed, table_reason = 128, "DDR5 6400MHz", "ورک‌استیشن رندر"
        
            
        # ============================================================
        # اعمال منطق ورودی کاربر (User Override) - بخش مهم
        # ============================================================
        
        final_cap = table_cap
        final_speed = table_speed
        final_reason = table_reason

        # شرط اصلی: اگر کاربر عددی بزرگتر از 0 وارد کرده بود، حجم تغییر کند
        # اما سرعت (DDR4/DDR5) دست نخورد (چون وابسته به مادربرد است)
        if user_ram > 0:
            final_cap = user_ram
            final_reason = f"انتخاب کاربر ({table_reason})"

        
        # تعیین نام مدل
        model_name = "Generic RAM"
        if "DDR4" in final_speed:
            model_name = "Corsair Vengeance LPX / G.Skill Ripjaws"
        elif "DDR5" in final_speed:
            model_name = "G.Skill Trident Z5 / Corsair Vengeance"

        # ثبت نهایی
        self.declare(SelectedRAM(
            capacity=final_cap,
            speed=final_speed,
            model=f"{model_name} ({final_reason})"
        ))