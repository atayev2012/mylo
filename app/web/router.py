from fastapi import APIRouter, HTTPException, status, Request

from app.web.schemas import WebApplication
from app.web.utils import verify_email, strip_phone_number, raise_bad_request

from app.web.db_manager import (
    ProjectDBM, ImageDBM, TagDBM, UserDBM, ServiceTypeDBM, BudgetTypeDBM,
    DeadlineTypeDBM, ClientTypeDBM, ApplicationDBM, initial_db_type_values
)

# creating router
router = APIRouter()

@router.post("/apply", status_code=status.HTTP_201_CREATED)
async def apply(data: WebApplication):
    # verify user if in database by phone
    # strip phone number and leave only digits
    phone_number = await strip_phone_number(data.phone)
    user = await UserDBM.find_one_or_none(**{"phone": phone_number})
    if not user:
        if not await verify_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid email format: {data.email}",
            )

        user_info = {
            "name": data.name,
            "phone": phone_number,
            "email": data.email,
        }

        user = await UserDBM.add(**user_info)

    # preparing application data to be saved to database
    # get service type id
    service_type = await ServiceTypeDBM.find_one_or_none(**{"name": data.service_type})
    if not service_type:
        await raise_bad_request("service type", data.service_type)

    # get client type id
    client_type = await ClientTypeDBM.find_one_or_none(**{"name": data.client_type})
    if not client_type:
        await raise_bad_request("client type", data.client_type)

    # get budget type id
    budget_type = await BudgetTypeDBM.find_one_or_none(**{"name": data.budget_type})
    if not budget_type:
        await raise_bad_request("budget type", data.budget_type)

    # get deadline type id
    deadline_type = await DeadlineTypeDBM.find_one_or_none(**{"name": data.deadline_type})
    if not deadline_type:
        await raise_bad_request("deadline type", data.deadline_type)

    # assembling dict to save to applications
    application_info= {
        "user_id": user.id,
        "service_type_id": service_type.id,
        "client_type_id": client_type.id,
        "budget_type_id": budget_type.id,
        "deadline_type_id": deadline_type.id,
        "client_name": data.name,
        "client_email": data.email,
        "client_phone": phone_number,
        "client_comment": data.comment,
    }

    # adding data to database
    new_application = await ApplicationDBM.add(**application_info)

    return {
        "success": True,
        "detail": f"new application was created: #{new_application.id}",
    }


@router.get("/applications")
async def get_app():
    applications = await ApplicationDBM.find_all()
    return applications


# get information on projects
@router.get("/projects")
async def get_projects(project_id: int | None = None):
    # if only one project requested, then provide one project only
    if project_id:
        project = await ProjectDBM.find_one_with_relations_or_none_by_id(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id:{project_id} was not found"
            )
        tag_ids = [tag.id for tag in project.tags]
        tags = []
        for i in tag_ids:
            data = await TagDBM.find_one_or_none_by_id(i)
            tags.append(data.name)
        images = [image.image_url for image in project.images]

        return {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "tags": tags,
            "cover": project.cover,
            "imgs": images,
            "tasks": project.task,
            "done": project.done,
            "price": project.price
        }
    else:
        # provide list of all projects
        projects = await ProjectDBM.find_all_projects_with_relations()
        return projects



