import os
import discord
from discord.ext import commands

import discord
from discord.ext import commands

# 인텐트 설정
intents = discord.Intents.default()
intents.members = True          # 멤버 입퇴장 감지
intents.message_content = True  # 명령어(!) 감지

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. 관리자 ID 설정 (본인의 디스코드 ID를 숫자로 입력하세요)
# * 본인 ID 확인법: 개발자 모드 켜기 -> 프로필 우클릭 -> ID 복사
OWNER_ID = 123456789012345678 

# 로그 채널 ID를 저장할 변수
log_channel_id = None

@bot.event
async def on_ready():
    print(f'{bot.user}로 로그인 성공!')
    print("초대 방지 및 입퇴장 로그 기능이 활성화되었습니다.")

import asyncio # 코드 맨 위에 추가

@bot.event
ot.event
async def on_guild_join(guild):
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
        if entry.user.id != OWNER_ID:
            print(f"권한 없는 사용자가 초대함: {entry.user.name}. 즉시 탈퇴합니다.")
            await guild.leave()

# 3. 로그 채널 설정 명령어
@bot.command()
async def 입장로그(ctx):
    global log_channel_id
    log_channel_id = ctx.channel.id
    await ctx.send(f"✅ 입장 로그 채널이 이곳({ctx.channel.name})으로 설정되었습니다.")

@bot.command()
async def 퇴장로그(ctx):
    global log_channel_id
    log_channel_id = ctx.channel.id
    await ctx.send(f"✅ 퇴장 로그 채널이 이곳({ctx.channel.name})으로 설정되었습니다.")

# 4. 입퇴장 로그 출력
@bot.event
async def on_member_join(member):
    if log_channel_id:
        channel = bot.get_channel(log_channel_id)
        if channel:
            embed = discord.Embed(title="입장 로그", color=discord.Color.green())
            embed.description = f"{member.mention}님이 서버에 입장했습니다.\n유저 ID: {member.id}"
            await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    if log_channel_id:
        channel = bot.get_channel(log_channel_id)
        if channel:
            embed = discord.Embed(title="퇴장 로그", color=discord.Color.red())
            embed.description = f"{member.name}님이 서버를 나갔습니다.\n유저 ID: {member.id}"
            await channel.send(embed=embed)

bot.run(os.environ['TOKEN'])
