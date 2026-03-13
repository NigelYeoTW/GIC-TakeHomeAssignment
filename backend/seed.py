"""
Run with: python seed.py
Seeds the database with sample cafes and employees.
"""
from datetime import date, timedelta
from app.database import SessionLocal, engine
from app.models import Cafe, Employee, CafeEmployee
import uuid

# Create tables
from app.database import Base
Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(CafeEmployee).delete()
        db.query(Employee).delete()
        db.query(Cafe).delete()
        db.commit()

        # Seed cafes
        cafes = [
            Cafe(id=str(uuid.uuid4()), name="The Grind", description="Specialty coffee in the heart of the city", location="Orchard"),
            Cafe(id=str(uuid.uuid4()), name="Brew & Co", description="Artisanal brews and light bites", location="Bugis"),
            Cafe(id=str(uuid.uuid4()), name="Kopi House", description="Traditional Singapore kopi experience", location="Chinatown"),
        ]
        db.add_all(cafes)
        db.commit()

        # Seed employees
        employees = [
            Employee(id="UIAB12345", name="Alice Tan", email_address="alice@example.com", phone_number="91234567", gender="Female"),
            Employee(id="UIBC23456", name="Bob Lim", email_address="bob@example.com", phone_number="82345678", gender="Male"),
            Employee(id="UICD34567", name="Carol Ng", email_address="carol@example.com", phone_number="93456789", gender="Female"),
            Employee(id="UIDE45678", name="David Koh", email_address="david@example.com", phone_number="84567890", gender="Male"),
            Employee(id="UIEF56789", name="Eva Chen", email_address="eva@example.com", phone_number="95678901", gender="Female"),
        ]
        db.add_all(employees)
        db.commit()

        # Assign employees to cafes
        assignments = [
            CafeEmployee(cafe_id=cafes[0].id, employee_id="UIAB12345", start_date=date.today() - timedelta(days=120)),
            CafeEmployee(cafe_id=cafes[0].id, employee_id="UIBC23456", start_date=date.today() - timedelta(days=60)),
            CafeEmployee(cafe_id=cafes[1].id, employee_id="UICD34567", start_date=date.today() - timedelta(days=200)),
            CafeEmployee(cafe_id=cafes[1].id, employee_id="UIDE45678", start_date=date.today() - timedelta(days=30)),
            # Eva is unassigned
        ]
        db.add_all(assignments)
        db.commit()

        print("Seed complete.")
        print(f"  {len(cafes)} cafes, {len(employees)} employees, {len(assignments)} assignments")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
