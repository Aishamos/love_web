#!/usr/bin/env bash
# 设置 MySQL 远程连接：监听所有网卡、授权远程用户、提示防火墙放行。
# 用法：sudo bash setup_mysql_remote.sh <远程来源IP|%> [数据库用户] [数据库名]
set -euo pipefail

REMOTE_IP="${1:?用法: sudo bash setup_mysql_remote.sh <远程IP|%> [数据库用户] [数据库名]}"
DB_USER="${2:-love}"
DB_NAME="${3:-love_web}"

if [ "$REMOTE_IP" = "%" ]; then
  echo "⚠️  你选择了 '%'，将允许任意主机远程连接，存在安全风险。"
fi

read -rsp "请输入数据库用户 '${DB_USER}' 的远程访问密码: " DB_PASSWORD
echo

# 1. 让 MySQL 监听所有网卡
MYSQL_CONF="/etc/mysql/mysql.conf.d/mysqld.cnf"
if [ -f "$MYSQL_CONF" ]; then
  if grep -q "^bind-address" "$MYSQL_CONF"; then
    sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' "$MYSQL_CONF"
  else
    echo "bind-address = 0.0.0.0" >> "$MYSQL_CONF"
  fi
  systemctl restart mysql
else
  echo "未找到 ${MYSQL_CONF}，请手动确保 bind-address = 0.0.0.0"
fi

# 2. 创建/更新远程用户并授权（MySQL root 通过 auth_socket 免密）
mysql -uroot -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'${REMOTE_IP}' IDENTIFIED BY '${DB_PASSWORD}'; ALTER USER '${DB_USER}'@'${REMOTE_IP}' IDENTIFIED BY '${DB_PASSWORD}'; GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'${REMOTE_IP}'; FLUSH PRIVILEGES;"

echo "✅ MySQL 远程连接已配置完成。"
echo "如开启了防火墙，请放行 3306 端口："
if [ "$REMOTE_IP" = "%" ]; then
  echo "  sudo ufw allow 3306"
else
  echo "  sudo ufw allow from ${REMOTE_IP} to any port 3306"
fi
