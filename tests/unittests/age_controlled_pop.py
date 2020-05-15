import covasim as cv
import json

debug = True
victim_count = 1000
parameters = cv.make_pars()
parameters['pop_size'] = victim_count
parameters['pop_infected'] = 10
results = {}
for seed in range(10):
    parameters['rand_seed'] = seed
    fixed_age_sim = cv.Sim(pars=parameters, load_pop=True)
    fixed_age_sim.initialize()
    fixed_age_sim.people['age'][:] = 25
    fixed_age_sim.people.set_prognoses()
    fixed_age_sim.run(verbose=0)
    simulation_result = fixed_age_sim.to_json(tostring=False)
    result = {}
    result['infections'] = simulation_result['results']['cum_infections'][-1]
    result['symptomatics'] = simulation_result['results']['cum_symptomatic'][-1]
    result['ratio'] = result['symptomatics'] / result['infections']
    results[seed] = result

# average_cumulative_symptomatic = sum(results.values()) / (seed + 1)
total_infections = 0
total_symptos = 0
for r in results:
    total_infections += results[r]['infections']
    total_symptos += results[r]['symptomatics']

average_infections = total_infections/(seed + 1)
average_symptos = total_symptos/(seed + 1)

symptomatic_prognoses_by_age = fixed_age_sim['prognoses']['symp_probs']
expected_cumulative_symptomatic_min = average_infections * symptomatic_prognoses_by_age[1] # under 20 bucket
expected_cumulative_symptomatic_max = average_infections * symptomatic_prognoses_by_age[2] # under 30 bucket
if debug:
    print(results)
    print(f"For a ratio of: {total_infections / total_symptos}")
    print(f"Average number of symptomatics: {average_symptos}")
    print(f"Expected min: {expected_cumulative_symptomatic_min}")
    print(f"Expected_max: {expected_cumulative_symptomatic_max}")
    with open('DEBUG_sim_100.json', 'w') as outfile:
        json.dump(simulation_result, outfile, indent=4, sort_keys=True)
assert average_symptos > expected_cumulative_symptomatic_min,\
    f"Expected more than the 20 year age bucket: {expected_cumulative_symptomatic_min}"
assert average_symptos < expected_cumulative_symptomatic_max, \
    f"Expected less than the 30 year age bucket: {expected_cumulative_symptomatic_max}"