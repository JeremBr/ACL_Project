# ACL_Project

## BROUILLON
## A METTRE EN ANGLAIS

R_T_P et P_TC

Position P à l'instant T du runner R
Product P qui arrive à TC = T+C (temps quand il arrive sur conveyor puis temps qu'il met dessus)


On test toutes les possibilités pour runner i (et pour tous les runners, puis pour tous ceux qui restent)


3 Trucs à prendre en compte:

  - à chaque fois qu'on détermine où le runner va aller, qu'il y est pas déjà quelqu'un

  C'est à dire, par exemple, si à un instant t le runner 1 se trouve à p3, il faut pas que le runner 2 arrive à ce même instant à p3

  Car ça voudrait dire qu'il mette le product en même temps sur le conveyor, donc que ça arrivera en même temps

  DONC JE REDIS, quand on détermine où va runner, qu'il y est pas déjà qlq !!


  - que ça n'arrive pas en même temps au point de packaging (fin du conveyor)
  
  donc pour ça on utilise nos variables P_TC pour faire clauses : Λ(V(-P_TC,-p_TC))
  
  Autrement dit que deux product different n'arrive pas à TC égale
  
  et on rajoute clauses pour dire que tous les products sont acheminés, c'est à dire:  Λ(V(P_TC,P_tc))
  
  Autrement dit on check que le product P soit acheminé n'importe quand
  



  - Le runner quand il pose produit, il repart direct cet esclave, cest a dire IL EST TJRS ACTIF, il a pas moment de répis, il faut bien faire des clauses sur ca



---

DONE:
- Runners arrivent pas en même temps au même endroit
- 

