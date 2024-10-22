from sqlalchemy.orm import Session

from app.models.post import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tag_by_name(self, name: str) -> Tag:
        return self.db.query(Tag).filter(Tag.name == name).first()

    def create_tag(self, name: str) -> Tag:
        new_tag = Tag(name=name)
        self.db.add(new_tag)
        self.db.commit()
        self.db.refresh(new_tag)
        return new_tag

    def get_or_create_tag(self, name: str) -> Tag:
        tag = self.get_tag_by_name(name)
        if tag:
            return tag
        return self.create_tag(name)
