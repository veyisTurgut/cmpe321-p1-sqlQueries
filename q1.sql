SELECT COUNT(*) /* Return number of rows.*/
FROM GrandPrixs G /*Select all the rows from Granpdrix table*/
WHERE G.ending_date < '2021-05-01 00:00:00.000' AND G.starting_date >= '2021-04-01 00:00:00.000';
/* Where ending date is before May 1 and starting date is after or equal to April 1. */