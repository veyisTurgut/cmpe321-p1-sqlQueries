SELECT full_name, team_chief, technical_chief, team_wc_count /*return these columns*/
FROM 
    (SELECT * FROM Teams T,/*Choose Teams table*/
             (SELECT DISTINCT pum_name AS short_name FROM PUMs) P /*Create a Table "P" with one column named "short_name" and insert all distinct Pum names to that column.*/
              WHERE T.short_name = P.short_name/* Choose all the rows where pum name equals to teams short name*/)  
    /*Return the rows where teams' short name equals to one of the pums name columns that are identical to Teams' */
ORDER BY team_wc_count DESC;/*Sort with respect to the team world cup count in descending order*/
/*General idea: Select the distinct values of pum_name from PUMs and rename it. Treat this single column as a table P. 
Then select from Teams table where the team short name is in P. 
Finally return the asked columns only with descending order of wc count .*/