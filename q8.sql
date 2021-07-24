SELECT T.team_id, T.short_name, T.full_name, ROUND(sumx,3) /*display up to three precision*/ as total_driven
            FROM (SELECT team, SUM(clim*total_laps*1.0/1000)/*convert length of the circut to km's*/ as sumx
                FROM Drivers, Tracks 
                WHERE country_of_birth != 'England' 
                /* drivers who are not born in England */
                AND lap_recorder = driver_id 
                /* considering only the drivers of the team who hold a lap record in any track */
                GROUP BY team HAVING sumx >= 500
                /* only the teams that have driven at least 500 KMs in total */
                ORDER BY sumx/*in ascending order with respect to driven total*/) D INNER JOIN Teams T  ON D.team = T.team_id
                /* join the D table which we retrieved from subquery and Teams table*/
                /*General idea: First create a table D such that D has the teams that driven at least 500KMs and their total driven lengths.
				While constructing D we do not use Teams table, instead we infer teams' name from drivers by grouping them with respect to their teams and summing up their driven totals.
				After we get D, we join D with Teams table so that we can reach other details of these teams. Finally we round total driven to 3 preciison so that we can be consistent with outputs.*/