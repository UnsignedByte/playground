# -*- coding: utf-8 -*-
# @Author: UnsignedByte
# @Date:   15:20:25, 17-Sep-2020
# @Last Modified by:   UnsignedByte
# @Last Modified time: 15:44:12, 17-Sep-2020
# -*- coding: utf-8 -*-
# @Author: UnsignedByte
# @Date:	 23:20:21, 17-Jun-2020
# @Last Modified by:   UnsignedByte
# @Last Modified time: 21:53:57, 06-Aug-2020

import discord
import asyncio

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

class Client(discord.Client):
	async def on_ready(self):
		# create 10 guilds 
		# for i in range(10):
		# 	g = await self.create_guild("test_guild");
		# 	c = await g.create_text_channel('invite');
		# 	i = await c.create_invite();
		# 	print(i);
		# 	print(i.code);

		# give admin afterward
		# for g in self.guilds:
		# 	r = await g.create_role(name='admin', permissions=discord.Permissions(administrator=True));
		# 	await g.get_member(418827664304898048).add_roles(r);
	async def on_message(self, msg):
		pass;

bot = Client()

with open('token.txt', 'r') as f:
	bot.run(f.read().strip(), bot=True)
