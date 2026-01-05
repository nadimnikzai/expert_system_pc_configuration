from experta import Rule, KnowledgeEngine
from facts import UserInput, BaseRequirements

class UsageRules(KnowledgeEngine):
    
    # --- R1: Gaming ---
    @Rule(UserInput(usage='Gaming'))
    def r1_gaming(self):
        # طبق جدول: T, Med, Med, 16, 1TB
        self.declare(BaseRequirements(
            gpu_required='True',
            min_gpu_tier='Medium',
            cpu_importance='Medium',
            ram_base_requirement=16,
            storage_base='1 TB'
        ))

    # --- R2: Office ---
    @Rule(UserInput(usage='Office'))
    def r2_office(self):
        # طبق جدول: F, None, Low, 8, 256GB
        self.declare(BaseRequirements(
            gpu_required='False',
            min_gpu_tier='None',
            cpu_importance='Low',
            ram_base_requirement=8,
            storage_base='256 GB'
        ))

    # --- R3: Economic ---
    @Rule(UserInput(usage='Economic'))
    def r3_economic(self):
        # طبق جدول: F, None, Low, 8, 256GB
        self.declare(BaseRequirements(
            gpu_required='False',
            min_gpu_tier='None',
            cpu_importance='Low',
            ram_base_requirement=8,
            storage_base='256 GB'
        ))

    # --- R4: Engineering ---
    @Rule(UserInput(usage='Engineering'))
    def r4_engineering(self):
        # طبق جدول: Opt, Low, High, 16, 512GB
        self.declare(BaseRequirements(
            gpu_required='Optional', 
            min_gpu_tier='Low',
            cpu_importance='High',
            ram_base_requirement=16,
            storage_base='512 GB'
        ))

    # --- R5: Rendering ---
    @Rule(UserInput(usage='Rendering'))
    def r5_rendering(self):
        # طبق جدول: T, High, High, 32, 1TB
        self.declare(BaseRequirements(
            gpu_required='True',
            min_gpu_tier='High',
            cpu_importance='High',
            ram_base_requirement=32,
            storage_base='1 TB'
        ))

    # --- R6: Trading ---
    @Rule(UserInput(usage='Trading'))
    def r6_trading(self):
        # طبق جدول: F, None, High, 16, 512GB
        self.declare(BaseRequirements(
            gpu_required='False',
            min_gpu_tier='None',
            cpu_importance='High',
            ram_base_requirement=16,
            storage_base='512 GB'
        ))