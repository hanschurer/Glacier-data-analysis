import csv
import re
import utils
import matplotlib.pyplot as plt
from pathlib import Path


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        self.glaciers_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = float(lat)
        self.lon = float(lon)
        self.code = code
        self.mass = {}

    def add_mass_balance_measurement(self, year, mass_balance, partial):
        #validate year and mass balance
        utils.check_single_year_validate(year)
        utils.check_mass_balance_value(mass_balance)

        if year not in self.mass:
            self.mass[year] = []
        if partial:
            self.mass[year].append(mass_balance)
            total_balance = sum(self.mass[year])
            self.mass[year] = [total_balance]
        else:
            if len(self.mass[year]) == 0:
                self.mass[year] = [mass_balance, partial]

    def plot_mass_balance(self, output_path):
        if self.mass:
            years = self.mass.keys()
            values = [i for j in self.mass.values()
                      for i in j if type(i) == float]

        print(values)
        plt.plot(years, values)
        plt.xlabel("YERAS")
        plt.ylabel("MEASUREMENTS")
        plt.savefig(output_path)
        plt.close()


class GlacierCollection:
    def __init__(self, file_path):
        self.collection = []
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                utils.check_ID(row['WGMS_ID'])
                utils.check_political_unit(row['POLITICAL_UNIT'])
                utils.check_lon_range(row['LONGITUDE'])
                utils.check_lon_range(row['LATITUDE'])
                utils.check_code(row['PRIM_CLASSIFIC'] +
                                 row['FORM']+row['FRONTAL_CHARS'])
                glacier = Glacier(row['WGMS_ID'], row['NAME'], row['POLITICAL_UNIT'],
                                  float(row['LATITUDE']), float(row['LONGITUDE']), int(row['PRIM_CLASSIFIC']+row['FORM']+row['FRONTAL_CHARS']))
                self.collection.append(glacier)

    def read_mass_balance_data(self, file_path):
        partial = None

        # generate a list with all glacier id in it.
        glacier_id = []
        for glacier in self.collection:
            glacier_id.append(glacier.glaciers_id)

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            csv_reader = list(csv_reader)

            # check if the read in ID is in the collection
            for row in csv_reader:
                if row[2] not in glacier_id:
                    raise Exception(
                        'an unrecognised glacier identifier is encountered')

            for row in csv_reader:
                for glacier in self.collection:
                    utils.check_ID(row[2])
                    if row[11] == '':
                        continue
                    #check mass balance if it is valid
                    utils.check_mass_balance_value(row[11])

                    if (row[2] == glacier.glaciers_id):
                        # This proves that year can be converted to int, so it can be converted directly to int when passed in later
                        utils.check_single_year_validate(row[3])
                        utils.check_mass_balance_value(float(row[11]))

                        if (row[4] != '9999'):
                            partial = True
                            glacier.add_mass_balance_measurement(
                                int(row[3]), float(row[11]), partial)
                        else:
                            partial = False
                            glacier.add_mass_balance_measurement(
                                int(row[3]), float(row[11]), partial)

    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""
        utils.check_lat_range(lat)
        utils.check_lon_range(lon)

        distance = {}
        for i in self.collection:
            d = utils.haversine_distance(lat, lon, i.lat, i.lon)
            distance[d] = i.name

        sorted_dic = sorted(distance)
        result = []

        for i in range(n):
            result.append(distance[sorted_dic[i]])

        return result

    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        utils.check_code_pattern(code_pattern)

        patten = str(code_pattern).replace("?", "\\d")

        result = []
        for i in self.collection:
            utils.check_code(i.code)
            if(re.match(patten, str(i.code))):
                result.append(i.name)
        return result

    def sort_by_latest_mass_balance(self, n=5, reverse=False,):
        latest_mass_balance_and_year = {}
        temp = []
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        for i in self.collection:
            if i.mass:
                last_year = sorted(i.mass.keys())[-1]
                last_value = i.mass[last_year][0]
                latest_mass_balance_and_year[last_value] = i
                

        if reverse:
            for i in sorted(latest_mass_balance_and_year):
                temp.append(latest_mass_balance_and_year[i])
            return temp[0:n]

        else:
            for i in sorted(latest_mass_balance_and_year, reverse=True):
                temp.append(latest_mass_balance_and_year[i])
            return temp[0:n]

    def summary(self):
        earliest_year = []
        diction = {}
        for i in self.collection:
            if i.mass:
                earliest_year.append(min(i.mass.keys()))

        for i in self.collection:
            if i.mass:
                last_year = sorted(i.mass.keys())[-1]
                last_value = i.mass[last_year][0]
                diction[last_value] = i

        negetive = [i for i in diction.keys() if i < 0]

        shrunk = len(negetive)/len(diction)

        print(f'This collection has {len(self.collection)} glaciers.')
        print(f'The earliest measurement was in {min(earliest_year)}.')
        print(f'{round(shrunk,2)*100}% of glaciers shrunk in their last measurement.')

    def plot_extremes(self, output_path):

        grew_glacier = self.sort_by_latest_mass_balance(n=1, reverse=False)[0]
        shrunk_glacier = self.sort_by_latest_mass_balance(n=1, reverse=True)[0]

        grew_year = list(grew_glacier.mass.keys())
        grew_measurements = []
        for i in grew_glacier.mass.values():
            grew_measurements.append(i[0])

        shrunk_year = list(shrunk_glacier.mass.keys())
        shrunk_measuremnt = []
        for i in shrunk_glacier.mass.values():
            shrunk_measuremnt.append(i[0])

        figure = plt.figure(figsize=(15, 10))
        plt.subplot(211)
        plt.plot(grew_year, grew_measurements)
        plt.xlabel("YERAS")
        plt.ylabel("MEASUREMENTS")
        plt.subplot(212)
        plt.plot(shrunk_year, shrunk_measuremnt)
        plt.xlabel("YERAS")
        plt.ylabel("MEASUREMENTS")
        plt.savefig(output_path)
        plt.close()
