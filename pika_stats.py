import asyncio, aiohttp

colors = ['lightgray', 'lightcyan', 'lightblue', 'lightgreen', 'lightsalmon', 'lightcoral']

rank_colors = {
    'Champion': (170, 0, 0),     # Red
    'Titan': (255, 170, 0),      # Orange
    'Elite': (85, 255, 255),     # Cyan
    'VIP': (85, 255, 85),        # Green
}


def map_value(x, in_min, in_max, out_min, out_max):
    if x > in_max: return out_max
    return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def ratio(n1=0, n2=0):
    if n1 != 0 and n2 != 0:
        out = n1/n2
    elif n1 != 0 and n2 == 0:
        out = n1
    elif n1 == 0 and n2 != 0:
        out = 0
    elif n1 == 0 and n2 == 0:
        out = 0

    pp = round(out, 2)

    if pp < float(10):
        output = f"{pp:.2f}"
    elif float(100) > pp >= float(10):
        output = f"{pp:.1f}"
    elif pp >= float(100):
        output = str(int(pp))
    
    return output

def ratio_color(ratio):
    if float(ratio) < float(1):
        color = 'red'
    elif float(ratio) > float(1):
        color = 'lime'
    else:
        color = 'white'
    return color

async def stats(username, interval='lifetime', gamemode='all_modes'):
    async with aiohttp.ClientSession() as session:

        profilereq = session.get(f'https://stats.pika-network.net/api/profile/{username}')
        statsreq = session.get(f'https://stats.pika-network.net/api/profile/{username}/leaderboard?type=BEDWARS&interval={interval}&mode={gamemode}')

        profile, stats = await asyncio.gather(profilereq, statsreq)

        if profile.status != 200:
            return username, 'white'

        api = await profile.json()

        level = api['rank']['level']

        value_c = colors

        lvl = level
        if 0 < lvl < 5:
            level_color = 'gray'
        elif 5<=lvl<10 or 40<=lvl<45:
            level_color = 'lime'
        elif 10<=lvl<15 or 45<=lvl<50:
            level_color = 'aqua'
        elif 15<=lvl<20 or 50<=lvl<60:
            level_color = 'pink'
        elif 20<=lvl<25 or  60<=lvl<75:
            level_color = 'orange'
        elif 25<=lvl<30 or 75<=lvl<100:
            level_color = 'yellow'
        elif 30<=lvl<35 or lvl>=100:
            level_color = 'red'
        elif 35 <= lvl < 40:
            level_color = 'white'

        if lvl >= 35: level = f'<b style="color: {level_color}">[{level}]</b>'
        else: level = f'[{level}]'

        
        ranksjson = str(api['ranks'])
        ranklist = ['Champion', 'Titan', 'Elite', 'VIP']
        rank = next((ranks for ranks in ranklist if ranks in ranksjson), None)
        rank_color = rank_colors.get(rank, (170, 170, 170))
        

        if api['clan']:
            guild = api['clan']['tag']
        else:
            guild = '-'
        guild_c = 'white'

        if stats.status != 200:
            return username, rank_color, level_color, level, guild_c, guild

        api = await stats.json()

        # Fetching stats

        def fet(entry):
            js = api[entry]['entries']
            return int(js[0]['value']) if js else 0

        wins    = fet('Wins')
        winc    = value_c[map_value(wins, 0, 1500, 0, 5)]
        loss    = fet('Losses')
        wlr     = ratio(wins, loss)
        wlrc    = ratio_color(wlr)

        fkills  = fet('Final kills')
        fkillsc = value_c[map_value(fkills, 0, 2500, 0, 5)]
        fdeaths = fet('Final deaths')
        fkdr    = ratio(fkills, fdeaths)
        fkdrc   = ratio_color(fkdr)

        kills   = fet('Kills')
        killsc  = value_c[map_value(kills, 0, 8192, 0, 5)]
        deaths  = fet('Deaths')
        kdr     = ratio(kills, deaths)
        kdrc    = ratio_color(kdr)

        wsc     = 'white'
        hws     = fet('Highest winstreak reached')

        return username, rank_color, level_color, level, guild_c, guild, winc, wins, wlrc, wlr, fkillsc, fkills, fkdrc, fkdr, killsc, kills, kdrc, kdr, wsc, hws