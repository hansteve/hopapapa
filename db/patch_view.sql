-- 20170419
-- 视频资源view
DROP VIEW view_video;
CREATE VIEW view_video AS
SELECT id as res_id,type as res_type,name,poster,status,letv_video_id,user_id,
  letv_video_unique,url,ext,description,unix_timestamp(create_ts) as create_ts,
  concat('http://www.hopapapa.com/fabu/le_video.html?res_id=',id) as detail_url
FROM video WHERE is_del = 0 ORDER BY create_ts DESC ;
-- 文章资源view
DROP VIEW view_article;
CREATE VIEW view_article AS
SELECT id as res_id,6 as res_type,name,poster,posters->"$.posters" as posters,
  concat('http://www.hopapapa.com/fabu/news.html?id=',id) as url,content,
  concat('http://www.hopapapa.com/fabu/news.html?id=',id) as detail_url ,
  description,unix_timestamp(create_ts) as create_ts FROM article WHERE
  is_del = 0 ORDER BY create_ts DESC ;
-- 音频
DROP VIEW view_audio;
CREATE VIEW view_audio AS
SELECT id as res_id,11 as res_type,name,poster, url,ext,
  description,unix_timestamp(create_ts) as create_ts ,
  concat('http://www.hopapapa.com/fabu/le_audio.html?res_id=',id) as detail_url
  FROM audio WHERE
  is_del = 0 ORDER BY create_ts DESC ;
-- 图片
DROP VIEW view_image;
CREATE VIEW view_image as
SELECT id as res_id,4 as res_type,user_id,url,url as poster,unix_timestamp(create_ts)
  as create_ts FROM image WHERE is_del =0 ORDER BY create_ts DESC ;

-- 评论
DROP VIEW view_comment;
CREATE VIEW view_comment as
select id AS comment_id,user_id,res_id,res_type,content,to_user_id ,UNIX_TIMESTAMP(create_ts)
  as create_ts  from comment WHERE is_del = 0 ORDER BY create_ts DESC ;

-- 回复
DROP VIEW view_reply;
CREATE VIEW view_reply as
select id AS reply_id,user_id,res_id as comment_id,res_type,content,to_user_id ,UNIX_TIMESTAMP(create_ts)
  as create_ts  from comment WHERE is_del = 0 and res_type = 3 ORDER BY create_ts ASC ;

-- 用户
DROP VIEW view_user;
CREATE VIEW view_user as
select id AS user_id,id as res_id,1 as res_type,name,mobile,portrait,gender,
  age,status,ext ,banner,last_upload,
  UNIX_TIMESTAMP(create_ts) as create_ts  from user WHERE is_del = 0
ORDER BY create_ts DESC ;

-- 推送
DROP VIEW view_push;
CREATE VIEW view_push as
select id as push_id,'http://pic.hopapapa.com/static/Mask@2x.png' as portrait,
description,open_type,res_id,res_type,url, UNIX_TIMESTAMP(create_ts)
  as create_ts  from push WHERE is_del = 0  ORDER BY create_ts ASC ;

-- 最后上传位置的时间
DROP view view_last_location_time;
CREATE view view_last_location_time as
SELECT user_id,UNIX_TIMESTAMP(max(create_ts)) as create_ts FROM location GROUP BY user_id;

-- 集合
DROP VIEW view_collection;
CREATE VIEW view_collection AS
  SELECT
    id                        AS res_id,
    12                        AS res_type,
    name,
    poster,
    description,
    UNIX_TIMESTAMP(create_ts) AS create_ts
  FROM collection
  WHERE is_del = 0 AND is_offline = 0
  ORDER BY create_ts ASC;

-- 热门资源
DROP VIEW view_hot_res;
CREATE VIEW view_hot_res AS
  SELECT
    res_id,
    res_type,
    count(0) AS total,
    ''       AS name,
    ''       AS poster,
    ''       AS description
  FROM action
  WHERE type = 27 AND res_type != 1
  GROUP BY res_id, res_type
  ORDER BY total DESC;

-- 热门用户
DROP VIEW view_hot_user;
CREATE VIEW view_hot_user AS
  SELECT
    res_id,
    res_type,
    count(0) AS total,
    ''       AS name,
    ''       AS poster,
    ''       AS description
  FROM action
  WHERE type = 27 AND res_type = 1
  GROUP BY res_id, res_type
  ORDER BY total DESC;



