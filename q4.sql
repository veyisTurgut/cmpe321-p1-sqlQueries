SELECT SUM(D.total_points) 
            FROM Drivers D 
            INNER JOIN Teams T ON D.team = T.team_id 
            INNER JOIN PUMs P ON T.pum = P.pum_id 
            /*join three tables*/
            WHERE D.country_of_driver_license = D.country_of_birth/*drivers who received their
            driving licenses from the country they were born*/ 
            AND T.base_location = 'England' /*teams that are based in England*/
            AND P.pum_name !='Mercedes'/*do not buy power units from Mercedes*/
            /*General idea: First join drivers and teams table so that we can access drivers' teams easily. 
            Then join teams and pums too so that we can access teams' pum supplers easily. Finally filter with respect to requirements.*/