# Integrantes: Ariadna Bonilla, Isabella Guarente.

from producto import Producto
from tarjeta import Tarjeta
from venta import Venta
from restock import Restock

class MaquinaExpendedora:
    """
    Clase controladora de la maquina expendedora.
    Consideraciones de eficiencia:
    - self.inventario y self.tarjetas son diccionarios, lo que permite busquedas (get) en O(1) tiempo promedio.
    """
    def __init__(self):
        """Inicializador de los diccionarios. Eficiencia: O(1)."""
        self.inventario = {}
        self.tarjetas = {}

    def iniciar_sistema(self):
        """
        Funcion principal larga y monolitica para respetar la regla arquitectonica.
        Eficiencia: 
        - Carga desde JSON: O(N) donde N es el numero de productos/clientes.
        - Bucle principal: O(1) operaciones interactivas (busqueda diccionarios O(1)).
        - Renderizado matriz: O(R * C) donde R y C son filas y columnas.
        - Generacion reportes: O(V + R_s) donde V son ventas y R_s los restocks procesados.
        """
        import requests
        import json
        import datetime
        import os
        
        url_cli = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/clientes.json"
        url_prod = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/productos.json"
        
        datos_cli = None
        datos_prod = None
        
        print("Iniciando sistema...")
        print("Cargando inventario local...")
        
        base_dir = os.path.dirname(__file__)
        path_prod = os.path.join(base_dir, "productos_local.txt")
        path_rs = os.path.join(base_dir, "restock_local.txt")
        path_ven = os.path.join(base_dir, "ventas_local.txt")
        path_rep = os.path.join(base_dir, "reporte_ventas.txt")
        path_gb = os.path.join(base_dir, "grafico_barras.png")
        path_gc = os.path.join(base_dir, "grafico_circular.png")
        path_gl = os.path.join(base_dir, "grafico_lineas.png")
        
        # O(N) Carga local de inventario
        datos_prod = []
        try:
            with open(path_prod, "r", encoding="utf-8") as f_prod:
                for line in f_prod:
                    parts = line.strip().split(";")
                    if len(parts) >= 6:
                        datos_prod.append({
                            "cod": parts[0],
                            "prod": parts[1],
                            "precio": float(parts[2]),
                            "despedida": parts[3],
                            "coordenada": parts[4],
                            "stock_actual": int(parts[5])
                        })
        except Exception:
            print("Archivo de inventario no encontrado. La maquina esta vacia.")

        if datos_prod:
            filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            c_idx = 1
            r_idx = 1
            
            for p in datos_prod:
                cod = p.get("cod")
                nom = p.get("prod", p.get("nombre", ""))
                pre = p.get("precio", 0.0)
                des = p.get("despedida", "")
                coord = p.get("coordenada", "")
                stk = p.get("stock_actual", 10)
                
                if coord == "":
                    coord = f"{filas[c_idx-1]}{r_idx}"
                    c_idx += 1
                    if c_idx > 4:
                        c_idx = 1
                        r_idx += 1
                self.inventario[coord] = Producto(cod, nom, pre, des, coord, stk)

        # O(N) Actualizar precios de Github si hay conexion, sin agregar nuevos
        print("Revisando actualizacion de precios en la red....")
        try:
            res_cli = requests.get(url_cli, timeout=5)
            api_cli = res_cli.json()
            for cli in api_cli:
                hash_id = str(cli.get("id"))
                if hash_id not in self.tarjetas:
                    self.tarjetas[hash_id] = Tarjeta(hash_id, cli.get("saldo", 0))
            
            res_prod = requests.get(url_prod, timeout=5)
            api_prod = res_prod.json()
            for p_api in api_prod:
                cod_api = p_api.get("cod")
                pre_api = p_api.get("precio")
                for coord, prod_obj in self.inventario.items():
                    if prod_obj.get_cod() == cod_api:
                        if prod_obj.get_precio() != pre_api:
                            prod_obj.set_precio(pre_api)
                        break
            print("Precios actualizados exitosamente.")
        except Exception:
            print("No se pudo conectar al repositorio. Se mantienen los precios actuales.")

        continuar_menu = True
        while continuar_menu:
            
            # --- IMPRESION MATRIZ ESTRICTA 5x4 ---
            print("\n====================================")
            print("|       MAQUINA EXPENDEDORA        |")
            print("====================================")
            print("|    A      B      C      D       |")
            
            for r in range(1, 6):
                print(f"| {r:<2} ", end="")
                for c in range(1, 5):
                    coordenada = f"{chr(ord('A') + c - 1)}{r}"
                    prod = self.inventario.get(coordenada)
                    if prod is not None and prod.get_stock_actual() > 0:
                        print(f"{prod.get_cod():<7}", end="")
                    else:
                        print("       ", end="")
                print(" |")
            print("====================================\n")

            # --- INPUT MASIVO O(1) Promedio ---
            opc_input = input("Introduce el codigo de un producto, o elige una accion [vacio=Vender | RS=Restock | RP=Reportes]: ").strip()
            
            es_venta = False
            coord_venta = ""
            
            if opc_input.upper() == "RS":
                print("\n--- MODO MANTENIMIENTO ---")
                print("1. Actualizar existencia de inventario")
                print("2. Cambiar producto")
                sub_opc = input("Seleccione opcion: ")
                
                if sub_opc == "1":
                    coord_rs = input("Coordenada del producto a actualizar (ej. A1): ").upper()
                    if coord_rs in self.inventario:
                        prod = self.inventario[coord_rs]
                        print(f"Producto actual: {prod.get_nombre()} | Stock: {prod.get_stock_actual()}")
                        try:
                            cant = int(input("Ingrese nueva cantidad a ESTABLECER: "))
                            if cant >= 0:
                                diff = cant - prod.get_stock_actual()
                                prod.set_stock_actual(cant)
                                print("Stock actualizado.")
                                
                                # Logica: Guardar restock solo si se agregaron. Si diff > 0.
                                if diff > 0:
                                    fecha_ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    nuevo_rs = Restock(prod.get_cod(), diff, fecha_ahora)
                                    try:
                                        with open(path_rs, "a") as f_rs:
                                            f_rs.write(nuevo_rs.exportar_a_bd_txt())
                                    except Exception: pass
                            else:
                                print("Cantidad no puede ser negativa.")
                        except Exception:
                            print("Entrada invalida.")
                    else:
                        print("La coordenada no existe.")
                
                elif sub_opc == "2":
                    coord_rs = input("Coordenada del nuevo producto (ej. E3): ").upper()
                    cod_n = input("Codigo (5 letras): ")
                    nom_n = input("Nombre completo: ")
                    try:
                        pre_n = float(input("Precio: "))
                        des_n = input("Despedida: ")
                        cant_n = int(input("Cantidad en existencia: "))
                        
                        nuevo_p = Producto(cod_n, nom_n, pre_n, des_n, coord_rs, cant_n)
                        self.inventario[coord_rs] = nuevo_p
                        print("Producto configurado exitosamente.")
                        
                        fecha_ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        nuevo_rs = Restock(cod_n, cant_n, fecha_ahora)
                        try:
                            with open(path_rs, "a") as f_rs:
                                f_rs.write(nuevo_rs.exportar_a_bd_txt())
                        except Exception: pass
                    except Exception:
                        print("Datos invalidos.")
                else:
                    print("Opcion de mantenimiento invalida.")
                
                # Sobreescribir O(N)
                try:
                    with open(path_prod, "w", encoding="utf-8") as f_prod_out:
                        for k, v in self.inventario.items():
                            f_prod_out.write(f"{v.get_cod()};{v.get_nombre()};{v.get_precio()};{v.get_despedida()};{v.get_coordenada()};{v.get_stock_actual()}\n")
                except Exception: pass
                    
            elif opc_input.upper() == "RP":
                try:
                    import matplotlib.pyplot as plt
                    import numpy as np
                except ImportError:
                    print("Instale matplotlib (pip install matplotlib) para graficos.")
                    continue
                    
                print("\n--- GENERANDO REPORTES Y GRAFICOS ---")
                
                ventas_lista = []
                restock_lista = []
                
                try:
                    with open(path_ven, "r") as f_v:
                        for linea_v in f_v:
                            p = linea_v.strip().split(",")
                            if len(p) == 3:
                                ventas_lista.append({"id_t": p[0], "cod": p[1], "m": float(p[2])})
                except Exception: pass
                
                try:
                    with open(path_rs, "r") as f_r:
                        for linea_r in f_r:
                            p = linea_r.strip().split(",")
                            if len(p) == 3:
                                restock_lista.append({"cod": p[1], "cant": int(p[2])})
                except Exception: pass
                
                conteo_vendidos = {}
                monto_total = 0.0
                gastos_usuario = {}
                monto_acumulado_lista = []
                ac_temp = 0.0
                
                for v in ventas_lista:
                    c = v["cod"]
                    m = v["m"]
                    u = v["id_t"]
                    conteo_vendidos[c] = conteo_vendidos.get(c, 0) + 1
                    monto_total += m
                    gastos_usuario[u] = gastos_usuario.get(u, 0.0) + m
                    ac_temp += m
                    monto_acumulado_lista.append(ac_temp)
                    
                conteo_restock = {}
                for r in restock_lista:
                    c = r["cod"]
                    conteo_restock[c] = conteo_restock.get(c, 0) + r["cant"]
                
                # Escribir txt O(N)
                with open(path_rep, "w") as f_rep:
                    f_rep.write("=== REPORTE DE SISTEMA ===\n")
                    f_rep.write(f"Total productos vendidos: {len(ventas_lista)}\n")
                    f_rep.write(f"Dinero total cobrado: ${monto_total:.2f}\n")
                    f_rep.write(f"Numero total de usuarios unicos: {len(gastos_usuario)}\n\n")
                    
                    f_rep.write("--- Desglose por Producto ---\n")
                    todos_cods = set(list(conteo_vendidos.keys()) + list(conteo_restock.keys()))
                    for c in todos_cods:
                        vend = conteo_vendidos.get(c, 0)
                        rest = conteo_restock.get(c, 0)
                        f_rep.write(f"Producto {c} -> Cargados: {rest} | Vendidos: {vend}\n")
                        
                    f_rep.write("\n--- Gastos por Usuario (Hash) ---\n")
                    for u, g in gastos_usuario.items():
                        f_rep.write(f"Usuario {u}: ${g:.2f}\n")
                        
                print("Reporte de texto 'reporte_ventas.txt' generado.")
                
                # Grafica 1: Barras dobles (Cargado vs Vendido)
                if len(todos_cods) > 0:
                    plt.figure()
                    nombres_b = list(todos_cods)
                    cargados_b = [conteo_restock.get(n, 0) for n in nombres_b]
                    vendidos_b = [conteo_vendidos.get(n, 0) for n in nombres_b]
                    
                    x = np.arange(len(nombres_b))
                    w = 0.35
                    plt.bar(x - w/2, cargados_b, w, label='Cargados', color='blue')
                    plt.bar(x + w/2, vendidos_b, w, label='Vendidos', color='orange')
                    plt.xticks(x, nombres_b, rotation=45)
                    plt.legend()
                    plt.title("Stock Cargado vs Vendido por Producto")
                    plt.tight_layout()
                    plt.savefig(path_gb)
                    plt.close()
                
                # Grafica 2: Circular (Usuarios)
                if len(gastos_usuario) > 0:
                    plt.figure()
                    plt.pie(gastos_usuario.values(), labels=gastos_usuario.keys(), autopct='%1.1f%%')
                    plt.title("Participacion de Gastos por Usuario")
                    plt.savefig(path_gc)
                    plt.close()
                    
                # Grafica 3: Linea
                if len(monto_acumulado_lista) > 0:
                    plt.figure()
                    plt.plot(range(1, len(monto_acumulado_lista) + 1), monto_acumulado_lista, marker='o', color='green')
                    plt.title("Aumento Total Vendido")
                    plt.xlabel("Numero de Venta")
                    plt.ylabel("Ingreso Acumulado ($)")
                    plt.savefig(path_gl)
                    plt.close()
                    
                print("Graficos generados (barras, circular, lineas).")
                
            elif opc_input.upper() == "SALIR":
                continuar_menu = False
                
            elif opc_input == "":
                coord_venta = input("Ha elegido comprar. Ingrese coordenada (ej. A1): ").upper()
                es_venta = True
                
            else:
                # Determinar si es codigo o coord (O(N))
                es_codigo = False
                for k, v in self.inventario.items():
                    if v.get_cod().upper() == opc_input.upper():
                        print(f">> El precio de {v.get_nombre()} es ${v.get_precio():.2f}")
                        es_codigo = True
                        break
                        
                if not es_codigo:
                    coord_venta = opc_input.upper()
                    es_venta = True

            if es_venta:
                if coord_venta in self.inventario:
                    prod = self.inventario[coord_venta]
                    if prod.get_stock_actual() > 0:
                        print(f"Producto seleccionado: {prod.get_nombre()} | Precio: ${prod.get_precio():.2f}")
                        tarj_in = input("Ingrese su numero de tarjeta (Deje en blanco para cancelar): ").strip()
                        if tarj_in != "":
                            hash_in = str(hash(tarj_in))
                            t_obj = self.tarjetas.get(hash_in)
                            if t_obj is None:
                                t_obj = self.tarjetas.get(tarj_in) # Backup
                                
                            if t_obj is not None:
                                if t_obj.get_saldo() >= prod.get_precio():
                                    conf = input(f"¿Confirma la compra de {prod.get_nombre()} por ${prod.get_precio():.2f}? (S/N): ")
                                    if conf.upper() == "S":
                                        t_obj.descontar_saldo(prod.get_precio())
                                        prod.descontar_stock(1)
                                        
                                        print(f"Dispensando... {prod.get_nombre()}")
                                        print(prod.get_despedida())
                                        
                                        # Guardar Venta
                                        nueva_venta = Venta(prod, tarj_in, prod.get_precio())
                                        try:
                                            with open(path_ven, "a") as f_ventas:
                                                f_ventas.write(nueva_venta.exportar_a_bd_txt())
                                        except Exception: pass
                                        
                                        # Actualizar archivo productos
                                        try:
                                            with open(path_prod, "w", encoding="utf-8") as f_prod_out:
                                                for k, v in self.inventario.items():
                                                    f_prod_out.write(f"{v.get_cod()};{v.get_nombre()};{v.get_precio()};{v.get_despedida()};{v.get_coordenada()};{v.get_stock_actual()}\n")
                                        except Exception: pass
                                    else:
                                        print("Venta cancelada.")
                                else:
                                    print("Saldo insuficiente en su tarjeta.")
                            else:
                                print("Tarjeta no valida o no encontrada.")
                        else:
                            print("Venta cancelada.")
                    else:
                        print("Producto agotado.")
                else:
                    print("Coordenada invalida.")
