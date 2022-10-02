-- INSERT INTO budgets_saver values(
--        1, 3);
-- INSERT INTO budgets_saver values(
--       2, 4);

-----------------------------------------
insert into budgets_period(name, start_day, end_day, owner) values(
	'Sierpień', '01-08-2022', '31-08-2022', 1);
insert into budgets_period(name, start_day, end_day, owner) values(
	'Wrzesień', '01-08-2022', '31-08-2022', 1);
insert into budgets_period(name, start_day, end_day, owner) values(
	'Sierpień', '10-08-2022', '10-09-2022', 2);
insert into budgets_period(name, start_day, end_day, owner) values(
	'Wrzesień', '01-09-2022', '30-09-2022', 2);
	
--------------------------------	

insert into budgets_balance(amount, period_id_budgets_period, owner) values(
	3845.5, 1, 1);
insert into budgets_balance(amount, period_id_budgets_period, owner) values(
	4787.50, 2, 1);
insert into budgets_balance(amount, period_id_budgets_period, owner) values(
	8531.41, 3, 2);
insert into budgets_balance(amount, period_id_budgets_period, owner) values(
	8432.54, 4, 2);
	
	
--------------------------------------------

insert into budgets_category(category_name, category_active, owner) values(
	'Food', TRUE, 1);
insert into budgets_category(category_name, category_active,owner) values(
	'Housing', TRUE,  1);
insert into budgets_category(category_name, category_active,owner) values(
	'Other', TRUE, 1);

	
	
	
--------------------------

insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 1, 1, 1);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 1, 2, 1);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 3, 3, 1);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 3, 4, 1);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 2, 1, 2);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 2, 2, 2);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 3, 3, 2);
insert into budgets_monthly_goal(goal, category_id_budgets_category, period_id_budgets_period, owner) values(
	600, 3, 4, 2);
	
	
	--------------------------------
	
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,owner) values(
	15, '20-08-2022', null, 1, 1);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,owner) values(
	2076.45 , '20-08-2022', null, 1, 2);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,owner) values(
	76, '20-08-2022', 'Lokówka', 2, 1);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,owner) values(
	89.50, '20-08-2022', null, 3, 2);
insert into budgets_expenditure(expenditure_amount, expenditure_date, description, 
								category_id_budgets_category,owner) values(
	89.50, '20-08-2022', null, 3, 1);