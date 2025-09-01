import json
from surrealdb import AsyncSurreal
from utils.customlogger import CustomLogger

# Setting up custom logger
logger = CustomLogger(name="DataBaseLogger", log_file="database.log").get_logger()


class SurrealDataBase:
    def __init__(self,
                 url: str = "ws://localhost:8001/rpc",  # Changed to WebSocket
                 username: str = "root",
                 password: str = "root",
                 namespace: str = "test",
                 database: str = "test"
                 ) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.namespace = namespace
        self.database = database
        self.client = AsyncSurreal(self.url)

    async def use_connection(self) -> None:
        """Connect to SurrealDB and select namespace + database"""
        try:
            logger.info("Connected to SurrealDB")
            
            # Then sign in
            await self.client.signin({
                "username": self.username, 
                "password": self.password
            })
            logger.info("Successfully signed in")
            
            # Then use namespace and database
            await self.client.use(namespace=self.namespace, database=self.database)
            logger.info(f"Using namespace: {self.namespace}, database: {self.database}")
            
        except Exception as e:
            logger.error(f"Connection error: {e}")
            raise

    async def import_patients(self, patients_dict: dict) -> None:
        """
        Dump patients dictionary into SurrealDB exactly as in JSON file.
        patients_dict format: { patient_id: {name: ..., age: ...}, ... }
        """
        try:
            # Start a transaction to ensure all data is committed
            transaction_queries = []
            
            for patient_id, patient_data in patients_dict.items():
                # Create the patient record with the exact structure from JSON
                # Use the patient_id as part of the record ID for easy reference
                record_data = {
                    "patient_id": patient_id,  # Keep the original ID as a field
                    **patient_data  # Include all the patient data exactly as in JSON
                }
                
                # Add to transaction
                transaction_queries.append(f"""
                    CREATE patient:{patient_id} CONTENT {json.dumps(record_data)};
                """)
            
            # Execute all queries in a transaction to ensure atomic commit
            if transaction_queries:
                transaction_query = "BEGIN TRANSACTION;\n" + "\n".join(transaction_queries) + "\nCOMMIT;"
                result = await self.client.query(transaction_query)
                logger.info(f"Transaction completed: {len(patients_dict)} patients imported")
                
        except Exception as e:
            logger.error(f"Error importing patients: {e}")
            raise

    async def close_connection(self) -> None:
        """Close SurrealDB connection"""
        try:
            await self.client.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")