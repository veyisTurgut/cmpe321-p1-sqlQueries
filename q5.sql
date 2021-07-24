SELECT first_name, last_name, base_location, total_podiums, driver_hrf /*return these columns*/
             FROM Drivers D INNER JOIN Teams T ON  D.team = T.team_id /*join teams and drivers table*/
             WHERE T.base_location LIKE '%land' /*drivers whose teams’ base location end with “LAND”*/
             ORDER BY T.base_location DESC, D.total_podiums, D.driver_hrf
             /* sort them with respect to the base location in descending order.
			 If base locations are same, then sort them with respect to total podiums in ascending order.
			 If total podiums are equal too, then sort them with respect to (hrf) in ascending order */
			 /*General idea: First join drivers and teams table so that we can access drivers' teams easily. 
			 Then filter teams those base locations contains 'land' at the end. Finally sort with respect to requirements. */