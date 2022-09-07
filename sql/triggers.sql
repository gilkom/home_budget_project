CREATE OR REPLACE FUNCTION trigger_function()
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


CREATE TRIGGER insert_user_aiu
	AFTER INSERT ON auth_user
	FOR EACH ROW
	EXECUTE PROCEDURE trigger_function();