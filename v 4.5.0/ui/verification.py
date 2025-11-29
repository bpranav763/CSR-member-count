"""
═══════════════════════════════════════════════════════════════
✅ Verification System - Interactive verification flow
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import ui
from config import *

class VerificationModal(ui.Modal, title="Verification"):
    """Verification modal"""
    
    roblox_username = ui.TextInput(
        label="Roblox Username",
        placeholder="Enter your Roblox username...",
        required=True,
        max_length=20
    )
    
    age = ui.TextInput(
        label="Age",
        placeholder="How old are you?",
        required=True,
        max_length=3
    )
    
    rules = ui.TextInput(
        label="Rules Agreement",
        placeholder='Type "I agree" if you\'ve read the rules',
        required=True,
        max_length=20
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Handle verification submission"""
        
        # Check age
        try:
            age_num = int(self.age.value)
            if age_num < 13:
                await interaction.response.send_message(
                    "❌ You must be at least 13 years old to use Discord.",
                    ephemeral=True
                )
                return
        except ValueError:
            await interaction.response.send_message(
                "❌ Please enter a valid age (number).",
                ephemeral=True
            )
            return
        
        # Check rules agreement
        if self.rules.value.lower() not in ["i agree", "agree"]:
            await interaction.response.send_message(
                "❌ You must agree to the rules to join!",
                ephemeral=True
            )
            return
        
        # Remove pending role, add approved role
        try:
            pending_role = interaction.guild.get_role(VERIFICATION_PENDING_ROLE_ID)
            approved_role = interaction.guild.get_role(MEMBER_APPROVED_ROLE_ID)
            
            if pending_role:
                await interaction.user.remove_roles(pending_role)
            if approved_role:
                await interaction.user.add_roles(approved_role)
            
            # Send success message
            embed = discord.Embed(
                title="✅ Verification Complete!",
                description=f"Welcome, {interaction.user.mention}! You're now verified!",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Your Details",
                value=f"**Roblox:** {self.roblox_username.value}\n**Age:** {age_num}",
                inline=False
            )
            embed.add_field(
                name="Next Steps",
                value=f"• Explore the server\n• Join game events\n• Have fun!",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Verification failed: {e}",
                ephemeral=True
            )

class VerificationView(ui.View):
    """Verification button view"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @ui.button(label="Verify", style=discord.ButtonStyle.green, emoji="✅", custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: ui.Button):
        """Open verification modal"""
        await interaction.response.send_modal(VerificationModal())
