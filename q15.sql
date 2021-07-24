SELECT short_name, D1.total_podiums, D2.total_podiums 
            FROM Teams T INNER JOIN Drivers D1 ON D1.driver_id = T.driver_one 
            INNER JOIN Drivers D2 ON D2.driver_id = T.driver_two 
            /* join teams table and two different drivers table*/
            AND D1.total_podiums > 5* D2.total_podiums 
            /*driver one’s podium count is at least five times of driver two’s podium count*/
            ORDER BY short_name /* in ascending order of short name */
            /*General idea: Since we are gonna compare two drivers, we should join two different Driver tables, plus we will need teams. 
            After joining Teams table and Drivers tables, just compare drivers of teams. */  