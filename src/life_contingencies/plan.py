from life_contingencies.level_benefits import life_annuity_due
from life_contingencies import mortality

mort_table = mortality.load_mortality_table(
    r'C:\Proyectos\life-contingencies-python\data\mortality\1980_cso_male.csv'
)
life_table = mortality.build_life_table(mort_table)
commutation_table = mortality.build_commutation_table(life_table, 0.04)

class Plan():
    def __init__(
        self,
        benefit_value,
        issue_age,
        deferral_period, 
        coverage_period
    ):
        self.benefit_value = benefit_value
        self.issue_age = issue_age
        self.deferral_period = deferral_period
        self.coverage_period = coverage_period


    def net_single_premium(self):
        return self.benefit_value


    def level_annual_net_premium(self):
        premium_annuity_value = life_annuity_due(
            current_age=self.issue_age,
            payment_term=None,
            deferral_period=0,
            commutation_table=commutation_table,
        )
        net_single_premium = self.net_single_premium()

        return  net_single_premium / premium_annuity_value


    def limited_payment_net_premium(self, premium_payment_term):
        premium_annuity_value = life_annuity_due(
            current_age=self.issue_age,
            payment_term=premium_payment_term,
            deferral_period=0,
            commutation_table=commutation_table,
        )
        net_single_premium = self.net_single_premium()

        return  net_single_premium / premium_annuity_value
