from VRP_models import Data, CP_VehicleRoutingModel
import pickle


'definition of sets'
sets = {}
sets['nodes'] = [0,1,2,3,4]

sets['edges'] = [(0,1),(0,2),(0,3),(0,4),
                 (1,0),(1,2),(1,3),(1,4),
                 (2,0),(2,1),(2,3),(2,4),
                 (3,0),(3,1),(3,2),(3,4),
                 (4,0),(4,1),(4,2),(4,3)
                 ]

sets['days'] = [1,2,3,4,5]
sets['vehicles'] = [1,2,3,4,5,6,7,8,9]
sets['service_days'] = {1: [1,2],
                        2: [1,2,3],
                        3: [2,3,4],
                        4: [3,4,5],
                        5: [4,5]
                        }

'definition of parameters'
parameters = {}
parameters['travel_cost'] = 10
parameters['stop_cost'] = 50
parameters['distance'] = {(0,1):2451, (0,2):713, (0,3):1018, (0,4):1631,
                          (1,0):2451, (1,2):1745, (1,3):1524, (1,4): 831,
                          (2,0):713, (2,1):1745, (2,3):355, (2,4): 920,
                          (3,0): 1018, (3,1): 1524, (3,2):355, (3,4):700,
                          (4,0):1631, (4,1): 831, (4,2): 920, (4,3):700
                          }
parameters['distance_max'] = 30
parameters['demand'] = {(1,1): 50, (1,2): 60, (1,3): 25, (1,4):50, (1,5):90,
                        (2,1): 35, (2,2): 20, (2,3): 80, (2,4):5, (2,5):1,
                        (3,1): 140, (3,2): 160, (3,3): 75, (3,4):95, (3,5):65,
                        (4,1): 45, (4,2): 10, (4,3): 80, (4,4):15, (4,5):8
                        }
parameters['capacity'] = 200



#### experiments ####

### this experiment takes lots of compute time ! ###
min_number_vehicles = max([int(sum(parameters['demand'].get((i,t),0) for i in sets['nodes'])/parameters['capacity']) for t in sets['days']])
min_number_vehicles = max(min_number_vehicles, 2)
max_number_vehicles = min_number_vehicles+2
max_num_demand_shifts = 5

#result = {}
#for i in range(max_num_demand_shifts):
#    for n in range(min_number_vehicles, max_number_vehicles):
#        sets['vehicles'] = list(range(n))
#        data = Data(sets, parameters)
#        vrp = CP_VehicleRoutingModel(data, 30.0, i)
#        vrp.solve_model()
#        result[n,i] = [vrp.status, vrp.objective_value]

#print(result)

### run vrp with one parameter setting ###
sets['vehicles'] = list(range(min_number_vehicles))
data = Data(sets, parameters)

vrp = CP_VehicleRoutingModel(data, 30.0, 0)
vrp.solve_model()

print(vrp.status)
print()
print()
print(vrp.objective_value)
print()
print()
for t in sets['days']:
    for k in sets['vehicles']:
        print(f'Tour of vehicle {k} on day {t}')
        print(vrp.get_tour(k,t))
        print()
        print()


output = open('tours.pkl', 'wb')
pickle.dump(vrp.get_tours(), output)
output.close()