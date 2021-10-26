# ACL_Project

## BROUILLON
## A METTRE EN ANGLAIS

R_T_P_C

Position P à l'instant T du runner R
C coût en temps de la position précédente jusqu'à celle-ci

On test toutes les possibilités pour runner i (et pour tous les runners, puis pour tous ceux qui restent)


2 Trucs à prendre en compte:

- à chaque fois qu'on détermine où le runner va aller, qu'il y est pas déjà quelqu'un
C'est à dire, par exemple, si à un instant t le runner 1 se trouve à p3, il faut pas que le runner 2 arrive à ce même instant à p3
Car ça voudrait dire qu'il mette le product en même temps sur le conveyor, donc que ça arrivera en même temps
DONC JE REDIS, quand on détermine où va runner, qu'il y est pas déjà qlq !!

- que ça n'arrive pas en même temps au point de packaging (fin du conveyor)
C'est à dire qu'il faut faire des soft clauses (x) à chaque fois qu'on pose un product
avec x qui a pour valeur T+CT c'est à dire le temps que ça arrivera
(CT le Conveyor Time)
Dans l'exemple, on voit que le product 1 arrivera à 1+3
donc la clause (4) est True, il peut pas y en avoir d'autres de true
(réfléchir à comment faire)
