import covasim as cv
import json
import pytest


def set_all_ages_to(simulation : cv.Sim, age_in_years):
    simulation.initialize()
    simulation.people['age'][:] = age_in_years
    simulation.people.set_prognoses()
    return simulation

def set_prognosis_under_test(simulation : cv.Sim, prognosis):
    numerator_channel = None
    denominator_channel = None
    prognosis_name = None
    if prognosis == 'symptomatic':
        numerator_channel = 'cum_symptomatic'
        denominator_channel = 'cum_infections'
        prognosis_name = 'symp_probs'
    elif prognosis == 'severe':
        simulation['prognoses']['symp_probs'][:] = 1.0
        numerator_channel = 'cum_severe'
        denominator_channel = 'cum_symptomatic'
        prognosis_name = 'severe_probs'
    else:
        raise ValueError(f"Need prognosis in [symptomatic, severe] but got: {prognosis}")
    return numerator_channel, denominator_channel, prognosis_name
    pass

def test_25_bucket_symptomatic_prognosis():
    debug = False
    population_count = 1010
    parameters = cv.make_pars()
    parameters['pop_size'] = population_count
    parameters['pop_infected'] = 10
    number_iterations = 10
    total_denominator = 0
    total_numerator = 0
    simulation_result = None
    for seed in range(number_iterations):
        parameters['rand_seed'] = seed
        fixed_age_sim = cv.Sim(pars=parameters, load_pop=True)
        numerator_channel, denominator_channel, prognosis_name = set_prognosis_under_test(
            simulation=fixed_age_sim,
            prognosis='symptomatic'
        )
        fixed_age_sim = set_all_ages_to(fixed_age_sim, 25)
        fixed_age_sim.run(verbose=0)
        simulation_result = fixed_age_sim.to_json(tostring=False)
        total_denominator += simulation_result['results'][denominator_channel][-1]
        total_numerator += simulation_result['results'][numerator_channel][-1]
        pass
    if debug:
        with open('DEBUG_sim_25_bucket_symptomatic_prognosis.json', 'w') as outfile:
            json.dump(simulation_result, outfile, indent=4, sort_keys=True)
    evaluate_ratio(fixed_age_sim, total_numerator, total_denominator,
                   prognosis_name, min_bucket_index=1, number_iterations=number_iterations,
                   debug=debug)

    # average_cumulative_symptomatic = sum(results.values()) / (seed + 1)

# def test_35_bucket_symptomatic_prognosis():
#     debug = True
#     population_count = 1010
#     parameters = cv.make_pars()
#     parameters['pop_size'] = population_count
#     parameters['pop_infected'] = 10
#     number_iterations = 10
#     total_denominator = 0
#     total_numerator = 0
#     simulation_result = None
#     for seed in range(number_iterations):
#         parameters['rand_seed'] = seed
#         fixed_age_sim = cv.Sim(pars=parameters, load_pop=True)
#         numerator_channel, denominator_channel, prognosis_name = set_prognosis_under_test(
#             simulation=fixed_age_sim,
#             prognosis='symptomatic'
#         )
#         fixed_age_sim = set_all_ages_to(fixed_age_sim, 35)
#         fixed_age_sim.run(verbose=0)
#         simulation_result = fixed_age_sim.to_json(tostring=False)
#         total_denominator += simulation_result['results'][denominator_channel][-1]
#         total_numerator += simulation_result['results'][numerator_channel][-1]
#         pass
#
#     if debug:
#         with open('DEBUG_sim_25_bucket_symptomatic_prognosis.json', 'w') as outfile:
#             json.dump(simulation_result, outfile, indent=4, sort_keys=True)
#
#     evaluate_ratio(fixed_age_sim, total_numerator, total_denominator,
#                    prognosis_name, min_bucket_index=1, number_iterations=number_iterations,
#                    debug=debug)

def evaluate_ratio(fixed_age_sim, total_numerator, total_denominator,
                   prognosis_name,  min_bucket_index=2, number_iterations=1,
                   debug=False):
    average_denominator = total_denominator/(number_iterations + 1)
    average_numerator = total_numerator/(number_iterations + 1)

    symptomatic_prognoses_by_age = fixed_age_sim['prognoses'][prognosis_name]
    expected_cumulative_numerator_min = average_denominator * symptomatic_prognoses_by_age[min_bucket_index]
    expected_cumulative_numerator_max = average_denominator * symptomatic_prognoses_by_age[min_bucket_index + 1]
    if debug:
        with open("DEBUG_test_25_bucket_symptomatic_prognosis.txt",'w') as outfile:
            outfile.write(f"For a ratio of: {total_denominator / total_numerator}")
            outfile.write(f"Average number of symptomatics: {average_numerator}")
            outfile.write(f"Expected min: {expected_cumulative_numerator_min}")
            outfile.write(f"Expected_max: {expected_cumulative_numerator_max}")
    assert average_numerator > expected_cumulative_numerator_min,\
        f"Expected more than the 20 year age bucket: {expected_cumulative_numerator_min}"
    assert average_numerator < expected_cumulative_numerator_max, \
        f"Expected less than the 30 year age bucket: {expected_cumulative_numerator_max}"

test_25_bucket_symptomatic_prognosis()