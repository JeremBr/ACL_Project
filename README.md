# ACL_Project

## How does it work?

R_T_P and P_TC : are our special set of constraints 

*R_T_P* : "P" reprents the position of the runner "R" at a certain moment "T".

*P_TC* : "P" represents one product which arrives at the moment "TC" = T+C (the moment when it is placed on the conveyor + the time on it)

---


## Importants aspects of this project:

	- (1): Big implementation with all Possibilities

	- (2): Everytime we path the way for a runner, we must check that no one is already there, and especially that no one is putting a product at the conveyor at the same place, otherwise a conflict can happen.

	- (3): We have to make sure that every runners stay active without taking any pauses. 
	
	- (4): We also have to check that it doesn't arrive at the same time on the packaging area (end of the conveyor)
	
	- (5): All products must arrive at the packaging area


## Clauses

- (1): ΛΛΛ(R_T_P V p_TC)  For all R, For all P, and TC=T+Ti,j
- (2): Λ(-(R_T_P) V -(r_T_P))  For all T, For all P, R from 1 to number of Runners
- (3): ΛΛΛ(R_T_P -> R_t_p) For all R,T and t=T+(time from P to p)
- (4): Λ(-(P_T) V -(p_T)  (if 2 products arrive at same time) For all T
- (5): ΛV(P_T) For all P, and T from 1 to t


## Complexity

number of clauses (NC):
- (2): NC = n * t * m (n number of runners, t time, m number of products)
- (4): NC = total product to package * T
- (5): NC = total product to package

---

DONE:
- No conflict about runners paths
- Runners keep moving
- Products arriving at the same time at the packaging area without conflict
- Every products arrive at the packaging area

---

TO DO:
- Correct the last implementation (the big one with every possibilities)
- Correct the OUTPUT Format, but we can't do it without good SAT solver
