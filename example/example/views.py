from typing import List
from django.db.models.query import QuerySet
from fastapi import APIRouter, Query
from .models import Example
from .serializers import ExampleSerializer, ExampleCreateUpdateSerializer

example_router = APIRouter()


# Get with pagination and ordering (asc/desc) and filtering by partial name
@example_router.get(
    '/',
    response_model=List[ExampleSerializer]
)
async def examples(
    page: int = Query(1, alias='page', ge=1),
    per_page: int = Query(10, alias='per_page', ge=1),
    order_type: str = Query('asc', alias='order_type'),
    partial_name: str = Query(None, alias='partial_name')
):
    if partial_name:
        examples: QuerySet[Example] = Example.objects.filter(
            name__icontains=partial_name
        )
    else:
        examples: QuerySet[Example] = Example.objects.all()
    examples = examples.order_by(
        f'{"-" if order_type == "desc" else ""}id'
    )[(page - 1) * per_page:page * per_page]
    return [ExampleSerializer.from_orm(example) for example in examples]


@example_router.get(
    '/{example_id}',
    response_model=ExampleSerializer
)
async def example(example_id: int):
    example: Example = Example.objects.get(id=example_id)
    return ExampleSerializer.from_orm(example)


@example_router.post(
    '/',
    response_model=ExampleSerializer,
    status_code=201,
)
async def create_example(example: ExampleCreateUpdateSerializer):
    example: Example = Example(**example.dict())
    example.save()
    return ExampleSerializer.from_orm(example)


@example_router.put('/{example_id}')
async def update_example(
    example_id: int,
    example: ExampleCreateUpdateSerializer
):
    example_obj: Example = Example.objects.get(id=example_id)
    example_obj.__dict__.update(**example.dict())
    example_obj.save()
    return ExampleSerializer.from_orm(example_obj)


@example_router.delete('/{example_id}', status_code=204)
async def delete_example(example_id: int):
    print('example_id', example_id)
    example: Example = Example.objects.get(id=example_id)
    example.delete()
