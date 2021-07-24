SELECT circuit_type,ROUND(sumx,3) as total_length FROM /*set precision to 3*/
            (SELECT circuit_type, SUM(clim*total_laps*1.0/1000) as sumx 
            /* compute the length of a track in KMs by multiplying its clim and number of laps */
            FROM Tracks T 
            WHERE circuit_country LIKE '%a%' AND circuit_country != 'Italy' 
            /* only the circuits in the countries with an “A” in their names except for Italy */
            GROUP BY circuit_type /* Group rows by their circuit type */
            ORDER BY sumx DESC /*descending order with respect to total length */)
            /*General idea: First select all the circuits whose countries contain an 'A' and not Italy. Then group them by their circuit types.
             Take the sum of their total length for each group. Finally round this sum such that precision will be 3.*/