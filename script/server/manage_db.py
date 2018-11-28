import pyodbc

con_string = 'driver=MySQL ODBC 8.0 Unicode Driver;server=localhost;database=sncs_db;uid=root;pwd=root'

def execute_non_query(sql_cmd, con_string, params=None):
	with pyodbc.connect(con_string) as con:
		if params:
			con.execute(sql_cmd, params)


def insert_con_info(params):
	execute_non_query("""
		insert into website_controller(hostname, ip, status, sensor1, sensor2, sensor3, sensor4) 
		VALUES(?, ?, '1', 'wait..', 'wait..', 'wait..', 'wait..')
		""", con_string, params)


def update_sensor(params):
	execute_non_query("""
		update website_controller 
		set sensor1 = ?, sensor2 = ?, sensor3 = ?, sensor4 = ? 
		where hostname = ?
		""", con_string, params)


def base_template(model):
	with pyodbc.connect(con_string) as con:
		data = con.execute('select upload from website_base_template where modID_id = ?;', model)
		data = data.fetchone()
		return data


def insert_log_management(params):
	execute_non_query("""
		insert into website_management(ser_num_id, userID_id, new_config, date) 
		VALUES(?, ?, ?, ?)
		""", con_string, params)


def check_data(sql_cmd, sn):
	with pyodbc.connect(con_string) as con:
		for i in con.execute(sql_cmd):
			if sn in i[0] or i[0] in sn:
				return True


def check_id(sql_cmd, params):
	with pyodbc.connect(con_string) as con:
		data = con.execute(sql_cmd, params)
		data = data.fetchone()
		for i in data:
			return i


def insert_net_device(data_set, con_info):
	con_info = con_info[0].split(': ')
	data = []
	data.insert(0, data_set[0])
	data.insert(1, data_set[2])
	data.insert(2, check_id('select id from website_controller where hostname = ?;', con_info[0]))
	data.insert(3, 1)
	data.insert(4, check_id('select id from website_model where name = ?;', data_set[1]))
	 
	execute_non_query("""
		insert into website_network_devices(ser_num, hostname, con_id_id, devID_id, modID_id) 
		VALUES(?, ?, ?, ?, ?)
		""", con_string, data)


def insert_model(model):
	execute_non_query("""
		insert into website_model(name, devID_id)
		VALUES(?, ?)""", con_string, model)


def insert_device_detail(params):
	params[1] = 'Up'
	del params[2]
	execute_non_query("""
		insert into website_detail(ser_num_id, status, manufacturer, up_time, 
			interface_using, sw_image, sw_version, last_reset, fan, temp, power, serial_port) 
		VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		""", con_string, params)


def update_device_detail(params):
	update_host_device = []
	update_host_device.append(params[2])
	update_host_device.append(params[0])
	execute_non_query('update website_network_devices set hostname = ? where ser_num = ?;', con_string, update_host_device)
	del params[0:4]
	del params[2:4]
	params.insert(0, 'Up')
	execute_non_query("""
		update website_detail 
		set status = ?, up_time = ?, interface_using = ?, last_reset = ?, fan = ?, temp = ?, power = ?
		where serial_port = ?""", con_string, params)


def update_device_status(params):
	execute_non_query("""
		update website_detail
		set status = ?
		where serial_port = ?""", con_string, params)


def update_password(params):
	execute_non_query("""
		update website_network_devices
		set enable_pass = ?, console_pass = ?
		where ser_num = ?""", con_string, params)


def select_password():
	data = ''
	with pyodbc.connect(con_string) as con:
		for i in con.execute("""
			select website_detail.serial_port, website_network_devices.console_pass, website_network_devices.enable_pass
			from website_network_devices, website_detail
			where website_network_devices.ser_num = website_detail.ser_num_id"""):
			for j in i:
				data += j + ','
			data += ':'
	return data

if __name__ == '__main__':
	insert_con_info(params)
	update_sensor(params)
	check_data(sql_cmd, sn)
	check_id(sql_cmd, hostname)
	insert_net_device(data_set, con_info)
	insert_device_detail(params)
	update_device_detail(params)
	update_device_status(params)
	base_template(model)
	update_log_management(params)
	insert_log_management(params)
	update_password(params)
	select_password()
	insert_model(model)