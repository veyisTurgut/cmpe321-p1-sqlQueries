SELECT ABS(total_old - total_young) 
            /* the absolute difference of total points received by the old and young drivers */
            FROM (SELECT SUM(total_points) as total_old 
                     FROM Drivers 
                     WHERE year_of_birth >= 1980 AND year_of_birth <= 1989),
                     /* return the sum of the points of the old drivers as the ones born between 1980 and 1989 */
                 (SELECT SUM(total_points) as total_young 
                     FROM Drivers 
                     WHERE year_of_birth >= 1990 AND year_of_birth <= 1999)
                     /* return the sum of the points of the young drivers as the ones born between 1990 and 1999 */
            /*General idea: Create two variables, one for olds and one for youngs. To do this, filter drivers by their birth years. Then sum their total points. Finally take absolute difference of these values.*/