SELECT D.*, circuit_name, lrims  
            FROM (SELECT driver_id, first_name, last_name 
                        FROM Drivers INNER JOIN Teams ON  team = team_id
                        /* hoin drivers and teams table*/
                        WHERE short_name = 'Red Bull Racing'
                        /*Red Bull Racing drivers*/) D INNER JOIN Tracks ON lap_recorder = D.driver_id/*drivers who hold a lap record*/
            ORDER BY lrims/*Sort the results in ascending order of lrims*/
            /*General idea: First create table D such that D contains information of Red Bull Racing teams' drivers. Then join these drivers with track which they have a record. Finally return intended columns.*/