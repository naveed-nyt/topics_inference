import csv
import sys
import os
from openpyxl import load_workbook
import codecs, cStringIO
import re
import argparse

from text_cleaner import TextCleaner

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

	def get_email_dict_array(self, clean=False):
		extension = self.file_name.split('.')[-1].strip()
		if extension == 'csv':
			self._read_in_csv(self.file_name)
		elif extension == 'xlsx':
			data = self._read_in_xlxs(self.file_name)
		else:
			print "Unsupported data format!"
		email_dict_array = []
		for row in data:
			subject = ' '.join(TextCleaner(row[3]).tokenize_str())
			body = ' '.join(TextCleaner(row[4]).tokenize_str())
			email_dict_array.append({'direction': row[1], 'date': row[2], 'subject': subject, 'body': body})
		return email_dict_array	

	def write_to_text(self, file_name, dict_data, filter_outbound):
		file_name = file_name.split('/')[-1].split('.')[0] + '.txt' 
		with open(file_name, 'w') as f:
			for row in dict_data:
				if row and not filter_outbound or row['direction'] == 'inbound':
					if row['subject'] is not None and type(row['subject']) is unicode:
						f.write(row['subject'].encode('utf-8'))
					if row['body'] is not None and type(row['body']) is unicode:
						f.write(row['body'].encode('utf-8') + '\n')
		print("Wrote to " + file_name)

	def write_to_individual_files(self, file_name, output_dir, dict_data, filter_outbound):
		prefix = file_name.split('/')[-1].split('.')[0] + '_'
		file_counter = 1
		for row in dict_data:
			if not filter_outbound or row['direction'] == 'inbound':
				with open(os.path.join(output_dir, prefix + str(file_counter) + '.txt'), 'w') as f:
					if row['subject'] is not None and type(row['subject']) is unicode:
						f.write(row['subject'].encode('utf-8') + '\n')
					if row['body'] is not None and type(row['body']) is unicode:
						f.write(row['body'].encode('utf-8'))
					file_counter += 1

if __name__ == '__main__':

	if len(sys.argv) < 3:
		print("Usage: python email_reader.py splitfile FILE_NAME DIR_OUTPUT\n" + 
			  "                              singlefile FILE_NAME\n")
	elif len(sys.argv) >= 3:
		cmd = sys.argv[1]
		file_name = sys.argv[2]
		email_loader = EmailLoader(file_name)
		dict_arr = email_loader.get_email_dict_array()

		if cmd == 'singlefile':
			email_loader.write_to_text(file_name, dict_arr, True)

		if cmd == 'splitfile' and len(sys.argv) >= 4:	
			output_dir = sys.argv[3]
			email_loader.write_to_individual_files(file_name, output_dir, dict_arr, True)

