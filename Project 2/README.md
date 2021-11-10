# ACL_Project_2

ist1101360 - Jérémy Breton

ist1101618 - Marc Traverso

## How does it work?

Variables: X__R_T_P, A__R_T and Y__TC_P

- The variable X is the task for a runner "R" at the position "P" at time "T".

- The variable A is the activity of a runner "R" at time "T". If he is active or not.

- The variable Y represents when a product P arrives at the packaging area at time TC (TC=T+C, time when it's placed on the conveyor + time to arrives).

---


## Importants aspects of this project:

    - (1): We have to make sure that two runners are not at the same position at time T.
  
    - (2): We also have to check that a runner doesn't have a task between two tasks. If he is running from position p at time t to position q, he can't be at any position between t and t+t_pq.
    
    - (3): If a runner is at position p he can't be at position q at the same time t.
    
    - (4):
    
    
    
    - (x): If a runner is inactive at time t, then he is inactive at time k+1.
    
    - (x): If a runner is active at time t, then all others runners must be active at time t/2.
    
    - (x): If a runner is at a given position, then then it must move to another position or he becomes inactive.
    
    - (x): If a product p arrives at time t, then a runner must be at position p at time t-c_p.
    
    



## Clauses




## Complexity


## TO DO:
- check si ya pas d'erreur
- qu'il manque pas de clauses avec Y car c'est bizarre, j'ai limpression c'est jamais déposé
