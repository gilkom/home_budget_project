CREATE OR REPLACE FUNCTION trigger_function()
   RETURNS TRIGGER
   LANGUAGE PLPGSQL
AS $$
BEGIN
   INSERT INTO budgets_saver(user_id) values(NEW.id);
   RETURN NEW;
END;
$$

CREATE TRIGGER insert_user_biu
	BEFORE INSERT ON auth_user
	FOR EACH ROW
	EXECUTE PROCEDURE trigger_function();