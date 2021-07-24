SELECT short_name, team_hrf_count, SUM(D.driver_hrf_count) 
            /*List the short names, hrf counts and sums of their drivers’ hrf counts*/
            FROM Teams T INNER JOIN Drivers D ON D.driver_id = T.driver_one OR D.driver_id = T.driver_two
            /* join drivers and teams */
            GROUP BY D.team HAVING T.team_hrf_count < SUM(D.driver_hrf_count) 
            /*teams whose (hrf) count is less than the sum of their drivers’*/
            ORDER BY short_name DESC/*in descending order of short name*/
            /*General idea: First join teams and drivers such that we have all the team-driver combinations. After that group drivers by their teams and sum their hrfs.
            Finally compare this sum with team's hrf. If team's hrf is lesser select, otherwise eliminate. Finally order the result.*/