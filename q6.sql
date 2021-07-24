SELECT T.short_name, T.full_name, T.team_wc_count, SUM(D1.total_podiums + D2.total_podiums) 
            /* return short names, full names, world championship counts, and team total podiums*/
            FROM Teams T INNER JOIN Drivers D1 ON T.driver_one = D1.driver_id 
            INNER JOIN Drivers D2 ON T.driver_two = D2.driver_id 
            /* Join two drivers table and teams table*/
            WHERE (D1.country_of_birth != D1.country_of_driver_license 
                  OR D2.country_of_birth != D2.country_of_driver_license)
            /*teams that contain at least one driver who was NOT born in the country 
            where he/she received his/her license */ 
            GROUP BY T.team_id HAVING SUM(D1.total_podiums + D2.total_podiums) >= 10 
            /*teams that have at least 10 team total podiums*/
            ORDER BY T.short_name DESC/*Sort the results in descending order of short names*/
            /*General idea: First join two drivers tables and teams table. Then select them such that there will be
            at least one driver who was NOT born in the country where he/she received his/her license.
            After that group them by their teams. Select teams from these groups such that drivers' total podiums is at least 10.*/