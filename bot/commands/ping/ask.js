const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ask')
		.setDescription('Get documentation from the channel'),
	async execute(interaction) {
		await interaction.reply('Here is the reply');
	},
};