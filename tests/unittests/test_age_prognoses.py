import covasim as cv
import json
import unittest


class AgePrognosesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.is_debugging = False
        self.parameters = cv.make_pars()
        self.pop_size = 1000
        self.pop_infected = 10
        self.parameters['pop_size'] = self.pop_size
        self.parameters['pop_infected'] = self.pop_infected
        self.number_iterations = 5
        self.sim = None
        self.numerator_channel = None
        self.denominator_channel = None
        pass

    def tearDown(self) -> None:
        self.sim = None
        pass

    def initialize_sim_ages_to(self, age):
        self.sim = cv.Sim(pars=self.parameters)
        self.sim.initialize()
        self.sim.people['age'][:] = age
        self.sim.people.set_prognoses()

    def collect_sim_results(self, seed=1):
        self.parameters['rand_seed'] = seed
        self.sim.run(verbose=0)
        sim_result = self.sim.to_json(tostring=False)['results']
        numerator = sim_result[self.numerator_channel][-1]
        denominator = sim_result[self.denominator_channel][-1]
        return numerator, denominator

    def set_symptomatic_test(self):
        self.numerator_channel = 'cum_symptomatic'
        self.denominator_channel = 'cum_infections'
        self.prognosis_name = 'symp_probs'
        pass

    def get_min_max_prognoses(self, min_age_bucket):
        min_prognosis = self.sim['prognoses'][self.prognosis_name][min_age_bucket]
        max_prognosis = self.sim['prognoses'][self.prognosis_name][min_age_bucket + 1]
        return min_prognosis, max_prognosis

    def evaluate_results(self, total_numerator, total_denominator,
                         lower_age_bucket):
        average_numerator = total_numerator / self.number_iterations
        average_denominator = total_denominator / self.number_iterations

        younger_prognosis, older_prognosis = self.get_min_max_prognoses(lower_age_bucket)

        expected_numerator_min = younger_prognosis * average_denominator
        expected_numerator_max = older_prognosis * average_denominator
        if self.is_debugging:
            with open(f"DEBUG_{self.id()}.json", "w") as outfile:
                json.dump(self.sim.to_json(tostring=False), outfile, indent=4)
            print(f"Total numerator: {total_numerator} Total denominator: {total_denominator}")
            print(f"Average numerator: {average_numerator} Average denominator: {average_denominator}")
            print(f"Younger prognosis {younger_prognosis} means expected minimum numerator {expected_numerator_min}")
            print(f"Older prognosis {older_prognosis} means expected maximum numerator {expected_numerator_max}")
        assert average_numerator > expected_numerator_min, \
            f"Average numerator {average_numerator} should be higher than expected min {expected_numerator_min}"
        assert average_numerator < expected_numerator_max, \
            f"Average numerator {average_numerator} should be lower than expected max {expected_numerator_max}"
        pass

    def run_symptomatic_test_by_age(self, age_under_test):
        self.set_symptomatic_test()
        total_numerator = 0
        total_denominator = 0
        for seed in range(0, self.number_iterations):
            self.initialize_sim_ages_to(age_under_test)
            numerator, denominator = self.collect_sim_results(seed=seed)
            total_numerator += numerator
            total_denominator += denominator
            pass
        return total_numerator, total_denominator

    @unittest.skip("Not working right now, needs more flexible verification")
    def test_symptomatic_age15(self):
        self.is_debugging = True
        age_under_test = 15
        lower_age_bucket = 0
        self.number_iterations = 10
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age25(self):
        self.is_debugging = False
        age_under_test = 25
        lower_age_bucket = 1
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age35(self):
        self.is_debugging = False
        age_under_test = 35
        lower_age_bucket = 2
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age45(self):
        self.is_debugging = False
        age_under_test = 45
        lower_age_bucket = 3
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age55(self):
        self.is_debugging = False
        age_under_test = 55
        lower_age_bucket = 4
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age65(self):
        self.is_debugging = False
        age_under_test = 65
        lower_age_bucket = 5
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age75(self):
        self.is_debugging = False
        age_under_test = 75
        lower_age_bucket = 6
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)

    def test_symptomatic_age85(self):
        self.is_debugging = False
        age_under_test = 85
        lower_age_bucket = 7
        total_numerator, total_denominator = \
            self.run_symptomatic_test_by_age(age_under_test=age_under_test)
        self.evaluate_results(total_numerator=total_numerator,
                              total_denominator=total_denominator,
                              lower_age_bucket=lower_age_bucket)
