from experta import Rule, MATCH, KnowledgeEngine
from facts import UserInput, BudgetConstraints, SelectedCPU, SelectedMotherboard, SelectedCase

class MotherboardCaseRules(KnowledgeEngine):
    
    @Rule(
        UserInput(case_size=MATCH.size_pref),      # سایز دلخواه کاربر (Small, Mid, Large)
        SelectedCPU(socket=MATCH.sock),            # سوکت پردازنده (LGA1700, AM4, AM5)
        BudgetConstraints(budget_tier=MATCH.tier)  # سطح بودجه (Entry, Mid, High...)
    )
    def select_mb_and_case(self, size_pref, sock, tier):
        
        # متغیرهای موقت
        case_name = ""
        case_type = ""
        mb_name = ""
        mb_chipset = ""
        mb_size = ""

        # ====================================================
        # سناریو ۱: کیس کوچک (Small / Mini-ITX)
        # ====================================================
        if size_pref == 'Small':
            case_name = "Cooler Master NR200P"
            case_type = "Mini-ITX Case"
            mb_size = "Mini-ITX"

            # انتخاب مادربورد کوچک بر اساس سوکت
            if sock == "LGA1700": # Intel
                mb_name = "ASUS ROG STRIX B760-I GAMING"
                mb_chipset = "B760"
            elif sock == "AM4":   # AMD Old
                mb_name = "Gigabyte A520I AC"
                mb_chipset = "A520"
            elif sock == "AM5":   # AMD New
                mb_name = "MSI MPG B650I EDGE WIFI"
                mb_chipset = "B650"

        # ====================================================
        # سناریو ۲: کیس متوسط (Mid Tower) - استانداردترین حالت
        # ====================================================
        elif size_pref == 'Mid':
            # انتخاب کیس بر اساس بودجه
            if tier in ['Low', 'Entry']:
                case_name = "DeepCool CC560"
                case_type = "Mid Tower (Economic)"
            else:
                case_name = "Corsair 4000D Airflow"
                case_type = "Mid Tower (Premium)"
            
            mb_size = "ATX / mATX"

            # >>> انتخاب مادربورد بر اساس بودجه و سوکت <<<
            
            # --- اینتل (Intel LGA1700) ---
            if sock == "LGA1700":
                if tier in ['Low', 'Entry']:
                    mb_name = "ASUS PRIME H610M-K"
                    mb_chipset = "H610"
                elif tier == 'Mid':
                    mb_name = "ASUS PRIME B760-PLUS"
                    mb_chipset = "B760"
                elif tier in ['High', 'Enthusiast']:
                    mb_name = "ASUS TUF GAMING Z790-PLUS"
                    mb_chipset = "Z790"

            # --- ای‌ام‌دی قدیمی (AMD AM4) ---
            elif sock == "AM4":
                if tier in ['Low', 'Entry']:
                    mb_name = "ASUS Prime A520M-E"
                    mb_chipset = "A520"
                else:
                    mb_name = "ASUS TUF GAMING B550-PLUS"
                    mb_chipset = "B550"

            # --- ای‌ام‌دی جدید (AMD AM5) ---
            elif sock == "AM5":
                if tier in ['Low', 'Entry', 'Mid']:
                    mb_name = "MSI PRO B650-P WIFI"
                    mb_chipset = "B650"
                else:
                    mb_name = "ASUS ROG STRIX X670E-F"
                    mb_chipset = "X670E"

        # ====================================================
        # سناریو ۳: کیس بزرگ (Large / Full Tower)
        # ===================================================
        elif size_pref == 'Large':
            case_name = "Lian Li O11 Dynamic XL"
            case_type = "Full Tower"
            mb_size = "ATX"

            # معمولاً کسی که کیس بزرگ میبنده، مادربورد حرفه‌ای میخواد
            if sock == "LGA1700":
                mb_name = "ASUS ROG MAXIMUS Z790 HERO"
                mb_chipset = "Z790"
            elif sock == "AM5":
                mb_name = "ASUS ROG CROSSHAIR X670E HERO"
                mb_chipset = "X670E"
            elif sock == "AM4": # بعیده ولی محض احتیاط
                mb_name = "ASUS ROG Crosshair VIII Dark Hero"
                mb_chipset = "X570"

        # ====================================================
        # ثبت نهایی (Declare)
        # ====================================================
        self.declare(SelectedCase(
            model=case_name,
            form_factor=case_type
        ))
        
        self.declare(SelectedMotherboard(
            model=mb_name,
            chipset=mb_chipset,
            size=mb_size
        ))