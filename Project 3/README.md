# ACL_Project_2

ist1101360 - Jérémy Breton

ist1101618 - Marc Traverso

## How does it work?

python main.py < instances/enunciado1.wps > output.out
./wps-checker instances/enunciado1.wps output.out

close to be OK : when the output is close of the expected one, but it's not
never end : when it doesn't end in less than one or two minutes, in a correct computational time

instances/enunciado1.wps - OK
instances/enunciado2.wps - OK
instances/t_2_3_5_5_4.wps - close to be OK
instances/t_2_3_10_2_2.wps - never end
instances/t_2_3_10_3_2.wps - never end
instances/t_2_3_10_5_2.wps - never end
instances/t_2_3_10_5_4.wps - never end
instances/t_2_7_4_4_5.wps - close to be OK
instances/t_3_5_10_5_4.wps - never end
instances/t_3_5_10_10_4.wps - never end
instances/t_3_7_4_4_5.wps - close to be OK
instances/t_5_7_4_4_5.wps - close to be OK

## Logics

Main logic: task(R,T,P,O), activity(R,T), arrive(P,TC)

- The task for a runner "R" at the position "P" for the order "O" at time "T".

- The activity of a runner "R" at time "T". If he is active or not.

- When a product "P" arrives at the packaging area at time "TC" (TC=T+C, time T when it's placed on the conveyor + time C to arrives).

---


## Importants aspects of this project:

    - (0): Products MUST be achieved

    - (1): We have to make sure that two runners are not at the same position at time t.
  
    - (2): We also have to check that a runner doesn't have a task between two tasks. If he is running from position p at time t to position q, he can't be at any position between t and t+t_pq.
    
    - (3): If a runner is at position p he can't be at position q at the same time t.
    
    - (4): We have to make sure that every runners stay active without taking any pauses. It means that a runner must move to another position or he becomes inactive.
    
    - (5): A runner active at T, must be active before
    
    - (6): All runners must have a timespan of at least 50% of the maximum. So, for a runner active at time t, all others runners must be active at t/2.
    
    - (7): We have to check that two products doesnt arrive at the same time at the packaging area.
    

## Clauses:

### (0):

![img8](clauses/8.png)

### (1): 

![img1](clauses/1.png)

---

### (2): 

![img2](clauses/2.png)

---

### (3):

![img3](clauses/3.png)

---

### (4):

![img4](clauses/4.png)

---

### (5):

![img5](clauses/5.png)

---

### (6):

![img6](clauses/6.png)

---

### (7):

![img7](clauses/7.png)

---




