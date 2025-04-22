from sqlalchemy import String, BigInteger, ForeignKey, Boolean, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=True)
    user_type: Mapped[str] = mapped_column(String, nullable=False, default="user")
    job: Mapped[str] = mapped_column(String, nullable=True)
    has_telegram: Mapped[bool] = mapped_column(Boolean, default=False)
    telegram_username: Mapped[str] = mapped_column(String, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    has_whatsapp: Mapped[bool] = mapped_column(Boolean, default=False)
    user_image_url: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    extra_info: Mapped[str] = mapped_column(String, nullable=True)

    # relationships
    applications: Mapped[list["Application"]] = relationship("Application", back_populates="user")
    assigned_applications: Mapped[list["Application"]] = relationship("Assignment", back_populates="worker")


class ServiceType(Base):
    __tablename__ = "service_types"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class ClientType(Base):
    __tablename__ = "client_types"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

class BudgetType(Base):
    __tablename__ = "budget_types"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class DeadlineType(Base):
    __tablename__ = "deadline_types"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    client_name: Mapped[str] = mapped_column(String, nullable=False)
    client_phone: Mapped[str] = mapped_column(String, nullable=False)
    client_email: Mapped[str] = mapped_column(String, nullable=False)
    client_comment: Mapped[str] = mapped_column(String, nullable=True)
    status_label: Mapped[str] = mapped_column(String, nullable=False, default="worker not assigned")
    status_description: Mapped[str] = mapped_column(String, nullable=True)
    service_type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("service_types.id"))
    client_type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("client_types.id"))
    budget_type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("budget_types.id"))
    deadline_type_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("deadline_types.id"))
    approved_cost: Mapped[float] = mapped_column(Float, nullable=True)

    #relationships
    user: Mapped["User"] = relationship("User", back_populates="applications")
    workers: Mapped[list["User"]] = relationship("Assignment", back_populates="application")


class Assignment(Base):
    __tablename__ = "assignments"
    application_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("applications.id"), primary_key=True)
    worker_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    job_description: Mapped[str] = mapped_column(String, nullable=True)

    # relationships
    application: Mapped["Application"] = relationship("Application", back_populates="workers")
    worker: Mapped["User"] = relationship("User", back_populates="assigned_applications", foreign_keys=[worker_id])


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    cover: Mapped[str] = mapped_column(String, nullable=True)
    task: Mapped[str] = mapped_column(String, nullable=True)
    done: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[str] = mapped_column(String, nullable=True)
    from_application_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("applications.id"), nullable=True)

    # Relationships
    images: Mapped[list["Image"]] = relationship("Image", back_populates="project", uselist=True)
    tags: Mapped[list["Tag"]] = relationship("ProjectTag", back_populates="project", uselist=True)


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="images")


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    projects: Mapped[list["Project"]] = relationship("ProjectTag", back_populates="tag")


class ProjectTag(Base):
    __tablename__ = "project_tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id"))
    tag_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("tags.id"))

    __table_args__ = (
        UniqueConstraint("project_id", "tag_id", name="project_tag_unique_id"),
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="projects")




