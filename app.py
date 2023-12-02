from flask import Flask, render_template, request, redirect
from conexionBD import conectar_bd

programa = Flask(__name__)

mysql = conectar_bd(programa)
conexion = mysql.connect()
cursor = conexion.cursor()


@programa.route('/')
def index():
    return render_template('index.html')

@programa.route('/buscarCliente', methods = ['POST'])
def buscarCliente():

    buscador = request.form['cedula_reserva']

    if request.method == 'POST':

            # Estructura del codigo (#AA###A)
            if buscador[0].isdigit() and buscador[1:3].isalpha() and buscador[3:6].isdigit() and buscador[6:].isalpha():

                dato = buscador.upper()

                sql = f"SELECT res.codigo_reserva, cli.cedula, cli.nombres, cli.apellidos, cli.telefono, res.fecha_reserva FROM reservas AS res JOIN clientes AS cli ON res.id_cedula = cli.cedula WHERE res.codigo_reserva = '{dato}';"
                cursor.execute(sql)
                resultado = cursor.fetchone()
                conexion.commit()

                if resultado is None:

                    return render_template('index.html', mensaje = "No existe una reserva con este codigo.")

                else:

                    return render_template('index.html', cliente = resultado)
        
            elif len(buscador) > 4 or len(buscador) < 16:
                 
                if any(char.isdigit() for char in buscador) and buscador.isalnum():
                      
                    sql = f"SELECT res.codigo_reserva, cli.cedula, cli.nombres, cli.apellidos, cli.telefono, res.fecha_reserva FROM clientes AS cli LEFT JOIN reservas AS res ON cli.cedula = res.id_cedula WHERE cli.cedula = '{buscador}' ORDER BY fecha_reserva DESC;"                  
                    cursor.execute(sql)
                    resultado = cursor.fetchone()
                    conexion.commit()

                    if resultado is not None and len(resultado) > 0 and resultado[0] is not None:

                        return render_template('index.html', cliente = resultado)
                    
                    elif resultado is not None and len(resultado) > 0 and resultado[0] is None:

                        return render_template('index.html', cliente = resultado, mensaje = "El cliente no tiene una reserva.")
                    
                    else:

                        return render_template('index.html', mensaje = "La cedula no esta asociada con nuestro sistema.")
                                   
                else:

                    return  render_template('index.html', mensaje = "Digite un documento de indentidad valido.")
                    
            else:

                return render_template('index.html', mensaje = "Digite un documento de identidad valido.")       
       
    else:
        return redirect('/')

    
if __name__ == '__main__':
    programa.run(host='0.0.0.0', debug=True, port='8080')


