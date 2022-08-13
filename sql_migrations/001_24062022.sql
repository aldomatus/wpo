insert into wpo_logic_ctsport(sport_name, sport_slug, sport_status)
values
('Balonmano', 'balonmano', 1),
('Basquetbol', 'basquetbol', 1),
('Beisbol', 'beisbol', 1),
('Críquet', 'críquet', 1),
('Fut 7', 'fut-7', 1),
('Fútbol Americano', 'futbol-americano', 1),
('Fútbol de salón', 'futbol-de-salon', 1),
('Fútbol Soccer', 'futbol-soccer', 1),
('Hockey', 'hockey', 1),
('Hockey sobre césped', 'hockey-sobre-cesped', 1),
('Polo', 'polo', 1),
('Polo acuático', 'polo-acuatico', 1),
('Rugby', 'rugby', 1),
('Sóftbol', 'softbol', 1),
('Tocho bandera', 'tocho-bandera', 1),
('Ultimate Frisbee', 'ultimate-frisbee', 1),
('Voleibol', 'voleibol', 1),
('Voleibol de playa', 'voleibol-de-playa', 1);

insert into users_ctdomainwhitelist(domain_wl_dominio)
values ('gmail.com'),
('hotmail.com'),
('outlook.com'),
('outlook.es'),
('live.com'),
('icloud.com'),
('yahoo.com'),
('aol.com'),
('zohomail.com'),
('gmx.com'),
('gmx.es'),
('protonmail.com'),
('proton.me'),
('tutanota.com'),
('tutanota.de'),
('tutamail.com'),
('tuta.io'),
('keemail.de');

INSERT INTO `users_ctcountry` (`country_id`, `country_name`, `country_slug`, `country_abbreviation`, `country_political_division`, `country_status`) VALUES (1, 'Sin País', 'sin-pais', 'SP', 'NA', 0);
INSERT INTO `users_ctstate` (`state_id`, `state_name`, `state_slug`, `state_status`, `country_id`) VALUES (1, 'Sin Estado', 'sin-estado', 1, 1);
INSERT INTO `users_ctlocation` (`location_id`, `location_name`, `location_slug`, `location_status`, `state_id`) VALUES (1, 'sin-localidad', 'http://www.com', 1, 1);