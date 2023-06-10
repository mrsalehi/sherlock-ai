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

		// Execute python process and wait for the answer to be in a text readable file
		executePython(async (data) => {
			// Send the answer back to the user
			await interaction.reply(`You typed "${data}"`);
		})
	},
};