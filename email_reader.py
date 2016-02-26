import csv
import sys
import os
from openpyxl import load_workbook
import codecs, cStringIO
import re

##
# Usage:
# 
# email_loader = EmailLoader(file_name)
# email_dict = email_loader.get_email_dict_array()
#
# print email_dict[0] -> {'date': '..', 'subject': '..', 'body': '..'}
# 
class EmailLoader:

	def __init__(self, file_name):
		self.file_name = file_name

	def _read_in_csv(self, file_name):
		rows = []
		print 'Reading in csv'
		with open(file_name, 'r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			for row in csv_reader:
				rows.append(row)
		return rows

	def _read_in_xlxs(self, file_name):
		print 'Reading in xlxs'
		data = []
		wb = load_workbook(filename=file_name, read_only=True)
		ws = wb['Consolidated']
		for row in ws.rows:
			data_cols = []
			for cell in row:
				data_cols.append(cell.value)
			data.append(data_cols)
		return data[1:]

	def get_email_dict_array(self):
		extension = self.file_name.split('.')[-1].strip()
		if extension == 'csv':
			self._read_in_csv(file_name)
		elif extension == 'xlsx':
			data = self._read_in_xlxs(file_name)
		else:
			print "Unsupported data format!"
		email_dict_array = []
		for row in data:
			email_dict_array.append({'date': row[2], 'subject': row[3], 'body': row[4]})
		return email_dict_array

	def write_to_text(self, file_name, dict_data):
		with open(file_name, 'w') as f:
			for row in dict_data:
				if row['body']:
					f.write(row['body'] + '\n')
		print("Wrote to " + file_name)

	def write_to_individual_files(self, output_dir, dict_data):
		file_counter = 1
		for row in dict_data:
			with open(os.path.join(output_dir, str(file_counter) + '.txt'), 'w') as f:
				if row['subject'] is not None:
					f.write(str(row['subject']) + '\n')
				f.write(str(row['body']))
				file_counter += 1

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: python email_reader.py splitfile FILE_NAME DIR_OUTPUT\n")
	else:
		cmd = sys.argv[1]
		if cmd == 'splitfile' and len(sys.argv) == 4:	
			file_name = sys.argv[2]
			output_dir = sys.argv[3]
			email_loader = EmailLoader(file_name)
			dict_arr = email_loader.get_email_dict_array()
			email_loader.write_to_individual_files(output_dir, dict_arr)
