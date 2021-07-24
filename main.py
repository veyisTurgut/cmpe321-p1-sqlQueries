import sqlite3

con = sqlite3.connect('./f1.db')
cur = con.cursor()

############   1
"""Return the total number of Grand Prixs that starts and ends in April"""

cur.execute('''SELECT COUNT(*) /* Return number of rows.*/
FROM GrandPrixs G /*Select all the rows from Granpdrix table*/
WHERE G.ending_date < '2021-05-01 00:00:00.000' AND G.starting_date >= '2021-04-01 00:00:00.000';
/* Where ending date is before May 1 and starting date is after or equal to April 1. */''')

############   2
"""Print the sum of the total points of the drivers by birth year. Include
only the drivers born between 1990 and 1999, inclusive. Display birth
year and sum in descending order with respect to sum."""

cur.execute('''SELECT D.year_of_birth, SUM(D.total_points)   AS sum
/*Return all the years between 1990,1999 and total points of drivers who was born in that year*/
            FROM Drivers D 
			/*Select Drivers table as D*/
            WHERE D.year_of_birth >= 1990 AND D.year_of_birth <= 1999 
            /*All the drivers who born between 1990 and 1999 inclusive*/
			GROUP BY D.year_of_birth 
			/*Group those drivers with respect to their yeat of birth*/
            ORDER BY sum DESC;
			/*Sort with respect to sum of the total points of these drivers in descending order*/
			/*General idea: Group drivers by birth year, then sum their points. Finally sort it.*/''')

############   3
"""Write the following relational algebra query in SQL. List the results in
descending order of team world championship count:
Πfull name, team chief, technical chief, team wc count(
Teams ◃▹ short nameρ(P (1 → short name), Πpum namePUMs)
)
"""

cur.execute('''SELECT full_name, team_chief, technical_chief, team_wc_count /*return these columns*/
FROM 
    (SELECT * FROM Teams T,/*Choose Teams table*/
             (SELECT DISTINCT pum_name AS short_name FROM PUMs) P /*Create a Table "P" with one column named "short_name" and insert all distinct Pum names to that column.*/
              WHERE T.short_name = P.short_name/* Choose all the rows where pum name equals to teams short name*/)  
    /*Return the rows where teams' short name equals to one of the pums name columns that are identical to Teams' */
ORDER BY team_wc_count DESC;/*Sort with respect to the team world cup count in descending order*/
/*General idea: Select the distinct values of pum_name from PUMs and rename it. Treat this single column as a table P. 
Then select from Teams table where the team short name is in P. 
Finally return the asked columns only with descending order of wc count .*/''')

############   4
""" Return the sum of the total points of the drivers who received their
driving licenses from the country they were born in and whose teams
are based in England and do not buy power units from Mercedes."""

cur.execute('''SELECT SUM(D.total_points) 
            FROM Drivers D 
            INNER JOIN Teams T ON D.team = T.team_id 
            INNER JOIN PUMs P ON T.pum = P.pum_id 
            /*join three tables*/
            WHERE D.country_of_driver_license = D.country_of_birth/*drivers who received their
            driving licenses from the country they were born*/ 
            AND T.base_location = 'England' /*teams that are based in England*/
            AND P.pum_name !='Mercedes'/*do not buy power units from Mercedes*/
            /*General idea: First join drivers and teams table so that we can access drivers' teams easily. 
            Then join teams and pums too so that we can access teams' pum supplers easily. Finally filter with respect to requirements.*/''')

############   5
"""List the first name, last name, base locations of their teams, total
podiums, and highest race finishes (hrf) of the drivers whose teams’
base location end with “LAND” and sort them with respect to the base
location in descending order, then total podiums in ascending order,
and then drivers highest race finish (hrf) in ascending order."""

cur.execute('''SELECT first_name, last_name, base_location, total_podiums, driver_hrf /*return these columns*/
             FROM Drivers D INNER JOIN Teams T ON  D.team = T.team_id /*join teams and drivers table*/
             WHERE T.base_location LIKE '%land' /*drivers whose teams’ base location end with “LAND”*/
             ORDER BY T.base_location DESC, D.total_podiums, D.driver_hrf
             /* sort them with respect to the base location in descending order.
			 If base locations are same, then sort them with respect to total podiums in ascending order.
			 If total podiums are equal too, then sort them with respect to (hrf) in ascending order */
			 /*General idea: First join drivers and teams table so that we can access drivers' teams easily. 
			 Then filter teams those base locations contains 'land' at the end. Finally sort with respect to requirements. */''')

############   6
"""List the short names, full names, world championship counts, and team
total podiums of the teams that have at least 10 team total podiums
and that contain at least one driver who was NOT born in the country
where he/she received his/her license. Sort the results in descending
order of short names."""
cur.execute('''SELECT T.short_name, T.full_name, T.team_wc_count, SUM(D1.total_podiums + D2.total_podiums) 
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
            After that group them by their teams. Select teams from these groups such that drivers' total podiums is at least 10.*/''')

############   7
"""Display the total length of the circuits per circuit type in descending
order with respect to total length. Consider only the circuits in the
countries with an “A” in their names except for Italy. (Hint: You can
compute the length of a track in meters by multiplying its clim and
number of laps.)"""

cur.execute('''SELECT circuit_type,ROUND(sumx,3) as total_length FROM /*set precision to 3*/
            (SELECT circuit_type, SUM(clim*total_laps*1.0/1000) as sumx 
            /* compute the length of a track in KMs by multiplying its clim and number of laps */
            FROM Tracks T 
            WHERE circuit_country LIKE '%a%' AND circuit_country != 'Italy' 
            /* only the circuits in the countries with an “A” in their names except for Italy */
            GROUP BY circuit_type /* Group rows by their circuit type */
            ORDER BY sumx DESC /*descending order with respect to total length */)
            /*General idea: First select all the circuits whose countries contain an 'A' and not Italy. Then group them by their circuit types.
             Take the sum of their total length for each group. Finally round this sum such that precision will be 3.*/''')

############   8
"""List the team id, team short name, team full name, and team driven
total in KMs in ascending order with respect to driven total. Here,
compute the driven total of a team by considering only the drivers of
the team who hold a lap record in any track and who are not born in
England. Display only the teams that have driven at least 500 KMs in
total."""
cur.execute('''SELECT T.team_id, T.short_name, T.full_name, ROUND(sumx,3) /*display up to three precision*/ as total_driven
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
				After we get D, we join D with Teams table so that we can reach other details of these teams. Finally we round total driven to 3 preciison so that we can be consistent with outputs.*/''')

############   9
"""Return the absolute difference of total points received by the old and
young drivers? Here we define old drivers as the ones born between
1980 and 1989 and young drivers as the ones born between 1990 and
1999, both ranges being inclusive"""
cur.execute('''SELECT ABS(total_old - total_young) 
            /* the absolute difference of total points received by the old and young drivers */
            FROM (SELECT SUM(total_points) as total_old 
                     FROM Drivers 
                     WHERE year_of_birth >= 1980 AND year_of_birth <= 1989),
                     /* return the sum of the points of the old drivers as the ones born between 1980 and 1989 */
                 (SELECT SUM(total_points) as total_young 
                     FROM Drivers 
                     WHERE year_of_birth >= 1990 AND year_of_birth <= 1999)
                     /* return the sum of the points of the young drivers as the ones born between 1990 and 1999 */
            /*General idea: Create two variables, one for olds and one for youngs. To do this, filter drivers by their birth years. Then sum their total points. Finally take absolute difference of these values.*/''')

############   10
"""For the Red Bull Racing drivers who hold a lap record, list driver id,
first name, last name, name of the circuit which they hold a lap record,
and the lap record in milliseconds (lrims). Sort the results in ascending
order of lrims."""

cur.execute('''SELECT D.*, circuit_name, lrims  
            FROM (SELECT driver_id, first_name, last_name 
                        FROM Drivers INNER JOIN Teams ON  team = team_id
                        /* hoin drivers and teams table*/
                        WHERE short_name = 'Red Bull Racing'
                        /*Red Bull Racing drivers*/) D INNER JOIN Tracks ON lap_recorder = D.driver_id/*drivers who hold a lap record*/
            ORDER BY lrims/*Sort the results in ascending order of lrims*/
            /*General idea: First create table D such that D contains information of Red Bull Racing teams' drivers. Then join these drivers with track which they have a record. Finally return intended columns.*/''')

############   11
"""List the short names and base locations of the teams that contain at
least one driver who holds a lap record only in France or Monaco track.

List the lap recorder driver names, their countries of birth and the
countries they hold a lap record in, as well. Sort the results in ascending
order with respect to team’s short name."""

cur.execute('''SELECT T.short_name , T.base_location, D.first_name, D.country_of_birth, C.circuit_country  
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
            Finally sort with respect to teams' short name. */''')

############   12
"""List the name of the PUMs whose all customers had become world
champion in the past"""

cur.execute('''SELECT pum_name FROM PUMs 
            EXCEPT /* return all pum names except the pums returned subquery below */
            SELECT DISTINCT MYTABLEx.pum_name 
			/*this subquery returns the name of the pums where one of their customers has 0 world cup.*/
            FROM (SELECT pum_name, short_name, team_wc_count
                         FROM Teams T INNER JOIN PUMs P ON 
                         T.team_id = P.buyer_one 
                         OR T.team_id = P.buyer_two 
                         OR T.team_id = P.buyer_three 
                         OR T.team_id = P.buyer_four) MYTABLEx 
                         /*MYTABLEx has all the non-null pum-customer pairs with world cup counts of those teams. */
            WHERE MYTABLEx.team_wc_count = 0;
			/*General idea: Set difference. First create a table named MYTABLEx. 
			This table has all the non-null pum-customer pairs with world cup counts of those teams.
			From this table select the pairs such that teams has 0 world cups.
			Finally select distinct pums from this table and subtract them from all pums.*/''')

############   13
"""Find the most successful teams by circuit type (street, race) where the
most successful team is the one with the highest number of lap records.
If there are multiple winners for a circuit type, return all of them.
Display circuit type, short name of the team, and the number of lap
records they hold in ascending order of circuit type and team name."""

cur.execute('''WITH my_query AS ( /* form a subquery because this will be used twice*/
    select circuit_type, short_name, count(lap_recorder) as count from (
            /* join Tracks, Drivers and Teams Tables*/
             select circuit_type, lap_recorder, T.short_name from Tracks
                 /* using  Tracks table, select lap recorder-circuit_type pairs */
                left join (
                     select team, driver_id
                     from Drivers
                     ) D
                /* using Drivers table, match the lap recorders with drivers and reach their team id */
                on Tracks.lap_recorder = D.driver_id
                /* using Teams table, match the team ids and reach their short names */
                left join Teams T on T.team_id = D.team
         )
    /* We want the count for each circuit type - team pair, group by these two columns */
    group by circuit_type, short_name
)
/* from the above query take the select the teams with the highest count on that circuit type */
SELECT * FROM my_query
where (circuit_type,count)
          /* find the maximum count for each circuit type */
          in (select circuit_type, max(count) from my_query group by circuit_type);
	  /* General idea: First, create a query that will be used twice later, myquery.
	  In that query, select lap recorder and circuit type pair from the Tracks table.
	  For each pair, using the driver id, retrieve the team id information from the Drivers table.
	  Now, again gor each pair, using the team id, retrieve the team short name from the Teams table.
	  Now we have for each track, the circuit type, lap recorder and team short name information.
	  Now, we need the total count of tracks for each team on different circuit types. 
	  So we group by circuit type and short_name and count the number of lap records. 
	  Now, from this result, we need to select the rows that the count equals the maximum count on that circuit type.
	  For that purpose, find the maximum count for each circuit type by groupping by the circuit type and selecting max(count) (call this maxtable).
	  Finally, select again from the above query the rows where the circuit type-count pair appears in maxtable */''')

############   14
"""Find the teams whose highest race finish (hrf) count is less than the
sum of their drivers’. List the short names, hrf counts and sums of their
drivers’ hrf counts of such teams in descending order of short name."""
cur.execute('''SELECT short_name, team_hrf_count, SUM(D.driver_hrf_count) 
            /*List the short names, hrf counts and sums of their drivers’ hrf counts*/
            FROM Teams T INNER JOIN Drivers D ON D.driver_id = T.driver_one OR D.driver_id = T.driver_two
            /* join drivers and teams */
            GROUP BY D.team HAVING T.team_hrf_count < SUM(D.driver_hrf_count) 
            /*teams whose (hrf) count is less than the sum of their drivers’*/
            ORDER BY short_name DESC/*in descending order of short name*/
            /*General idea: First join teams and drivers such that we have all the team-driver combinations. After that group drivers by their teams and sum their hrfs.
            Finally compare this sum with team's hrf. If team's hrf is lesser select, otherwise eliminate. Finally order the result.*/''')

############   15
"""Find the teams whose driver one’s podium count is at least five times of
driver two’s podium count. Display the short names, driver one podium
counts and driver two podium counts of such teams in ascending order
of short name."""
cur.execute('''SELECT short_name, D1.total_podiums, D2.total_podiums 
            FROM Teams T INNER JOIN Drivers D1 ON D1.driver_id = T.driver_one 
            INNER JOIN Drivers D2 ON D2.driver_id = T.driver_two 
            /* join teams table and two different drivers table*/
            AND D1.total_podiums > 5* D2.total_podiums 
            /*driver one’s podium count is at least five times of driver two’s podium count*/
            ORDER BY short_name /* in ascending order of short name */
            /*General idea: Since we are gonna compare two drivers, we should join two different Driver tables, plus we will need teams. 
            After joining Teams table and Drivers tables, just compare drivers of teams. */  ''')

for row in cur.fetchall():
    print(row)

con.commit()
con.close()
