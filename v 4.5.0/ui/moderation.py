"""
═══════════════════════════════════════════════════════════════
🛡️ Moderation Review UI - For staff to review flagged content
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import ui
from datetime import datetime
from config import CSR_STAFF_ROLE_ID

class ModerationReviewView(ui.View):
    """Moderation review buttons"""
    
    def __init__(self, message_data):
        super().__init__(timeout=None)
        self.message_data = message_data
    
    @ui.button(label="Approve", style=discord.ButtonStyle.green, emoji="✅")
    async def approve_button(self, interaction: discord.Interaction, button: ui.Button):
        """Approve the flagged message"""
        
        # Check if user is staff
        staff_role = interaction.guild.get_role(CSR_STAFF_ROLE_ID)
        if not staff_role or staff_role not in interaction.user.roles:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Only staff can review moderation!",
                    ephemeral=True
                )
                return
        
        embed = discord.Embed(
            title="✅ Message Approved",
            description=f"Message was approved by {interaction.user.mention}",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Reviewed by", value=interaction.user.mention, inline=False)
        
        # Disable buttons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @ui.button(label="Confirm Delete", style=discord.ButtonStyle.red, emoji="🗑️")
    async def delete_button(self, interaction: discord.Interaction, button: ui.Button):
        """Confirm the deletion"""
        
        # Check if user is staff
        staff_role = interaction.guild.get_role(CSR_STAFF_ROLE_ID)
        if not staff_role or staff_role not in interaction.user.roles:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Only staff can review moderation!",
                    ephemeral=True
                )
                return
        
        embed = discord.Embed(
            title="🗑️ Deletion Confirmed",
            description=f"Deletion was confirmed by {interaction.user.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Reviewed by", value=interaction.user.mention, inline=False)
        
        # Disable buttons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @ui.button(label="Warn User", style=discord.ButtonStyle.gray, emoji="⚠️")
    async def warn_button(self, interaction: discord.Interaction, button: ui.Button):
        """Warn the user"""
        
        # Check if user is staff
        staff_role = interaction.guild.get_role(CSR_STAFF_ROLE_ID)
        if not staff_role or staff_role not in interaction.user.roles:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message(
                    "❌ Only staff can review moderation!",
                    ephemeral=True
                )
                return
        
        # Try to DM the user
        try:
            user = await interaction.client.fetch_user(self.message_data['user_id'])
            dm_embed = discord.Embed(
                title="⚠️ Warning",
                description="Your message was flagged by our moderation system.",
                color=discord.Color.orange()
            )
            dm_embed.add_field(name="Reason", value=self.message_data.get('reason', 'Unknown'), inline=False)
            dm_embed.add_field(name="Message", value=self.message_data.get('content', 'N/A')[:500], inline=False)
            dm_embed.add_field(name="Action", value="Please follow our server rules!", inline=False)
            
            await user.send(embed=dm_embed)
            
            await interaction.response.send_message(
                f"✅ Warning sent to user!",
                ephemeral=True
            )
        except:
            await interaction.response.send_message(
                "❌ Could not DM user (they may have DMs disabled)",
                ephemeral=True
            )
