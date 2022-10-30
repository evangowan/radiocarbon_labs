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

		self.entry_options = [
			{'number': 1, 'option': 'edit Lab Name'},
			{'number': 2, 'option': 'edit country'},
			{'number': 3, 'option': 'edit lab type'},
			{'number': 4, 'option': 'edit year opened'},
			{'number': 5, 'option': 'add fractionation notes'},
			{'number': 6, 'option': 'add uncertainty notes'},
			{'number': 7, 'option': 'add a reference'},
		  ]



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


	def add_fractionation_note(self):
		

		fractionation_note = self.fractionation_correction.copy()

		print("Input the year of the publication")
		try:
			year = int(input(">>> "))

			if year > 1600 and year < 2200: # hey, I am being conservative here
				success = True
				fractionation_note['year'] = year
			else:
				print("I suspect the year has been entered incorrectly")
				success = False
		except ValueError:
			print("Error in entering the year, aborting")
			success = False

		if success:
			print("Enter the notes about the fractionation:")
			fractionation_note['notes'] = input(">>> ")

			print("Enter the bibtex key for the reference:")
			fractionation_note['reference'] = input(">>> ")
			self.labinfo['fractionation_notes'].append(fractionation_note)

			self.labinfo['fractionation_notes'] = sorted(self.labinfo['fractionation_notes'], key=lambda k: k['year']) # sort the entries by year

		return success

	def add_uncertainty_note(self):
		

		uncertainty_note = self.uncertainty.copy()

		print("Input the year of the publication")
		try:
			year = int(input(">>> "))

			if year > 1600 and year < 2200: # hey, I am being conservative here
				success = True
				uncertainty_note['year'] = year
			else:
				print("I suspect the year has been entered incorrectly")
				success = False
		except ValueError:
			print("Error in entering the year, aborting")
			success = False

		if success:
			print("Enter the notes about the uncertainty:")
			uncertainty_note['notes'] = input(">>> ")

			print("Enter the bibtex key for the reference:")
			uncertainty_note['reference'] = input(">>> ")
			self.labinfo['uncertainty_notes'].append(uncertainty_note)

			self.labinfo['uncertainty_notes'] = sorted(self.labinfo['uncertainty_notes'], key=lambda k: k['year']) # sort the entries by year

		return success


	def add_reference(self):
		

		reference_note = self.reference.copy()

		print("Input the year of the publication")
		try:
			year = int(input(">>> "))

			if year > 1600 and year < 2200: # hey, I am being conservative here
				success = True
				reference_note['year'] = year
			else:
				print("I suspect the year has been entered incorrectly")
				success = False
		except ValueError:
			print("Error in entering the year, aborting")
			success = False

		if success:
			print("Enter the notes about the reference:")
			reference_note['notes'] = input(">>> ")

			print("Enter the lowest lab number found in this reference (enter to skip):")
			try:
				low_number = int(input(">>> "))
				if low_number < 1:
					print("Invalid number")
				else:
					reference_note['low_number'] = low_number
			except ValueError:
				print("Skipped adding lowest lab number")

			print("Enter the highest lab number found in this reference (enter to skip):")
			try:
				high_number = int(input(">>> "))
				if high_number < 1:
					print("Invalid number")
				else:
					reference_note['high_number'] = high_number
			except ValueError:
				print("Skipped adding lowest lab number")


			print("Enter the bibtex key for the reference:")
			reference_note['reference'] = input(">>> ")
			self.labinfo['references'].append(reference_note)

			self.labinfo['references'] = sorted(self.labinfo['references'], key=lambda k: k['year']) # sort the entries by year

		return success


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

		self.labcodes.sort()

		yaml.dump(self.labcodes, file, default_flow_style=False, allow_unicode=True)
		file.close()


	def write_labinfo_file(self):

		filename = "labs/" + self.labinfo['lab_id'] + ".yaml"

		file = open(filename, 'w')

		yaml.dump(self.labinfo, file, default_flow_style=False, allow_unicode=True)
		file.close()

	def print_options(self):

		for option in self.entry_options:
			print(f"{option['number']}) {option['option']}")

	def select_option(self):

		print("Select option")

		self.print_options()

		try:

			option_number = int(input(">>> "))
			found = False
			for option in self.entry_options:
				if option_number == option['number']:
					found = True

		except ValueError:
			found = False

		return found, option_number


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
	
		found, option_number = self.select_option()

		if found:
			if option_number == 1:
				self.add_lab_name()
				write_labinfo = True
			elif option_number == 2:
				self.add_country()
				write_labinfo = True
			elif option_number == 3:
				self.add_lab_type()
				write_labinfo = True
			elif option_number == 4:
				self.add_year_opened()
				write_labinfo = True
			elif option_number == 5:
				success = self.add_fractionation_note()
				if success:
					write_labinfo = True
			elif option_number == 6:
				success = self.add_uncertainty_note()
				if success:
					write_labinfo = True
			elif option_number == 7:
				success = self.add_reference()
				if success:
					write_labinfo = True
			else:
				print("nothing entered, exiting")

		if not found_labcode:
			self.write_labcode_file()

		if write_labinfo:
			self.write_labinfo_file()


if __name__ == "__main__":

	labentry_object = labentry()
	labentry_object.edit_entry()
