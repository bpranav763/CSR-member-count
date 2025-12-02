"""
═══════════════════════════════════════════════════════════════
🤖 AI Commands - Manage AI chat system
═══════════════════════════════════════════════════════════════
"""

import discord
from discord import app_commands
from config import *
from utils import is_staff

# Import AI system
try:
    from utils.ai_chat import get_ai_status, clear_memory, get_memory_stats
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

def setup(bot):
    """Setup AI commands"""
    
    @bot.tree.command(name="aistatus", description="Check AI system status")
    async def aistatus(interaction: discord.Interaction):
        """Check AI status"""
        if not AI_AVAILABLE:
            await interaction.response.send_message(
                "❌ AI system is not loaded!\n\n"
                "**Setup:**\n"
                "1. Get free API key: https://console.groq.com\n"
                "2. Add to `.env`: `GROQ_API_KEY=your_key_here`\n"
                "3. Restart bot",
                ephemeral=True
            )
            return
        
        status = get_ai_status()
        stats = get_memory_stats()
        
        embed = discord.Embed(
            title="🤖 AI System Status",
            description=status,
            color=discord.Color.green()
        )
        
        embed.add_field(
            name="💾 Memory Stats",
            value=stats,
            inline=False
        )
        
        embed.add_field(
            name="📖 How to Use",
            value=(
                "**Mention:** `@CSR SYSTEM your question`\n"
                "**Prefix:** `.csr your question` or `csr your question`\n"
                "**Reply:** Reply to any of my messages"
            ),
            inline=False
        )
        
        embed.add_field(
            name="✨ Features",
            value=(
                "✅ Natural conversations\n"
                "✅ Remembers last 5 messages\n"
                "✅ Searches wiki database\n"
                "✅ Gaming personality\n"
                "✅ Fast responses (1-2s)"
            ),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="clearmemory", description="Clear AI conversation memory for this channel")
    async def clearmemory(interaction: discord.Interaction):
        """Clear AI memory"""
        if not AI_AVAILABLE:
            await interaction.response.send_message(
                "❌ AI system is not available!",
                ephemeral=True
            )
            return
        
        if clear_memory(interaction.channel.id):
            await interaction.response.send_message(
                "✅ Conversation memory cleared for this channel!\n"
                "The AI will start fresh. 🧹",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "ℹ️ No conversation memory found for this channel.",
                ephemeral=True
            )
    
    @bot.tree.command(name="aitest", description="[STAFF] Test AI chat system")
    @app_commands.describe(message="Test message to send to AI")
    async def aitest(interaction: discord.Interaction, message: str):
        """Test AI"""
        if not is_staff(interaction):
            await interaction.response.send_message(
                "❌ This command is for staff only!",
                ephemeral=True
            )
            return
        
        if not AI_AVAILABLE:
            await interaction.response.send_message(
                "❌ AI system is not loaded!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            from utils.ai_chat import chat_with_groq
            
            response, sources = await chat_with_groq(
                message,
                interaction.channel.id,
                interaction.user.name
            )
            
            embed = discord.Embed(
                title="🧪 AI Test Result",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="📝 Your Message",
                value=f"```{message}```",
                inline=False
            )
            
            embed.add_field(
                name="🤖 AI Response",
                value=response[:1000] + ("..." if len(response) > 1000 else ""),
                inline=False
            )
            
            if sources:
                sources_text = "\n".join([f"• [{game}: {title}]({url})" for game, title, url in sources])
                embed.add_field(
                    name="📚 Sources Used",
                    value=sources_text,
                    inline=False
                )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ AI test failed!\n```{type(e).__name__}: {e}```",
                ephemeral=True
            )
    
    print("✅ AI commands loaded!")
