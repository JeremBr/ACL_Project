#const r = 2.
#const t = 17.
#const p = 7.

order(1,4).
order(1,5).
order(1,6).
order(2,1).
order(2,3).
order(2,7).
order(2,2).
order(3,6).
order(3,7).
order(3,4).
order(3,1).
order(4,2).
order(4,5).
order(4,3).
order(4,4).

runner(1..r).
time(1..t).
product(1..p).

task(1,0,2,0).
task(2,0,5,0).

travel_time(1,1,1).
travel_time(1,2,3).
travel_time(1,3,4).
travel_time(1,4,3).
travel_time(1,5,4).
travel_time(1,6,3).
travel_time(1,7,4).

travel_time(2,1,3).
travel_time(2,2,1).
travel_time(2,3,3).
travel_time(2,4,2).
travel_time(2,5,2).
travel_time(2,6,3).
travel_time(2,7,3).

travel_time(3,1,4).
travel_time(3,2,3).
travel_time(3,3,1).
travel_time(3,4,4).
travel_time(3,5,4).
travel_time(3,6,2).
travel_time(3,7,2).

travel_time(4,1,3).
travel_time(4,2,2).
travel_time(4,3,4).
travel_time(4,4,1).
travel_time(4,5,4).
travel_time(4,6,4).
travel_time(4,7,4).

travel_time(5,1,4).
travel_time(5,2,2).
travel_time(5,3,4).
travel_time(5,4,4).
travel_time(5,5,1).
travel_time(5,6,3).
travel_time(5,7,3).

travel_time(6,1,3).
travel_time(6,2,3).
travel_time(6,3,2).
travel_time(6,4,4).
travel_time(6,5,3).
travel_time(6,6,1).
travel_time(6,7,3).

travel_time(7,1,4).
travel_time(7,2,3).
travel_time(7,3,2).
travel_time(7,4,4).
travel_time(7,5,3).
travel_time(7,6,3).
travel_time(7,7,1).


conveyor_time(1,2).
conveyor_time(2,4).
conveyor_time(3,2).
conveyor_time(4,4).
conveyor_time(5,3).
conveyor_time(6,1).
conveyor_time(7,2).



%------------------------------
%(0): Products MUST be achieved
1{task(R,T,P,O):time(T),T>0,runner(R)}1 :- order(O,P).
%------------------------------

%------------------------------
%(1): We have to make sure that two runners are not at the same position at time t.
:- task(R1,T,P,_), task(R2,T,P,_), R1!=R2, T>0.
%------------------------------

%------------------------------
%(2): no task between two tasks/positions
:- task(R,T1,P1,_), task(R,T2,P2,_), T2=TT+T1, travel_time(P1,P2,TT), task(R,T3,_,_), T1<T3, T3<T2.
%------------------------------

%------------------------------
% (3): If a runner is at position p he can't be at position q at the same time t.
:- task(R,T,P,_), task(R,T,Q,_), P!=Q.
:- task(R,T,P,O), task(R,T,P,M), M!=O.
%------------------------------

%------------------------------
% (4): We have to make sure that every runners stay active without taking any pauses. It means that a runner must move to another position or he becomes inactive.
activity(R,T):- task(R,T,P,_).
-activity(R,T):- not activity(R,T), runner(R), time(T).
valid_pos(R,T2,Q):- task(R,T1,P,O), travel_time(P,Q,TT),T2=TT+T1.
-task(R,T,P,O) :- not valid_pos(R,T,P), order(O,P), runner(R), time(T).
%------------------------------

%------------------------------
%(5): runner active at T, must be active before
activity(R,T-1) :- activity(R,T), T>1.
%------------------------------

%------------------------------
%(6): All runners must have a timespan of at least 50% of the maximum. So, for a runner active at time t, all others runners must be active at t/2.
:- activity(R1,T1), -activity(R2,T2), T2<T1/2, R1!=R2.
%------------------------------

%------------------------------
%(7): two products doesnt arrive at the same time at the packaging area.
arrive(P,T+C) :- task(R,T,P,O), conveyor_time(P,C), T>0.
:- arrive(P1,T), arrive(P2,T), P1!=P2.
%------------------------------

#show task/4.
#show arrive/2.