'Special variant of the Vehicle Routing Problem'

from ortools.sat.python import cp_model


class Data:

    def __init__(self, sets, parameters):
        self.nodes = sets['nodes'] #list of nodes
        self.edges = sets['edges'] #list of tuples where each tuple (i,j) describes an edge
        self.days = sets['days'] #list of days
        self.vehicles = sets['vehicles'] #list of vehicles
        self.service_days = sets['service_days'] #dict containing list of feasible days for pickup

        self.travel_cost = parameters['travel_cost']
        self.stop_cost = parameters['stop_cost']
        self.distance = parameters['distance']
        self.distance_max = parameters['distance_max']
        self.demand = parameters['demand'] #dict of demand for node i on day t
        self.capacity = parameters['capacity']


class VehicleRoutingModel:

    def __init__(self, data):
        self.data = data

    def solve_model(self):
        'define model'
        self.model = cp_model.CpModel()

        'define routing variables'
        y = {}
        for i,j in self.data.edges:
            for k in self.data.vehicles:
                for t in self.data.days:
                    y[i,j,k,t] = self.model.NewBoolVar(f'y_{i}_{j}_{k}_{t}')

        'define demand to vehicle allocation variables'
        x = {}
        for i,j in self.data.edges:
            for k in self.data.vehicles:
                for t in self.data.days:
                    for l in self.data.service_days[t]:
                        x[i,j,k,t,l] = self.model.NewBoolVar(f'x_{i}_{j}_{k}_{t}_{l}')

        'define constraints'
        'truck capacity'
        for l in self.data.days:
            for k in self.data.vehicles:
                self.model.Add(
                    sum(
                        self.data.demand[i,t] * x[i,j,k,t,l]    for t in self.data.service_days[l] 
                                                                for i in self.data.nodes[1:] 
                                                                for j in [edge[1] for edge in self.data.edges if edge[0]==i])
                        <= self.data.capacity
                    )

        'Demand fulfillment'
        for t in self.data.days:
            for i in self.data.nodes:
                self.model.Add(
                    sum(x[i,j,k,t,l]    for l in self.data.service_days[t] 
                                        for k in self.data.vehicles 
                                        for j in [edge[1] for edge in self.data.edges if edge[0]==i]) 
                    == 1
                )

        'start at depot'
        for k in self.data.vehicles:
            for l in self.data.days:
                self.model.Add(
                    sum(y[self.data.nodes[0],j,k,t] for j in self.data.nodes[1:]) == 1
                )

        'netflow'
        for h in self.data.nodes:
            for k in self.data.vehicles:
                for l in self.data.days:
                    self.model.Add(
                        sum(y[i,h,k,l] for i in [edge[0] for edge in self.data.edges if edge[1]==h]) 
                        - sum(y[h,j,k,l] for j in [edge[1] for edge in self.data.edges if edge[0]==h]) 
                        == 0
                    )

        'vehicle returns to depot'
        for k in self.data.vehicles:
            for l in self.data.days:
                self.model.Add(
                    sum(y[i,self.data.nodes[0],k,t] for i in self.data.nodes[1:]) == 1
                )

        'connection between loading and routing variable'
        for i,j in self.data.edges:
            for k in self.data.vehicles:
                for l in self.data.days:
                    self.model.Add(
                        sum(x[i,j,k,t,l] for t in self.data.service_days[l]) <= len(self.data.service_days[l]) * y[i,j,k,l]
                    )

        'objective function'
        self.model.Minimize(
            sum(self.data.distance[i,j] * self.data.travel_cost * y[i,j,k,t] + self.data.stop_cost * y[i,j,k,t] for i,j, in self.data.edges for k in self.data.vehicles for t in self.data.days)
            )

        'solve model'
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0
        
        'get results'
        self.status = solver.Solve(self.model)
        self.objective_value = solver.ObjectiveValue()
        
        self.tours = {}
        for k in self.data.vehicles:
            for t in self.data.days:
                self.tours[k,t] = {(i,j): sum(self.data.demand.get((i,t),0) * solver.Value(x[i,j,k,l,t]) for l in self.data.service_days[t]) for i,j in self.data.edges if solver.Value(y[i,j,k,t]) == 1}

    def get_tour(self, k, t):
        return self.tours[k,t]    
        

        