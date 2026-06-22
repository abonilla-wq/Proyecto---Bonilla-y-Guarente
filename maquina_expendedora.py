# Integrantes: Ariadna Bonilla, Isabella Guarente.

from producto import Producto
from tarjeta import Tarjeta
from venta import Venta
from restock import Restock

class MaquinaExpendedora:
    def __init__(self):
        self.inventario = {}
        self.tarjetas = {}

    def iniciar_sistema(self):
        import requests
        import json
        
        url_cli = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/clientes.json"
        url_prod = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/productos.json"
        
        datos_cli = None
        datos_prod = None
        
        try:
            res_cli = requests.get(url_cli, timeout=5)
            datos_cli = res_cli.json()
            
            res_prod = requests.get(url_prod, timeout=5)
            datos_prod = res_prod.json()
            
            with open("clientes_local.json", "w") as f_cli:
                json.dump(datos_cli, f_cli)
            with open("productos_local.json", "w") as f_prod:
                json.dump(datos_prod, f_prod)
                
        except Exception:
            try:
                with open("clientes_local.json", "r") as f_cli:
                    datos_cli = json.load(f_cli)
                with open("productos_local.json", "r") as f_prod:
                    datos_prod = json.load(f_prod)
            except Exception:
                datos_cli = []
                datos_prod = []

        if datos_cli is not None:
            for cli in datos_cli:
                hash_id = cli.get("id")
                saldo = cli.get("saldo", 0)
                if hash_id is not None:
                    self.tarjetas[str(hash_id)] = Tarjeta(str(hash_id), saldo)
                    
        if datos_prod is not None:
            filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            f_idx = 0
            c_idx = 1
            
            for p in datos_prod:
                cod = p.get("cod")
                nom = p.get("nombre")
                pre = p.get("precio", 0.0)
                des = p.get("despedida", "")
                
                coord = f"{filas[f_idx]}{c_idx}"
                
                if coord in self.inventario:
                    prod = self.inventario[coord]
                    if prod.get_precio() != pre:
                        prod.set_precio(pre)
                else:
                    self.inventario[coord] = Producto(cod, nom, pre, des, coord, 10)
                
                c_idx += 1
                if c_idx > 3:
                    c_idx = 1
                    f_idx += 1

        print("\n==================================")
        print("      CATALOGO DISPONIBLE")
        print("==================================")
        
        for coord_k, prod_v in self.inventario.items():
            print(f"[{coord_k}] {prod_v.get_nombre()} | Precio: ${prod_v.get_precio():.2f} | Stock: {prod_v.get_stock_actual()}")
            
        print("==================================\n")
        
        continuar_menu = True
        while continuar_menu:
            opc_input = input("\nIngrese coordenada (ej. A1), RS (Mantenimiento), RP (Reportes) o SALIR: ")
            
            if opc_input.upper() == "RS":
                print("\n--- MODO MANTENIMIENTO ---")
                coord_rs = input("Ingrese coordenada a modificar o crear (ej. C1): ")
                
                if coord_rs in self.inventario:
                    prod = self.inventario[coord_rs]
                    print(f"Producto actual: {prod.get_nombre()} | Stock: {prod.get_stock_actual()}")
                    try:
                        cant = int(input("Ingrese cantidad a agregar: "))
                        prod.set_stock_actual(prod.get_stock_actual() + cant)
                        print("Stock actualizado con exito.")
                        
                        import datetime
                        fecha_ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        nuevo_rs = Restock(prod.get_cod(), cant, fecha_ahora)
                        try:
                            with open("restock_local.txt", "a") as f_rs:
                                f_rs.write(nuevo_rs.exportar_a_bd_txt())
                        except Exception:
                            pass
                    except Exception:
                        print("Cantidad invalida.")
                else:
                    print("Coordenada nueva detectada. Creando producto...")
                    cod_n = input("Codigo: ")
                    nom_n = input("Nombre: ")
                    try:
                        pre_n = float(input("Precio: "))
                        des_n = input("Mensaje de despedida: ")
                        cant_n = int(input("Stock inicial: "))
                        
                        nuevo_p = Producto(cod_n, nom_n, pre_n, des_n, coord_rs, cant_n)
                        self.inventario[coord_rs] = nuevo_p
                        print("Producto nuevo agregado al inventario.")
                        
                        import datetime
                        fecha_ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        nuevo_rs = Restock(cod_n, cant_n, fecha_ahora)
                        try:
                            with open("restock_local.txt", "a") as f_rs:
                                f_rs.write(nuevo_rs.exportar_a_bd_txt())
                        except Exception:
                            pass
                    except Exception:
                        print("Datos invalidos. Cancelando creacion.")
                
                lista_export = []
                for k, v in self.inventario.items():
                    dict_p = {
                        "cod": v.get_cod(),
                        "nombre": v.get_nombre(),
                        "precio": v.get_precio(),
                        "despedida": v.get_despedida()
                    }
                    lista_export.append(dict_p)
                    
                import json
                try:
                    with open("productos_local.json", "w") as f_prod_out:
                        json.dump(lista_export, f_prod_out)
                    print("Archivo local de inventario sobreescrito satisfactoriamente.")
                except Exception:
                    print("Error al guardar inventario local.")
                    
            elif opc_input.upper() == "RP":
                import matplotlib.pyplot as plt
                print("\n--- GENERANDO REPORTES Y GRAFICOS ---")
                
                try:
                    ventas_lista = []
                    try:
                        with open("ventas_local.txt", "r") as f_v:
                            for linea_v in f_v:
                                partes = linea_v.strip().split(",")
                                if len(partes) == 3:
                                    ventas_lista.append({
                                        "id_tarjeta": partes[0],
                                        "cod_prod": partes[1],
                                        "monto": float(partes[2])
                                    })
                    except Exception:
                        pass
                    
                    if len(ventas_lista) > 0:
                        conteo_prod = {}
                        ingresos_prod = {}
                        monto_total = 0.0
                        
                        monto_acumulado_lista = []
                        ac_temp = 0.0
                        
                        for v_item in ventas_lista:
                            cp = v_item["cod_prod"]
                            m = v_item["monto"]
                            
                            conteo_prod[cp] = conteo_prod.get(cp, 0) + 1
                            ingresos_prod[cp] = ingresos_prod.get(cp, 0.0) + m
                            monto_total += m
                            
                            ac_temp += m
                            monto_acumulado_lista.append(ac_temp)
                            
                        with open("reporte_ventas.txt", "w") as f_rep:
                            f_rep.write("=== REPORTE DE VENTAS ===\n")
                            f_rep.write(f"Ventas totales registradas: {len(ventas_lista)}\n")
                            f_rep.write(f"Ingresos brutos totales: ${monto_total:.2f}\n\n")
                            f_rep.write("Desglose por producto (Unidades vendidas):\n")
                            for cod_p, cant_p in conteo_prod.items():
                                f_rep.write(f" - Codigo {cod_p}: {cant_p} unidades\n")
                        
                        print("Reporte de texto generado en 'reporte_ventas.txt'.")
                        
                        plt.figure()
                        nombres_b = list(conteo_prod.keys())
                        cantidades_b = list(conteo_prod.values())
                        plt.bar(nombres_b, cantidades_b, color='skyblue')
                        plt.title("Ventas por Producto")
                        plt.xlabel("Codigo de Producto")
                        plt.ylabel("Unidades Vendidas")
                        plt.savefig("grafico_barras.png")
                        plt.close()
                        
                        plt.figure()
                        nombres_c = list(ingresos_prod.keys())
                        ingresos_c = list(ingresos_prod.values())
                        plt.pie(ingresos_c, labels=nombres_c, autopct='%1.1f%%')
                        plt.title("Ingresos por Producto")
                        plt.savefig("grafico_circular.png")
                        plt.close()
                        
                        plt.figure()
                        plt.plot(range(1, len(monto_acumulado_lista) + 1), monto_acumulado_lista, marker='o', linestyle='-', color='green')
                        plt.title("Crecimiento de Ingresos (Secuencial)")
                        plt.xlabel("Numero de Venta")
                        plt.ylabel("Ingreso Acumulado ($)")
                        plt.savefig("grafico_lineas.png")
                        plt.close()
                        
                        print("Graficos generados y guardados con exito.")
                    else:
                        print("No hay ventas registradas para generar el reporte.")
                except Exception:
                    print("Error inesperado al leer el historial o generar los graficos.")
                    
            elif opc_input.upper() == "SALIR":
                continuar_menu = False
                
            elif opc_input in self.inventario:
                prod = self.inventario.get(opc_input)
                if prod.get_stock_actual() > 0:
                    tarj_in = input("Ingrese su numero de tarjeta: ")
                    hash_in = str(hash(tarj_in))
                    
                    t_obj = self.tarjetas.get(hash_in)
                    if t_obj is None:
                        t_obj = self.tarjetas.get(tarj_in)
                        
                    if t_obj is not None:
                        if t_obj.get_saldo() >= prod.get_precio():
                            t_obj.descontar_saldo(prod.get_precio())
                            prod.descontar_stock(1)
                            print(prod.get_despedida())
                            
                            nueva_venta = Venta(prod, tarj_in, prod.get_precio())
                            try:
                                with open("ventas_local.txt", "a") as f_ventas:
                                    f_ventas.write(nueva_venta.exportar_a_bd_txt())
                            except Exception:
                                pass
                        else:
                            print("Saldo insuficiente.")
                    else:
                        print("Tarjeta no reconocida.")
                else:
                    print("Producto agotado.")
            else:
                print("Opcion o coordenada invalida.")
