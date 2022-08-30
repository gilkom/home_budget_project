INSERT INTO budgets_saver values(
        1, 3);
INSERT INTO budgets_saver values(
        2, 4);
-----------------------------------------
insert into budgets_period values(
	1, 'Sierpień', '01-08-2022', '31-08-2022', 1);
insert into budgets_period values(
	2, 'Wrzesień', '01-08-2022', '31-08-2022', 1);
insert into budgets_period values(
	3, 'Sierpień', '10-08-2022', '10-09-2022', 2);
insert into budgets_period values(
	4, 'Wrzesień', '01-09-2022', '30-09-2022', 2);
	
--------------------------------	

insert into budgets_balance values(
	3845.5, 1, 1);
insert into budgets_balance values(
	4787.50, 2, 1);
insert into budgets_balance values(
	8531.41, 3, 2);
insert into budgets_balance values(
	8432.54, 4, 2);
	
	
--------------------------------------------

insert into budgets_category values(
	1, 'Jedzenie');
insert into budgets_category values(
	2, 'Mieszkanie');
insert into budgets_category values(
	3, 'Pozostałe');
insert into budgets_category values(
	4, 'Motoryzacja');
insert into budgets_category values(
	5, 'Kosmetyki');
	
	
	
--------------------------

insert into budgets_monthly_goal values(
	600, 1, 1, 1);
insert into budgets_monthly_goal values(
	600, 1, 2, 1);
insert into budgets_monthly_goal values(
	600, 3, 3, 1);
insert into budgets_monthly_goal values(
	600, 3, 4, 1);
insert into budgets_monthly_goal values(
	600, 2, 1, 2);
insert into budgets_monthly_goal values(
	600, 2, 2, 2);
insert into budgets_monthly_goal values(
	600, 4, 3, 2);
insert into budgets_monthly_goal values(
	600, 5, 4, 2);
	
	
	--------------------------------
	
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,id_budgets_saver) values(
	15, '20-08-2022', null, 1, 1);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,id_budgets_saver) values(
	2076.45 , '20-08-2022', null, 1, 2);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,id_budgets_saver) values(
	76, '20-08-2022', 'Lokówka', 2, 1);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,id_budgets_saver) values(
	89.50, '20-08-2022', null, 3, 2);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,id_budgets_saver) values(
	89.50, '20-08-2022', null, 4, 1);