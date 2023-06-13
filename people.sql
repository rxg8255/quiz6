CREATE TABLE q1c (
  id int IDENTITY(1,1),
  name varchar(255) NOT NULL,
  s_id varchar(255) NOT NULL,
  grade varchar(255) NOT NULL,
  picture_url text NOT NULL,
  notes varchar(1000) DEFAULT NULL,
  PRIMARY KEY (id)
);

INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Dhruvi','TX','99099','100','550','1000010','https://cse6332sa.blob.core.windows.net/images/dhru.jpg','Dhruvi is nice');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Chuck','TX','1000','98','420','','https://cse6332sa.blob.core.windows.net/images/chuck.jpg','Chuck is amazing');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Meena','TX','125000','99','','',' ','Meena is outa here');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Dave','NN','20','40','525','0','https://cse6332sa.blob.core.windows.net/images/dave.jpg','Who is this');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Tuan','CA','','80','-1','',' ','Tuan is gone');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Tavo','CA','220200',' ','','','https://cse6332sa.blob.core.windows.net/images/tavo.jpg','Tavo works very hard');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Nora','TX','-1','80','520','808',' ','');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Susan','OK','255000','84','101','911',' ','Susan is very smart');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Darwin','TN','25','100','','1009','https://cse6332sa.blob.core.windows.net/images/dar.jpg','Darwin is very creative');
INSERT INTO people (name,s_id,grade,picture_url,notes) values ('Sriya','TX','111001','100','221','','https://cse6332sa.blob.core.windows.net/images/sriya.jpg','Sriya is great');