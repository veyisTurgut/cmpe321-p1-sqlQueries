SELECT T.short_name , T.base_location, D.first_name, D.country_of_birth, C.circuit_country  
            FROM (SELECT lap_recorder 
                   /*select lap recorders of all the circuit countries*/
                   FROM Tracks WHERE (circuit_country IN ('France', 'Monaco'))       
                   /*take set difference of these two sets--below and above, result will be the
                   drivers who holds a lap record "ONLY" in France or Monaco track*/
                   EXCEPT 
                   /* select lap recorders of all the circuit countries except France and Monaco*/
                   SELECT DISTINCT lap_recorder FROM Tracks WHERE (circuit_country NOT IN ('France' ,'Monaco'))) LR
                   /*now LR has the drivers who holds a lap record "ONLY" in France or Monaco track */
                   INNER JOIN Teams T ON LR.lap_recorder = T.driver_one OR LR.lap_recorder = T.driver_two
                   INNER JOIN Drivers D ON D.driver_id = LR.lap_recorder 
                   INNER JOIN Tracks C ON C.lap_recorder = LR.lap_recorder 
                   /*join all the tables*/
            ORDER BY T.short_name /*Sort the results in ascending order with respect to team’s short name*/
            /*General idea: Create LR table such that LR is the set difference of two columns. 
                Column1 is the drivers who have record on France or Monaco, they may have records on different circuits too. 
                Column2 is the drivers who have record on circuits other than France and Monaco. 
                If we take the drivers those are in column1 and not in column2, we will get drivers who hold record 'ONLY' in France or Monaco.
            After having LR, join it with other tables so that we can get the intended columns.
            Finally sort with respect to teams' short name. */