from datetime import datetime, timezone, timedelta

CN_TZ = timezone(timedelta(hours=8))


def now_local():
    """北京时间墙上时间（MySQL DATETIME 无时区，统一存北京时区）"""
    return datetime.now(CN_TZ).replace(tzinfo=None)
