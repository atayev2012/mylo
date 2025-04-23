from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from app.database import async_session_maker

from app.models import (
    Project, Image, Tag, ProjectTag, User, Application,
    ServiceType,  ClientType, BudgetType, DeadlineType, Image
)


class BaseDBM:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        """
        Asynchronously finds and returns one sample of model by given criteria or None.
        Arguments:
            data_id: Filtering criteria as id.
        Returns:
            Model sample or None if nothing was found.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Asynchronously finds and returns one sample of model by given criteria or None.
        Arguments:
            **filter_by: Filtering criteria as named parameters.
        Returns:
            Model sample or None if nothing was found.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Asynchronously finds and returns all samples of model by given criteria.
        Arguments:
            **filter_by: Filtering criteria as named parameters.
        Returns:
            List of model samples.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        """
        Asynchronously creates new sample of model with given values.
        Arguments:
            **values: Named parameters for creation of new model sample.
        Returns:
            Newly created model sample.
        """
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

class ImageDBM(BaseDBM):
    model = Image

class TagDBM(BaseDBM):
    model = Tag

class ProjectDBM(BaseDBM):
    model = Project

    @classmethod
    async def find_one_with_relations_or_none_by_id(cls, data_id: int):
        """
        Asynchronously finds and returns one sample of model with it's all relations loaded by given criteria or None.
        Arguments:
            data_id: Filtering criteria as id.
        Returns:
            Model sample or None if nothing was found.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id).options(
                joinedload(cls.model.images),
                joinedload(cls.model.tags)
            )
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()

    @classmethod
    async def find_all_projects_with_relations(cls, **filter_by):
        """
        Asynchronously finds and returns all samples of model by given criteria.
        Arguments:
            **filter_by: Filtering criteria as named parameters.
        Returns:
            List of model samples.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).options(
                selectinload(cls.model.images),
                selectinload(cls.model.tags).selectinload(ProjectTag.tag)
            )
            result = await session.execute(query)
            result_data = result.scalars().all()
            projects_dicts = []
            for item in result_data:
                tag_names = [tag.tag.name for tag in item.tags]

                projects_dicts.append(
                    {
                        "id": item.id,
                        "title": item.title,
                        "description": item.description,
                        "tags": tag_names,
                        "cover": item.cover,
                        "imgs": [image.image_url for image in item.images],
                        "task": item.task,
                        "done": item.done,
                        "price": item.price
                    }
                )

            return projects_dicts


class UserDBM(BaseDBM):
    model = User

class ApplicationDBM(BaseDBM):
    model = Application

class BudgetTypeDBM(BaseDBM):
    model = BudgetType

class ClientTypeDBM(BaseDBM):
    model = ClientType

class DeadlineTypeDBM(BaseDBM):
    model = DeadlineType

class ServiceTypeDBM(BaseDBM):
    model = ServiceType



async def initial_db_type_values():
    service_types = [
        "дизайн печат. материалов",
        "брендинг",
        "логотип",
        "дизайн упаковки",
        "айдентика",
        "дизайн презентации",
        "ui/ux",
        "ребрендинг",
        "дизайн сайта"
    ]

    budget_types = [
        "не ограничен",
        "до 50 000",
        "до 100 000",
        "до 500 000",
        "надо считать",
        "другое"
    ]

    client_types = [
        "недвижимость",
        "красота",
        "рестораны и кафе",
        "авто",
        "доставка",
        "логистика",
        "образование",
        "медицина",
        "строительство",
        "финансы",
        "юридические услуги",
        "другое"
    ]

    deadline_types = [
        "2 недели",
        "не ограничен",
        "меньше 1 недели",
        "1 месяц"
    ]

    for service_type in service_types:
        await ServiceTypeDBM.add(**{"name": service_type})

    for budget_type in budget_types:
        await BudgetTypeDBM.add(**{"name": budget_type})

    for client_type in client_types:
        await ClientTypeDBM.add(**{"name": client_type})

    for deadline_type in deadline_types:
        await DeadlineTypeDBM.add(**{"name": deadline_type})
