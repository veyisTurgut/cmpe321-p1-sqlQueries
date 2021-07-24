SELECT D.year_of_birth, SUM(D.total_points)   AS sum
/*Return all the years between 1990,1999 and total points of drivers who was born in that year*/
            FROM Drivers D 
			/*Select Drivers table as D*/
            WHERE D.year_of_birth >= 1990 AND D.year_of_birth <= 1999 
            /*All the drivers who born between 1990 and 1999 inclusive*/
			GROUP BY D.year_of_birth 
			/*Group those drivers with respect to their yeat of birth*/
            ORDER BY sum DESC;
			/*Sort with respect to sum of the total points of these drivers in descending order*/
			/*General idea: Group drivers by birth year, then sum their points. Finally sort it.*/