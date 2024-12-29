def table_row(
      
  username = 'NICK',
  username_color = 'gray',
  level_color = 'white',
  level = 0,
  guild_color = 'white',
  guild = 'NICK',

  wins_color = 'white',
  wins = '-',
  wlr_color = 'white',
  wlr = '-',
  
  finals_color = 'white',
  finals = '-',
  fkdr_color = 'white',
  fkdr = '-',

  kills_color = 'white',
  kills = '-',
  kdr_color = 'white',
  kdr = '-',

  winstreak_color = 'white',
  winstreak = '-'

):
  
  row = f'''
<tr>
  <td id="heads"><img src="https://mc-heads.net/avatar/{username}/8"></td>
  <td style="color: {level_color}">{level}</td>
  <td style="color: rgb{username_color}; text-align: left;">&nbsp;{username}</td>
  <td style="color: {wins_color}">{wins}</td>
  <td style="color: {wlr_color}">{wlr}</td>
  <td style="color: {finals_color}">{finals}</td>
  <td style="color: {fkdr_color}">{fkdr}</td>
  <td style="color: {kills_color}">{kills}</td>
  <td style="color: {kdr_color}">{kdr}</td>
  <td style="color: {winstreak_color}">{winstreak}</td>
  <td style="color: {guild_color}">[{guild}]</td>
</tr>
  '''
  
  return row