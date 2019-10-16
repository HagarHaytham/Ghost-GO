experience = rl.combine_experience([
	collector1,
	collector2])
	
with h5py.File(experience_filename, 'w') as experience_outf:
	experience.serialize(experience_outf)