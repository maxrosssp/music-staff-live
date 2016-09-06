from msl.settings import Settings
import cPickle as pickle

class ParamOperator:

	def __init__(self, settings=None):

		if isinstance(settings, dict) or settings is None:
			settings = Settings(settings)
		self.settings = settings

		self.directory = self.settings.get('PARAMETER_DIR')

	def load(self, category):
		filename = self.settings.get(category)
		params = None
		try:
			params = pickle.load( open(self.directory + '/' + filename, 'rb') )
		except:
			print("Unable to load saved parameters. Using defaults?")
			params = self.settings.getdict(category + '_DEFAULT')
			
		return params 

	def dump(self, category, dictionary):
		filename = self.settings.get(category)
		pickle.dump(dictionary, open(self.directory + '/' + filename, 'wb'))