import csv
import sys
from openpyxl import load_workbook

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

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Need to specify file name as second argument.")
	else:
		file_name = sys.argv[1]
		email_loader = EmailLoader(file_name)
		print email_loader.get_email_dict_array()[0]