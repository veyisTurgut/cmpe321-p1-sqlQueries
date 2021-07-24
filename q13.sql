WITH my_query AS ( /* form a subquery because this will be used twice*/
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
	  Now, again for each pair, using the team id, retrieve the team short name from the Teams table.
	  Now we have for each track, the circuit type, lap recorder and team short name information.
	  Now, we need the total count of tracks for each team on different circuit types. 
	  So we group by circuit type and short_name and count the number of lap records. 
	  Now, from this result, we need to select the rows that the count equals the maximum count on that circuit type.
	  For that purpose, find the maximum count for each circuit type by groupping by the circuit type and selecting max(count) (call this maxtable).
	  Finally, select again from the above query the rows where the circuit type-count pair appears in maxtable */