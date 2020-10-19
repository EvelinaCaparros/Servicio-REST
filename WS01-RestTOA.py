#######################################################################################################################################
#    NOMBRE DEL SCRIPT:  WS01-RestTOA.py                                                                                              #
#                                                                                                                                     #
#    DESCRIPCION:  Servicios REST POST                                                                                                #
#                                                                                                                                     #
#    AUTOR/A: Evelina M. Caparrós Frentzel                                                                                            #
#                                                                                                                                     #
#    FRAMEWORKS: Flask														      #
#                BD: SQLAlchemy													      #
#                HTML: jinja2 													      #
#                                                                                                                                     #
#    DEPENDENCIAS:  datetime (lib de fechas)										              #
#                   Driver BD: postgres (lib psycopg2-binary)								              #
#																      #
#    Servicios dentro del archivo:                                                                                                    # 
#       				addCupoEmpresa                   				          		      # 
#      					addCupoIndividuos            					  			      # 
#######################################################################################################################################


from flask import Flask, jsonify, request, render_template 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from datetime import datetime
import jinja2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://USER:PASSWORD@IP:PORT/postgres'
db = SQLAlchemy(app)


#Definicion de Excepciones
class Error(Exception):
   """Base para todas las excepciones"""
   pass
   
class MaxLongError(Error):
   """Supera el valor máximo de la longitud definina en las clases de TOA_CUPOS_EMPRESA y TOA_CUPOS_INDIVIDUOS"""
   pass

class CampoNuloError(Error):
	"""Si uno de los campos que no debe ser nulo lo es"""
	pass
class ValorIncorrectoError(Error):
	"""Se recibe un valor incorrecto (un valor que no se encuentra dentro de la lista)"""
	pass
class REST04Error(Error):
	"""Se recibio un caracter no válido. Esto se encuentra definido en listaREST04"""
	pass
class REST05Error(Error):
	"""Se recibio un caracter no válido. Esto se encuentra definido en listaREST05"""
	pass


#Clase que representa el modelo de la tabla TOA_CUPOS_EMPRESA
class TOA_CUPOS_EMPRESA(db.Model):
	"""Definición de todos los campos para el servicio addCupoIndividuos"""
	access_technology = db.Column(db.String(10), primary_key=True)
	telephone_technology = db.Column(db.String(10), primary_key=True)
	broadband_technology = db.Column(db.String(10))
	tv_technology = db.Column(db.String(10))
	ubicacion = db.Column(db.String(20), primary_key=True)
	fecha = db.Column(db.DateTime, primary_key=True)
	time_slot = db.Column(db.String(5), primary_key=True)
	work_skill = db.Column(db.String(30), primary_key=True)
	available = db.Column(db.Integer, primary_key=True)
	sys_creation_date = db.Column(db.DateTime, default=datetime.now, primary_key=True)
	
	__table_args__ = {'schema':'connectis'}	
	__tablename__ = 'toa_cupos_empresa'
	
	def __init__(self,access_technology,telephone_technology,broadband_technology,tv_technology,ubicacion,fecha,time_slot,work_skill,available):
		"""Correlación con el campo de la BD"""
		self.access_technology = access_technology
		self.telephone_technology = telephone_technology
		self.broadband_technology = broadband_technology
		self.tv_technology = tv_technology
		self.ubicacion = ubicacion
		self.fecha = fecha
		self.time_slot = time_slot
		self.work_skill = work_skill
		self.available = available


#Clase que representa el modelo de la tabla TOA_CUPOS_INDIVIDUOS
class TOA_CUPOS_INDIVIDUOS(db.Model):
	"""Definición de todos los campos para el servicio addCupoEmpresa"""
	access_technology = db.Column(db.String(10), primary_key=True)
	telephone_technology = db.Column(db.String(10), primary_key=True)
	broadband_technology = db.Column(db.String(10))
	tv_technology = db.Column(db.String(10))
	ubicacion = db.Column(db.String(20), primary_key=True)
	fecha = db.Column(db.DateTime, primary_key=True)
	time_slot = db.Column(db.String(5), primary_key=True)
	work_skill = db.Column(db.String(30), primary_key=True)
	available = db.Column(db.Integer, primary_key=True)
	sys_creation_date = db.Column(db.DateTime, default=datetime.now, primary_key=True)
	
	__table_args__ = {'schema':'connectis'}
	__tablename__ = 'toa_cupos_individuos'
	
	def __init__(self,access_technology,telephone_technology,broadband_technology,tv_technology,ubicacion,fecha,time_slot,work_skill,available):
		"""Correlación con el campo de la BD"""
		self.access_technology = access_technology
		self.telephone_technology = telephone_technology
		self.broadband_technology = broadband_technology
		self.tv_technology = tv_technology
		self.ubicacion = ubicacion
		self.fecha = fecha
		self.time_slot = time_slot
		self.work_skill = work_skill
		self.available = available


#Valores válidos para los distintos campos (se encuentran sujetos a configuración)
listaAccesTechnology = ["COBRE", "FIBRA"]
listaTelephoneTechnology = ["PSTN", "VOIP"]
listaTimeSlot = ["AM", "PM"]

listaBroadbandTechnology = ["ADSL2Plus", "ADSL", "ADSL2", "VDSL", "FTTH", "FTTN"]
listaTVTechnology = ["IPTV"]

listaUbicacion = ["BK_JUNCAL", "BK_NORTE_ZONA_ATC", "BK_SAN_MARTIN", "BK_ISIDRO_CASANOVA_CTTA", "BK_ISIDRO_CASANOVA_NORTE", "BK_ISIDRO_CASANOVA_SUR", "BK_DESAMPARADO CTTA", "BK_DESAMPARADO_RG", "BK_DESAMPARADO", "BK_RESTO_NORTE", "BK_ACCESO ROSARIO", "BK_ACC_MAR_DEL_PLATA", "BK_MS_MAR_DEL_PLATA", "BK_TUPS_MAR_DEL_PL"]

listaWorkSkill = ["INS_FIBRA_RESID", "INS_ADSL_STB", "Cruzada FTTN", "INS_FIBRA_UNE2", "Instalar_Publica_Tasa", "INS_FIBRA_NEG", "INS_FIBRA_NEG2", "INS_EMPRESAS", "Cruzada FTTN 3ros", "INS_PUBLICA", "Desinstalar Publica TASA", "Desinstalar Publica Terceros", "INS_FIBRA_NEG2", "INS_FIBRA_RESID", "Cruzada FTTN", "INS_EMPRESAS", "INS_FIBRA_UNE2", "INS_FIBRA_UNE2", "INS_FIBRA_NEG2", "INS_ADSL_STB_NEG", "INS_FIBRA_RESID", "REP_PUBLICA", "REP COBRE", "REP_WLL", "REP_PI", "REP_PI_TX", "EMPALMADOR", "REP_FIBRA", "REPARTIDOR", "Rep_Bajadas_y_Supervision", "REP_AVDSL_INST"]


#Valores inválidos para los distintos campos
listaREST04 = ["-", ";", ",", "."]  
listaREST04f = [";", ",", "."]   
listaREST05 = ["#", "$", "%", "&", "/", "¿", "?", "(", ")", "=", "¡", "!", "{", "}", "[", "]", "|", "\\" ] 


#Servicio que guarda los cupos en la tabla TOA_CUPOS_EMPRESA
@app.route('/save_empresa', methods=['POST'])
def addCupoEmpresa():
	try:
		if len(request.json['access_technology']) > 10 or len(request.json['telephone_technology']) > 10 or len(request.json['broadband_technology']) > 10 or len(request.json['tv_technology'])> 10 or len(request.json['ubicacion']) > 20 or len(request.json['time_slot']) > 5 or len(request.json['work_skill']) > 30:
			raise MaxLongError
			
		elif not request.json['access_technology'] or not request.json['telephone_technology'] or not request.json['ubicacion'] or not request.json['fecha'] or not request.json['time_slot'] or not request.json['work_skill'] or not request.json['available'] :
			raise CampoNuloError 
			
		elif request.json['access_technology'] in listaREST04 or request.json['telephone_technology'] in listaREST04 or request.json['broadband_technology'] in listaREST04 or request.json['tv_technology'] in listaREST04 or request.json['ubicacion'] in listaREST04 or request.json['time_slot'] in listaREST04 or request.json['work_skill'] in listaREST04 or request.json['fecha'] in listaREST04f:
			raise REST04Error
		
		elif request.json['access_technology'] in listaREST05 or request.json['telephone_technology'] in  listaREST05 or request.json['broadband_technology'] in listaREST05 or request.json['tv_technology'] in listaREST05 or request.json['ubicacion'] in listaREST05 or request.json['time_slot'] in listaREST05 or request.json['work_skill'] in listaREST05 or request.json['fecha'] in listaREST05:
			raise REST05Error
			
		elif request.json['access_technology'] not in listaAccesTechnology or request.json['telephone_technology'] not in listaTelephoneTechnology or request.json['ubicacion'] not in listaUbicacion or request.json['time_slot'] not in listaTimeSlot or request.json['work_skill'] not in listaWorkSkill: 
			raise ValorIncorrectoError
						
		elif request.json['access_technology'] in listaAccesTechnology and request.json['telephone_technology'] in listaTelephoneTechnology and (request.json['broadband_technology'] in listaBroadbandTechnology or not request.json['broadband_technology']) and (request.json['tv_technology'] in listaTVTechnology or not request.json['tv_technology']) and request.json['ubicacion'] in listaUbicacion and request.json['time_slot'] in listaTimeSlot and request.json['work_skill'] in listaWorkSkill:
			new_cupo = TOA_CUPOS_EMPRESA(request.json['access_technology'], request.json['telephone_technology'], request.json['broadband_technology'], request.json['tv_technology'], request.json['ubicacion'], request.json['fecha'], request.json['time_slot'], request.json['work_skill'], request.json['available'])
			db.session.add(new_cupo)
			db.session.commit()
			return jsonify(response_code='200',
							response_text='El cupo ha sido creado correctamente'),200
		
		elif request.json['broadband_technology'] not in listaBroadbandTechnology or request.json['tv_technology'] not in listaTVTechnology:
			raise ValorIncorrectoError
		
	except CampoNuloError:
		return jsonify(response_code='REST01',
				   response_text='Se ha recibido un campo nulo.'), 400
	
	except MaxLongError:
		return jsonify(response_code='REST02',
				   response_text='La cantidad de caracteres supera el máximo permitido.'), 400
	
	except ValorIncorrectoError:
		return jsonify(response_code='REST03',
				   response_text='Se recibió un valor incorrecto.'), 400
	
	except REST04Error:
		return jsonify(response_code='REST04',
				   response_text='Se ha recibido un carácter no válido.'), 400
	
	except REST05Error:
		return jsonify(response_code='REST05',
				   response_text='Se ha recibido un carácter no válido.'), 400
	
	except exc.DataError:
		return jsonify(response_code='REST06',
				   response_text='Se recibió un valor incorrecto.'), 400

	except KeyError:
		return jsonify(response_code='REST07',
				       response_text='No se ha enviado un campo mandatorio.'), 400	


#Servicio que guarda los cupos en la tabla TOA_CUPOS_INDIVIDUOS
@app.route('/save_individuos', methods=['POST'])
def addCupoIndividuos():
	try:
		if len(request.json['access_technology']) > 10 or len(request.json['telephone_technology']) > 10 or len(request.json['broadband_technology']) > 10 or len(request.json['tv_technology'])> 10 or len(request.json['ubicacion']) > 20 or len(request.json['time_slot']) > 5 or len(request.json['work_skill']) > 30:
			raise MaxLongError
			
		elif not request.json['access_technology'] or not request.json['telephone_technology'] or not request.json['ubicacion'] or not request.json['fecha'] or not request.json['time_slot'] or not request.json['work_skill'] or not request.json['available'] :
			raise CampoNuloError 
			
		elif request.json['access_technology'] in listaREST04 or request.json['telephone_technology'] in listaREST04 or request.json['broadband_technology'] in listaREST04 or request.json['tv_technology'] in listaREST04 or request.json['ubicacion'] in listaREST04 or request.json['time_slot'] in listaREST04 or request.json['work_skill'] in listaREST04 or request.json['fecha'] in listaREST04f:
			raise REST04Error
		
		elif request.json['access_technology'] in listaREST05 or request.json['telephone_technology'] in  listaREST05 or request.json['broadband_technology'] in listaREST05 or request.json['tv_technology'] in listaREST05 or request.json['ubicacion'] in listaREST05 or request.json['time_slot'] in listaREST05 or request.json['work_skill'] in listaREST05 or request.json['fecha'] in listaREST05:
			raise REST05Error
			
		elif request.json['access_technology'] not in listaAccesTechnology or request.json['telephone_technology'] not in listaTelephoneTechnology or request.json['ubicacion'] not in listaUbicacion or request.json['time_slot'] not in listaTimeSlot or request.json['work_skill'] not in listaWorkSkill: 
			raise ValorIncorrectoError
						
		elif request.json['access_technology'] in listaAccesTechnology and request.json['telephone_technology'] in listaTelephoneTechnology and (request.json['broadband_technology'] in listaBroadbandTechnology or not request.json['broadband_technology']) and (request.json['tv_technology'] in listaTVTechnology or not request.json['tv_technology']) and request.json['ubicacion'] in listaUbicacion and request.json['time_slot'] in listaTimeSlot and request.json['work_skill'] in listaWorkSkill:
			new_cupo = TOA_CUPOS_INDIVIDUOS(request.json['access_technology'], request.json['telephone_technology'], request.json['broadband_technology'], request.json['tv_technology'], request.json['ubicacion'], request.json['fecha'], request.json['time_slot'], request.json['work_skill'], request.json['available'])
			db.session.add(new_cupo)
			db.session.commit()
			return jsonify(response_code='200',
							response_text='El cupo ha sido creado correctamente'), 200
		elif request.json['broadband_technology'] not in listaBroadbandTechnology or request.json['tv_technology'] not in listaTVTechnology:
			raise ValorIncorrectoError
	
	except CampoNuloError:
		return jsonify(response_code='REST01',
				   response_text='Se ha recibido un campo nulo.'), 400
	
	except MaxLongError:
		return jsonify(response_code='REST02',
				   response_text='La cantidad de caracteres supera el máximo permitido.'), 400
	
	except ValorIncorrectoError:
		return jsonify(response_code='REST03',
				   response_text='Se recibió un valor incorrecto.'), 400
	
	except REST04Error:
		return jsonify(response_code='REST04',
				   response_text='Se ha recibido un carácter no válido.'), 400
	
	except REST05Error:
		return jsonify(response_code='REST05',
				   response_text='Se ha recibido un carácter no válido.'), 400
	
	except exc.DataError:
		return jsonify(response_code='REST06',
				   response_text='Se recibió un valor incorrecto.'), 400

	except KeyError:
		return jsonify(response_code='REST07',
				       response_text='No se ha enviado un campo mandatorio.'), 400


#Se ejecuta como archivo principal (debug= True). El script se reinicia si hay un cambio.
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=5555) 
