from sqlalchemy.orm import Session
from app.models.country import Country
from app.schemas.country import CountryCreate


class CountryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_country_by_name(self, name: str) -> Country:
        return self.db.query(Country).filter(Country.name == name).first()

    def create_country(self, country: CountryCreate) -> Country:
        db_country = Country(name=country.name)
        self.db.add(db_country)
        self.db.commit()
        self.db.refresh(db_country)
        return db_country
