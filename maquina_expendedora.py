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
                print("Modo mantenimiento en construccion...")
            elif opc_input.upper() == "RP":
                print("Reportes en construccion...")
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
