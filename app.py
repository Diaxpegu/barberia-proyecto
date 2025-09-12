from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# Base de datos temporal
peluqueros = [
    {
        'id': 1,
        'nombre': 'Lucas Aldair',
        'instagram': 'lukas__aldair',
        'servicios': ['Corte básico', 'Corte premium', 'Tintura', 'Lavado', 'Peinado'],
        'precios': {
            'Corte básico': 15000,
            'Corte premium': 20000,
            'Tintura': 25000,
            'Lavado': 5000,
            'Peinado': 10000
        },
        'horarios': {
            '2023-12-20': {
                '08:00': 'disponible',
                '09:00': 'disponible',
                '10:00': 'disponible',
                '11:00': 'ocupado',
                '12:00': 'por confirmar',
                '13:00': 'disponible',
                '14:00': 'disponible',
                '15:00': 'disponible',
                '16:00': 'disponible',
                '17:00': 'disponible'
            },
            '2023-12-21': {
                '08:00': 'disponible',
                '09:00': 'disponible',
                '10:00': 'disponible',
                '11:00': 'disponible',
                '12:00': 'disponible',
                '13:00': 'disponible',
                '14:00': 'disponible',
                '15:00': 'disponible',
                '16:00': 'disponible',
                '17:00': 'disponible'
            }
        }
    },
    {
        'id': 2,
        'nombre': 'Alejandro',
        'instagram': 'ale_.cut',
        'servicios': ['Corte básico', 'Corte premium', 'Tintura', 'Lavado', 'Peinado'],
        'precios': {
            'Corte básico': 15000,
            'Corte premium': 20000,
            'Tintura': 25000,
            'Lavado': 5000,
            'Peinado': 10000
        },
        'horarios': {
            '2023-12-20': {
                '08:00': 'disponible',
                '09:00': 'disponible',
                '10:00': 'disponible',
                '11:00': 'disponible',
                '12:00': 'por confirmar',
                '13:00': 'disponible',
                '14:00': 'disponible',
                '15:00': 'disponible',
                '16:00': 'disponible',
                '17:00': 'disponible'
            },
            '2023-12-21': {
                '08:00': 'disponible',
                '09:00': 'disponible',
                '10:00': 'disponible',
                '11:00': 'disponible',
                '12:00': 'disponible',
                '13:00': 'disponible',
                '14:00': 'disponible',
                '15:00': 'disponible',
                '16:00': 'disponible',
                '17:00': 'disponible'
            }
        }
    }
]

clientes = []
reservas = []

@app.route('/')
def index():
    # Datos de ejemplo para las nuevas secciones
    about_info = {
        'titulo': 'VALIANT Barbería',
        'descripcion': 'En VALIANT nos especializamos en cortes de cabello modernos, arreglo de barba y tratamientos faciales. Nuestro equipo de barberos profesionales está comprometido con brindarte la mejor experiencia y resultados excepcionales.',
        'historia': 'Fundada en 2015, nuestra barbería se ha convertido en un referente en la ciudad gracias a nuestra atención personalizada y ambiente acogedor. Utilizamos productos de primera calidad y las técnicas más actualizadas.'
    }
    
    contact_info = {
        'direccion': 'Victoria 2486, Valparaíso, Chile',
        'telefono': '+56 9 1234 5678',
        'email': 'info@valiantbarber.com',
        'redes_sociales': {
            'instagram': 'https://instagram.com/valiant_barber',
            'facebook': '#',
            'twitter': '#'
        }
    }
    
    return render_template('index.html', peluqueros=peluqueros, about_info=about_info, contact_info=contact_info)

@app.route('/reserva/<int:peluquero_id>', methods=['GET', 'POST'])
def reserva(peluquero_id):
    peluquero = next((p for p in peluqueros if p['id'] == peluquero_id), None)
    
    if not peluquero:
        return redirect(url_for('index'))
    
    # Obtener la fecha actual del parámetro GET o usar la primera disponible
    fecha_actual = request.args.get('fecha')
    if not fecha_actual and peluquero['horarios']:
        fecha_actual = next(iter(peluquero['horarios'].keys()))
    
    if request.method == 'POST':
        try:
            # Procesar datos del formulario
            fecha = request.form['fecha']
            hora = request.form['hora']
            servicio = request.form['servicio']
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            email = request.form['email']
            telefono = request.form['telefono']
            rut = request.form.get('rut', '').strip().upper()
            
            # Verificar y crear horarios si la fecha no existe
            if fecha not in peluquero['horarios']:
                peluquero['horarios'][fecha] = {
                    '08:00': 'disponible',
                    '09:00': 'disponible',
                    '10:00': 'disponible',
                    '11:00': 'disponible',
                    '12:00': 'disponible',
                    '13:00': 'disponible',
                    '14:00': 'disponible',
                    '15:00': 'disponible',
                    '16:00': 'disponible',
                    '17:00': 'disponible'
                }
            
            # Validar disponibilidad del horario
            if peluquero['horarios'][fecha].get(hora) != 'disponible':
                return render_template('reserva.html', 
                                   peluquero=peluquero,
                                   fecha_actual=fecha,
                                   error="El horario seleccionado ya no está disponible")
            
            # Actualizar estado del horario
            peluquero['horarios'][fecha][hora] = 'ocupado'
            
            # Buscar cliente existente o crear uno nuevo
            cliente_existente = next((c for c in clientes if c['email'] == email), None)
            
            if cliente_existente:
                cliente_existente['visitas'] += 1
                cliente_existente['telefono'] = telefono
                if rut:
                    cliente_existente['rut'] = rut
                cliente_id = cliente_existente['id']
            else:
                nuevo_cliente = {
                    'id': len(clientes) + 1,
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': email,
                    'telefono': telefono,
                    'rut': rut,
                    'visitas': 1
                }
                clientes.append(nuevo_cliente)
                cliente_id = nuevo_cliente['id']
            
            # Crear nueva reserva
            nueva_reserva = {
                'id': len(reservas) + 1,
                'peluquero_id': peluquero_id,
                'cliente_id': cliente_id,
                'fecha': fecha,
                'hora': hora,
                'servicio': servicio,
                'estado': 'confirmada',
                'email': email,
                'telefono': telefono,
                'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            reservas.append(nueva_reserva)
            
            # Redirigir a página de confirmación o panel
            return redirect(url_for('confirmacion_reserva', reserva_id=len(reservas)))
            
        except Exception as e:
            print(f"Error al procesar reserva: {str(e)}")
            return render_template('reserva.html', 
                               peluquero=peluquero,
                               fecha_actual=fecha_actual,
                               error="Ocurrió un error al procesar tu reserva. Por favor intenta nuevamente.")
    
    return render_template('reserva.html', 
                         peluquero=peluquero,
                         fecha_actual=fecha_actual)

@app.route('/confirmacion/<int:reserva_id>')
def confirmacion_reserva(reserva_id):
    if reserva_id > len(reservas) or reserva_id < 1:
        return redirect(url_for('index'))
    
    reserva = reservas[reserva_id - 1]
    peluquero = next((p for p in peluqueros if p['id'] == reserva['peluquero_id']), None)
    cliente = next((c for c in clientes if c['id'] == reserva['cliente_id']), None)
    
    if not peluquero or not cliente:
        return redirect(url_for('index'))
    
    return render_template('confirmacion.html',
                         reserva=reserva,
                         peluquero=peluquero,
                         cliente=cliente)

@app.route('/panel/<int:peluquero_id>')
def panel_peluquero(peluquero_id):
    peluquero = next((p for p in peluqueros if p['id'] == peluquero_id), None)
    if not peluquero:
        return redirect(url_for('index'))
    
    # Obtener reservas del peluquero con datos del cliente
    reservas_peluquero = []
    for r in reservas:
        if r['peluquero_id'] == peluquero_id:
            cliente = next((c for c in clientes if c['id'] == r['cliente_id']), None)
            if cliente:
                reserva_con_datos = {
                    'id': r['id'],
                    'fecha': r['fecha'],
                    'hora': r['hora'],
                    'servicio': r['servicio'],
                    'estado': r['estado'],
                    'cliente_nombre': f"{cliente['nombre']} {cliente['apellido']}",
                    'email': cliente['email'],
                    'telefono': cliente.get('telefono', ''),
                    'rut': cliente.get('rut', ''),
                    'visitas': cliente['visitas'],
                    'fecha_registro': r.get('fecha_registro', '')
                }
                reservas_peluquero.append(reserva_con_datos)
    
    # Ordenar reservas por fecha y hora (más recientes primero)
    reservas_peluquero.sort(key=lambda x: (x['fecha'], x['hora']), reverse=True)
    
    return render_template('panel_peluquero.html',
                         peluquero=peluquero,
                         reservas=reservas_peluquero)

# API para obtener horarios disponibles
@app.route('/api/horarios/<int:peluquero_id>/<fecha>')
def api_horarios(peluquero_id, fecha):
    peluquero = next((p for p in peluqueros if p['id'] == peluquero_id), None)
    
    if not peluquero:
        return jsonify({'error': 'Peluquero no encontrado'}), 404
    
    # Si la fecha no existe en los horarios, crear horarios por defecto
    if fecha not in peluquero['horarios']:
        peluquero['horarios'][fecha] = {
            '08:00': 'disponible',
            '09:00': 'disponible',
            '10:00': 'disponible',
            '11:00': 'disponible',
            '12:00': 'disponible',
            '13:00': 'disponible',
            '14:00': 'disponible',
            '15:00': 'disponible',
            '16:00': 'disponible',
            '17:00': 'disponible'
        }
    
    return jsonify(peluquero['horarios'][fecha])

if __name__ == '__main__':
    app.run(debug=True)