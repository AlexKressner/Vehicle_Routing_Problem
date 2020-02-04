from VRP_models import Data, CP_VehicleRoutingModel


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


data = Data(sets, parameters)

vrp = CP_VehicleRoutingModel(data, 20.0)
vrp.solve_model()
print(vrp.status) #status codes 2: feasible, https://developers.google.com/optimization/cp/cp_solver
print(vrp.objective_value)

for t in sets['days']:
    for k in sets['vehicles']:
        print(f'Tour of vehicle {k} on day {t}')
        print(vrp.get_tour(k,t))
        print()
        print()

