import enum
from datetime import datetime
from typing import Optional, Any, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import String, Enum, Integer, DateTime, func, Select, null
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

sqlalchemy_base_model = declarative_base()


class BaseTaskModel(sqlalchemy_base_model):
    class TaskStatus(enum.Enum):
        PENDING = 'pending'
        PROCESSING = 'processing'
        COMPLETED = 'completed'

    task_name: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    worker_id: Mapped[int] = mapped_column(Integer, default=null, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class TaskModel(sqlalchemy_base_model):
    pass


class TaskResult(PydanticBaseModel):
    worker_id: int
    task_id: int
    status: str
    completed_at: datetime
    result: Any


class BaseWorker:
    TASK = TypeVar('TASK', bound=BaseTaskModel)

    def __init__(self,
                 worker_id: int,
                 db,
                 results: list[TaskResult],
                 tasks_model: TASK,
                 tasks_result_model: TASK):

        self._worker_id = worker_id
        self._db = db
        self._results = results
        self._task_model = tasks_model
        self._result_model = tasks_result_model

    @property
    def worker_id(self):
        return self._worker_id

    async def run(self):
        while True:
            task = await self._fetch_task()
            if task:
                result = await self.process_task(task)
                self._results.append(result)
                # log result

    async def _fetch_task(self) -> Optional[TASK]:
        async with self._db.begin():
            query = (
                Select(self._task_model)
                .where(self._task_model.status == self._task_model.TaskStatus.PENDING)
                .limit[1]
                .with_for_update(skip_locked=True)
            )

            task = await self._db.execute(query).scalars().first()

            if task:
                task.status = self._task_model.TaskStatus.PROCESSING
                task.worker_id = self.worker_id
                return task

    def _pack_to_pydantic_model(self, task: TaskModel, result) -> TaskResult:
        result = {
            'worker_id': task.worker_id,
            'task_id': task.id,
            'status': task.status,
            'completed_at': task.updated_at,
            'result': result
        }

        return TaskResult(**result)

    async def complete_task(self, task: TASK, result) -> TaskResult:
        task.status = self._task_model.TaskStatus.COMPLETED
        await self._db.commit()
        return self._pack_to_pydantic_model(task, result)

    async def process_task(self, task: TASK) -> TaskResult:
        raise NotImplemented


class RandomWorker(BaseWorker):
    async def process_task(self, task: TaskModel) -> TaskResult:
        result = 'do something with TaskModel.task_name'
        return await self.complete_task(task, result)



