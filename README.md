# TSP 
Task 1: The gnomic projection is in the file `svg_dumper.py `, the distance calculation is in the file `data_model.py `
Task 2: The MILP formulation is in the file `milp.py `
Task 3 and 4: in the file `approximation.py `, best result = 44422.60388012291 km
Task 5: in the file `lp-relaxation.py `, 32445.211824121514 km


The heuristic works based on a 2-approximation:
`best_result = inf`
for each city `v` of the set `V`:
    Find an approximation by running a search from the city `v`
    Eliminate intersections
    If the result for city `v` is better than `best_result`, update the value of `best_result`

