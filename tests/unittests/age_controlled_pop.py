import covasim as cv
import json

debug = True
victim_count = 1000
parameters = cv.make_pars()
parameters['pop_size'] = victim_count
parameters['pop_infected'] = victim_count
results = {}
for seed in range(50):
    parameters['rand_seed'] = seed
    fixed_age_sim = cv.Sim(pars=parameters, load_pop=True)
    fixed_age_sim.initialize()
    fixed_age_sim.people['age'][:] = 25
    fixed_age_sim.people.set_prognoses()
    fixed_age_sim.run(verbose=0)
    simulation_result = fixed_age_sim.to_json(tostring=False)
    results[seed] = simulation_result['results']['cum_symptomatic'][-1]

average_cumulative_symptomatic = sum(results.values()) / (seed + 1)
if debug:
    print(results)
    print("For an average of:")
    print(average_cumulative_symptomatic)
    with open('DEBUG_sim_100.json', 'w') as outfile:
        json.dump(simulation_result, outfile, indent=4, sort_keys=True)
symptomatic_prognoses_by_age = fixed_age_sim['prognoses']['symp_probs']
expected_cumulative_symptomatic_min = victim_count * symptomatic_prognoses_by_age[1] # under 20 bucket
expected_cumulative_symptomatic_max = victim_count * symptomatic_prognoses_by_age[2] # under 30 bucket
assert average_cumulative_symptomatic > expected_cumulative_symptomatic_min,\
    f"Expected more than the 20 year age bucket: {expected_cumulative_symptomatic_min}"
assert average_cumulative_symptomatic < expected_cumulative_symptomatic_max, \
    f"Expected less than the 30 year age bucket: {expected_cumulative_symptomatic_max}"