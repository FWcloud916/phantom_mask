"""
Mask CURD Service
"""
from sqlalchemy import func, select

from app.models.masks import Mask as MaskModel
from app.services.service import BaseService


class MaskService(BaseService):
    """Mask Service"""

    def __init__(self, db):
        """init"""
        super().__init__(db)

    def get_masks(self, skip=0, limit=100):
        """Get masks"""
        return self.db.query(MaskModel).offset(skip).limit(limit).all()

    def get_masks_by_pharmacy_id(
        self,
        pharmacy_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "price",
        sort_order="desc",
    ):
        """Get mask by pharmacy id"""
        query = self.db.query(MaskModel).filter(MaskModel.pharmacy_id == pharmacy_id)
        if sort_by:
            if sort_order == "desc":
                query = query.order_by(getattr(MaskModel, sort_by).desc())
            else:
                query = query.order_by(getattr(MaskModel, sort_by).asc())
        return query.offset(skip).limit(limit).all()

    def search_masks_by_name(self, query):
        """Search pharmacies by name"""
        tsquery = func.plainto_tsquery("simple", f"{query}:*")

        stmt = (
            select(MaskModel)
            .where(MaskModel.name_tsv.bool_op("@@")(tsquery))
            .order_by(func.ts_rank(MaskModel.name_tsv, tsquery).desc())
        )

        return self.db.execute(stmt).all()
