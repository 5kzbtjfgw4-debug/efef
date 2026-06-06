# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

import discord
from discord import app_commands


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
SERVER_ICON_PATH = Path(os.getenv("SERVER_ICON_PATH", "assets/server-icon.png"))

BOT_VERSION = "CLAZ FULL TICKET SYSTEM v3"
SERVER_NAME = "Claz Services"
BRAND_COLOR = discord.Color.from_rgb(255, 145, 35)
GOLD_COLOR = discord.Color.from_rgb(255, 205, 75)
DANGER_COLOR = discord.Color.from_rgb(220, 53, 69)

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN Railway variable.")

GUILD_ID = int(GUILD_ID) if GUILD_ID else None

OWNER_ROLES = ["Owner", "Co Owner"]
ADMIN_ROLES = ["Owner", "Co Owner", "Head Admin", "Admin"]
STAFF_ROLES = [
    "Owner", "Co Owner", "Head Admin", "Admin", "Shop Manager",
    "Ticket Manager", "Builder Manager", "Partner Manager",
    "Senior Staff", "Staff", "Trial Staff",
]
BUILDER_TIERS = ["Trial Builder", "Junior Builder", "Senior Builder", "Expert Builder"]
TRUSTED_SKELLY_ROLES = ["Trusted Buyer", "Trusted Seller"]

ROLE_SPECS = [
    ("Owner", 0xFFB000, discord.Permissions(administrator=True), False),
    ("Co Owner", 0xFF7A1A, discord.Permissions(administrator=True), False),
    ("Head Admin", 0xE84D2A, discord.Permissions(administrator=True), False),
    ("Admin", 0xD93838, discord.Permissions(administrator=True), False),
    ("Shop Manager", 0xFF9F1C, discord.Permissions(manage_guild=True, manage_roles=True, manage_channels=True, manage_messages=True, kick_members=True, ban_members=True, moderate_members=True), False),
    ("Ticket Manager", 0xF7B731, discord.Permissions(manage_channels=True, manage_messages=True), False),
    ("Builder Manager", 0xC77DFF, discord.Permissions(manage_channels=True, manage_messages=True), False),
    ("Partner Manager", 0x7B61FF, discord.Permissions(manage_channels=True, manage_messages=True), False),
    ("Senior Staff", 0x4EA8DE, discord.Permissions(manage_messages=True, moderate_members=True), False),
    ("Staff", 0x72C3FC, discord.Permissions(manage_messages=True, moderate_members=True), False),
    ("Trial Staff", 0xA9DEF9, discord.Permissions(manage_messages=True), False),
    ("Expert Builder", 0xFFD166, discord.Permissions(), False),
    ("Senior Builder", 0xF9C74F, discord.Permissions(), False),
    ("Junior Builder", 0x90BE6D, discord.Permissions(), False),
    ("Trial Builder", 0x43AA8B, discord.Permissions(), False),
    ("Middleman", 0x7AA7FF, discord.Permissions(manage_messages=True), False),
    ("Trusted Buyer", 0x2EC4B6, discord.Permissions(), False),
    ("Trusted Seller", 0x06D6A0, discord.Permissions(), False),
    ("Supplier", 0x2BD9FE, discord.Permissions(), False),
    ("Partner", 0xB07CFF, discord.Permissions(), False),
    ("VIP Customer", 0xF6C945, discord.Permissions(), False),
    ("Customer", 0xF9844A, discord.Permissions(), False),
    ("Restock Ping", 0xFFB703, discord.Permissions(), True),
    ("Giveaway Ping", 0xFB8500, discord.Permissions(), True),
    ("Build Ping", 0xC77DFF, discord.Permissions(), True),
    ("Skelly Ping", 0x8ECAE6, discord.Permissions(), True),
    ("Member", 0xAAB7C4, discord.Permissions(), False),
    ("Muted", 0x2B2D31, discord.Permissions(), False),
]

CLAIMABLE_ROLES = [
    ("Member", "member", "Member"),
    ("Customer", "customer", "Customer"),
    ("Restock Ping", "restock_ping", "Restock Ping"),
    ("Giveaway Ping", "giveaway_ping", "Giveaway Ping"),
    ("Build Ping", "build_ping", "Build Ping"),
    ("Skelly Ping", "skelly_ping", "Skelly Ping"),
]

TICKET_CONFIGS = {
    "build": {
        "label": "Base Build",
        "prefix": "build",
        "panel_channel": "base-build-ticket",
        "panel_title": "Base Build Tickets",
        "panel_description": "Open a build ticket for Donut SMP bases, farms, vaults, walls, interiors, rooms, or custom projects.\n\nBudget routing:\n- 10m or less: Trial Builder and higher\n- 15m or less: Junior Builder and higher\n- 25m or less: Senior Builder and higher\n- Above 25m: Expert Builder",
        "modal_title": "Base Build Request",
        "fields": [
            ("budget", "Budget", "Example: 10m, 15m, 25m, 50m", False),
            ("build_type", "Build Type", "Base, farm, vault, wall, interior, etc.", False),
            ("details", "Build Details", "Size, style, blocks, deadline, location, etc.", True),
        ],
    },
    "buy_skelly": {
        "label": "Buy Skellies",
        "prefix": "buy-skelly",
        "panel_channel": "buy-skellies-ticket",
        "panel_title": "Buy Skellies",
        "panel_description": "Open this ticket if you want to buy skellies.",
        "modal_title": "Buy Skellies",
        "fields": [
            ("amount", "How many are you buying?", "Example: 2 skellies", False),
            ("budget", "Budget / Offer", "Example: 30m total or 15m each", False),
            ("details", "Extra Details", "Payment method, urgency, questions, etc.", True),
        ],
    },
    "sell_skelly": {
        "label": "Sell Skellies",
        "prefix": "sell-skelly",
        "panel_channel": "sell-skellies-ticket",
        "panel_title": "Sell Skellies",
        "panel_description": "Open this ticket if you want to sell skellies.",
        "modal_title": "Sell Skellies",
        "fields": [
            ("amount", "How many are you selling?", "Example: 3 skellies", False),
            ("price", "Asking Price", "Example: 45m total or 15m each", False),
            ("details", "Proof / Extra Details", "Proof, location, and anything important.", True),
        ],
    },
    "report": {
        "label": "Report User",
        "prefix": "report",
        "panel_channel": "report-user-ticket",
        "panel_title": "Report A User",
        "panel_description": "Reports are private. Only owners can answer report tickets.",
        "modal_title": "Report User",
        "fields": [
            ("user_id", "User ID", "Paste the Discord user ID you are reporting.", False),
            ("reason", "What Happened?", "Explain what happened clearly.", True),
            ("evidence", "Evidence", "Links, screenshots, dates, witnesses, etc.", True),
        ],
    },
}


def role_by_name(guild: discord.Guild, name: str):
    return discord.utils.get(guild.roles, name=name)


def has_any_role(member: discord.Member, role_names: list[str]) -> bool:
    names = {role.name for role in member.roles}
    return bool(names.intersection(role_names))


def parse_money_to_millions(value: str) -> float | None:
    cleaned = value.lower().replace(",", "").replace("$", "").strip()
    match = re.search(r"(\d+(?:\.\d+)?)\s*([mb]?)", cleaned)
    if not match:
        return None
    amount = float(match.group(1))
    if match.group(2) == "b":
        amount *= 1000
    return amount


def builder_route_for_budget(budget_text: str) -> tuple[str, list[str]]:
    millions = parse_money_to_millions(budget_text)
    if millions is None or millions <= 10:
        index = 0
    elif millions <= 15:
        index = 1
    elif millions <= 25:
        index = 2
    else:
        index = 3

    tier = BUILDER_TIERS[index]
    eligible = BUILDER_TIERS[index:] + ["Builder Manager"] + ADMIN_ROLES
    return tier, eligible


def claim_route(ticket_type: str, data: dict[str, str]) -> tuple[str, list[str]]:
    if ticket_type == "build":
        return builder_route_for_budget(data.get("budget", ""))
    if ticket_type in {"buy_skelly", "sell_skelly"}:
        return "Trusted Skelly Team", TRUSTED_SKELLY_ROLES + ADMIN_ROLES
    if ticket_type == "report":
        return "Owner Only", ["Owner"]
    return "Staff", STAFF_ROLES


def clean_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9-]+", "-", value.lower()).strip("-")
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned[:50] or "ticket"


def build_topic(ticket_type: str, owner_id: int, claim_roles: list[str], claimed_by: int = 0):
    return (
        f"claz_ticket|type={ticket_type}|owner={owner_id}|claimed={claimed_by}"
        f"|claim_roles={','.join(claim_roles)}"
    )


def parse_topic(topic: str | None) -> dict[str, str]:
    if not topic or not topic.startswith("claz_ticket"):
        return {}
    data = {}
    for part in topic.split("|")[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            data[key] = value
    return data


def ticket_claim_roles(channel: discord.TextChannel) -> list[str]:
    data = parse_topic(channel.topic)
    return [role for role in data.get("claim_roles", "").split(",") if role]


def ticket_owner_id(channel: discord.TextChannel) -> int | None:
    data = parse_topic(channel.topic)
    owner = data.get("owner")
    return int(owner) if owner and owner.isdigit() else None


def can_claim(member: discord.Member, channel: discord.TextChannel) -> bool:
    return member.guild_permissions.administrator or has_any_role(member, ticket_claim_roles(channel))


def can_close(member: discord.Member, channel: discord.TextChannel) -> bool:
    return can_claim(member, channel) or ticket_owner_id(channel) == member.id


async def send_or_edit(channel: discord.TextChannel, marker: str, embed: discord.Embed, view: discord.ui.View | None = None):
    embed.set_footer(text=marker)
    async for message in channel.history(limit=30):
        if client.user and message.author.id == client.user.id and message.embeds and message.embeds[0].footer and message.embeds[0].footer.text == marker:
            await message.edit(embed=embed, view=view)
            return False
    await channel.send(embed=embed, view=view)
    return True


class RoleButton(discord.ui.Button):
    def __init__(self, label: str, custom_id: str, role_name: str):
        super().__init__(label=label, style=discord.ButtonStyle.secondary, custom_id=f"claz_role_{custom_id}")
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("Use this inside the server.", ephemeral=True)
            return
        role = role_by_name(interaction.guild, self.role_name)
        if role is None:
            await interaction.response.send_message(f"Missing role: {self.role_name}", ephemeral=True)
            return
        try:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role, reason="Role button")
                await interaction.response.send_message(f"Removed {role.mention}.", ephemeral=True)
            else:
                await interaction.user.add_roles(role, reason="Role button")
                await interaction.response.send_message(f"Added {role.mention}.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I cannot manage that role. Move my bot role higher.", ephemeral=True)


class ClaimRolesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for label, custom_id, role_name in CLAIMABLE_ROLES:
            self.add_item(RoleButton(label, custom_id, role_name))


class TicketOpenButton(discord.ui.Button):
    def __init__(self, ticket_type: str):
        config = TICKET_CONFIGS[ticket_type]
        super().__init__(
            label=f"Open {config['label']} Ticket",
            style=discord.ButtonStyle.primary if ticket_type != "report" else discord.ButtonStyle.danger,
            custom_id=f"claz_open_{ticket_type}",
        )
        self.ticket_type = ticket_type

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketModal(self.ticket_type))


class TicketPanelView(discord.ui.View):
    def __init__(self, ticket_type: str):
        super().__init__(timeout=None)
        self.add_item(TicketOpenButton(ticket_type))


class TicketControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.success, custom_id="claz_claim_ticket")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("Use this in a ticket channel.", ephemeral=True)
            return
        if not isinstance(interaction.user, discord.Member) or not can_claim(interaction.user, interaction.channel):
            await interaction.response.send_message("You cannot claim this ticket.", ephemeral=True)
            return

        data = parse_topic(interaction.channel.topic)
        if data.get("claimed") and data.get("claimed") != "0":
            await interaction.response.send_message("This ticket is already claimed.", ephemeral=True)
            return

        topic = build_topic(
            data.get("type", "unknown"),
            int(data.get("owner", "0")),
            ticket_claim_roles(interaction.channel),
            interaction.user.id,
        )
        await interaction.channel.edit(topic=topic, reason=f"Claimed by {interaction.user}")
        await interaction.response.send_message(f"{interaction.user.mention} claimed this ticket.")

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="claz_close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("Use this in a ticket channel.", ephemeral=True)
            return
        if not isinstance(interaction.user, discord.Member) or not can_close(interaction.user, interaction.channel):
            await interaction.response.send_message("You cannot close this ticket.", ephemeral=True)
            return
        await interaction.response.send_message("Closing ticket.", ephemeral=True)
        await interaction.channel.delete(reason=f"Closed by {interaction.user}")


class TicketModal(discord.ui.Modal):
    def __init__(self, ticket_type: str):
        self.ticket_type = ticket_type
        config = TICKET_CONFIGS[ticket_type]
        super().__init__(title=config["modal_title"])
        self.inputs = {}
        for key, label, placeholder, paragraph in config["fields"]:
            item = discord.ui.TextInput(
                label=label,
                placeholder=placeholder,
                required=True,
                max_length=900 if paragraph else 120,
                style=discord.TextStyle.paragraph if paragraph else discord.TextStyle.short,
            )
            self.inputs[key] = item
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("Use tickets inside the server.", ephemeral=True)
            return
        data = {key: str(item.value).strip() for key, item in self.inputs.items()}
        try:
            channel = await create_ticket(interaction, self.ticket_type, data)
        except discord.Forbidden:
            await interaction.response.send_message("I need Manage Channels to create tickets.", ephemeral=True)
            return
        await interaction.response.send_message(f"Ticket opened: {channel.mention}", ephemeral=True)


class ClazBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(ClaimRolesView())
        for ticket_type in TICKET_CONFIGS:
            self.add_view(TicketPanelView(ticket_type))
        self.add_view(TicketControls())

        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}.")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} global command(s).")


client = ClazBot()


@client.event
async def on_ready():
    print(f"Logged in as {client.user} | {BOT_VERSION}")


@client.event
async def on_member_join(member: discord.Member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel is None:
        channel = member.guild.system_channel
    if channel is None:
        return

    embed = discord.Embed(
        title="Welcome to Claz Services",
        description=(
            f"{member.mention}, welcome in.\n\n"
            "Open a ticket for base builds, skelly buying/selling, support, or reports. "
            "Check rules, products, prices, and restocks before ordering."
        ),
        color=BRAND_COLOR,
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Member Count", value=f"#{member.guild.member_count}", inline=True)
    embed.set_footer(text="Claz Services | Donut SMP Fortune Shop")
    await channel.send(content=f"Welcome {member.mention}!", embed=embed)


async def ensure_roles(guild: discord.Guild):
    roles = {}
    created = 0
    updated = 0
    warnings = []
    for name, color, permissions, mentionable in reversed(ROLE_SPECS):
        role = role_by_name(guild, name)
        if role is None:
            try:
                role = await guild.create_role(name=name, colour=discord.Color(color), permissions=permissions, mentionable=mentionable, reason="Claz Services revamp")
                created += 1
            except discord.Forbidden:
                warnings.append(f"Could not create role: {name}")
                continue
        else:
            try:
                if not role.managed:
                    await role.edit(colour=discord.Color(color), permissions=permissions, mentionable=mentionable, reason="Claz Services revamp")
                    updated += 1
            except discord.Forbidden:
                warnings.append(f"Could not update role: {name}")
        roles[name] = role
    return roles, created, updated, warnings


async def fix_role_hierarchy(guild: discord.Guild, roles: dict[str, discord.Role]):
    warnings = []
    bot_member = guild.me
    if bot_member is None:
        return ["Could not read bot member for hierarchy."]

    top_position = bot_member.top_role.position - 1
    if top_position <= 0:
        return ["Move the bot role higher so it can reorder roles."]

    positions = {}
    position = top_position
    for name, *_ in ROLE_SPECS:
        role = roles.get(name)
        if role is None or role.managed:
            continue
        if role >= bot_member.top_role:
            warnings.append(f"Could not move {name}; it is above/equal to the bot role.")
            continue
        positions[role] = position
        position -= 1
        if position <= 0:
            warnings.append("Bot role is not high enough to place every role.")
            break

    if positions:
        try:
            await guild.edit_role_positions(positions=positions, reason="Claz role hierarchy fix")
        except discord.Forbidden:
            warnings.append("Could not edit role hierarchy. Move bot role higher.")
    return warnings


async def give_runner_owner_role(guild: discord.Guild, member: discord.Member, roles: dict[str, discord.Role]):
    role = roles.get("Owner")
    if role is None or role in member.roles:
        return None
    if guild.me is None or role >= guild.me.top_role:
        return "Could not give command runner Owner role. Move bot role higher."
    try:
        await member.add_roles(role, reason="Revamp command runner")
    except discord.Forbidden:
        return "Could not give command runner Owner role."
    return None


async def brand_server(guild: discord.Guild):
    warnings = []
    edit_kwargs = {"name": SERVER_NAME, "reason": "Claz Services branding"}
    if SERVER_ICON_PATH.exists():
        edit_kwargs["icon"] = SERVER_ICON_PATH.read_bytes()
    else:
        warnings.append("Icon not changed. Add your image as assets/server-icon.png.")
    try:
        await guild.edit(**edit_kwargs)
    except discord.Forbidden:
        warnings.append("Could not rename/set icon. Bot needs Manage Server.")
    except discord.HTTPException:
        warnings.append("Could not set icon. Use a smaller PNG/JPG.")
    return warnings


def get_roles(roles: dict, names: list[str]):
    return [roles[name] for name in names if roles.get(name)]


def overwrites_for(guild: discord.Guild, roles: dict, mode: str):
    everyone = guild.default_role
    muted = roles.get("Muted")

    if mode == "readonly":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True)}
        for role in get_roles(roles, STAFF_ROLES):
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, read_message_history=True)
    elif mode == "staff":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=False)}
        for role in get_roles(roles, STAFF_ROLES):
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    elif mode == "hidden":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=False)}
    elif mode == "panel":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=True, send_messages=False, read_message_history=True)}
        for role in get_roles(roles, STAFF_ROLES):
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, read_message_history=True)
    elif mode == "voice":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)}
    else:
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)}

    if muted:
        overwrites[muted] = discord.PermissionOverwrite(send_messages=False, add_reactions=False, speak=False)
    return overwrites


async def ensure_category(guild: discord.Guild, name: str, overwrites: dict):
    category = discord.utils.get(guild.categories, name=name)
    if category is None:
        return await guild.create_category(name=name, overwrites=overwrites, reason="Claz revamp")
    await category.edit(overwrites=overwrites, reason="Claz revamp")
    return category


async def ensure_text(guild: discord.Guild, category: discord.CategoryChannel, name: str, overwrites: dict):
    channel = discord.utils.get(guild.text_channels, name=name)
    if channel is None:
        return await guild.create_text_channel(name=name, category=category, overwrites=overwrites, reason="Claz revamp")
    await channel.edit(category=category, overwrites=overwrites, reason="Claz revamp")
    return channel


async def ensure_voice(guild: discord.Guild, category: discord.CategoryChannel, name: str, overwrites: dict):
    channel = discord.utils.get(guild.voice_channels, name=name)
    if channel is None:
        return await guild.create_voice_channel(name=name, category=category, overwrites=overwrites, reason="Claz revamp")
    await channel.edit(category=category, overwrites=overwrites, reason="Claz revamp")
    return channel


async def send_rules(channel: discord.TextChannel):
    embed = discord.Embed(
        title="Claz Services Rules",
        description=(
            "**Rule 1:** No mass pinging. Mass pinging can result in mute/ban.\n"
            "**Rule 2:** Be respectful to staff, builders, buyers, sellers, and members.\n"
            "**Rule 3:** No NSFW, scams, hate speech, or unsafe links.\n"
            "**Rule 4:** Be patient in tickets. Do not spam staff/builders.\n"
            "**Rule 5:** Vouch after every completed sale or build.\n"
            "**Rule 6:** Use the correct ticket panel.\n"
            "**Rule 7:** Reports must include user ID, explanation, and evidence."
        ),
        color=BRAND_COLOR,
    )
    embed.add_field(name="Ticket Reminder", value="Fake tickets, spam, or wasting time can remove ticket access.", inline=False)
    await send_or_edit(channel, "Claz Services | rules", embed)


async def send_claim_roles(channel: discord.TextChannel):
    embed = discord.Embed(
        title="Claim Your Shop Roles",
        description="Use the buttons below to claim customer and ping roles.",
        color=GOLD_COLOR,
    )
    embed.add_field(name="Available Roles", value="Member, Customer, Restock Ping, Giveaway Ping, Build Ping, Skelly Ping", inline=False)
    return await send_or_edit(channel, "Claz Services | claim roles", embed, ClaimRolesView())


async def send_panel(channel: discord.TextChannel, ticket_type: str):
    config = TICKET_CONFIGS[ticket_type]
    embed = discord.Embed(
        title=config["panel_title"],
        description=config["panel_description"],
        color=DANGER_COLOR if ticket_type == "report" else BRAND_COLOR,
    )
    embed.add_field(name="How It Works", value="Click the button, fill out the form, then wait for the correct team to claim it.", inline=False)
    embed.add_field(name="Do Not Spam", value="Open one ticket per request. Duplicates/fake tickets may be closed.", inline=False)
    return await send_or_edit(channel, f"Claz Services | ticket panel | {ticket_type}", embed, TicketPanelView(ticket_type))


async def build_layout(guild: discord.Guild, roles: dict):
    panel_messages = 0
    readonly = overwrites_for(guild, roles, "readonly")
    public = overwrites_for(guild, roles, "public")
    panel = overwrites_for(guild, roles, "panel")
    hidden = overwrites_for(guild, roles, "hidden")
    staff = overwrites_for(guild, roles, "staff")
    voice = overwrites_for(guild, roles, "voice")

    info = await ensure_category(guild, "CLAZ INFORMATION", readonly)
    await ensure_text(guild, info, "announcements", readonly)
    rules_channel = await ensure_text(guild, info, "rules", readonly)
    await ensure_text(guild, info, "legit-check", readonly)
    await ensure_text(guild, info, "restocks", readonly)
    await ensure_text(guild, info, "products", readonly)
    await ensure_text(guild, info, "prices", readonly)
    await ensure_text(guild, info, "role-info", readonly)
    claim_channel = await ensure_text(guild, info, "claim-roles", readonly)
    await ensure_text(guild, info, "welcome", readonly)
    await send_rules(rules_channel)
    if await send_claim_roles(claim_channel):
        panel_messages += 1

    shop = await ensure_category(guild, "DONUT SMP SHOP", public)
    await ensure_text(guild, shop, "buy-here", public)
    await ensure_text(guild, shop, "stock", readonly)
    await ensure_text(guild, shop, "donut-items", readonly)
    await ensure_text(guild, shop, "sell-to-us", public)
    await ensure_text(guild, shop, "trading", public)
    await ensure_text(guild, shop, "vouches", public)

    builds = await ensure_category(guild, "BUILD SERVICES", readonly)
    await ensure_text(guild, builds, "build-info", readonly)
    await ensure_text(guild, builds, "build-prices", readonly)
    await ensure_text(guild, builds, "build-portfolio", readonly)

    panels = await ensure_category(guild, "TICKET PANELS", panel)
    for ticket_type, config in TICKET_CONFIGS.items():
        channel = await ensure_text(guild, panels, config["panel_channel"], panel)
        if await send_panel(channel, ticket_type):
            panel_messages += 1

    await ensure_category(guild, "ACTIVE TICKETS", hidden)

    giveaways = await ensure_category(guild, "GIVEAWAYS", readonly)
    await ensure_text(guild, giveaways, "daily-giveaway", readonly)
    await ensure_text(guild, giveaways, "weekly-giveaway", readonly)
    await ensure_text(guild, giveaways, "big-giveaways", readonly)

    community = await ensure_category(guild, "COMMUNITY", public)
    await ensure_text(guild, community, "chat", public)
    await ensure_text(guild, community, "temp-chat", public)
    await ensure_text(guild, community, "market", public)
    await ensure_text(guild, community, "commands", public)
    await ensure_text(guild, community, "leveling", public)
    await ensure_text(guild, community, "streams", public)
    await ensure_text(guild, community, "media", public)

    partners = await ensure_category(guild, "PARTNERSHIP", public)
    await ensure_text(guild, partners, "our-ad", readonly)
    await ensure_text(guild, partners, "partners", readonly)
    await ensure_text(guild, partners, "partner-req", public)

    staff_cat = await ensure_category(guild, "STAFF", staff)
    await ensure_text(guild, staff_cat, "staff-chat", staff)
    await ensure_text(guild, staff_cat, "staff-announcements", staff)
    await ensure_text(guild, staff_cat, "staff-logs", staff)
    await ensure_text(guild, staff_cat, "order-logs", staff)
    await ensure_text(guild, staff_cat, "build-logs", staff)

    voice_cat = await ensure_category(guild, "VOICE CHANNELS", voice)
    await ensure_voice(guild, voice_cat, "General 1", voice)
    await ensure_voice(guild, voice_cat, "General 2", voice)
    await ensure_voice(guild, voice_cat, "Build Calls", voice)
    await ensure_voice(guild, voice_cat, "Trusted Deals", voice)

    return panel_messages


async def create_ticket(interaction: discord.Interaction, ticket_type: str, data: dict[str, str]):
    guild = interaction.guild
    user = interaction.user
    config = TICKET_CONFIGS[ticket_type]
    route_name, claim_role_names = claim_route(ticket_type, data)

    category = discord.utils.get(guild.categories, name="ACTIVE TICKETS")
    if category is None:
        category = await guild.create_category(
            name="ACTIVE TICKETS",
            overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=False)},
            reason="Ticket category created",
        )

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, read_message_history=True),
    }
    if guild.me:
        overwrites[guild.me] = discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True, read_message_history=True)

    claim_roles = []
    for name in claim_role_names:
        role = role_by_name(guild, name)
        if role:
            claim_roles.append(role)
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True, read_message_history=True)

    muted = role_by_name(guild, "Muted")
    if muted:
        overwrites[muted] = discord.PermissionOverwrite(view_channel=False, send_messages=False)

    channel_name = clean_name(f"{config['prefix']}-{user.name}")
    channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        overwrites=overwrites,
        topic=build_topic(ticket_type, user.id, claim_role_names),
        reason=f"{config['label']} ticket opened by {user}",
    )

    embed = discord.Embed(
        title=f"{config['label']} Ticket",
        description=f"Opened by {user.mention}\nRouted to: **{route_name}**",
        color=DANGER_COLOR if ticket_type == "report" else BRAND_COLOR,
    )
    for key, value in data.items():
        embed.add_field(name=key.replace("_", " ").title(), value=value[:1024], inline=False)
    embed.add_field(name="Claim Access", value=", ".join(role.mention for role in claim_roles) or "Configured staff", inline=False)
    embed.set_footer(text="Use the buttons below to claim or close this ticket.")

    mentions = " ".join(role.mention for role in claim_roles)
    await channel.send(
        content=f"{user.mention} {mentions}".strip(),
        embed=embed,
        view=TicketControls(),
        allowed_mentions=discord.AllowedMentions(users=True, roles=True),
    )
    return channel


def missing_bot_permissions(member: discord.Member):
    checks = [
        ("Manage Server", member.guild_permissions.manage_guild),
        ("Manage Roles", member.guild_permissions.manage_roles),
        ("Manage Channels", member.guild_permissions.manage_channels),
        ("Manage Messages", member.guild_permissions.manage_messages),
        ("Send Messages", member.guild_permissions.send_messages),
        ("Embed Links", member.guild_permissions.embed_links),
    ]
    return [name for name, ok in checks if not ok]


@client.tree.command(name="revamp_server", description="Set up Claz Services roles, channels, tickets, rules, branding, and permissions.")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def revamp_server(interaction: discord.Interaction):
    if interaction.guild is None or not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message("Use this inside your server.", ephemeral=True)
        return

    guild = interaction.guild
    if guild.me is None:
        await interaction.response.send_message("I cannot read my bot member yet.", ephemeral=True)
        return

    missing = missing_bot_permissions(guild.me)
    if missing:
        await interaction.response.send_message("I need these permissions first: " + ", ".join(missing), ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True, thinking=True)
    warnings = []
    warnings.extend(await brand_server(guild))

    roles, created, updated, role_warnings = await ensure_roles(guild)
    warnings.extend(role_warnings)
    warnings.extend(await fix_role_hierarchy(guild, roles))

    owner_warning = await give_runner_owner_role(guild, interaction.user, roles)
    if owner_warning:
        warnings.append(owner_warning)

    panel_messages = await build_layout(guild, roles)

    summary = (
        f"{BOT_VERSION}\n"
        "Claz Services revamp complete.\n"
        f"Roles created: {created}\n"
        f"Roles updated: {updated}\n"
        f"Ticket/role panel messages created: {panel_messages}\n"
        "Ticket system: online\n"
        "Rules embed: posted/updated\n"
        "Welcome message: enabled"
    )
    if warnings:
        summary += "\n\nWarnings:\n" + "\n".join(f"- {warning}" for warning in warnings)
    await interaction.followup.send(summary[:1900], ephemeral=True)


@client.tree.command(name="lockdown_channel", description="Lock a channel so only Owner can type.")
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def lockdown_channel(interaction: discord.Interaction, channel: discord.TextChannel | None = None, reason: str = "Channel lockdown"):
    if interaction.guild is None or not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message("Use this inside your server.", ephemeral=True)
        return

    target = channel or interaction.channel
    if not isinstance(target, discord.TextChannel):
        await interaction.response.send_message("Pick a text channel.", ephemeral=True)
        return

    owner_role = role_by_name(interaction.guild, "Owner")
    if owner_role is None:
        await interaction.response.send_message("Run /revamp_server first.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True, thinking=True)
    await target.set_permissions(interaction.guild.default_role, send_messages=False, add_reactions=False, reason=reason)
    for role in interaction.guild.roles:
        if role.is_default() or role.managed or role == owner_role:
            continue
        await target.set_permissions(role, send_messages=False, add_reactions=False, reason=reason)
    await target.set_permissions(owner_role, view_channel=True, send_messages=True, add_reactions=True, read_message_history=True, reason=reason)
    if interaction.guild.me:
        await target.set_permissions(interaction.guild.me, view_channel=True, send_messages=True, manage_channels=True, reason=reason)

    embed = discord.Embed(title="Channel Locked", description=f"{target.mention} is locked. Only Owner can type.", color=DANGER_COLOR)
    embed.add_field(name="Reason", value=reason, inline=False)
    await target.send(embed=embed)
    await interaction.followup.send(f"Locked {target.mention}.", ephemeral=True)


async def handle_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        message = "Only admins can use this command."
    else:
        message = f"Something went wrong: {error}"
    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


@revamp_server.error
async def revamp_server_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


@lockdown_channel.error
async def lockdown_channel_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await handle_command_error(interaction, error)


client.run(TOKEN)
