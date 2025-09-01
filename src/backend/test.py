import asyncio
from src.backend.database import SurrealDataBase


async def main() -> None:
    """This is main function"""
    try:
        # Initialize wrapper
        db = SurrealDataBase(
            url="ws://localhost:8000/rpc",
            username="root",
            password="root",
            namespace="test",
            database="test"
        )

        # Step 1: Connect + signin + select ns/db
        await db.use_connection()

        # Step 2: Insert some dummy patients
        patients = {
            "P007":  {
            "name":"Rohan",
            "city":"Hyderabad",
            "age":25,
            "gender":"male",
            "height":1.82,
            "weight":80,
            "bmi":21,
            "verdict":"Normal"
        }
        }
        await db.import_patients(patients)

        # Step 3: Read them back
        result = await db.client.query("SELECT * FROM patient;")
        print("Patients in DB:", result)

        # Step 4: Close connection
        await db.close_connection()
    except Exception as e:
        print(f"Error occured inside the main function: {e}")

if __name__ == "__main__":
    asyncio.run(main())
