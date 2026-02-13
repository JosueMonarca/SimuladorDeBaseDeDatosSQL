import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controller.database import DataBase
from app.query_processor.manager import QueryProcessor

def main():
    db = DataBase()
    processor = QueryProcessor(db)

    print("Simulador de Base de Datos SQL")
    print("Escribe 'EXIT' para salir.")
    
    while True:
        try:
            query = input("SQL> ")
            if query.strip().upper() == 'EXIT':
                break
            
            result = processor.execute(query)
            print(result)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

