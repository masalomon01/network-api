import os
from app import get_vars

schema = get_vars( os.getenv('CONFIG') or 'default', 'schema')

wkt_dict = {'traceid': 'linkid_parade', 'reverseid_trace': 'reverseid_parade', 'gid': 'linkid_ptv',
            'reverseid_gid': 'reverseid_ptv', 'fromnodeid_trace': 'fromnodeid_parade',
            'tonodeid_trace': 'tonodeid_parade', 'fromnodeid_gid': 'fromnodeid_ptv',
            'tonodeid_gid': 'tonodeid_ptv', 'wkt': 'wkt', 'length': 'length', 'speed': 'speed', 'ltype': 'ltype',
            'fftt': 'fftt', 'road': 'primaryname', 'tmc': 'tmc', 'lanes': 'numlanes', 'successors': 'successors',
            'predecessors': 'predecessors', 'new_ltype': 'new_ltype'}
var = '{}, '
var_last = '{} '
from_q = 'FROM {}.{}_{}'
from_table = 'FROM {}.{} '
group_by = 'GROUP BY {} '


class SQL_wkt:


	def __init__(self, city, id, args):
		self.city = city
		self.id = id
		self.arg_list = args


	def main_sql(self):
		query = """SELECT """
		num_of_args = len(self.arg_list)

		count = 0
		while count < num_of_args:
			query += var
			count += 1
		query += var_last
		query += from_q

		format = []
		for i in self.arg_list:
			v = wkt_dict[i]
			format.append(v)
		format.insert(0, wkt_dict[self.id])
		format.append(schema)
		format.append('wkt') # this is to specify that this is the wkt
		format.append(self.city)

		query = query.format(*format)

		return query


	def all_sql(self):
		query = """SELECT """
		keys = list(wkt_dict.keys())
		keys.remove(self.id)
		format = list(wkt_dict.values())
		format.remove(wkt_dict[self.id])
		format.insert(0, wkt_dict[self.id])
		format.append(schema)
		format.append('wkt')
		format.append(self.city)

		count = 1
		len_wkt = len(wkt_dict)
		while count < len_wkt:
			query += var
			count += 1
		query += var_last
		query += from_q
		query = query.format(*format)

		return query, keys



class SQL_id_only:


	def __init__(self, city, id, table, col_list=[]):
		self.city = city
		self.id = id
		self.table = table
		self.col_list = col_list

	def main_sql(self):
		query = """SELECT {}, """.format(self.id)
		table_name = self.table + '_' + self.city
		for each in self.col_list:
			query += each
			query += ', '
		query = query[:-2]  # remove the lat ', ' from the previous loop
		query += ' '
		query += from_table
		format = []
		format.append(schema)
		format.append(table_name)
		query = query.format(*format)

		return query


	def poe_sql(self):
		query = """SELECT {}, array_agg({}::int) """.format(self.id, self.col_list[0])
		table_name = self.table + '_' + self.city
		query += from_table
		query += group_by
		format = []
		format.append(schema)
		format.append(table_name)
		format.append(self.id)
		query = query.format(*format)

		return query




class SQL_census:


	def __init__(self, city, lat, lon):
		self.city = city
		self.lat = lat
		self.lon = lon


	def main_sql(self):
		# schema = 'sandbox'
		keys = ["city", "geojson"]
		if self.city == 'elpaso':
			query = """SELECT cve_ageb::text as zoneid, city, ST_AsGeoJSON(geom) from {}.elpaso_censustracts
					where city = 'Juarez'
					UNION
					SELECT tractce::text as zoneid, city, ST_AsGeoJSON(geom) from {}.elpaso_censustracts
					where city = 'elpaso'""".format(schema, schema)
		else:
			query = """ SELECT tractce as zoneid, city, ST_AsGeoJSON(geom) from {}.{}_censustracts""".format(schema, self.city)

		return query, keys


	def point_in_zone(self):
		# schema = 'sandbox'
		query = """ SELECT * FROM {}.{}_censustracts
					WHERE ST_Contains({}_censustracts.geom,
                    ST_Transform(
                        ST_GeomFromText('POINT({} {})', 4326), 4269)
                        )=true """.format(schema, self.city, self.city, self.lon, self.lat)  # -106.385386 31.757942

		return query



class SQL_main:


	def __init__(self, city, id, args, table):
		self.city = city
		self.id = id
		self.arg_list = args
		self.table = table


	def main_sql(self):
		query = """SELECT """
		num_of_args = len(self.arg_list)
		table_name = self.table + '_' + self.city

		count = 0
		while count < num_of_args:
			query += var
			count += 1
		query += var_last
		query += from_table

		format = []
		for i in self.arg_list:
			format.append(i)
		format.insert(0, self.id)
		format.append(schema)
		format.append(table_name)

		query = query.format(*format)

		return query


	def all_sql(self):
		query = """SELECT {}, *"""
		table_name = self.table + '_' + self.city
		format = []
		format.insert(0, self.id)
		format.append(schema)
		format.append(table_name)

		query += from_table

		query = query.format(*format)

		return query



class SQL_noid:


		def __init__(self, city, table, col_list=[]):
			self.city = city
			self.table = table
			self.col_list = col_list

		def all_sql(self):
			query = """SELECT *"""
			table_name = self.table + '_' + self.city
			format = []
			format.append(schema)
			format.append(table_name)

			query += from_table
			query = query.format(*format)

			return query

		def some_col(self):
			query = """SELECT """
			table_name = self.table + '_' + self.city
			for each in self.col_list:
				query += each
				query += ', '
			query = query[:-2]  # remove the lat ', ' from the previous loop
			format = []
			format.append(schema)
			format.append(table_name)
			query += ' '
			query += from_table
			query = query.format(*format)

			return query



class SQL_dma:
	def __init__(self, cityCode, idType, args, table):
		self.city = cityCode
		self.idType = idType
		self.arg_list = args
		self.table = table


	def main_sql(self):
		loq = []  # loq stands for list of queries
		if len(self.arg_list) > 1:
			links_q = tuple(self.arg_list)
		elif len(self.arg_list) == 1:   # added this logic because you don't want to tuple only one link
			links_q = '(' + self.arg_list[0] + ')'
		table_name = self.table + '_' + self.city
		if self.idType == 'gid':
			type = 'linkid_ptv'
		elif self.idType == 'traceid':
			type = 'linkid_parade'

		query = """ SELECT {}, '{}' as city, linkid_parade as contain, ST_AsGeoJSON(geom),
			            fftt, firstorientation, fromnodeid_parade, linkid_ptv, linkid_parade, lastorientation, length, 
			            new_ltype, primaryname, numlanes, predecessors, reverseid_parade, speed, successors, tmc, tonodeid_parade
			            FROM {}.{}
			            WHERE {} in {}""".format(type, self.city, schema, table_name, type, links_q)


		return query



class SQL_info:
	def __init__(self, table):
		self.table = table


	def active_network(self):
		query = """SELECT city, environment, network_version, to_char(deployment_date, 'MM-DD-YYYY HH24:MI:SS') as deployment_date, description
					FROM {}.{}
					WHERE deployment_date in (SELECT MAX(deployment_date) FROM {}.{} 
					GROUP BY city)""".format(schema, self.table,schema, self.table)

		return query






