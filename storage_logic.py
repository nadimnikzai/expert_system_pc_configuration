from experta import Rule, MATCH, KnowledgeEngine
from facts import UserInput, BudgetConstraints, SelectedStorage

class StorageRules(KnowledgeEngine):
    
    @Rule(
        UserInput(usage=MATCH.task, storage_pref=MATCH.user_store), # کاربری + انتخاب دستی
        BudgetConstraints(budget_tier=MATCH.tier)                   # سطح بودجه
    )
    def select_storage_30rows(self, task, user_store, tier):
        
        # متغیرهای موقت جدول
        table_cap = ""
        table_model = ""
        table_tech = ""
        
        # ============================================================
        # منطق دقیق ۳۰ ردیف جدول حافظه (Image d40e88)
        # ============================================================

        # --- Tier: Very Low ---
        if tier == "Very Low":
            if task == "Office":
                table_cap, table_model, table_tech = "256 GB", "Lexar NQ100 SATA", "SATA SSD"
            elif task == "Economic":
                table_cap, table_model, table_tech = "256 GB", "PNY CS900 SATA", "SATA SSD"
            elif task == "Trading":
                table_cap, table_model, table_tech = "256 GB", "Crucial BX500 SATA", "SATA SSD"
            elif task == "Engineering":
                table_cap, table_model, table_tech = "256 GB", "Kingston A400 SATA", "SATA SSD"
            elif task == "Gaming":
                table_cap, table_model, table_tech = "512 GB", "ADATA SU650 SATA", "SATA SSD"
            elif task == "Rendering":
                table_cap, table_model, table_tech = "512 GB", "Silicon Power A55 SATA", "SATA SSD"

        # --- Tier: Entry ---
        elif tier == "Entry":
            if task == "Office":
                table_cap, table_model, table_tech = "512 GB", "WD Green SATA SSD", "SATA SSD"
            elif task == "Economic":
                table_cap, table_model, table_tech = "512 GB", "Lexar NM620 (Gen3)", "NVMe Gen3"
            elif task == "Trading":
                table_cap, table_model, table_tech = "512 GB", "Crucial P3 (Gen3)", "NVMe Gen3"
            elif task == "Engineering":
                table_cap, table_model, table_tech = "512 GB", "Samsung 980 (Gen3)", "NVMe Gen3"
            elif task == "Gaming":
                table_cap, table_model, table_tech = "512 GB", "Biwin Black Opal NV7400", "NVMe Gen4"
            elif task == "Rendering":
                table_cap, table_model, table_tech = "512 GB", "Orico O7000 (Budget Gen4)", "NVMe Gen4"

        # --- Tier: Mid ---
        elif tier == "Mid":
            if task == "Office":
                table_cap, table_model, table_tech = "512 GB", "Samsung 870 EVO", "SATA SSD"
            elif task == "Economic":
                table_cap, table_model, table_tech = "512 GB", "Crucial P3 Plus", "NVMe Gen4"
            elif task == "Trading":
                table_cap, table_model, table_tech = "1 TB", "WD Blue SN580", "NVMe Gen4"
            elif task == "Engineering":
                table_cap, table_model, table_tech = "1 TB", "Samsung 990 EVO Plus", "NVMe Gen4"
            elif task == "Gaming":
                table_cap, table_model, table_tech = "1 TB", "WD Black SN770", "NVMe Gen4"
            elif task == "Rendering":
                table_cap, table_model, table_tech = "1 TB", "Crucial T500 (Pro)", "NVMe Gen4"

        # --- Tier: High ---
        elif tier == "High":
            if task == "Office":
                table_cap, table_model, table_tech = "1 TB", "Kingston FURY Renegade", "NVMe Gen4"
            elif task == "Economic":
                table_cap, table_model, table_tech = "1 TB", "Acer Predator GM7000", "NVMe Gen4"
            elif task == "Trading":
                table_cap, table_model, table_tech = "1 TB", "Samsung 990 Pro", "NVMe Gen4"
            elif task == "Engineering":
                table_cap, table_model, table_tech = "2 TB", "WD Black SN850X", "NVMe Gen4"
            elif task == "Gaming":
                table_cap, table_model, table_tech = "2 TB", "Lexar NM790", "NVMe Gen4"
            elif task == "Rendering":
                table_cap, table_model, table_tech = "2 TB", "TeamGroup MP44", "NVMe Gen4"

        # --- Tier: Enthusiast ---
        elif tier == "Enthusiast":
            if task == "Office":
                table_cap, table_model, table_tech = "1 TB", "Addlink AddGame A93", "NVMe Gen4"
            elif task == "Economic":
                table_cap, table_model, table_tech = "2 TB", "Samsung 870 QVO", "SATA SSD (High Cap)"
            elif task == "Trading":
                table_cap, table_model, table_tech = "2 TB", "Crucial T700 (Gen5)", "NVMe Gen5"
            elif task == "Engineering":
                table_cap, table_model, table_tech = "4 TB", "Samsung 990 Pro", "NVMe Gen4"
            elif task == "Gaming":
                table_cap, table_model, table_tech = "4 TB", "WD Black SN850X", "NVMe Gen4"
            elif task == "Rendering":
                table_cap, table_model, table_tech = "4 TB", "Crucial T705 (Extreme)", "NVMe Gen5"

        # توری ایمنی (اگر چیزی پیدا نشد)
        if table_cap == "":
            table_cap = "500 GB"
            table_model = "Generic SSD"
            table_tech = "SATA/NVMe"

        # ============================================================
        # اعمال انتخاب کاربر (User Override)
        # ============================================================
        
        final_cap = table_cap
        final_model = table_model
        final_tech = table_tech
        
        # اگر کاربر چیزی غیر از Auto انتخاب کرده باشد
        if user_store != "Auto" and user_store != "":
            final_cap = user_store
            # تکنولوژی را حفظ می‌کنیم تا با بودجه بخواند، اما مدل را جنریک می‌کنیم
            final_model = f"Custom Selection ({final_tech})"

        self.declare(SelectedStorage(
            capacity=final_cap,
            model=final_model,
            type=final_tech
        ))