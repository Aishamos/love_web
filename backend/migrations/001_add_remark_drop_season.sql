-- photos 表：新增 remark 列、删除 season 列
-- 部署顺序：先执行本脚本，再部署新后端代码

ALTER TABLE photos
  ADD COLUMN remark VARCHAR(255) NOT NULL DEFAULT '' AFTER height,
  DROP COLUMN season;
