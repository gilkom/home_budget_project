
-- object: public.budgets_category | type: TABLE --
-- DROP TABLE IF EXISTS public.budgets_category CASCADE;

CREATE TABLE IF NOT EXISTS public.budgets_category
(
    category_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    category_name character varying(20) COLLATE pg_catalog."default" NOT NULL,
    category_active BOOLEAN NOT NULL,
    owner bigint NOT NULL,
    CONSTRAINT budgets_category_pkey PRIMARY KEY (category_id)
);

-- ddl-end --
ALTER TABLE public.budgets_category OWNER TO postgres;
-- ddl-end --

-- object: public.budgets_monthly_goal | type: TABLE --
-- DROP TABLE IF EXISTS public.budgets_monthly_goal CASCADE;
CREATE TABLE public.budgets_monthly_goal (
    monthly_goal_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
	goal numeric(8,2) NOT NULL,
	category_id_budgets_category bigint NOT NULL,
	period_id_budgets_period bigint NOT NULL,
	owner bigint NOT NULL,
	CONSTRAINT budgets_monthly_goal_pk PRIMARY KEY (monthly_goal_id)

);
-- ddl-end --
ALTER TABLE public.budgets_monthly_goal OWNER TO postgres;
-- ddl-end --

-- object: public.budgets_balance | type: TABLE --
-- DROP TABLE IF EXISTS public.budgets_balance CASCADE;
CREATE TABLE public.budgets_balance (
    balance_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
	amount numeric(8,2) NOT NULL,
	period_id_budgets_period bigint NOT NULL,
	owner bigint NOT NULL,
	CONSTRAINT budgets_balance_pk PRIMARY KEY (balance_id)

);
-- ddl-end --
ALTER TABLE public.budgets_balance OWNER TO postgres;
-- ddl-end --

-- object: public.budgets_expenditure | type: TABLE --
-- DROP TABLE IF EXISTS public.budgets_expenditure CASCADE;
CREATE TABLE public.budgets_expenditure (
	expenditure_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
	expenditure_amount numeric(8,2) NOT NULL,
	expenditure_date date NOT NULL,
	description varchar(300),
	category_id_budgets_category bigint NOT NULL,
	owner bigint NOT NULL,
	CONSTRAINT "EXPENDITURE_pk" PRIMARY KEY (expenditure_id)

);
-- ddl-end --
ALTER TABLE public.budgets_expenditure OWNER TO postgres;
-- ddl-end --

-- object: public.budgets_period | type: TABLE --
-- DROP TABLE IF EXISTS public.budgets_period CASCADE;
CREATE TABLE public.budgets_period (
	period_id bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
	name varchar(30) NOT NULL,
	start_day date NOT NULL,
	end_day date NOT NULL,
	owner bigint NOT NULL,
	CONSTRAINT "PERIOD_pk" PRIMARY KEY (period_id)

);
-- ddl-end --
ALTER TABLE public.budgets_period OWNER TO postgres;
-- ddl-end --

-- object: budgets_saver_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_expenditure DROP CONSTRAINT IF EXISTS budgets_saver_fk CASCADE;
ALTER TABLE public.budgets_expenditure ADD CONSTRAINT owner_fk FOREIGN KEY (owner)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: budgets_saver_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_monthly_goal DROP CONSTRAINT IF EXISTS budgets_saver_fk CASCADE;
ALTER TABLE public.budgets_monthly_goal ADD CONSTRAINT owner_fk FOREIGN KEY (owner)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: budgets_saver_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_balance DROP CONSTRAINT IF EXISTS budgets_saver_fk CASCADE;
ALTER TABLE public.budgets_balance ADD CONSTRAINT owner_fk FOREIGN KEY (owner)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: budgets_period_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_balance DROP CONSTRAINT IF EXISTS budgets_period_fk CASCADE;
ALTER TABLE public.budgets_balance ADD CONSTRAINT budgets_period_fk FOREIGN KEY (period_id_budgets_period)
REFERENCES public.budgets_period (period_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: budgets_category_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_expenditure DROP CONSTRAINT IF EXISTS budgets_category_fk CASCADE;
ALTER TABLE public.budgets_expenditure ADD CONSTRAINT budgets_category_fk FOREIGN KEY (category_id_budgets_category)
REFERENCES public.budgets_category (category_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: budgets_category_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_monthly_goal DROP CONSTRAINT IF EXISTS budgets_category_fk CASCADE;
ALTER TABLE public.budgets_monthly_goal ADD CONSTRAINT budgets_category_fk FOREIGN KEY (category_id_budgets_category)
REFERENCES public.budgets_category (category_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: budgets_saver_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_period DROP CONSTRAINT IF EXISTS budgets_saver_fk CASCADE;
ALTER TABLE public.budgets_period ADD CONSTRAINT owner_fk FOREIGN KEY (owner)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

ALTER TABLE public.budgets_category ADD CONSTRAINT owner_fk FOREIGN KEY (owner)
REFERENCES public.auth_user (id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;

-- object: budgets_period_fk | type: CONSTRAINT --
-- ALTER TABLE public.budgets_monthly_goal DROP CONSTRAINT IF EXISTS budgets_period_fk CASCADE;
ALTER TABLE public.budgets_monthly_goal ADD CONSTRAINT budgets_period_fk FOREIGN KEY (period_id_budgets_period)
REFERENCES public.budgets_period (period_id) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- alter table budgets_expenditure drop CONSTRAINT expenditure_nonnegative;
alter table budgets_expenditure add constraint expenditure_nonnegative check(expenditure_amount >= 0);

ALTER SEQUENCE budgets_category_category_id_seq RESTART WITH 1;
ALTER SEQUENCE budgets_expenditure_expenditure_id_seq RESTART WITH 1;
ALTER SEQUENCE budgets_period_period_id_seq RESTART WITH 1;
ALTER SEQUENCE budgets_balance_balance_id_seq RESTART WITH 1;
ALTER SEQUENCE budgets_monthly_goal_monthly_goal_id_seq RESTART WITH 1;


---------------------------------------

alter table budgets_monthly_goal
add unique (category_id_budgets_category, period_id_budgets_period, owner);