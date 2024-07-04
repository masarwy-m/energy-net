Usage
=====

Here's a simple Python script that initializes your EnergyNetEnv environment

   .. code-block:: python

      def main():
		# Initialize the environment
		env = EnergyNetEnv()

		# Reset the environment; typically returns the initial observation
		observations = env.reset()
		print("Initial Observations:", observations)

		# Loop over agents in the environment
		for agent in env.agent_iter():
			# Obtain the observation, reward, done status, and additional info for this agent
			observation, reward, done, info = env.last()
			print(f"Agent: {agent}, Observation: {observation}, Reward: {reward}, Done: {done}")

			# If the agent's episode is over, pass an empty dict as the action
			if done:
				action = None
			else:
				# Otherwise, choose a sample action from the action space
				# This is a simplified example assuming discrete action spaces
				action = env.action_spaces[agent].sample()

			# Step the environment forward by providing the action
			env.step(action)

			# Optionally break the loop if all agents are done
			if all(env.dones.values()):
				break

		# Close the environment properly
		env.close()

	  if __name__ == "__main__":
		main()



