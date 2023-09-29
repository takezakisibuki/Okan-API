-- select 'create database trading' where not exists (select from pg_database where datname='trading');
-- \c trading

create table if not exists users (
  id serial not null
  , name character varying not null
  , constraint users_PKC primary key (id)
) ;

