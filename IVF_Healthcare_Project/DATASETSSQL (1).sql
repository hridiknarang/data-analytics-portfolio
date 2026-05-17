SELECT * FROM dataset.`reports and dashboards datacsv`;
describe dataset.`reports and dashboards datacsv`;
 #rename columns
ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE `PATIENT NAME AND SURNAME` Patient_name_and_Surname TEXT;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE `Spouse_AGE` Spouse_age INT;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE `Clinical pregnancy: 0:0, Chemical: 1:1 Positive` Pregnancy_type INT;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE `Live Birth` Live_birth INT;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE `ABORTION` Abortion INT;

describe dataset.`reports and dashboards datacsv`;


ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE COLUMN `PROGESTERONE` `Progesterone` float;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE COLUMN `Number_of_Oocytes` `Number_of_oocytes` int;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE COLUMN `Embryo_Tranfer_Day` `Embryo_transfer_day` int;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE COLUMN `ENDOMETRIAL_THICKNESS_ON_THE_DAY_OF_TRANSFER`
`Endometrial_thickness_on_transfer_day` float;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE COLUMN `IND_NUMBER_OF_DAYS` `Ind_number_of_days` int;

ALTER TABLE `dataset`.`reports and dashboards datacsv`
CHANGE COLUMN `Number_of_Embryos_Transferred`
`Number_of_embryos_transferred` int;

#handling missing values
select week_of_birth from `dataset`.`reports and dashboards datacsv`  where week_of_birth  = 0;
update `dataset`.`reports and dashboards datacsv` set week_of_birth  = null where week_of_birth = 0;

select count(*) from `dataset`.`reports and dashboards datacsv` where FSH = 0;
update `dataset`.`reports and dashboards datacsv` set FSH = null where FSH = 0;

select count(*) from `dataset`.`reports and dashboards datacsv`where e2 = ' ';
select count(*) from `dataset`.`reports and dashboards datacsv` where e2 = 0;
update`dataset`. `reports and dashboards datacsv` set e2 = null where e2 = 0;
SET SQL_SAFE_UPDATES=0;

select count(*) from `dataset`.`reports and dashboards datacsv` where progesterone = 0; 
select avg(progesterone) from `dataset`.`reports and dashboards datacsv`;
update `dataset`.`reports and dashboards datacsv` set progesterone = null where progesterone = 0;

select count(*) from `dataset`.`reports and dashboards datacsv` where number_of_oocytes = 0;
select avg(number_of_oocytes) from `dataset`.`reports and dashboards datacsv`;
update `dataset`.`reports and dashboards datacsv` set number_of_oocytes = null where number_of_oocytes = 0;

select count(*) from `dataset`.`reports and dashboards datacsv` where ind_number_of_days = 0;
update `dataset`.`reports and dashboards datacsv`set ind_number_of_days = null where ind_number_of_days = 0;

select * from `dataset`.`reports and dashboards datacsv`;

select count(*) from `dataset`.`reports and dashboards datacsv` where number_of_embryos_transferred = 0;
update `dataset`.`reports and dashboards datacsv` set number_of_embryos_transferred = null where number_of_embryos_transferred = 0;

select count(*) from `dataset`.`reports and dashboards datacsv`where amh = 0;
update `dataset`.`reports and dashboards datacsv` set amh = null where amh = 0;

desc `dataset`.`reports and dashboards datacsv`;
select * from `dataset`.`reports and dashboards datacsv`;


# changing data types
alter table `dataset`.`reports and dashboards datacsv` modify WEEK_OF_BIRTH int;

alter table `dataset`.`reports and dashboards datacsv` modify FSH float;

alter table `dataset`.`reports and dashboards datacsv` modify E2 float;

alter table `dataset`.`reports and dashboards datacsv` modify progesterone int;

alter table `dataset`.`reports and dashboards datacsv` modify number_of_oocytes int;

alter table `dataset`.`reports and dashboards datacsv` modify ind_number_of_days int;

alter table `dataset`.`reports and dashboards datacsv` modify number_of_embryos_transferred int;

alter table `dataset`.`reports and dashboards datacsv` modify amh float;

# Data distribution

select min(age),
max(age), 
avg(age)
from `dataset`.`reports and dashboards datacsv`;

select min(week_of_birth),
max(week_of_birth),
avg(week_of_birth)
from `dataset`.`reports and dashboards datacsv`;

select * from `dataset`.`reports and dashboards datacsv`;

select min(fsh),
max(fsh),
avg(fsh)
from `dataset`.`reports and dashboards datacsv`;

select min(e2),
max(e2),
avg(e2)
from `dataset`.`reports and dashboards datacsv`;

select min(number_of_oocytes),
max(number_of_oocytes),
avg(number_of_oocytes)
from `dataset`.`reports and dashboards datacsv`;

select pregnancy_type, count(*) as total_count
from `dataset`.`reports and dashboards datacsv` group by pregnancy_type
order by total_count desc;

select abortion, count(*) as total_count 
from `dataset`.`reports and dashboards datacsv` group by abortion
order by total_count desc;

select twin, count(*) as total_count
from `dataset`.`reports and dashboards datacsv` group by twin
order by total_count desc;

select indication, count(*) as total_count
from `dataset`.`reports and dashboards datacsv` group by indication
order by total_count desc;

select eu, count(*) as total_count
from `dataset`.`reports and dashboards datacsv` group by eu
order by total_count desc;

select * from `dataset`.`reports and dashboards datacsv`;




















