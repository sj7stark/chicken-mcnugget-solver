import gurobipy as gp

def nugget_solve(pack_size_1, pack_size_2, pack_size_3, threshold_solve=100, total_solve_lim=2500):

    # dictionary containing the different pack sizes we can purchase
    pack_size = {1: pack_size_1,
                 2: pack_size_2,
                 3: pack_size_3
                 }

    # current count of sucessful consecutive solves
    consecutive_solve = 0

    # total solve attempts
    # cancel if too many
    total_solves = 0

    # the number of McNuggets we try to purchase and increment by 1 after each solve
    nugget_rhs = 1

    # largest number of McNuggets that CANNOT be purchased (changes after each solve with no solution)
    mcnuggets_sol = 0

    # create model
    opt_model = gp.Model(name="McNugget_Solver")

    # create variables
    x = opt_model.addVars(pack_size.keys(), vtype=gp.GRB.INTEGER, name='x')

    # We don't need to optimize anything, so just make it nothing
    opt_model.ModelSense = gp.GRB.MAXIMIZE
    opt_model.setObjective(0)

    # loop
    while consecutive_solve != threshold_solve:

        # add the constraint to the model
        opt_model.addConstr(gp.quicksum(pack_size[i]*x[i] for i in pack_size.keys() ) == nugget_rhs)
        
        # solve the problem
        opt_model.optimize()
        total_solves += 1
    
        # if there is no solution, set the new obj and reset consecutive_solve counter
        if opt_model.status == 3:
            mcnuggets_sol = nugget_rhs
            consecutive_solve = 0

        # else, increment the consecutive_solve counter
        else:
            consecutive_solve += 1

        # increment nugget_rhs
        nugget_rhs += 1

        # clear model constraints
        opt_model.remove(opt_model.getConstrs()[0])

        # exit if we have tried too many solves
        if total_solves > total_solve_lim:
            break

    # return the solution
    return mcnuggets_sol


if __name__ == '__main__':

    pack_size_1 = 6
    pack_size_2 = 9
    pack_size_3 = 20
    threshold_solve=500
    total_solve_lim=10000

    mcnuggets_sol = nugget_solve(pack_size_1, pack_size_2, pack_size_3,threshold_solve,total_solve_lim)

    print(f"{mcnuggets_sol=}")


