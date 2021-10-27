# ACL_Project

## How does it work?

R_T_P and O_P_TC 

are our special set of constraints 

*R_T_P*

"P" reprents the position of the runner "R" at a certain moment "T".

*O_P_TC*

"P" represents one product from the order O which arrives at the moment "TC" = T+C (the time to get to the conveyor + the time on it)

---

We test every possibility for each runner "i"

---

##3 importants aspects of this project:

	- everytime we path the way for a runner, we must check that no one is already there, and especially that no one is putting a product at the conveyor at the same place, otherwise a conflict can happen.

	- we also have to check that is doesn't arrive at the same time on the point of packaging (end of the conveyor)

	- we have to make sure that every runners stay active without taking any pauses. 

---

DONE:
- No conflict about runners paths
- Products arriving at the same time at the packaging area without conflict
- Runners keep moving

---

TO DO:
- Finish the last implementation 
- Correct the OUTPUT Format
