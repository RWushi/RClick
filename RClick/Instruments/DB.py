from .Config import DB


async def add_new_user(user_id):
    async with DB() as conn:
        await conn.execute('''
            INSERT INTO users (id) 
            VALUES ($1) ON CONFLICT (id) DO NOTHING
        ''', user_id)


async def language_set(user_id, language_code):
    async with DB() as conn:
        await conn.execute('UPDATE users SET language = $2 WHERE id = $1', user_id, language_code)


async def create_game(user_id, bet, account):
    async with DB() as conn:
        allowed = await conn.fetchval('''SELECT CASE WHEN $3 = 'demo' THEN demo >= $2
        WHEN $3 = 'real' THEN real >= $2 END FROM users WHERE id = $1
        ''', user_id, bet, account)
        if allowed:
            await conn.execute('''
                INSERT INTO games (host, bet, account) 
                VALUES ($1, $2, $3)
            ''', user_id, bet, account)
            return True
        else:
            return False


async def cancel_game(user_id):
    async with DB() as conn:
        await conn.execute('''
            UPDATE games SET status = 'canceled' WHERE id =
            (SELECT id FROM games WHERE host = $1 AND status = 'waiting')
            ''', user_id)


async def get_games(account, lower=None, upper=None, bet=None):
    query = '''SELECT id, bet FROM games WHERE account = $1
               AND status = 'waiting' AND bet '''
    params = [account]

    if lower:
        query += '>= $2'
        params.append(lower)
        if upper:
            query += ' AND bet <= $3'
            params.append(upper)
    elif bet:
        query += '= $2'
        params.append(bet)

    async with DB() as conn:
        games = await conn.fetch(query, *params)
    return games


async def check_game(game_id, opponent_id):
    async with DB() as conn:
        exists = await conn.fetchval('SELECT EXISTS(SELECT 1 FROM games WHERE id = $1)', game_id)
        if exists:
            free = await conn.fetchval('''SELECT EXISTS(SELECT 1 FROM games
                                       WHERE id = $1 AND status = 'waiting')''', game_id)
            if free:
                await conn.execute('''UPDATE games SET guest = $2, status = 'in progress'
                                   WHERE id = $1''', game_id, opponent_id)
                host_id = await conn.fetchval('SELECT host FROM games WHERE id = $1', game_id)
                return host_id
            return 'not_free'
        return 'not_exists'


async def show_account(user_id):
    async with DB() as conn:
        result = await conn.fetchrow('SELECT real, demo FROM users WHERE id = $1', user_id)
        real = result['real']
        demo = result['demo']
    return real, demo


async def check_game_id(game_id):
    async with DB() as conn:
        exists = await conn.fetchval('SELECT EXISTS(SELECT 1 FROM games WHERE id = $1)', game_id)
    return exists


async def check_relevance_game(game_id, user_id):
    async with DB() as conn:
        exists = await conn.fetchval('''
        SELECT EXISTS(SELECT 1 FROM games WHERE id = $1
        AND (host = $2 OR guest = $2))''', game_id, user_id)
    return exists


async def get_opponent_id(game_id, user_id):
    async with DB() as conn:
        opponent_id = await conn.fetchval('''
        SELECT CASE WHEN host = $2 THEN guest
        ELSE host END AS opponent_id
        FROM games WHERE id = $1
        ''', game_id, user_id)
    return opponent_id


async def warning_check(user_id):
    async with DB() as conn:
        warning = await conn.fetchval('SELECT warning FROM users WHERE id = $1', user_id)
    return warning


async def fine(accused_id, accuser_id, game_id):
    async with DB() as conn:
        bet = await conn.fetchval('SELECT bet FROM games WHERE id = $1', game_id)
        await conn.execute('UPDATE users SET warning = True, real = real - $2 WHERE id = $1', accused_id, bet*2)
        amount = await conn.fetchval("""
            UPDATE users SET real =
            CASE WHEN d.real < $3 THEN real + d.real ELSE real + $3 END
            FROM (SELECT real FROM users WHERE id = $1) AS d
            WHERE users.id = $2
            RETURNING 
                CASE WHEN d.real < $3 THEN d.real ELSE $3 END
        """, accuser_id, accused_id, bet*2)
    return amount


async def full_fine(accused_id, accuser_id):
    async with DB() as conn:
        await conn.execute('UPDATE users SET warning = True, real = 0 WHERE id = $1', accused_id)
        amount = await conn.fetchval("""
            UPDATE users SET real = real + d.real
            FROM (SELECT real FROM users WHERE id = $1) AS d
            WHERE users.id = $2
            RETURNING d.real
        """, accused_id, accuser_id)
    return amount


async def full_fine_w(accused_id, accuser_id):
    async with DB() as conn:
        await conn.execute('UPDATE users SET real = 0 WHERE id = $1', accused_id)
        amount = await conn.fetchval("""
            UPDATE users SET real = real + d.real
            FROM (SELECT real FROM users WHERE id = $1) AS d
            WHERE users.id = $2
            RETURNING d.real
        """, accused_id, accuser_id)
    return amount
