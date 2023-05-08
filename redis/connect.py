import redis

redis_pool = redis.ConnectionPool(host='127.0.0.1', port= 6379, db= 0)
redis_conn = redis.Redis(connection_pool=redis_pool)

# 设置单个kv对
def set_single():
    redis_conn.set("game","lol")


    v = redis_conn.get("game")

    print(v)

# 设置多个kv对
def set_more():
    game_dic = {
        "game:1":"lol",
        "game:2":"cf",
        "game:3":"dnf"
    }

    redis_conn.mset(game_dic)

    m = redis_conn.mget(game_dic.keys())
    print(m)


if __name__=="__main__":
    game_type = redis_conn.type("game:1")
    print(game_type)
    v = redis_conn.smembers()
