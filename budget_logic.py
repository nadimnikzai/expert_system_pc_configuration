from experta import Rule, MATCH, KnowledgeEngine
from facts import UserInput, BudgetConstraints

class BudgetRules(KnowledgeEngine):
    
    # قانون بررسی بودجه (عدد را از ورودی می‌گیرد)
    @Rule(UserInput(budget=MATCH.b))
    def check_budget(self, b):
        money = b
        # تبدیل ورودی به عدد (جهت اطمینان)
        # try:
        #     money = int(b)
        # except:
        #     return # اگر عدد نبود کاری نکن

        # --- بازه ۱: کمتر از ۴۰ میلیون (R1) ---
        if 20 <=money < 40:
            self.declare(BudgetConstraints(
                budget_tier='Low',
                max_gpu_tier='Low',
                max_cpu_tier='Low',
                ram_limit=8,
                storage_limit='256 GB'
            ))
             # اینجا اگر در عکس چیزی تعریف شده بنویس، وگرنه معمولا ارور میدیم
            

        # --- بازه ۲: بین ۴۰ تا ۶۰ میلیون (R2 - Entry) ---
        elif 40 <= money < 60:
            self.declare(BudgetConstraints(
                budget_tier='Entry',
                max_gpu_tier='Medium',
                max_cpu_tier='Medium',
                ram_limit=16,
                storage_limit='512 GB'
            ))

        # --- بازه ۳: بین ۶۰ تا ۹۰ میلیون (R3 - Mid) ---
        elif 60 <= money < 90:
            self.declare(BudgetConstraints(
                budget_tier='Mid',
                max_gpu_tier='Medium', # یا High بسته به عکس
                max_cpu_tier='High',
                ram_limit=32,
                storage_limit='1 TB'
            ))

        # --- بازه ۴: بین ۹۰ تا ۱۵۰ میلیون (R4 - High) ---
        elif 90 <= money < 150:
            self.declare(BudgetConstraints(
                budget_tier='High',
                max_gpu_tier='High',
                max_cpu_tier='High',
                ram_limit=64,
                storage_limit='2 TB'
            ))

        # --- بازه ۵: بالای ۱۵۰ میلیون (R5 - Enthusiast) ---
        elif money >= 150:
            self.declare(BudgetConstraints(
                budget_tier='Enthusiast',
                max_gpu_tier='Ultra',
                max_cpu_tier='Ultra',
                ram_limit=128,
                storage_limit='4 TB'
            ))