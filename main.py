# -*- coding: utf-8 -*-
import os

import discord
from discord import app_commands


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

BLUE = discord.Color.from_rgb(0, 102, 255)

if not TOKEN:
    raise RuntimeError("Missing DISCORD_TOKEN Railway variable.")

GUILD_ID = int(GUILD_ID) if GUILD_ID else None


ROLE_SPECS = [
    ("Owner", 0x004CFF, discord.Permissions(administrator=True), False),
    ("Co Owner", 0x0066FF, discord.Permissions(administrator=True), False),
    ("Head Admin", 0x0A74FF, discord.Permissions(administrator=True), False),
    ("Admin", 0x1F7AFF, discord.Permissions(administrator=True), False),
    (
        "Shop Manager",
        0x2490FF,
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
        0x3199FF,
        discord.Permissions(
            manage_channels=True,
            manage_messages=True,
            moderate_members=True,
        ),
        False,
    ),
    (
        "Partner Manager",
        0x45A3FF,
        discord.Permissions(
            manage_channels=True,
            manage_messages=True,
            mention_everyone=True,
        ),
        False,
    ),
    (
        "Senior Staff",
        0x66B5FF,
        discord.Permissions(manage_messages=True, moderate_members=True),
        False,
    ),
    (
        "Staff",
        0x8BC8FF,
        discord.Permissions(manage_messages=True, moderate_members=True),
        False,
    ),
    ("Trial Staff", 0xB9DDFF, discord.Permissions(manage_messages=True), False),
    ("Middleman", 0x7AA7FF, discord.Permissions(manage_messages=True), False),
    ("Supplier", 0x2BD9FE, discord.Permissions(), False),
    ("Trusted Seller", 0xFFD166, discord.Permissions(), False),
    ("Partner", 0xB07CFF, discord.Permissions(), False),
    ("Big Spender", 0xF6C945, discord.Permissions(), False),
    ("Customer", 0x4DD4AC, discord.Permissions(), False),
    ("Restock Ping", 0x2F80FF, discord.Permissions(), True),
    ("Giveaway Ping", 0xF7B801, discord.Permissions(), True),
    ("Donut SMP Ping", 0xFF7A00, discord.Permissions(), True),
    ("Member", 0xAAB7C4, discord.Permissions(), False),
    ("Muted", 0x2B2D31, discord.Permissions(), False),
]

CLAIMABLE_ROLES = [
    ("Member", "claim_member", "Member"),
    ("Customer", "claim_customer", "Customer"),
    ("Restock Ping", "claim_restock_ping", "Restock Ping"),
    ("Giveaway Ping", "claim_giveaway_ping", "Giveaway Ping"),
    ("Donut SMP Ping", "claim_donut_smp_ping", "Donut SMP Ping"),
]


def role_by_name(guild: discord.Guild, name: str):
    return discord.utils.get(guild.roles, name=name)


class RoleButton(discord.ui.Button):
    def __init__(self, label: str, custom_id: str, role_name: str):
        super().__init__(
            label=label,
            style=discord.ButtonStyle.primary,
            custom_id=custom_id,
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
                await interaction.user.remove_roles(
                    role,
                    reason="Claim roles button",
                )
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


class DonutSMPShopBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(ClaimRolesView())

        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} command(s) to guild {GUILD_ID}.")
        else:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} global command(s).")


client = DonutSMPShopBot()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


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
                    reason="Donut SMP shop server revamp",
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
                        reason="Donut SMP shop server revamp",
                    )
                    updated += 1
            except discord.Forbidden:
                warnings.append(f"Could not update role: {name}")

        roles[name] = role

    return roles, created, updated, warnings


def overwrites_for(guild: discord.Guild, roles: dict, mode: str):
    everyone = guild.default_role
    muted = roles.get("Muted")
    staff_roles = [
        roles.get("Owner"),
        roles.get("Co Owner"),
        roles.get("Head Admin"),
        roles.get("Admin"),
        roles.get("Shop Manager"),
        roles.get("Ticket Manager"),
        roles.get("Partner Manager"),
        roles.get("Senior Staff"),
        roles.get("Staff"),
        roles.get("Trial Staff"),
    ]

    if mode == "readonly":
        overwrites = {
            everyone: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True,
            )
        }
        for role in staff_roles:
            if role:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_messages=True,
                    read_message_history=True,
                )
    elif mode == "private_staff":
        overwrites = {
            everyone: discord.PermissionOverwrite(view_channel=False),
        }
        for role in staff_roles:
            if role:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                )
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


async def ensure_category(
    guild: discord.Guild,
    name: str,
    overwrites: dict,
):
    category = discord.utils.get(guild.categories, name=name)
    if category is None:
        return await guild.create_category(
            name=name,
            overwrites=overwrites,
            reason="Donut SMP shop server revamp",
        )

    await category.edit(overwrites=overwrites, reason="Donut SMP shop server revamp")
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
            reason="Donut SMP shop server revamp",
        )

    await channel.edit(
        category=category,
        overwrites=overwrites,
        reason="Donut SMP shop server revamp",
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
            reason="Donut SMP shop server revamp",
        )

    await channel.edit(
        category=category,
        overwrites=overwrites,
        reason="Donut SMP shop server revamp",
    )
    return channel


async def send_claim_roles_message(channel: discord.TextChannel):
    async for message in channel.history(limit=25):
        if message.author == client.user and message.components:
            return False

    embed = discord.Embed(
        title="Donut SMP Shop Roles",
        description="Use the buttons below to claim shop pings and customer roles.",
        color=BLUE,
    )
    embed.set_footer(text="Click again to remove a role.")

    await channel.send(embed=embed, view=ClaimRolesView())
    return True


async def build_server_layout(guild: discord.Guild, roles: dict):
    created_claim_message = False

    readonly = overwrites_for(guild, roles, "readonly")
    public = overwrites_for(guild, roles, "public")
    voice = overwrites_for(guild, roles, "voice")
    staff_only = overwrites_for(guild, roles, "private_staff")

    info = await ensure_category(guild, "📜━━【Donut Shop Info】━━", readonly)
    await ensure_text_channel(guild, info, "📢︱announcements", readonly)
    await ensure_text_channel(guild, info, "📖︱rules", readonly)
    await ensure_text_channel(guild, info, "✅︱legit-check", readonly)
    await ensure_text_channel(guild, info, "📦︱restocks", readonly)
    await ensure_text_channel(guild, info, "💎︱products", readonly)
    await ensure_text_channel(guild, info, "💰︱prices", readonly)
    await ensure_text_channel(guild, info, "❔︱role-info", readonly)
    claim_roles = await ensure_text_channel(guild, info, "⭐︱claim-roles", readonly)
    await ensure_text_channel(guild, info, "🚧︱welcome", readonly)

    shop = await ensure_category(guild, "🛒━━【Donut SMP Shop】━━", public)
    await ensure_text_channel(guild, shop, "🛒︱buy-here", public)
    await ensure_text_channel(guild, shop, "💎︱stock", readonly)
    await ensure_text_channel(guild, shop, "🍩︱donut-items", readonly)
    await ensure_text_channel(guild, shop, "💵︱sell-to-us", public)
    await ensure_text_channel(guild, shop, "🔁︱trading", public)
    await ensure_text_channel(guild, shop, "🔎︱vouches", public)

    tickets = await ensure_category(guild, "🎫━━【Tickets】━━", public)
    await ensure_text_channel(guild, tickets, "🎫︱tickets", public)
    await ensure_text_channel(guild, tickets, "🛡️︱middleman-request", public)
    await ensure_text_channel(guild, tickets, "❔︱support", public)
    await ensure_text_channel(guild, tickets, "💻︱apply-for-staff", public)

    giveaways = await ensure_category(guild, "🎉━━【Giveaways】━━", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱daily-giveaway", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱weekly-50m", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱giveaways", readonly)
    await ensure_text_channel(guild, giveaways, "🎉︱10b-giveaway", readonly)

    text_channels = await ensure_category(guild, "🌐━━【Community】━━", public)
    await ensure_text_channel(guild, text_channels, "🌍︱chat", public)
    await ensure_text_channel(guild, text_channels, "🌍︱temp-chat", public)
    await ensure_text_channel(guild, text_channels, "🛒︱market", public)
    await ensure_text_channel(guild, text_channels, "⚙️︱commands", public)
    await ensure_text_channel(guild, text_channels, "💬︱leveling", public)
    await ensure_text_channel(guild, text_channels, "🎥︱streams", public)
    await ensure_text_channel(guild, text_channels, "📸︱media", public)

    partnership = await ensure_category(guild, "🟡━━【Partnership】━━", public)
    await ensure_text_channel(guild, partnership, "📌︱our-ad", readonly)
    await ensure_text_channel(guild, partnership, "🤝︱partners", readonly)
    await ensure_text_channel(guild, partnership, "📕︱partner-req", public)

    staff = await ensure_category(guild, "🛡️━━【Staff】━━", staff_only)
    await ensure_text_channel(guild, staff, "📝︱staff-chat", staff_only)
    await ensure_text_channel(guild, staff, "📢︱staff-announcements", staff_only)
    await ensure_text_channel(guild, staff, "📋︱staff-logs", staff_only)
    await ensure_text_channel(guild, staff, "🧾︱order-logs", staff_only)

    voice_channels = await ensure_category(guild, "🔊━━【Voice Channels】━━", voice)
    await ensure_voice_channel(guild, voice_channels, "🔊︱General 1", voice)
    await ensure_voice_channel(guild, voice_channels, "🔊︱General 2", voice)
    await ensure_voice_channel(guild, voice_channels, "🎲︱Trusted Game", voice)

    if claim_roles:
        created_claim_message = await send_claim_roles_message(claim_roles)

    return created_claim_message


@client.tree.command(
    name="revamp_server",
    description="Create Donut SMP shop roles, channels, and permissions.",
)
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def revamp_server(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "Use this command inside your server.",
            ephemeral=True,
        )
        return

    guild = interaction.guild
    bot_member = guild.get_member(client.user.id)

    if bot_member is None:
        await interaction.response.send_message(
            "I could not read my server permissions yet. Try again in a few seconds.",
            ephemeral=True,
        )
        return

    missing = []
    if not bot_member.guild_permissions.manage_roles:
        missing.append("Manage Roles")
    if not bot_member.guild_permissions.manage_channels:
        missing.append("Manage Channels")

    if missing:
        await interaction.response.send_message(
            "I need these permissions first: " + ", ".join(missing),
            ephemeral=True,
        )
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    roles, created_roles, updated_roles, warnings = await ensure_roles(guild)
    claim_message_created = await build_server_layout(guild, roles)

    summary = (
        "Donut SMP shop revamp complete.\n"
        f"Roles created: {created_roles}\n"
        f"Roles updated: {updated_roles}\n"
        f"Claim roles message created: {'yes' if claim_message_created else 'already existed'}"
    )

    if warnings:
        summary += "\n\nWarnings:\n" + "\n".join(f"- {warning}" for warning in warnings)

    await interaction.followup.send(summary, ephemeral=True)


@revamp_server.error
async def revamp_server_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
):
    if isinstance(error, app_commands.MissingPermissions):
        message = "Only admins can use `/revamp_server`."
    else:
        message = f"Something went wrong: {error}"

    if interaction.response.is_done():
        await interaction.followup.send(message, ephemeral=True)
    else:
        await interaction.response.send_message(message, ephemeral=True)


client.run(TOKEN)
