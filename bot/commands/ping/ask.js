const { SlashCommandBuilder } = require('discord.js');
const { executePython } = require('../../executePython.js')

module.exports = {
	data: new SlashCommandBuilder()
		.setName('ask')
		.setDescription('Get documentation from the channel')
		.addStringOption((option) => option.setName('question').setDescription('Enter your question').setRequired(true)),
	async execute(interaction) {
		// Contains the user's prompt
		const string = interaction.options.get("question").value

		console.log('a')

		await interaction.reply('Working on it...');

		// Execute python process and wait for the answer to be in a text readable file
		const response = await executePython(string)

		console.log(response, 'response')
		await interaction.followUp(response);
	},
};