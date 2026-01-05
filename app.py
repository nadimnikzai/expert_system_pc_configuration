from flask import Flask, render_template, request
from facts import UserInput, BaseRequirements, BudgetConstraints, SelectedCPU, SelectedGPU, SelectedMotherboard, SelectedCase
# ایمپورت کردن فایل جداگانه Usage
from usage_logic import UsageRules
from budget_logic import BudgetRules
from cpu_logic import CPURules
from gpu_logic import GPURules
from mb_case_logic import MotherboardCaseRules

app = Flask(__name__)

# فعلاً فقط UsageRules را به ارث می‌بریم
class ExpertSystemEngine(UsageRules, BudgetRules, CPURules, GPURules, MotherboardCaseRules):
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    budget_result = None
    cpu_result = None
    gpu_result = None
    mb_result = None   
    case_result = None
    flag_usage= False
    
    if request.method == 'POST':
        # دریافت ورودی از فرم
        u_usage = request.form.get('usage')
        u_budget_str = request.form.get('budget')
        try:
            u_budget = int(u_budget_str)
        except ValueError:
            u_budget = 0 # اگر عدد نبود

        u_cpu_pref = request.form.get('cpu_pref')
        u_gpu_pref = request.form.get('gpu_pref')
        u_case_size = request.form.get('case_size') # دریافت سایز کیس
        
        if u_usage and u_budget and u_cpu_pref and u_gpu_pref and u_case_size:

            engine = ExpertSystemEngine()
            engine.reset()
            # داده‌ها را به سیستم می‌دهیم (بقیه فعلاً خالی هستند)
            engine.declare(UserInput(
                usage=u_usage,
                budget=u_budget, cpu_pref=u_cpu_pref, gpu_pref=u_gpu_pref, case_size=u_case_size, ram_pref="", storage_pref=""
            ))
            engine.run()
            
            # جستجو برای پیدا کردن نتیجه جدول اول
            for fact in engine.facts.values():
                if isinstance(fact, BaseRequirements):
                    result = fact
                if isinstance(fact, BudgetConstraints):
                    budget_result = fact
                if isinstance(fact, SelectedCPU):
                    cpu_result = fact
                if isinstance(fact, SelectedGPU):
                    gpu_result = fact
                if isinstance(fact, SelectedMotherboard):
                    mb_result = fact
                if isinstance(fact, SelectedCase):
                    case_result = fact
                    
                

    return render_template('index.html', result=result, budget_result=budget_result, cpu_result=cpu_result, gpu_result=gpu_result, mb_result=mb_result, case_result=case_result)

if __name__ == '__main__':
    app.run(debug=True)