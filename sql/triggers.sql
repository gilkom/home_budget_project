-- when a new user is created, his category tables are populated with three basic categories
CREATE OR REPLACE FUNCTION trigger_insert_user_categories()
   RETURNS TRIGGER
   LANGUAGE PLPGSQL
AS $$
BEGIN
   INSERT INTO budgets_category(category_name, owner) values('Food',NEW.id);
   INSERT INTO budgets_category(category_name, owner) values('Housing', NEW.id);
   INSERT INTO budgets_category(category_name, owner) values('Other', NEW.id);
   RETURN NEW;
END;
$$


CREATE TRIGGER insert_user_categories_ai
	AFTER INSERT ON auth_user
	FOR EACH ROW
	EXECUTE PROCEDURE trigger_insert_user_categories();

------------------------------------------------------------------------------------

-- when a new period is created, we add a new balance to this period
CREATE OR REPLACE FUNCTION trigger_insert_period_balance()
   RETURNS TRIGGER
   LANGUAGE PLPGSQL
AS $$
BEGIN
	INSERT INTO budgets_balance(amount, period_id_budgets_period, owner) values(0, NEW.period_id, NEW.owner);
   	RETURN NEW;
END;
$$


CREATE TRIGGER insert_period_balance_ai
	AFTER INSERT ON budgets_period
	FOR EACH ROW
	EXECUTE PROCEDURE trigger_insert_period_balance();

------------------------------------------------------------------------------------