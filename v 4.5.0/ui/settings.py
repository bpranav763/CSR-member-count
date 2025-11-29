"""
═══════════════════════════════════════════════════════════════
⚙️ Settings UI - Interactive settings menus
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import ui
from config import SUPPORTED_LANGUAGES, SUPPORTED_TIMEZONES
from utils import set_user_language, set_user_timezone

class LanguageSelect(ui.Select):
    """Language selection dropdown"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=code, emoji=name.split()[0])
            for code, name in list(SUPPORTED_LANGUAGES.items())[:25]  # Discord limit: 25 options
        ]
        
        super().__init__(
            placeholder="Choose your language...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle language selection"""
        selected_lang = self.values[0]
        
        if set_user_language(interaction.user.id, selected_lang):
            lang_name = SUPPORTED_LANGUAGES[selected_lang]
            await interaction.response.send_message(
                f"✅ Language set to {lang_name}!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to save language setting.",
                ephemeral=True
            )

class TimezoneSelect(ui.Select):
    """Timezone selection dropdown"""
    
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=code)
            for code, name in list(SUPPORTED_TIMEZONES.items())[:25]  # Discord limit: 25 options
        ]
        
        super().__init__(
            placeholder="Choose your timezone...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Handle timezone selection"""
        selected_tz = self.values[0]
        
        if set_user_timezone(interaction.user.id, selected_tz):
            tz_name = SUPPORTED_TIMEZONES[selected_tz]
            await interaction.response.send_message(
                f"✅ Timezone set to {tz_name}!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to save timezone setting.",
                ephemeral=True
            )

class SettingsView(ui.View):
    """Settings menu with dropdowns"""
    
    def __init__(self):
        super().__init__(timeout=180)  # 3 minute timeout
        self.add_item(LanguageSelect())
        self.add_item(TimezoneSelect())
    
    @ui.button(label="Close", style=discord.ButtonStyle.gray, emoji="❌", row=2)
    async def close_button(self, interaction: discord.Interaction, button: ui.Button):
        """Close settings menu"""
        await interaction.response.edit_message(content="Settings closed.", embed=None, view=None)
