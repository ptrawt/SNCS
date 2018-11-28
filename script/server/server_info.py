import socket
import manage_db
import datetime
import client_config
from subprocess import run, PIPE
password = []

def auto_config(data_set):
	mod_id = manage_db.check_id('select id from website_model where name = ?;', data_set[1])
	file_name = manage_db.base_template(mod_id)
	data_write = ''
	time = datetime.datetime.now()
	time_to_filename = time.strftime("%Y%m%d-%H%M%S")
	if file_name == 'None':
		pass
	else:
		file_name = file_name[0]

		fo = open("C:/Users/dell/Documents/GitHub/SNCS/website/data/" + file_name, "r")
		txt = fo.read()
		command = ''
		enable_pass = ''
		console_pass = ''
		for i in txt.split('\n'):
			command += i + ','
			if 'pass' in i:
				if 'en' in i:
					i = i.split(' ')
					enable_pass = i[len(i)-1]
				else:
					i = i.split(' ')
					console_pass = i[len(i)-1]
		
		inp = '1:' + data_set[12] + ':'+ console_pass + ':' + enable_pass + ':' + command
		data = client_config.send_receive(inp)
		for line in data.split(','):
			data_write += line+'\r\n'
		with open('C:/Users/dell/Documents/GitHub/SNCS/website/data/logging_config/'+data_set[0]+'_'+time_to_filename+'.txt','wb+') as destination:
			destination.write(data_write.encode())
	
	print ('Auto configuration successed')
	file_name = data_set[0]+'_'+time_to_filename+'.txt'
	
	params = [data_set[0], '4', file_name, time] #serial_id, userID_id, new_config, old_config
	password = [enable_pass, console_pass, data_set[0]]
	return params, password


def controller_info(data_set): # function is insert information of Controller to database
	outdata = data_set[0].split(': ')
	if manage_db.check_data('select hostname from website_controller', outdata[0]):
		pass
	else:
		manage_db.insert_con_info(outdata)
		print ('control insert successed.')


def sensor(data_set): # function is update sensor values of Controller
	host = data_set[4].split(': ')
	del data_set[4]
	data_set.append(host[0])
	manage_db.update_sensor(data_set)

	print ('sensor update successed.')


def device_info(data_set, con_info): # function is insert and update information of Netowrk device to database
	if manage_db.check_data('select ser_num from website_network_devices', data_set[0]):
		manage_db.update_device_detail(data_set)
		print ('device update successed.')
	else:
		params, password = auto_config(data_set)
		model(data_set[1])
		manage_db.insert_net_device(data_set, con_info)
		manage_db.insert_device_detail(data_set)
		manage_db.update_password(password)
		print(params)
		manage_db.insert_log_management(params)

		print ('device insert successed.')


def model(model):
	if manage_db.check_data('select name from website_model', model):
		print('model have in db.')
	else:
		manage_db.insert_model([model, '1'])
		print ('model insert successed.')


def device_status(data_set):
	manage_db.update_device_status(data_set)
	print ('device status Down update.')
	

def main():
	print("Start server information.")
	host = '' # Get local machine name
	port = 30001                # Reserve a port for your service.
	s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)         # Create a socket object

	try:
		s.bind((host, port))    # Bind to the port
	except socket.error as e:
		raise e
	# except:
	# 	print ('Socket is not connect.')
		# main()

	s.listen(5)                 # Now wait for client connection.
	c, addr = s.accept()        # Establish connection with client.
				 
	print( "Start socket.....")
	print ('Got connection from', addr)
	con_info = []
	
	while True:
		try:
			data = c.recv(1024)
		except Exception as e:
			print (e)
			break
		else:
			data = data.decode()
			data_set = data.split('\n')
			password = manage_db.select_password()
			if 'password' in data_set:
				if password != '':
					print (password)
					c.send(password.encode())
				else:
					c.send('no password'.encode())
			elif 'controller info:' in data_set:
				del data_set[0]
				con_info = data_set
				controller_info(data_set)	
				#print (data_set)
			elif 'Sensor' in data_set:
				del data_set[0]
				sensor(data_set)
				#print (data_set)
			elif 'device_info' in data_set:
				del data_set[0]
				if data_set[0] == 'Down':
					device_status(data_set)
				#print (data_set)
				elif data_set[0] == "Cannot connect serial":
					pass
				else:
					device_info(data_set, con_info)
			else:
				pass

	c.close()                # Close the connection
	main()

if __name__ == '__main__':
	main()