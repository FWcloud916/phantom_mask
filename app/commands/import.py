import click

from app.commands.utils import parse_mask, parse_open_hours, read_json_file
from app.models.masks import Mask as MaskModel
from app.models.open_hours import OpenHours as OpenHoursModel
from app.models.pharmacies import Pharmacy as PharmacyModel
from app.models.purchase_histories import PurchaseHistory
from app.schemas.pharmacies import ImportPharmacy
from app.schemas.users import ImportUser, UserCreate
from app.services.users import UserService
from app.utils.database import get_db_session


@click.group()
def cli():
    """cli"""


@click.command("import-user-data")
@click.option(
    "--filepath", "-f", prompt="File path", help="File path", default="data/users.json"
)
def import_user_data(filepath):
    """Simple program that greets NAME for a total of COUNT times."""
    try:
        db = next(get_db_session())
        data = read_json_file(filepath)
        user_service = UserService(db)
        for user in data:
            import_user = ImportUser(**user)
            user = user_service.create_user(
                UserCreate(
                    **{
                        "name": import_user.name,
                        "email": f'{import_user.name.lower().replace(" ", "_")}@example.com',
                        "password": "password",
                        "cash_balance": import_user.cash_balance,
                    }
                )
            )
            for purchase_history in import_user.purchase_histories:
                db_purchase_history = PurchaseHistory(
                    user_id=user.id,
                    pharmacy_name=purchase_history.pharmacy_name,
                    mask_name=purchase_history.mask_name,
                    transaction_date=purchase_history.transaction_date,
                    transaction_amount=purchase_history.transaction_amount,
                )
                db.add(db_purchase_history)
            db.commit()
    except FileNotFoundError:
        print("File not found")


@click.command("import-pharmacy-data")
@click.option(
    "--filepath",
    "-f",
    prompt="File path",
    help="File path",
    default="data/pharmacies.json",
)
def import_pharmacy_data(filepath):
    """import pharmacy data"""
    try:
        data = [ImportPharmacy(**d) for d in read_json_file(filepath)]
        db = next(get_db_session())
        for pharmacy in data:
            db_pharmacy = PharmacyModel(
                name=pharmacy.name,
                cash_balance=pharmacy.cash_balance,
                # open_hours=test_hour,
                # masks=masks
            )
            db.add(db_pharmacy)
            db.commit()
            db.refresh(db_pharmacy)

            for mask in pharmacy.masks:
                db.add(MaskModel(**parse_mask(mask).dict(), pharmacy_id=db_pharmacy.id))
            db.commit()

            for open_hour in parse_open_hours(pharmacy.open_hours):
                db.add(OpenHoursModel(**open_hour.dict(), pharmacy_id=db_pharmacy.id))
            db.commit()
    except FileNotFoundError:
        print("File not found")


@click.command("create-test-user")
def create_test_user():
    db = next(get_db_session())
    user_service = UserService(db)
    user_service.create_user(
        UserCreate(
            **{
                "name": "test",
                "email": "test@example.com",
                "password": "password",
                "cash_balance": 0,
            }
        )
    )


cli.add_command(import_user_data)
cli.add_command(import_pharmacy_data)
cli.add_command(create_test_user)

if __name__ == "__main__":
    cli()
