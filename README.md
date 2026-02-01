# Simulador de Base de Datos

Este proyecto es un simulador de base de datos que permite realizar operaciones básicas de gestión de datos. A continuación se describen las funcionalidades y la estructura del proyecto.

## Estructura del Proyecto

```
README.md
App/
    __init__.py
	main.py
	table.py
	__pycache__/
Test/
	__init__.py
	TestMain.py
	__pycache__/
```

- **App/**: Contiene la lógica principal del simulador.
  - `main.py`: Archivo principal que ejecuta el simulador.
  - `table.py`: Contiene las definiciones de las tablas y sus operaciones.

- **Test/**: Contiene las pruebas unitarias para asegurar el correcto funcionamiento del simulador.
  - `TestMain.py`: Archivo que ejecuta las pruebas.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JosueMonarca/SimuladorDeBaseDeDatosSQL.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd SimuladorDeBaseDeDatos
   ```

## Uso

Para ejecutar el simulador, utilize el siguiente comando:
```bash
python -m app/main.py
```

## Tests

Si quiere solo ejecutar los tests utilize el siguiente comando:
```bash
python -m test/test_database.py
```
```bash
python -m test/test_persistence_manager.py
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.
