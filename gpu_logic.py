from experta import Rule, MATCH, KnowledgeEngine
from facts import UserInput, BaseRequirements, BudgetConstraints, SelectedGPU

class GPURules(KnowledgeEngine):
    
    @Rule(
        UserInput(gpu_pref=MATCH.brand_pref),             # انتخاب کاربر (Nvidia/AMD)
        BaseRequirements(min_gpu_tier=MATCH.min_tier),    # حداقل نیاز (Low, Medium, High, None)
        BudgetConstraints(max_gpu_tier=MATCH.max_tier)    # سقف بودجه (Low, Medium, High, Ultra)
    )
    def select_gpu_logic_table(self, brand_pref, min_tier, max_tier):
        
        # =========================================================
        # مرحله ۱: تعیین رده نهایی (Final Tier) - طبق سمت چپ جدول
        # =========================================================
        final_tier = "Unknown"

        # --- ردیف ۱: وقتی نیاز None است (Office/Trading) ---
        if min_tier == 'None':
            final_tier = 'Integrated'

        # --- ردیف ۲: وقتی نیاز Low است ---
        elif min_tier == 'Low':
            # طبق جدول: هر بودجه‌ای باشد، نتیجه Low است
            final_tier = 'Low'

        # --- ردیف ۳ و ۴: وقتی نیاز Medium است ---
        elif min_tier == 'Medium':
            if max_tier == 'Low':
                # بودجه کمه -> افت به Low (محدودیت بودجه)
                final_tier = 'Low'
            else:
                # بودجه Medium یا High یا Ultra -> همون Medium
                final_tier = 'Medium'

        # --- ردیف ۵ و ۶: وقتی نیاز High است ---
        elif min_tier == 'High':
            if max_tier in ['Low', 'Medium']:
                # بودجه کمه -> افت به Medium (محدودیت بودجه)
                final_tier = 'Medium'
            else:
                # بودجه High یا Ultra -> همون High (یا Ultra اگه بودجه برسه)
                if max_tier == 'Ultra':
                    final_tier = 'Ultra'
                else:
                    final_tier = 'High'

        # =========================================================
        # مرحله ۲: انتخاب سخت‌افزار (Hardware Mapping) - طبق سمت راست جدول
        # =========================================================
        
        selected_brand = brand_pref
        if selected_brand == 'Auto' or selected_brand == '':
            selected_brand = 'Nvidia' # طبق ستون "پیشنهاد سیستم"

        final_model = ""

        # --- حالت Integrated ---
        if final_tier == 'Integrated':
            final_model = "Integrated Graphics (Onboard)"
            selected_brand = "Integrated"

        # --- حالت Low ---
        elif final_tier == 'Low':
            if selected_brand == 'AMD':
                final_model = "RX 6500 XT"
            else: # Nvidia or Auto
                final_model = "GTX 1650"

        # --- حالت Medium ---
        elif final_tier == 'Medium':
            if selected_brand == 'AMD':
                final_model = "RX 7600"
            else: # Nvidia or Auto
                final_model = "RTX 4060"

        # --- حالت High ---
        elif final_tier == 'High':
            if selected_brand == 'AMD':
                final_model = "RX 7800 XT"
            else: # Nvidia or Auto
                final_model = "RTX 4070 Super"

        # --- حالت Ultra ---
        elif final_tier == 'Ultra':
            if selected_brand == 'AMD':
                final_model = "RX 7900 XTX"
            else: # Nvidia or Auto
                final_model = "RTX 4090 / 4080 Super"

        # ثبت نهایی
        self.declare(SelectedGPU(
            tier=final_tier,
            brand=selected_brand,
            model=final_model
        ))