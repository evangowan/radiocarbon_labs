#!/usr/bin/env python3

import yaml
import sys
import os

class labentry:


	def __init__(self):

		self.labinfo = {
			'lab_name': '',
			'country': '',
			'lab_id': '',
			'lab_type': '', # conventional or AMS
			'year_opened': '', # the year that the lab opened, if known
			'fractionation_notes': [],
			'uncertainty_notes': [],
			'references': []
		  }

		self.labtypes = [ {'number': 1, 'type': 'conventional'}, {'number': 2, 'type': 'AMS'} ]

		self.fractionation_correction = {'year': '', 'notes': '', 'reference': ''}
		self.uncertainty = {'year': '', 'notes': '', 'reference': ''}

		self.reference =  {'year': '', 'notes': '', 'reference': '', 'low_number': '', 'high_number': ''}

		self.labcode_file = "labcodes.yaml"

		file = open(self.labcode_file, 'r')

		self.labcodes = yaml.safe_load(file)

		file.close()



	def add_lab_name(self):
		if self.labinfo['lab_name']:
			print(f"Current lab name: {self.labinfo['lab_name']}")

		print("Enter lab name:")

		self.labinfo['lab_name'] = input(">>> ")

	def add_country(self):
		if self.labinfo['country']:
			print(f"Current country: {self.labinfo['lab_name']}")

		print("Enter country:")

		self.labinfo['country'] = input(">>> ")

	def add_year_opened(self):
		if self.labinfo['year_opened']:
			print(f"Currently entered year open: {self.labinfo['year_opened']}")

		print("Enter year opened:")

		
		try:
			year = int(input(">>> "))


			if year > 1930:
				self.labinfo['year_opened'] = year
				found = True
			else:
				found = False

		except ValueError:
			found = False

		if not found:
			print("invalid input, nothing added")

	def add_lab_type(self):
		if self.labinfo['lab_type']:
			print(f"Current lab_type: {self.labinfo['lab_type']}")

		print("Enter the number of the lab type:")

		for lab_type in self.labtypes:
			print(f"{lab_type['number']}) {lab_type['type']}")

		try:
			lab_type_number = int(input(">>> "))

			found = False
			for lab_type in self.labtypes:
				if lab_type_number == lab_type['number']:
					self.labinfo['lab_type'] = lab_type['type']
					found = True
		except ValueError:
			found = False

		if not found:
			print("invalid input, nothing added")


	def check_labcode(self, lab_id):

		if lab_id in self.labcodes:
			found = True
		else:
			found = False

		return found


	def load_entry(self, lab_id):

		filename = 'labs/' + str(lab_id) + ".yaml"

		fileexists = os.path.isfile(filename)

		if fileexists:

			file = open(filename, 'r')

			datastore = yaml.safe_load(file)

			self.labinfo.update(datastore)
			
			file.close()

		else:
			print("file doesn't exist")
			sys.exit()


	def write_labcode_file(self):

		file = open(self.labcode_file, 'w')

		yaml.dump(self.labcodes, file, default_flow_style=False, allow_unicode=True)
		file.close()


	def write_labinfo_file(self):

		filename = "labs/" + self.labinfo['lab_id'] + ".yaml"

		file = open(filename, 'w')

		yaml.dump(self.labinfo, file, default_flow_style=False, allow_unicode=True)
		file.close()


	def edit_entry(self,lab_id=''):


		if lab_id == '':
			print("Enter the lab id code:")
			lab_id = input(">>> ")


		# check if it is in the lab code is entered yet

		found_labcode = self.check_labcode(lab_id)

		write_labinfo = False
		
		if found_labcode:
			# load the database file
			self.load_entry(lab_id)
		else:
			# enter the first few pieces of information

			self.labcodes.append(lab_id)
			self.labinfo['lab_id'] = str(lab_id)
			self.add_lab_name()
			self.add_country()
			self.add_lab_type()
			self.add_year_opened()

			write_labinfo = True
	
		print(self.labinfo)

		if not found_labcode:
			self.write_labcode_file()

		if write_labinfo:
			self.write_labinfo_file()


if __name__ == "__main__":

	labentry_object = labentry()
	labentry_object.edit_entry()
