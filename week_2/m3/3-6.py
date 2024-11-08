import enum
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import String, Enum, Integer, DateTime, func, Select, null
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

sqlalchemy_base_model = declarative_base()


class TaskModel(sqlalchemy_base_model):
    __tablename__ = 'tasks'

    class TaskStatus(enum.Enum):
        PENDING = 'pending'
        PROCESSING = 'processing'
        COMPLETED = 'completed'

    task_name: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    worker_id: Mapped[int] = mapped_column(Integer, default=null, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class TaskResult(PydanticBaseModel):
    worker_id: int
    task_id: int
    status: str
    completed_at: datetime
    result: Any


class RandomWorker:
    def __init__(self, worker_id: int, db, results: list[TaskResult]):
        self._worker_id = worker_id
        self._db = db
        self._results = results

    @property
    def worker_id(self):
        return self._worker_id

    async def run(self):
        while True:
            task = await self._fetch_task()
            if task:
                result = await self._process_task(task)
                self._results.append(result)
                # log result

    async def _fetch_task(self) -> Optional[TaskModel]:
        async with self._db.begin():
            query = (
                Select(TaskModel)
                .where(TaskModel.status == TaskModel.TaskStatus.PENDING)
                .limit[1]
                .with_for_update(skip_locked=True)
            )

            task = await self._db.execute(query).scalars().first()

            if task:
                task.status = TaskModel.TaskStatus.PROCESSING
                task.worker_id = self.worker_id
                return task

    async def _process_task(self, task: TaskModel) -> TaskResult:
        result = 'do something with TaskModel.task_name'
        return await self._complete_task(task, result)

    async def _complete_task(self, task: TaskModel, result) -> TaskResult:
        task.status = TaskModel.TaskStatus.COMPLETED
        await self._db.commit()

        result = {
            'worker_id': task.worker_id,
            'task_id': task.id,
            'status': TaskModel.TaskStatus.COMPLETED,
            'completed_at': task.updated_at,
            'result': result
        }

        return TaskResult(**result)



