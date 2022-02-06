from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.views import View
from asgiref.sync import sync_to_async
from . services import FilterDBData, add_db_match_to_users, create_dummy_data_for_db
import asyncio


class MyView(View):

    def get(self, request):
        try:
            first_name = request.GET["first_name"]
        except MultiValueDictKeyError:
            first_name = None

        try:
            last_name = request.GET["last_name"]
        except MultiValueDictKeyError:
            last_name = None

        try:
            email = request.GET["email"]
        except MultiValueDictKeyError:
            email = None

        try:
            db = request.GET["db"]
        except MultiValueDictKeyError:
            db = "default"

        data_source_object = FilterDBData(db)
        users = data_source_object.query(first_name=first_name, last_name=last_name, email=email)

        return JsonResponse(users, safe=False, status=200)


async def parallel_calls_to_databases(request):
    try:
        first_name = request.GET["first_name"]
    except MultiValueDictKeyError:
        first_name = None

    try:
        last_name = request.GET["last_name"]
    except MultiValueDictKeyError:
        last_name = None

    try:
        email = request.GET["email"]
    except MultiValueDictKeyError:
        email = None

    task_default_db_users = asyncio.ensure_future(get_users("default", first_name, last_name, email))
    task_db1_db_users = asyncio.ensure_future(get_users("db1", first_name, last_name, email))
    task_db2_db_users = asyncio.ensure_future(get_users("db2", first_name, last_name, email))

    default_db_users = await task_default_db_users
    db1_db_users = await task_db1_db_users
    db2_db_users = await task_db2_db_users

    users = []
    task1 = add_db_match_to_users(users, default_db_users)
    task2 = add_db_match_to_users(users, db1_db_users)
    task3 = add_db_match_to_users(users, db2_db_users)

    await asyncio.wait([task1, task2, task3])

    return JsonResponse(users, safe=False, status=200)


@sync_to_async
def get_users(db, first_name, last_name, email):
    db_object = FilterDBData(db)
    return db_object.query(first_name=first_name, last_name=last_name, email=email)
