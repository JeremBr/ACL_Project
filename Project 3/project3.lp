% nb of runners
#const r = 2.
#const t = 5.
#const p = 3.


runner(1..r).
time(1..t).
product(1..p).


order(1,1).
order(1,2).
order(1,3).
order(2,1).
order(2,4).


% generate

p { task(I, J, K) : runner(I), time(J), product(K) } r*t*p.

r { activity(I, J) : runner(I), time(J) } r*t.

p { arrives(I,J) : time(I), product(J) } p.




%-------------------------------
% (1): We have to make sure that two runners are not at the same position at time t.
:- task(R1,T,P), task(R2,T,P), R1!=R2, T>0.

% il faut ajouter condition que ca peut etre le cas a linitialisation T!=0
%-------------------------------


%-------------------------------
% (2): We also have to check that a runner doesn't have a task between two tasks. If he is running from position p at time t to position q, he can't be at any position between t and t+t_pq.

%:- task(R,T1,P), activity(R,T1) un truc à faire avec les activity

%-------------------------------

%-------------------------------
% (3): If a runner is at position p he can't be at position q at the same time t.
:- task(R,T,P), task(R,T,Q), P!=Q.
%-------------------------------



%-------------------------------
% (4): We have to make sure that every runners stay active without taking any pauses. It means that a runner must move to another position or he becomes inactive.
%-------------------------------

:- activity(R,T), task(R,T,P).

:- task(R,T,P), task(R,T+1,P), activity(R,T+1).

%-------------------------------
% (5): If we have a runner inactive at time t it implies that he is inactive at t+1.
:- activity(R, T), activity(R, T+1).


% (6): All runners must have a timespan of at least 50% of the maximum. So, for a runner active at time t, all others runners must be active at t/2.



% (7): We have to check that a runner was at position p at time t-c_p when a product p arrives at the packaging area at time t.


%-------------------------------
% (8): All products must arrive at the packaging area.
:- count{ arrives(T,X) : time(T), product(X) }!=p.
% que arrives soit true peut importe T et qui en ait un nombre egal au nombre de produit
%-------------------------------
