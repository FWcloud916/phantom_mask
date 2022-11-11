"""
Pharmacy Service
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.masks import Mask as MaskModel
from app.models.open_hours import OpenHours as OpenHoursModel
from app.models.pharmacies import Pharmacy as PharmacyModel
from app.schemas.open_hours import OpenHoursDay
from app.services.service import BaseService


class PharmacyService(BaseService):
    """PharmacyService"""

    def __init__(self, db: Session):
        """init"""
        super().__init__(db)

    def get_pharmacies(
        self,
        skip: int = 0,
        limit: int = 100,
        day: OpenHoursDay = None,
        open_time: str = None,
        close_time: str = None,
        quantity: int = None,
        compare_type: str = None,
        max_price: float = None,
        min_price: float = None,
    ):
        """Get pharmacies"""
        query = self.db.query(PharmacyModel)

        if day or open_time or close_time:
            query = query.join(OpenHoursModel)
        if day:
            query = query.filter(OpenHoursModel.day == day)
        if open_time:
            query = query.filter(OpenHoursModel.open_time >= open_time)
        if close_time:
            query = query.filter(OpenHoursModel.close_time <= close_time)

        if quantity or max_price or min_price:
            query = query.join(MaskModel)

        if max_price:
            query = query.filter(PharmacyModel.masks.any(MaskModel.price <= max_price))
        if min_price:
            query = query.filter(PharmacyModel.masks.any(MaskModel.price >= min_price))

        if quantity:
            if compare_type == "gt":
                query = query.group_by(PharmacyModel.id).having(
                    func.count(MaskModel.id) > quantity
                )
            else:
                query = query.group_by(PharmacyModel.id).having(
                    func.count(MaskModel.id) < quantity
                )

        return query.offset(skip).limit(limit).all()

    def search_pharmacies_by_name(self, query):
        """Search pharmacies by name"""
        tsquery = func.plainto_tsquery("simple", f"{query}:*")

        stmt = (
            select(PharmacyModel)
            .where(PharmacyModel.name_tsv.bool_op("@@")(tsquery))
            .order_by(func.ts_rank(PharmacyModel.name_tsv, tsquery).desc())
        )

        return self.db.execute(stmt).all()
