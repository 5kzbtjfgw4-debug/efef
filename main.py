# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

import discord
from discord import app_commands


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
SERVER_ICON_PATH = Path(os.getenv("SERVER_ICON_PATH", "assets/server-icon.png"))

SERVER_NAME = "Claz Services"
BRAND_COLOR = discord.Color.from_rgb(255, 142, 36)
GOLD_COLOR = discord.Color.from_rgb(255, 196, 55)
DANGER_COLOR = discord.Color.from_rgb(220, 53, 69)

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN Railway variable.")

GUILD_ID = int(GUILD_ID) if GUILD_ID else None


OWNER_ROLES = ["Owner", "Co Owner"]
ADMIN_ROLES = ["Owner", "Co Owner", "Head Admin", "Admin"]
STAFF_ROLES = [
    "Owner",
    "Co Owner",
    "Head Admin",
    "Admin",
    "Shop Manager",
    "Ticket Manager",
    "Builder Manager",
    "Partner Manager",
    "Senior Staff",
    "Staff",
    "Trial Staff",
]
BUILDER_TIERS = ["Trial Builder", "Junior Builder", "Senior Builder", "Expert Builder"]
BUILDER_MANAGER_ROLES = ["Builder Manager"]
TRUSTED_SKELLY_ROLES = ["Trusted Buyer", "Trusted Seller"]


# Top-to-bottom role order. The revamp command tries to place these under the bot role.
ROLE_SPECS = [
    ("Owner", 0xFFB000, discord.Permissions(administrator=True), False),
    ("Co Owner", 0xFF7A1A, discord.Permissions(administrator=True), False),
    ("Head Admin", 0xE84D2A, discord.Permissions(administrator=True), False),
    ("Admin", 0xD93838, discord.Permissions(administrator=True), False),
    (
        "Shop Manager",
        0xFF9F1C,
        discord.Permissions(
            manage_guild=True,
            manage_roles=True,
            manage_channels=True,
            manage_messages=True,
            kick_members=True,
            ban_members=True,
            moderate_members=True,
        ),
        False,
    ),
    (
        "Ticket Manager",
        0xF7B731,
        discord.Permissions(
            manage_channels=True,
            manage_messages=True,
            moderate_members=True,
        ),
        False,
    ),
    (
        "Builder Manager",
        0xC77DFF,
        discord.Permissions(manage_channels=True, manage_messages=True),
        False,
    ),
    (
        "Partner Manager",
        0x7B61FF,
        discord.Permissions(manage_channels=True, manage_messages=True),
        False,
    ),
    (
        "Senior Staff",
        0x4EA8DE,
        discord.Permissions(manage_messages=True, moderate_members=True),
        False,
    ),
    (
        "Staff",
        0x72C3FC,
        discord.Permissions(manage_messages=True, moderate_members=True),
        False,
    ),
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
    ("Member", "claim_member", "Member"),
    ("Customer", "claim_customer", "Customer"),
    ("Restock Ping", "claim_restock_ping", "Restock Ping"),
    ("Giveaway Ping", "claim_giveaway_ping", "Giveaway Ping"),
    ("Build Ping", "claim_build_ping", "Build Ping"),
    ("Skelly Ping", "claim_skelly_ping", "Skelly Ping"),
]

TICKET_CONFIGS = {
    "build": {
        "label": "Base Build",
        "emoji": "🏗️",
        "button_style": discord.ButtonStyle.primary,
        "channel_prefix": "build",
        "panel_channel": "🏗️︱base-build-ticket",
        "panel_title": "Base Build Tickets",
        "panel_description": (
            "Request a Donut SMP base, farm, room, wall, vault, or full custom build.\n\n"
            "**Budget routing:**\n"
            "10m or less -> Trial Builder\n"
            "15m or less -> Junior Builder\n"
            "25m or less -> Senior Builder\n"
            "Above 25m -> Expert Builder"
        ),
        "modal_title": "Base Build Request",
        "fields": [
            ("budget", "Budget", "Example: 10m, 15m, 25m, 50m", False),
            ("build_type", "Build Type", "Base, farm, vault, wall, interior, etc.", False),
            ("details", "Build Details", "Describe size, style, blocks, deadline, and location.", True),
        ],
    },
    "buy_skelly": {
        "label": "Buy Skellies",
        "emoji": "💀",
        "button_style": discord.ButtonStyle.success,
        "channel_prefix": "buy-skelly",
        "panel_channel": "💀︱buy-skellies-ticket",
        "panel_title": "Buy Skellies",
        "panel_description": (
            "Open this ticket if you want to buy skellies from trusted shop sellers."
        ),
        "modal_title": "Buy Skellies",
        "fields": [
            ("amount", "How many are you buying?", "Example: 2 skellies", False),
            ("budget", "Budget / offer", "Example: 30m total or 15m each", False),
            ("details", "Extra Details", "Payment method, urgency, questions, etc.", True),
        ],
    },
    "sell_skelly": {
        "label": "Sell Skellies",
        "emoji": "💰",
        "button_style": discord.ButtonStyle.success,
        "channel_prefix": "sell-skelly",
        "panel_channel": "💰︱sell-skellies-ticket",
        "panel_title": "Sell Skellies",
        "panel_description": (
            "Open this ticket if you want to sell skellies to trusted shop buyers."
        ),
        "modal_title": "Sell Skellies",
        "fields": [
            ("amount", "How many are you selling?", "Example: 3 skellies", False),
            ("price", "Asking price", "Example: 45m total or 15m each", False),
            ("details", "Proof / Extra Details", "Tell us proof, location, and anything important.", True),
        ],
    },
    "report": {
        "label": "Report User",
        "emoji": "🚨",
        "button_style": discord.ButtonStyle.danger,
        "channel_prefix": "report",
        "panel_channel": "🚨︱report-user-ticket",
        "panel_title": "Report A User",
        "panel_description": (
            "Reports are private. Only the ticket opener and Owner role can view or answer them."
        ),
        "modal_title": "Report User",
        "fields": [
            ("user_id", "User ID", "Paste the Discord user ID you are reporting.", False),
            ("reason", "What happened?", "Explain what happened clearly.", True),
            ("evidence", "Evidence", "Links, screenshots, dates, or witnesses.", True),
        ],
    },
}


def role_by_name(guild: discord.Guild, name: str):
    return discord.utils.get(guild.roles, name=name)


def has_any_role(member: discord.Member, role_names: list[str]) -> bool:
    member_role_names = {role.name for role in member.roles}
    return bool(member_role_names.intersection(role_names))


def parse_money_to_millions(value: str) -> float | None:
    cleaned = value.lower().replace(",", "").replace("$", "").strip()
    match = re.search(r"(\d+(?:\.\d+)?)\s*([mb]?)", cleaned)
    if not match:
        return None

    amount = float(match.group(1))
    suffix = match.group(2)
    if suffix == "b":
        amount *= 1000
    return amount


def builder_roles_for_budget(budget_text: str):
    millions = parse_money_to_millions(budget_text)

    if millions is None or millions <= 10:
        tier_index = 0
    elif millions <= 15:
        tier_index = 1
    elif millions <= 25:
        tier_index = 2
    else:
        tier_index = 3

    tier = BUILDER_TIERS[tier_index]
    eligible = BUILDER_TIERS[tier_index:] + BUILDER_MANAGER_ROLES + ADMIN_ROLES
    return tier, eligible


def claim_roles_for_ticket(ticket_type: str, data: dict[str, str]) -> tuple[str, list[str]]:
    if ticket_type == "build":
        tier, roles = builder_roles_for_budget(data.get("budget", ""))
        return tier, roles

    if ticket_type in {"buy_skelly", "sell_skelly"}:
        return "Trusted Skelly Team", TRUSTED_SKELLY_ROLES + ADMIN_ROLES

    if ticket_type == "report":
        return "Owner Only", ["Owner"]

    return "Staff", STAFF_ROLES


def clean_channel_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9-]+", "-", value.lower()).strip("-")
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned[:40] or "ticket"


def build_ticket_topic(
    ticket_type: str,
    owner_id: int,
    claim_role_names: list[str],
    claimed_by: int | None = None,
) -> str:
    claimed = claimed_by or 0
    return (
        "claz_ticket"
        f"|type={ticket_type}"
        f"|owner={owner_id}"
        f"|claimed={claimed}"
        f"|claim_roles={','.join(claim_role_names)}"
    )


def parse_ticket_topic(topic: str | None) -> dict[str, str]:
    if not topic or not topic.startswith("claz_ticket"):
        return {}

    data = {}
    for part in topic.split("|")[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            data[key] = value
    return data


def ticket_claim_role_names(channel: discord.TextChannel) -> list[str]:
    meta = parse_ticket_topic(channel.topic)
    return [name for name in meta.get("claim_roles", "").split(",") if name]


def ticket_owner_id(channel: discord.TextChannel) -> int | None:
    meta = parse_ticket_topic(channel.topic)
    owner = meta.get("owner")
    return int(owner) if owner and owner.isdigit() else None


def can_claim_ticket(member: discord.Member, channel: discord.TextChannel) -> bool:
    if member.guild_permissions.administrator:
        return True

    allowed_roles = ticket_claim_role_names(channel)
    return has_any_role(member, allowed_roles)


def can_close_ticket(member: discord.Member, channel: discord.TextChannel) -> bool:
    if member.guild_permissions.administrator or can_claim_ticket(member, channel):
        return True

    owner_id = ticket_owner_id(channel)
    return owner_id == member.id


async def send_or_update_embed(
    channel: discord.TextChannel,
    marker: str,
    embed: discord.Embed,
    view: discord.ui.View | None = None,
) -> bool:
    embed.set_footer(text=marker)

    async for message in channel.history(limit=30):
        if (
            message.author == channel.guild.me
            and message.embeds
            and message.embeds[0].footer
            and message.embeds[0].footer.text == marker
        ):
            await message.edit(embed=embed, view=view)
            return False

    await channel.send(embed=embed, view=view)
    return True


class RoleButton(discord.ui.Button):
    def __init__(self, label: str, custom_id: str, role_name: str):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            custom_id=f"claz_role_{custom_id}",
        )
        self.role_name = role_name

    async def callback(self, interaction: discord.Interaction):
        if interaction.guild is None or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message(
                "This can only be used inside the server.",
                ephemeral=True,
            )
            return

        role = role_by_name(interaction.guild, self.role_name)
        if role is None:
            await interaction.response.send_message(
                f"The {self.role_name} role does not exist yet.",
                ephemeral=True,
            )
            return

        try:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role, reason="Claim roles button")
                await interaction.response.send_message(
                    f"Removed {role.mention}.",
                    ephemeral=True,
                )
            else:
                await interaction.user.add_roles(role, reason="Claim roles button")
                await interaction.response.send_message(
                    f"Added {role.mention}.",
                    ephemeral=True,
                )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I cannot manage that role. Move my bot role above it.",
                ephemeral=True,
            )


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
            emoji=config["emoji"],
            style=config["button_style"],
            custom_id=f"claz_ticket_open_{ticket_type}",
        )
        self.ticket_type = ticket_type

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketModal(self.ticket_type))


class TicketPanelView(discord.ui.View):
    def __init__(self, ticket_type: str):
        super().__init__(timeout=None)
        self.add_item(TicketOpenButton(ticket_type))


class TicketControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Claim Ticket",
        emoji="✅",
        style=discord.ButtonStyle.success,
        custom_id="claz_ticket_claim",
    )
    async def claim_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message(
                "This button only works inside a ticket channel.",
                ephemeral=True,
            )
            return

        if not isinstance(interaction.user, discord.Member) or not can_claim_ticket(
            interaction.user,
            interaction.channel,
        ):
            await interaction.response.send_message(
                "You do not have permission to claim this ticket.",
                ephemeral=True,
            )
            return

        meta = parse_ticket_topic(interaction.channel.topic)
        if meta.get("claimed") and meta.get("claimed") != "0":
            await interaction.response.send_message(
                "This ticket has already been claimed.",
                ephemeral=True,
            )
            return

        topic = build_ticket_topic(
            ticket_type=meta.get("type", "unknown"),
            owner_id=int(meta.get("owner", "0")),
            claim_role_names=ticket_claim_role_names(interaction.channel),
            claimed_by=interaction.user.id,
        )

        await interaction.channel.edit(
            topic=topic,
            reason=f"Ticket claimed by {interaction.user}",
        )
        await interaction.response.send_message(
            f"{interaction.user.mention} claimed this ticket.",
        )

    @discord.ui.button(
        label="Close Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="claz_ticket_close",
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message(
                "This button only works inside a ticket channel.",
                ephemeral=True,
            )
            return

        if not isinstance(interaction.user, discord.Member) or not can_close_ticket(
            interaction.user,
            interaction.channel,
        ):
            await interaction.response.send_message(
                "You do not have permission to close this ticket.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "Closing this ticket now.",
            ephemeral=True,
        )
        await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")


class TicketModal(discord.ui.Modal):
    def __init__(self, ticket_type: str):
        self.ticket_type = ticket_type
        config = TICKET_CONFIGS[ticket_type]
        super().__init__(title=config["modal_title"])
        self.inputs: dict[str, discord.ui.TextInput] = {}

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
            await interaction.response.send_message(
                "Tickets can only be opened inside the server.",
                ephemeral=True,
            )
            return

        data = {key: str(item.value).strip() for key, item in self.inputs.items()}
        try:
            channel = await create_ticket_channel(
                interaction=interaction,
                ticket_type=self.ticket_type,
                data=data,
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I need Manage Channels and permission to edit ticket channels.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Your ticket is open: {channel.mention}",
            ephemeral=True,
        )


class ClazServicesBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(ClaimRolesView())
        for ticket_type in TICKET_CONFIGS:
            self.add_view(TicketPanelView(ticket_type))
        self.add_view(TicketControlView())

        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}.")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} global command(s).")


client = ClazServicesBot()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_member_join(member: discord.Member):
    channel = discord.utils.get(member.guild.text_channels, name="👋︱welcome")
    if channel is None:
        channel = member.guild.system_channel
    if channel is None:
        return

    embed = discord.Embed(
        title="Welcome to Claz Services",
        description=(
            f"{member.mention}, welcome in.\n\n"
            "Open a ticket for base builds, skelly buying/selling, support, or reports. "
            "Check the rules and product channels before ordering."
        ),
        color=BRAND_COLOR,
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(
        name="Member Count",
        value=f"You are member #{member.guild.member_count}.",
        inline=True,
    )
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
                role = await guild.create_role(
                    name=name,
                    colour=discord.Color(color),
                    permissions=permissions,
                    mentionable=mentionable,
                    reason="Claz Services revamp",
                )
                created += 1
            except discord.Forbidden:
                warnings.append(f"Could not create role: {name}")
                continue
        else:
            try:
                if not role.managed:
                    await role.edit(
                        colour=discord.Color(color),
                        permissions=permissions,
                        mentionable=mentionable,
                        reason="Claz Services revamp",
                    )
                    updated += 1
            except discord.Forbidden:
                warnings.append(f"Could not update role: {name}")

        roles[name] = role

    return roles, created, updated, warnings


async def fix_role_hierarchy(guild: discord.Guild, roles: dict[str, discord.Role]):
    warnings = []
    bot_member = guild.me
    if bot_member is None:
        warnings.append("Could not read the bot member for role hierarchy.")
        return warnings

    top_target = bot_member.top_role.position - 1
    if top_target <= 0:
        warnings.append("Move the bot role higher so it can reorder shop roles.")
        return warnings

    positions = {}
    target_position = top_target

    for name, *_ in ROLE_SPECS:
        role = roles.get(name)
        if role is None or role.managed:
            continue
        if role >= bot_member.top_role:
            warnings.append(f"Could not move {name}; it is above or equal to the bot role.")
            continue
        if target_position <= 0:
            warnings.append("The bot role is not high enough to place every shop role.")
            break

        positions[role] = target_position
        target_position -= 1

    if positions:
        try:
            await guild.edit_role_positions(
                positions=positions,
                reason="Claz Services role hierarchy fix",
            )
        except discord.Forbidden:
            warnings.append("Could not edit role hierarchy. Move the bot role higher.")

    return warnings


async def assign_owner_role(
    guild: discord.Guild,
    member: discord.Member,
    roles: dict[str, discord.Role],
):
    owner_role = roles.get("Owner")
    if owner_role is None or owner_role in member.roles:
        return None

    bot_member = guild.me
    if bot_member is None or owner_role >= bot_member.top_role:
        return "Could not give you Owner role because it is above/equal to the bot role."

    try:
        await member.add_roles(owner_role, reason="Claz Services revamp runner")
    except discord.Forbidden:
        return "Could not give you Owner role. Move the bot role higher."

    return None


async def brand_server(guild: discord.Guild):
    warnings = []
    icon_bytes = None

    if SERVER_ICON_PATH.exists():
        icon_bytes = SERVER_ICON_PATH.read_bytes()
    else:
        warnings.append(
            "Server icon was not changed. Add your image as assets/server-icon.png "
            "or set SERVER_ICON_PATH."
        )

    try:
        edit_kwargs = {"name": SERVER_NAME, "reason": "Claz Services revamp"}
        if icon_bytes:
            edit_kwargs["icon"] = icon_bytes
        await guild.edit(**edit_kwargs)
    except discord.Forbidden:
        warnings.append("Could not rename or set server icon. I need Manage Server.")
    except discord.HTTPException:
        warnings.append("Could not set server icon. Try a smaller PNG/JPG image.")

    return warnings


def overwrites_for(guild: discord.Guild, roles: dict, mode: str):
    everyone = guild.default_role
    muted = roles.get("Muted")

    def role_list(names: list[str]):
        return [roles.get(name) for name in names if roles.get(name)]

    if mode == "readonly":
        overwrites = {
            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True,
            )
        }
        for role in role_list(STAFF_ROLES):
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
            )
    elif mode == "staff_only":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=False)}
        for role in role_list(STAFF_ROLES):
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            )
    elif mode == "owner_only":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=False)}
        for role in role_list(OWNER_ROLES):
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            )
    elif mode == "panel":
        overwrites = {
            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True,
            )
        }
        for role in role_list(STAFF_ROLES):
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_messages=True,
                read_message_history=True,
            )
    elif mode == "hidden":
        overwrites = {everyone: discord.PermissionOverwrite(view_channel=False)}
    elif mode == "voice":
        overwrites = {
            everyone: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,
                speak=True,
            )
        }
    else:
        overwrites = {
            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
            )
        }

    if muted:
        overwrites[muted] = discord.PermissionOverwrite(
            send_messages=False,
            add_reactions=False,
            speak=False,
        )

    return overwrites


async def ensure_category(guild: discord.Guild, name: str, overwrites: dict):
    category = discord.utils.get(guild.categories, name=name)
    if category is None:
        return await guild.create_category(
            name=name,
            overwrites=overwrites,
            reason="Claz Services revamp",
        )

    await category.edit(overwrites=overwrites, reason="Claz Services revamp")
    return category


async def ensure_text_channel(
    guild: discord.Guild,
    category: discord.CategoryChannel,
    name: str,
    overwrites: dict,
):
    channel = discord.utils.get(guild.text_channels, name=name)
    if channel is None:
        return await guild.create_text_channel(
            name=name,
            category=category,
            overwrites=overwrites,
            reason="Claz Services revamp",
        )

    await channel.edit(
        category=category,
        overwrites=overwrites,
        reason="Claz Services revamp",
    )
    return channel


async def ensure_voice_channel(
    guild: discord.Guild,
    category: discord.CategoryChannel,
    name: str,
    overwrites: dict,
):
    channel = discord.utils.get(guild.voice_channels, name=name)
    if channel is None:
        return await guild.create_voice_channel(
            name=name,
            category=category,
            overwrites=overwrites,
            reason="Claz Services revamp",
        )

    await channel.edit(
        category=category,
        overwrites=overwrites,
        reason="Claz Services revamp",
    )
    return channel


async def send_rules_embed(channel: discord.TextChannel):
    embed = discord.Embed(
        title="Claz Services Rules",
        description=(
            "**Rule 1:** No mass pinging. Mass pinging can result in a mute or ban.\n"
            "**Rule 2:** Be respectful to staff, builders, sellers, buyers, and members.\n"
            "**Rule 3:** No NSFW, hate speech, scams, or unsafe links.\n"
            "**Rule 4:** Be patient in tickets. Do not spam staff or builders.\n"
            "**Rule 5:** Vouch after every completed sale or build.\n"
            "**Rule 6:** Use the correct ticket panel for builds, skellies, or reports.\n"
            "**Rule 7:** Reports must include a user ID, what happened, and evidence."
        ),
        color=BRAND_COLOR,
    )
    embed.add_field(
        name="Ticket Reminder",
        value="Opening fake tickets or wasting time may lead to losing ticket access.",
        inline=False,
    )
    await send_or_update_embed(channel, "Claz Services | rules", embed)


async def send_claim_roles_message(channel: discord.TextChannel):
    embed = discord.Embed(
        title="Claim Your Shop Roles",
        description="Use the buttons below to claim customer roles and ping roles.",
        color=GOLD_COLOR,
    )
    embed.add_field(
        name="Available",
        value="Member, Customer, Restock Ping, Giveaway Ping, Build Ping, Skelly Ping",
        inline=False,
    )

    return await send_or_update_embed(
        channel,
        "Claz Services | claim roles",
        embed,
        ClaimRolesView(),
    )


async def send_ticket_panel(channel: discord.TextChannel, ticket_type: str):
    config = TICKET_CONFIGS[ticket_type]
    embed = discord.Embed(
        title=config["panel_title"],
        description=config["panel_description"],
        color=DANGER_COLOR if ticket_type == "report" else BRAND_COLOR,
    )
    embed.add_field(
        name="How It Works",
        value=(
            "Click the button, fill out the form, then wait for the correct team "
            "to claim and answer your ticket."
        ),
        inline=False,
    )
    embed.add_field(
        name="Do Not Spam",
        value="One ticket per request. Staff may close duplicate or fake tickets.",
        inline=False,
    )

    return await send_or_update_embed(
        channel,
        f"Claz Services | panel | {ticket_type}",
        embed,
        TicketPanelView(ticket_type),
    )


async def build_server_layout(guild: discord.Guild, roles: dict):
    panel_messages = 0

    readonly = overwrites_for(guild, roles, "readonly")
    public = overwrites_for(guild, roles, "public")
    panel = overwrites_for(guild, roles, "panel")
    hidden = overwrites_for(guild, roles, "hidden")
    staff_only = overwrites_for(guild, roles, "staff_only")
    voice = overwrites_for(guild, roles, "voice")

    info = await ensure_category(guild, "📌━━【Claz Information】━━", readonly)
    await ensure_text_channel(guild, info, "📢︱announcements", readonly)
    rules = await ensure_text_channel(guild, info, "📖︱rules", readonly)
    await ensure_text_channel(guild, info, "✅︱legit-check", readonly)
    await ensure_text_channel(guild, info, "📦︱restocks", readonly)
    await ensure_text_channel(guild, info, "💎︱products", readonly)
    await ensure_text_channel(guild, info, "💰︱prices", readonly)
    await ensure_text_channel(guild, info, "❔︱role-info", readonly)
    claim_roles = await ensure_text_channel(guild, info, "⭐︱claim-roles", readonly)
    await ensure_text_channel(guild, info, "👋︱welcome", readonly)

    await send_rules_embed(rules)
    if await send_claim_roles_message(claim_roles):
        panel_messages += 1

    shop = await ensure_category(guild, "🛒━━【Donut SMP Shop】━━", public)
    await ensure_text_channel(guild, shop, "🛒︱buy-here", public)
    await ensure_text_channel(guild, shop, "💎︱stock", readonly)
    await ensure_text_channel(guild, shop, "🍩︱donut-items", readonly)
    await ensure_text_channel(guild, shop, "💵︱sell-to-us", public)
    await ensure_text_channel(guild, shop, "🔁︱trading", public)
    await ensure_text_channel(guild, shop, "🔎︱vouches", public)

    builds = await ensure_category(guild, "🏗️━━【Build Services】━━", readonly)
    await ensure_text_channel(guild, builds, "🏗️︱build-info", readonly)
    await ensure_text_channel(guild, builds, "💸︱build-prices", readonly)
    await ensure_text_channel(guild, builds, "🖼️︱build-portfolio", readonly)

    panels = await ensure_category(guild, "🎫━━【Ticket Panels】━━", panel)
    for ticket_type, config in TICKET_CONFIGS.items():
        panel_channel = await ensure_text_channel(
            guild,
            panels,
            config["panel_channel"],
            panel,
        )
        if await send_ticket_panel(panel_channel, ticket_type):
            panel_messages += 1

    await ensure_category(guild, "📩━━【Active Tickets】━━", hidden)

    giveaways = await ensure_category(guild, "🎉━━【Giveaways】━━", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱daily-giveaway", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱weekly-giveaway", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱big-giveaways", readonly)

    community = await ensure_category(guild, "🌐━━【Community】━━", public)
    await ensure_text_channel(guild, community, "🌍︱chat", public)
    await ensure_text_channel(guild, community, "🌍︱temp-chat", public)
    await ensure_text_channel(guild, community, "🛒︱market", public)
    await ensure_text_channel(guild, community, "⚙️︱commands", public)
    await ensure_text_channel(guild, community, "💬︱leveling", public)
    await ensure_text_channel(guild, community, "🎥︱streams", public)
    await ensure_text_channel(guild, community, "📸︱media", public)

    partnership = await ensure_category(guild, "🤝━━【Partnership】━━", public)
    await ensure_text_channel(guild, partnership, "📌︱our-ad", readonly)
    await ensure_text_channel(guild, partnership, "🤝︱partners", readonly)
    await ensure_text_channel(guild, partnership, "📕︱partner-req", public)

    staff = await ensure_category(guild, "🛡️━━【Staff】━━", staff_only)
    await ensure_text_channel(guild, staff, "📝︱staff-chat", staff_only)
    await ensure_text_channel(guild, staff, "📢︱staff-announcements", staff_only)
    await ensure_text_channel(guild, staff, "📋︱staff-logs", staff_only)
    await ensure_text_channel(guild, staff, "🧾︱order-logs", staff_only)
    await ensure_text_channel(guild, staff, "🏗️︱build-logs", staff_only)

    voice_category = await ensure_category(guild, "🔊━━【Voice Channels】━━", voice)
    await ensure_voice_channel(guild, voice_category, "🔊︱General 1", voice)
    await ensure_voice_channel(guild, voice_category, "🔊︱General 2", voice)
    await ensure_voice_channel(guild, voice_category, "🏗️︱Build Calls", voice)
    await ensure_voice_channel(guild, voice_category, "💎︱Trusted Deals", voice)

    return panel_messages


async def create_ticket_channel(
    interaction: discord.Interaction,
    ticket_type: str,
    data: dict[str, str],
):
    guild = interaction.guild
    user = interaction.user
    config = TICKET_CONFIGS[ticket_type]
    route_name, claim_role_names = claim_roles_for_ticket(ticket_type, data)

    active_category = discord.utils.get(guild.categories, name="📩━━【Active Tickets】━━")
    if active_category is None:
        active_category = await guild.create_category(
            name="📩━━【Active Tickets】━━",
            overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=False)},
            reason="Ticket category created",
        )

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            attach_files=True,
            embed_links=True,
            read_message_history=True,
        ),
    }

    bot_member = guild.me
    if bot_member:
        overwrites[bot_member] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            manage_channels=True,
            read_message_history=True,
        )

    claim_roles = []
    for role_name in claim_role_names:
        role = role_by_name(guild, role_name)
        if role:
            claim_roles.append(role)
            overwrites[role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                attach_files=True,
                embed_links=True,
                read_message_history=True,
            )

    muted = role_by_name(guild, "Muted")
    if muted:
        overwrites[muted] = discord.PermissionOverwrite(
            view_channel=False,
            send_messages=False,
        )

    username = clean_channel_name(user.name)
    prefix = config["channel_prefix"]
    channel_name = clean_channel_name(f"{prefix}-{username}")

    channel = await guild.create_text_channel(
        name=channel_name,
        category=active_category,
        overwrites=overwrites,
        topic=build_ticket_topic(ticket_type, user.id, claim_role_names),
        reason=f"{config['label']} ticket opened by {user}",
    )

    embed = discord.Embed(
        title=f"{config['emoji']} {config['label']} Ticket",
        description=(
            f"Opened by {user.mention}\n"
            f"Routed to: **{route_name}**"
        ),
        color=DANGER_COLOR if ticket_type == "report" else BRAND_COLOR,
    )

    for key, value in data.items():
        embed.add_field(name=key.replace("_", " ").title(), value=value[:1024], inline=False)

    embed.add_field(
        name="Claim Access",
        value=", ".join(role.mention for role in claim_roles) or "Configured staff",
        inline=False,
    )
    embed.set_footer(text="Use the buttons below to claim or close this ticket.")

    role_mentions = " ".join(role.mention for role in claim_roles)
    await channel.send(
        content=f"{user.mention} {role_mentions}".strip(),
        embed=embed,
        view=TicketControlView(),
        allowed_mentions=discord.AllowedMentions(users=True, roles=True),
    )

    return channel


def required_bot_permissions(member: discord.Member) -> list[str]:
    checks = [
        ("Manage Server", member.guild_permissions.manage_guild),
        ("Manage Roles", member.guild_permissions.manage_roles),
        ("Manage Channels", member.guild_permissions.manage_channels),
        ("Manage Messages", member.guild_permissions.manage_messages),
        ("Send Messages", member.guild_permissions.send_messages),
        ("Embed Links", member.guild_permissions.embed_links),
    ]
    return [name for name, allowed in checks if not allowed]


@client.tree.command(
    name="revamp_server",
    description="Set up Claz Services roles, channels, tickets, rules, branding, and permissions.",
)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def revamp_server(interaction: discord.Interaction):
    if interaction.guild is None or not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message(
            "Use this command inside your server.",
            ephemeral=True,
        )
        return

    guild = interaction.guild
    bot_member = guild.me

    if bot_member is None:
        await interaction.response.send_message(
            "I could not read my server permissions yet. Try again in a few seconds.",
            ephemeral=True,
        )
        return

    missing = required_bot_permissions(bot_member)
    if missing:
        await interaction.response.send_message(
            "I need these permissions first: " + ", ".join(missing),
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    warnings = []
    warnings.extend(await brand_server(guild))

    roles, created_roles, updated_roles, role_warnings = await ensure_roles(guild)
    warnings.extend(role_warnings)
    warnings.extend(await fix_role_hierarchy(guild, roles))

    owner_warning = await assign_owner_role(guild, interaction.user, roles)
    if owner_warning:
        warnings.append(owner_warning)

    panel_messages = await build_server_layout(guild, roles)

    summary = (
        "Claz Services revamp complete.\n"
        f"Roles created: {created_roles}\n"
        f"Roles updated: {updated_roles}\n"
        f"New panel/role messages created: {panel_messages}\n"
        "Ticket system: online\n"
        "Rules embed: posted/updated\n"
        "Welcome message: enabled"
    )

    if warnings:
        summary += "\n\nWarnings:\n" + "\n".join(f"- {warning}" for warning in warnings)

    await interaction.followup.send(summary[:1900], ephemeral=True)


@client.tree.command(
    name="lockdown_channel",
    description="Lock a channel so only the Owner role can type.",
)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def lockdown_channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel | None = None,
    reason: str = "Channel lockdown",
):
    if interaction.guild is None or not isinstance(interaction.user, discord.Member):
        await interaction.response.send_message(
            "Use this command inside your server.",
            ephemeral=True,
        )
        return

    target = channel or interaction.channel
    if not isinstance(target, discord.TextChannel):
        await interaction.response.send_message(
            "Please choose a text channel.",
            ephemeral=True,
        )
        return

    owner_role = role_by_name(interaction.guild, "Owner")
    if owner_role is None:
        await interaction.response.send_message(
            "The Owner role does not exist yet. Run `/revamp_server` first.",
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    await target.set_permissions(
        interaction.guild.default_role,
        send_messages=False,
        add_reactions=False,
        reason=reason,
    )

    for role in interaction.guild.roles:
        if role.is_default() or role.managed or role == owner_role:
            continue
        await target.set_permissions(
            role,
            send_messages=False,
            add_reactions=False,
            reason=reason,
        )

    await target.set_permissions(
        owner_role,
        view_channel=True,
        send_messages=True,
        add_reactions=True,
        read_message_history=True,
        reason=reason,
    )

    if interaction.guild.me:
        await target.set_permissions(
            interaction.guild.me,
            view_channel=True,
            send_messages=True,
            manage_channels=True,
            reason=reason,
        )

    embed = discord.Embed(
        title="Channel Locked",
        description=f"{target.mention} is now locked. Only the Owner role can type.",
        color=DANGER_COLOR,
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    await target.send(embed=embed)
    await interaction.followup.send(f"Locked {target.mention}.", ephemeral=True)


@revamp_server.error
@lockdown_channel.error
async def command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
):
    if isinstance(error, app_commands.MissingPermissions):
        message = "Only admins can use this command."
    else:
        message = f"Something went wrong: {error}"

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


client.run(TOKEN)
