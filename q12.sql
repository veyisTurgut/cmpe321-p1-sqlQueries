SELECT pum_name FROM PUMs 
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
			Finally select distinct pums from this table and subtract them from all pums.*/