% INITIALIZATIONS:

#const r = 2. %nb of runners
#const t = 8. %time (decrease till UNSAT)
#const p = 4. %nb of products

runner(1..r).
time(1..t).
product(1..p).

%Initialize pos runners
task(1,0,1,0).
task(2,0,1,0).

%list order/product to achieve
order(1,1).
order(1,2).
order(1,3).
order(2,1).
order(2,4).

%time from going to point i to j
travel_time(1,1,1).
travel_time(1,2,5).
travel_time(1,3,3).
travel_time(1,4,3).

travel_time(2,1,5).
travel_time(2,2,1).
travel_time(2,3,3).
travel_time(2,4,3).

travel_time(3,1,3).
travel_time(3,2,3).
travel_time(3,3,1).
travel_time(3,4,2).

travel_time(4,1,3).
travel_time(4,2,3).
travel_time(4,3,2).
travel_time(4,4,1).

%time for a product to reach conveyor
conveyor_time(1,3).
conveyor_time(2,1).
conveyor_time(3,3).
conveyor_time(4,2).

%-------------------------------
%(0): Products MUST be achieved
1{task(R,T,P,O):time(T),T>0,runner(R)}1 :- order(O,P).

%(1): We have to make sure that two runners are not at the same position at time t.
:- task(R1,T,P,_), task(R2,T,P,_), R1!=R2, T>0.

%(2): no task between two tasks/positions
:- task(R,T1,P1,_), task(R,T2,P2,_), T2=TT+T1, travel_time(P1,P2,TT), task(R,T3,_,_), T1<T3, T3<T2.

%(3): runner cant be at 2pos in same time
:- task(R,T,P,_), task(R,T,Q,_), P!=Q.
:- task(R,T,P,O), task(R,T,P,M), M!=O.


%(4): We have to make sure that every runners stay active without taking any pauses. It means that a runner must move to another position or he becomes inactive.
activity(R,T):- task(R,T,P,_). %define activity
-activity(R,T):- not activity(R,T), runner(R), time(T).


valid_pos(R,T2,Q):- task(R,T1,P,O), travel_time(P,Q,TT),T2=TT+T1.
-task(R,T,P,O) :- not valid_pos(R,T,P), order(O,P), runner(R), time(T).



%(5): runner active at T, must be active before
activity(R,T-1) :- activity(R,T), T>1.



%(7): All runners must have a timespan of at least 50% of the maximum. So, for a runner active at time t, all others runners must be active at t/2.
:- activity(R1,T1), -activity(R2,T2), T2<T1/2, R1!=R2.

%(8): two products doesnt arrive at the same time at the packaging area
arrive(P,T+C) :- task(R,T,P,O), conveyor_time(P,C), T>0.
:- arrive(P1,T), arrive(P2,T), P1!=P2.

%#show arrive/2.
%#show activity/2.
%#show valid_pos/3.

#show task/4.


