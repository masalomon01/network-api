

wkt_dict = {'traceid': 'linkid_parade', 'reverseid_trace': 'reverseid_parade', 'gid': 'linkid_ptv',
            'reverseid_gid': 'reverseid_ptv', 'fromnodeid_trace': 'fromnodeid_parade',
            'tonodeid_trace': 'tonodeid_parade', 'fromnodeid_gid': 'fromnodeid_ptv',
            'tonodeid_gid': 'tonodeid_ptv', 'wkt': 'wkt', 'length': 'length', 'speed': 'speed', 'ltype': 'ltype',
            'fftt': 'fftt', 'road': 'primaryname', 'tmc': 'tmc', 'lanes': 'numlanes', 'successors': 'successors',
            'predecessors': 'predecessors', 'new_ltype': 'new_ltype'}
schema = 'dev_wkts'
var = '{}, '
var_last = '{} '
from_q = 'FROM {}.dev_wkts_{}'


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



class SQL_zone:


	def __init__(self, city, id):
		self.city = city
		self.id = id

	def main_sql(self):
		zone_dict = {'traceid': 'linkid_parade', 'gid':'gid'}
		query = """SELECT {}, {} FROM {}.zones_{}"""
		format = ['zone']
		format.insert(0, zone_dict[self.id])
		format.append(schema)
		format.append(self.city)
		query = query.format(*format)

		return query



class SQL_census:


	def __init__(self, city):
		self.city = city


	def main_sql(self):
		schema = 'sandbox'
		if self.city == 'elpaso':
			query = """SELECT cve_ageb::text as zoneid, city, ST_AsGeoJSON(geom) from sandbox.elpaso_juarez_censustracts
					where city = 'Juarez'
					UNION
					SELECT tractce::text as zoneid, city, ST_AsGeoJSON(geom) from sandbox.elpaso_juarez_censustracts
					where city = 'elpaso'"""
		else:
			query = """ SELECT tractce as zoneid, city, ST_AsGeoJSON(geom) from {}.{}_censustracts""".format(schema, self.city)

		return query
